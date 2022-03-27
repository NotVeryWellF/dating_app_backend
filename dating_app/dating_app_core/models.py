from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
import uuid


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_active, is_superuser, is_staff, **extra_fields):
        if not username:
            raise ValueError("User must have an username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.username = username
        user.set_password(password)
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email, password=password,
                                 is_active=True, is_superuser=False, is_staff=False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email, password=password,
                                 is_active=True, is_superuser=True, is_staff=True, **extra_fields)

    def create_staffuser(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email, password=password,
                                 is_active=True, is_superuser=False, is_staff=True, **extra_fields)


def image_upload_path(instance, filename):
    return f'/images/user_{instance.user.id}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.IntegerChoices):
        Male = 1, "Male"
        Female = 2, "Female"
        Other = 3, "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.EmailField(max_length=256, unique=True, db_index=True)
    first_name = models.CharField(max_length=64, db_index=True)
    last_name = models.CharField(max_length=64, db_index=True)
    avatar = models.ImageField(upload_to=image_upload_path, null=True)
    fist_login = models.DateTimeField(default=datetime.datetime.now)
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    birth_date = models.DateField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'gender', 'birth_date']


