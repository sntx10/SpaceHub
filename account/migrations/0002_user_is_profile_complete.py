# Generated by Django 4.2.5 on 2023-10-19 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_profile_complete",
            field=models.BooleanField(default=False),
        ),
    ]
