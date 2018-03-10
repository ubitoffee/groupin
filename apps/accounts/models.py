from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    team = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=500, blank=True)
    birthday = models.DateField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    about_me = models.TextField(max_length=500, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()
