from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username should be provided")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Invoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    invoice_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=200)
    date = models.DateField()


class Items(models.Model):
    invoice = models.ForeignKey(
        Invoices, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )
    desc = models.TextField()
    rate = models.FloatField()
    quantity = models.IntegerField()
