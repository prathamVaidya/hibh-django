# Generated by Django 4.2.3 on 2023-07-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "hibh_api",
            "0003_alert_created_at_alert_updated_at_tracker_created_at_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="tracker",
            name="email_token",
            field=models.CharField(default="abcd", max_length=255, unique=True),
            preserve_default=False,
        ),
    ]