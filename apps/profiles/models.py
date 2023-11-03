from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from slugify import slugify


# Create your models here.

User = get_user_model()


# class Location(models.Model):
#     country = models.CharField(max_length=35)
#     region = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.country
#
#
# class Language(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField('First Name', max_length=30)
#     last_name = models.CharField('Last name', max_length=30)
#     professions = models.CharField('speciality', max_length=35)
#     native_language = models.ForeignKey(Language, related_name="native_speakers_profiles", on_delete=models.SET_NULL,
#                                         blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profile_image/', verbose_name='Profile-Image', blank=True, null=True)
#     country = models.CharField(max_length=50, unique=True)
#     arial = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.user}'


# class LanguageProficiency(models.Model):
#     LEVEL_CHOICES = [
#         ('A1', 'A1'),
#         ('A2', 'A2'),
#         ('B1', 'B1'),
#         ('B2', 'B2'),
#         ('C1', 'C1'),
#         ('C2', 'C2'),
#     ]
#
#     profile = models.ForeignKey(Profile, related_name='proficiencies', on_delete=models.CASCADE)
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)
#     level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
#
#     class Meta:
#         unique_together = ('profile', 'language')
#         ordering = ['language']
#
#     def __str__(self):
#         return f"{self.profile} - {self.language} ({self.level})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField('User Name', max_length=30)
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last name', max_length=30)
    professions = models.CharField('speciality', max_length=35)
    profile_image = models.ImageField(upload_to='profile_image/', verbose_name='Profile-Image', blank=True, null=True)
    profile_background = models.ImageField(upload_to='profile_background/', verbose_name='Profile-Background', blank=True, null=True)
    subscriptions = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    country = models.CharField(max_length=50)
    arial = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print(f"User {instance.email} was created: {created}")
    if created:
        UserProfile.objects.create(user=instance)
