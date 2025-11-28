"""
Settings package for adminired project.
"""
from decouple import config

# Determine which settings to import based on DJANGO_SETTINGS_MODULE
# or default to development
ENVIRONMENT = config('DJANGO_ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *

