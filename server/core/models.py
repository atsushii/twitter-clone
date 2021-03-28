from django.db import models
from django.contrib.auth.models import BaseUserManager, \
                                       AbstractBaseUser, \
                                       PermissionsMixin
from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError('User must have an username')

        user = self.model(username=self.model.normalize_username(username), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=20,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return f'{self.username}'


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    tweet = models.TextField(max_length=280)
    created_date = models.DateTimeField(auto_now=True)


class ThreadManager(models.Manager):
    def by_user(self, user):
        lookup = Q(first=user) | Q(second=user)
        lookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(lookup).exclude(lookup2).distinct()
        return qs

    def get_or_new(self, user, target_username):
        try:
            username = user.username
            if username == target_username:
                return None
            lookup = Q(first__username=username) & Q(second__username=target_username)
            lookup2 = Q(first__username=target_username) & Q(second__username=username)
            qs = self.get_queryset().filter(lookup | lookup2).distinct()
            if qs.count() == 1:
                return qs.first()
            elif qs.count() > 1:
                return qs.order_by('timestamp').first()
            else:
                cls = user.__class__
                user2 = cls.objects.get(username=target_username)
                if user != user2:
                    obj = self.model(
                        first=user,
                        second=user2
                    )
                    obj.save()
                    return obj
            return None
        except Exception as e:
            return None


class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cat_thread_first')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name='threads')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.id}: {self.sender}: {self.message}: {self.timestamp}'




