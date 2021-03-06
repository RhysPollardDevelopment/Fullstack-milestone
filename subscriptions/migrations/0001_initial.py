# Generated by Django 3.2 on 2021-05-07 12:11

from django.db import migrations, models
import django.db.models.deletion
import subscriptions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("expiry_date", models.DateTimeField(null=True, blank=True)),
                (
                    "user_profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="profiles.userprofile",
                    ),
                ),
            ],
        ),
    ]
