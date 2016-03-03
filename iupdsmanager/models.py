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
    last_login = models.DateTimeField(auto_now=None)

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
    admin_type = models.CharField(max_length=15,
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
        (ACTIVATION, 'Freshman'),
        (PASSWORD, 'Password'),
    )

    user_uuid = models.UUIDField(null=False)
    email_sent = models.SmallIntegerField(default=0)
    mail_type = models.CharField(max_length=2,
                                 choices=MAIL_TYPE,
                                 default=ACTIVATION)

    def is_upperclass(self):
        return self.mail_type in (self.ACTIVATION, self.PASSWORD)