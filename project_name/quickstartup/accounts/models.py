# coding: utf-8


import datetime
import re
import random
import hashlib

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser as DjangoAbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.dispatch import Signal
from django.contrib.auth.models import BaseUserManager


SHA1_RE = re.compile('^[a-f0-9]{40}$')
ACTIVATED = u"ALREADY_ACTIVATED"

inactive_user_created = Signal(providing_args=["user", "extra_info"])
user_activated = Signal(providing_args=["user"])


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, commit=True):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), is_active=is_active)
        user.set_password(password)

        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def _get_activation_key(self, email):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        activation_key = hashlib.sha1(salt + email).hexdigest()
        return activation_key

    def create_inactive_user(self, email, password, extra_info=None):
        user = self.create_user(email=email, password=password, is_active=False)
        user.activation_key = self._get_activation_key(user.email)
        user.save()

        inactive_user_created.send(sender=user, extra_info=extra_info)

        return user

    def activate_user(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                user = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return

            if user.activation_key_expired():
                return

            user.is_active = True
            user.activation_key = ACTIVATED
            user.save()

            user_activated.send(sender=user)

            return user


class BaseUser(DjangoAbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(_("email"), max_length=255, unique=True, db_index=True)
    created = models.DateTimeField(_("created"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    activation_key = models.CharField(_('activation key'), max_length=40, db_index=True)

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

    activation_key_expired.boolean = True


class User(BaseUser):
    name = models.CharField(max_length=255, blank=True, null=True)
