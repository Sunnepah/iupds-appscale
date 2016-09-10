# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Django settings for iupds project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-c&qt=71oi^e5s8(ene*$b89^#%*0xeve$x_trs91veok9#0h0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # 'corsheaders',
    'rest_framework',
    'iupdsmanager',
    'authentication',
    'corsheaders',
    'pdsoauth',
)

MIDDLEWARE_CLASSES = (
    'google.appengine.ext.ndb.django_middleware.NdbDjangoMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'iupds.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # "django.core.context_processors.request",
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'iupds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# [START db_setup]
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/<your-cloud-sql-instance>',
            'NAME': '<your-database-name>',
            'USER': 'root',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'iupds_db',
            'USER': 'root',
            'PASSWORD': 'secret',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
# [END db_setup]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # 'DEFAULT_PERMISSION_CLASSES': (
    #    'rest_framework.permissions.AllowAny',
    # ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_REGEX_WHITELIST = ()
CORS_URLS_REGEX = '^.*$'  # r'^/api/.*$'

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

CORS_EXPOSE_HEADERS = ()

CORS_PREFLIGHT_MAX_AGE = 86400

CORS_ALLOW_CREDENTIALS = False

CORS_REPLACE_HTTPS_REFERER = False

AUTHORIZATION_CODE_EXPIRE_SECONDS = 60
ACCESS_TOKEN_EXPIRE_SECONDS = 36000
REFRESH_TOKEN_EXPIRE_SECONDS = None
ALLOWED_REDIRECT_URI_SCHEMES = ['http', 'https']

CLIENT_ID_GENERATOR_CLASS = 'oauth2_provider.generators.ClientIdGenerator'
CLIENT_SECRET_GENERATOR_CLASS = 'oauth2_provider.generators.ClientSecretGenerator'
CLIENT_SECRET_GENERATOR_LENGTH = 128
OAUTH2_SERVER_CLASS = 'oauthlib.oauth2.Server'
OAUTH2_VALIDATOR_CLASS = 'iupdsmanager.oauth2_validators.OAuth2Validator'
OAUTH2_BACKEND_CLASS = 'iupdsmanager.oauth2_backends.OAuthLibCore'
SCOPES = {"read": "Reading scope"}
DEFAULT_SCOPES = ['__all__']
READ_SCOPE = 'read'
WRITE_SCOPE = 'write'

REQUEST_APPROVAL_PROMPT = 'force'

# Special settings that will be evaluated at runtime
_SCOPES = []
_DEFAULT_SCOPES = []

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'applogfile': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_DIR, 'iupds.log'),
#             'maxBytes': 1024 * 1024 * 15,  # 15MB
#             'backupCount': 10,
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }

# ===================APPSCALE========================
APPSC_KEY = 'app_secret'
APPSCALE_PDS_HOST = 'http://192.168.33.10:8080'


# ==============TYK API GATEWAY========================
TYK_API_ORG_ID = "577417e90b0c240354000001"
TYK_API_POLICY_ID = "57741e9f0b0c240354000003"

TYK_GATEWAY = 'http://192.168.33.30:8080'

# If the user accepts the Client access and has authenticated successfully,
# your app calls the Tyk REST API OAuth Authorization endpoint (/tyk/oauth/authorize-client/) with the POST parameters
TYK_OAUTH_AUTHORIZE_ENDPOINT = TYK_GATEWAY + '/tyk/oauth/authorize-client/'

PDS_API_ID = '4818d7eadbb44c66546536015933a3bc'
PDS_API_NAME = 'PDS API v1'

# https://tyk.io/docs/tyk-api-gateway-v1-9/tyk-rest-api/
# x-tyk-authorization - node_secret located at /opt/tyk-gateway/tyk.conf on tyk server
# Authorization Endpoints below use this authorization secret
TYK_AUTHORIZATION_NODE_SECRET = '352d20ee67be67f6340b4c0605b044b7'

# Create a new OAuth Client ID
TYK_CREATE_CLIENT_ENDPOINT = TYK_GATEWAY + '/tyk/oauth/clients/create'

# Retrieve or delete OAuth Clients
TYK_CLIENTS_ENDPOINT = TYK_GATEWAY + '/tyk/oauth/clients/'

# Hot reload API Definitions and reload all muxers
TYK_RELOAD_ENDPOINT = TYK_GATEWAY + '/tyk/reload/'

# Health-check: get a snapshot of your API and tyk node performance
TYK_HEALTH_ENDPOINT = TYK_GATEWAY + '/tyk/health/'

# Invalidate Refresh Token DELETE
TYK_INVALIDATE_REFRESH_TOKEN = TYK_GATEWAY + '/tyk/oauth/refresh'

TYK_DELETE_ACCESS_TOKEN = TYK_GATEWAY + '/tyk/keys/'


# ===========VIRTUOSO DATABASE==============================
VIRTUOSO_HOST = "192.168.33.30"
VIRTUOSO_PORT = "8890"
VIRTUOSO_USER = "dba"
VIRTUOSO_PASSW = "dba"

SPARQL_ENDPOINT = "http://192.168.33.30:8890/sparql"
SPARQL_AUTH_ENDPOINT = "http://192.168.33.30:8890/sparql-auth"


# =========PDS GRAPH API SERVICE==============================
GRAPH_ROOT = 'https://mypds.me/users'
GRAPH_USER_PERMISSION_ENDPOINT = 'http://192.168.33.30:9000/api/v1/user/graph/grant/'
GRAPH_USER_PW = 'secret'
NEW_SQL_USER_ENDPOINT = 'http://192.168.33.30:9000/api/v1/user/new/'
