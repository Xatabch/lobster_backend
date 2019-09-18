from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Count

class UserManager(UserManager):
    def get_user_profile(self, username):
        return self.all().annotate(num_followers=Count('target'), num_following=Count('subscriber')).get(username=username)
    
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

class UserRelationsManager(models.Manager):
    def is_follow(self, subscriber, target):
        target_user = User.objects.all().get(username=target)
        return self.all().filter(subscriber=subscriber, target=target_user)

class UserRelations(models.Model):
    objects = UserRelationsManager()

    subscriber = models.ForeignKey(User, on_delete = models.CASCADE, related_name='subscriber')
    target = models.ForeignKey(User, on_delete = models.CASCADE, related_name='target')

    class Meta:
        unique_together = (("subscriber", "target"))
