# Generated by Django 4.2.3 on 2023-07-27 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hibh_api", "0004_tracker_email_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tracker",
            name="email_token",
            field=models.CharField(max_length=255),
        ),
    ]