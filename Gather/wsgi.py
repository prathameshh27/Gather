"""
WSGI config for Gather project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from Gather.settings import base_settings


if base_settings.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gather.settings.local_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gather.settings.prod_settings')


application = get_wsgi_application()
