Social Authentication
=====================

The social authentication is implemented based on `python-social-auth
<http://python-social-auth.readthedocs.org/en/latest/index.html/>`_ and their documentation, please
check it seriously if you are going to implement social authentication.


Setting up social authentication
--------------------------------

TODO


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
