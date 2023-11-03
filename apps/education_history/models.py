from django.db import models
from apps.profiles.models import UserProfile
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()


class EducationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educ_history')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educ_history')
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=250, blank=True)
    field_of_study = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return f'{self.user}, {self.profile}'


class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='languages')
    LEVEL_CHOICES = [
            ('A1', 'A1'),
            ('A2', 'A2'),
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('C1', 'C1'),
            ('C2', 'C2'),
        ]
    languages = models.CharField(max_length=100)
    languages_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
