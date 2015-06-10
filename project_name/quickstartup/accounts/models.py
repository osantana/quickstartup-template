# coding: utf-8


import re
import datetime
import hashlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser as DjangoAbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.dispatch import Signal
from django.contrib.auth.models import BaseUserManager

from .messages import send_activation_email

SHA1_RE = re.compile('^[a-f0-9]{40}$')
ACTIVATED = u"ALREADY_ACTIVATED"

inactive_user_created = Signal(providing_args=["user", "extra_info"])
user_activated = Signal(providing_args=["user"])


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, commit=True, **extra_info):
        if not email:
            raise ValueError('Users must have an email address')

        user_model = get_user_model()
        user = user_model(email=self.normalize_email(email), is_active=is_active)
        user.set_password(password)

        for key, value in extra_info.items():
            if hasattr(user, key):
                setattr(user, key, value)

        if commit:
            user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def _get_activation_key(self, email):
        salt = get_random_string(50)[:5].encode("utf-8")
        if not isinstance(email, bytes):
            email = email.encode("utf-8")
        activation_key = hashlib.sha1(salt + email).hexdigest()
        return activation_key

    def create_inactive_user(self, email, password, **extra_info):
        user_model = get_user_model()
        user = self.create_user(email=email, password=password,
                                is_active=False, commit=False, **extra_info)
        user.activation_key = self._get_activation_key(user.email)
        user.save()

        inactive_user_created.send(sender=user_model, user=user, extra_info=extra_info)

        return user

    def activate_user(self, activation_key):
        user_model = get_user_model()

        if SHA1_RE.search(activation_key):
            try:
                user = self.get(activation_key=activation_key)
            except user_model.DoesNotExist:
                return

            if user.activation_key_expired():
                return

            user.is_active = True
            user.activation_key = ACTIVATED
            user.save()

            user_activated.send(sender=user)

            return user


# noinspection PyAbstractClass
class BaseUser(DjangoAbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(_("email"), max_length=255, unique=True, db_index=True)
    created = models.DateTimeField(_("created"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    activation_key = models.CharField(_('activation key'), max_length=40, db_index=True)

    ACTIVATED = u"ALREADY_ACTIVATED"
    USERNAME_FIELD = "email"

    class Meta:
        abstract = True

    def get_short_name(self):
        return self.email

    def get_username(self):
        return self.email

    def activation_key_expired(self):
        if self.activation_key == self.ACTIVATED:
            return True

        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        if self.created + expiration_date <= timezone.now():
            return True

        return False

    activation_key_expired.boolean = True


class User(BaseUser):
    name = models.CharField(max_length=255, blank=True, null=True)

    def get_full_name(self):
        return self.name


inactive_user_created.connect(send_activation_email, dispatch_uid="quickstartup.activation")
