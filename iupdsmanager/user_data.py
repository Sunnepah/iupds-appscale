# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.api.users import UserNotFoundError

from iupdsmanager.models import Profile


class UserData:

    def __init__(self):
        pass

    @staticmethod
    def get_user_data():
        try:
            user = users.get_current_user()
            if user:
                data = {"email": user.email(), "nickname": user.nickname(), "user_id": user.user_id(),
                        "is_current_user_admin": users.is_current_user_admin()}
                return data
            else:
                users.create_login_url('/')
        except UserNotFoundError:
            return None

    @staticmethod
    def get_user_id():
        user_profile = Profile.objects.get(email=UserData.get_user_email())
        return str(user_profile.id)

    @staticmethod
    def get_user_email():
        user = UserData.get_user_data()
        return str(user['email'])

    @staticmethod
    def get_profile():
        try:
            user_profile = Profile.objects.get(email=UserData.get_user_email())
            return user_profile
        except:
            return False