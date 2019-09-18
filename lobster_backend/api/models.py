from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class UserManager(UserManager):
    def create_user(self, username, email, password):

        if not username:
            raise ValueError('User must have a login!')

        user = self.model(
            username = username,
            email = email
        )

        user.set_password(password)
        user.save(using = self._db)

        return user

class User(AbstractUser):
    objects = UserManager()
