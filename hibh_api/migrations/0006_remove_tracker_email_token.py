# Generated by Django 4.2.3 on 2023-07-27 18:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hibh_api", "0005_alter_tracker_email_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tracker",
            name="email_token",
        ),
    ]
