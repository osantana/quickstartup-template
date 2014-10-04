Social Authentication
=====================

The social authentication is implemented based on `python-social-auth
<http://python-social-auth.readthedocs.org/en/latest/index.html/>`_ and their documentation, please
check it seriously if you are going to implement or customize social authentication.

The scope of this document are everything outside their documentation and the assumptions made in
the project.


Setting up social authentication
--------------------------------

Social authentication is enabled by default and its almost functional, since it depends on your
application to really work.

The basic assumptions and decisions made for social authentication are:

* User can sign-up with social accounts, but login is disabled
* User can connect to other social accounts when he is already authenticated
* The user email will not be overriden when connecting with other social account
* We will not handle disconnection (user should revoke the token in his social account)


With this in mind, let's add support for google-oauth authentication as an example (and it should be
similar for any social backend). First, we need to enable the AUTHENTICATION_BACKEND::


    AUTHENTICATION_BACKENDS = ('social.backends.google.GoogleOAuth',
                               ...other backends here ...)

After you register your application, Google will provide the consumer and secret keys::

    SOCIAL_AUTH_GOOGLE_OAUTH_KEY = 'app-key'
    SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = 'app-secret'

If you need to change the permission scope::

    SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [...]


That's all for this simple case. At this point an user should be able to sign-up using his Google
account.


Disabling social authentication
-------------------------------

If you want to disable social authentication, you should:

* Remove the url of social profile view
* Override the sign-up template and remove the social authentication links
* Remove all entries in AUTHENTICATION_BACKENDS in your settings that begins with "social."


This should be enough to remove social authentication of the application level. To completely
disable it, those are the additional steps:

* In your settings, remove all entries that starts with "SOCIAL_AUTH_*"
* In your settings, remove all entries in CONTEXT_PROCESSORS that starts with "social."
* In your settings, remove all entries in MIDDLEWARE_CLASSES that starts with "social."
* In your settings, remove all entries in INSTALLED_APPS that starts with "social."
* In your project urls.py, remove the entry with the namespace set as "social"
