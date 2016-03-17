from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Profile(models.Model):
    uid = models.BigIntegerField(blank=True)
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

    def __unicode__(self):
        return self.profile

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