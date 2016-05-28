from __future__ import unicode_literals

from datetime import timedelta

from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ImproperlyConfigured

from iupds import settings
from iupdsmanager.validators import validate_uris
from django.apps import apps


# Create your models here.
class Profile(models.Model):
    uid = models.BigIntegerField(blank=True)
    appscale_user_id = models.CharField(max_length=50, unique=True, null=False)
    user_id_old = models.PositiveIntegerField(unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)

    full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)

    is_cloud_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    CLOUD_ADMIN = 'CA'
    APPLICATION_OWNER = 'AO'
    REGULAR_USER = 'RU'

    ADMIN_TYPE = (
        (CLOUD_ADMIN, 'Cloud Admin'),
        (APPLICATION_OWNER, 'Application Owner'),
        (REGULAR_USER, 'Regular User'),
    )

    # Cloud admins, Application owners, Regular users
    admin_type = models.CharField(max_length=20,
                                  choices=ADMIN_TYPE,
                                  default=REGULAR_USER)

    def is_upperclass(self):
        return self.admin_type in (self.CLOUD_ADMIN, self.APPLICATION_OWNER, self.REGULAR_USER)

    # def __unicode__(self):
    #     return self.profile

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


class EmailTrack(models.Model):
    ACTIVATION = 'ACTIVATION'
    PASSWORD = 'PASSWORD'

    MAIL_TYPE = (
        (ACTIVATION, 'Activation'),
        (PASSWORD, 'Password'),
    )

    user_uuid = models.UUIDField(null=False)
    email_sent = models.BooleanField(default=False)
    mail_type = models.CharField(max_length=25,
                                 choices=MAIL_TYPE,
                                 default=ACTIVATION)

    def is_upperclass(self):
        return self.mail_type in (self.ACTIVATION, self.PASSWORD)


class Contact(models.Model):
    profile = models.ForeignKey(
            'Profile',
            on_delete=models.CASCADE,
        )
    contact = models.CharField(null=False, max_length=64)

    PHONE = 'PHONE'
    FAX = 'FAX'
    EMAIL = 'EMAIL'
    WWW = 'WWW'
    SKYPE = 'SKYPE'
    SKYPE_NO = 'SKYPE_NO'
    BLOG = 'BLOG'
    OTHER = 'OTHER'

    CONTACT_SECTION = (
        (PHONE, 'Phone'),
        (FAX, 'Fax'),
        (EMAIL, 'Email'),
        (WWW, 'www'),
        (SKYPE, 'Skype'),
        (SKYPE_NO, 'Skype_no'),
        (BLOG, 'Blog'),
        (OTHER, 'Other'),
    )

    contact_section = models.CharField(max_length=15,
                                       choices=CONTACT_SECTION, default=OTHER)

    HOME = 'HOME'
    OFFICE = 'OFFICE'
    MOBILE = 'MOBILE'
    VOICE = 'VOICE'

    CONTACT_TYPE = (
        (HOME, 'Home'),
        (OFFICE, 'Offcice'),
        (MOBILE, 'Mobile'),
        (VOICE, 'Voice'),
    )

    contact_type = models.CharField(max_length=15, choices=CONTACT_TYPE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deletion_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.contact


class Address(models.Model):
    profile = models.ForeignKey(
                'Profile',
                on_delete=models.CASCADE,
            )

    street = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=25, null=True)
    post_code = models.CharField(max_length=8, null=False)
    county = models.CharField(max_length=25, null=True)
    district = models.CharField(max_length=25, null=True)
    city_district = models.CharField(max_length=25, null=True)
    country = models.CharField(max_length=25, null=True)
    primary = models.BooleanField(null=False, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deletion_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.address


class Graph(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
    )

    graph = models.URLField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deletion_date = models.DateTimeField(null=True)


@python_2_unicode_compatible
class AbstractApplication(models.Model):
    """
    An Application instance represents a Client on the Authorization server.
    Usually an Application is created manually by client's developers after
    logging in on an Authorization Server.

    Fields:

    * :attr:`client_id` The client identifier issued to the client during the
                        registration process as described in :rfc:`2.2`
    * :attr:`user` ref to a Django user
    * :attr:`redirect_uris` The list of allowed redirect uri. The string
                            consists of valid URLs separated by space
    * :attr:`client_type` Client type as described in :rfc:`2.1`
    * :attr:`authorization_grant_type` Authorization flows available to the
                                       Application
    * :attr:`client_secret` Confidential secret issued to the client during
                            the registration process as described in :rfc:`2.2`
    * :attr:`name` Friendly name for the Application
    """
    CLIENT_CONFIDENTIAL = 'confidential'
    CLIENT_PUBLIC = 'public'
    CLIENT_TYPES = (
        (CLIENT_CONFIDENTIAL, _('Confidential')),
        (CLIENT_PUBLIC, _('Public')),
    )

    GRANT_AUTHORIZATION_CODE = 'authorization-code'
    GRANT_IMPLICIT = 'implicit'
    GRANT_PASSWORD = 'password'
    GRANT_CLIENT_CREDENTIALS = 'client-credentials'
    GRANT_TYPES = (
        (GRANT_AUTHORIZATION_CODE, _('Authorization code')),
        (GRANT_IMPLICIT, _('Implicit')),
        (GRANT_PASSWORD, _('Resource owner password-based')),
        (GRANT_CLIENT_CREDENTIALS, _('Client credentials')),
    )

    client_id = models.CharField(max_length=100, unique=True,
                                 null=False, db_index=True)
    # user = models.ForeignKey(Profile, related_name="%(app_label)s_%(class)s",
    #                          null=True, blank=True)

    help_text = _("Allowed URIs list, space separated")
    redirect_uris = models.TextField(help_text=help_text,
                                     validators=[validate_uris], blank=True)
    client_type = models.CharField(max_length=32, choices=CLIENT_TYPES)
    authorization_grant_type = models.CharField(max_length=32,
                                                choices=GRANT_TYPES)
    client_secret = models.CharField(max_length=255, blank=True,
                                     null=False, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    skip_authorization = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.redirect_uris \
            and self.authorization_grant_type \
            in (AbstractApplication.GRANT_AUTHORIZATION_CODE,
                AbstractApplication.GRANT_IMPLICIT):
            error = _('Redirect_uris could not be empty with {0} grant_type')
            raise ValidationError(error.format(self.authorization_grant_type))

    def get_absolute_url(self):
        return reverse('oauth2_provider:detail', args=[str(self.id)])

    def __str__(self):
        return self.name or self.client_id


class Application(AbstractApplication):
    class Meta(AbstractApplication.Meta):
        swappable = ''


@python_2_unicode_compatible
class Grant(models.Model):
    """
    A Grant instance represents a token with a short lifetime that can
    be swapped for an access token, as described in :rfc:`4.1.2`

    Fields:

    * :attr:`user` The Django user who requested the grant
    * :attr:`code` The authorization code generated by the authorization server
    * :attr:`application` Application instance this grant was asked for
    * :attr:`expires` Expire time in seconds, defaults to
                      :data:`settings.AUTHORIZATION_CODE_EXPIRE_SECONDS`
    * :attr:`redirect_uri` Self explained
    * :attr:`scope` Required scopes, optional
    """
    user = models.ForeignKey(Profile)
    code = models.CharField(max_length=255, db_index=True)  # code comes from oauthlib
    application = models.ForeignKey(Application)
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=255)
    scope = models.TextField(blank=True)

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    def redirect_uri_allowed(self, uri):
        return uri == self.redirect_uri

    def __str__(self):
        return self.code


@python_2_unicode_compatible
class AccessToken(models.Model):
    """
    An AccessToken instance represents the actual access token to
    access user's resources, as in :rfc:`5`.

    Fields:

    * :attr:`user` The Django user representing resources' owner
    * :attr:`token` Access token
    * :attr:`application` Application instance
    * :attr:`expires` Date and time of token expiration, in DateTime format
    * :attr:`scope` Allowed scopes
    """
    user = models.ForeignKey(Profile, blank=True, null=True)
    token = models.CharField(max_length=255, db_index=True)
    application = models.ForeignKey(Application)
    expires = models.DateTimeField()
    scope = models.TextField(blank=True)

    def is_valid(self, scopes=None):
        """
        Checks if the access token is valid.

        :param scopes: An iterable containing the scopes to check or None
        """
        return not self.is_expired() and self.allow_scopes(scopes)

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    def allow_scopes(self, scopes):
        """
        Check if the token allows the provided scopes

        :param scopes: An iterable containing the scopes to check
        """
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)

    def revoke(self):
        """
        Convenience method to uniform tokens' interface, for now
        simply remove this token from the database in order to revoke it.
        """
        self.delete()

    @property
    def scopes(self):
        """
        Returns a dictionary of allowed scope names (as keys) with their descriptions (as values)
        """
        return {name: desc for name, desc in settings.SCOPES.items() if name in self.scope.split()}

    def __str__(self):
        return self.token


@python_2_unicode_compatible
class RefreshToken(models.Model):
    """
    A RefreshToken instance represents a token that can be swapped for a new
    access token when it expires.

    Fields:

    * :attr:`user` The Django user representing resources' owner
    * :attr:`token` Token value
    * :attr:`application` Application instance
    * :attr:`access_token` AccessToken instance this refresh token is
                           bounded to
    """
    user = models.ForeignKey(Profile)
    token = models.CharField(max_length=255, db_index=True)
    application = models.ForeignKey(Application)
    access_token = models.OneToOneField(AccessToken,
                                        related_name='refresh_token')

    def revoke(self):
        """
        Delete this refresh token along with related access token
        """
        AccessToken.objects.get(id=self.access_token.id).revoke()
        self.delete()

    def __str__(self):
        return self.token


def get_application_model():
    """ Return the Application model that is active in this project. """
    try:
        app_label = "iupdsmanager"
    except ValueError:
        e = "APPLICATION_MODEL must be of the form 'app_label.model_name'"
        raise ImproperlyConfigured(e)
    app_model = apps.get_model(app_label, Application)
    if app_model is None:
        e = "APPLICATION_MODEL refers to model {0} that has not been installed"
        raise ImproperlyConfigured(e.format(Application))
    return app_model


def clear_expired():
    now = timezone.now()
    refresh_expire_at = None

    REFRESH_TOKEN_EXPIRE_SECONDS = settings.REFRESH_TOKEN_EXPIRE_SECONDS
    if REFRESH_TOKEN_EXPIRE_SECONDS:
        if not isinstance(REFRESH_TOKEN_EXPIRE_SECONDS, timedelta):
            try:
                REFRESH_TOKEN_EXPIRE_SECONDS = timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS)
            except TypeError:
                e = "REFRESH_TOKEN_EXPIRE_SECONDS must be either a timedelta or seconds"
                raise ImproperlyConfigured(e)
        refresh_expire_at = now - REFRESH_TOKEN_EXPIRE_SECONDS

    with transaction.atomic():
        if refresh_expire_at:
            RefreshToken.objects.filter(access_token__expires__lt=refresh_expire_at).delete()
        AccessToken.objects.filter(refresh_token__isnull=True, expires__lt=now).delete()
        Grant.objects.filter(expires__lt=now).delete()