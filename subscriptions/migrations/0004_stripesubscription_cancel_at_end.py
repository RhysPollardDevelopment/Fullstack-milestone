# Generated by Django 3.2 on 2021-06-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_invoice_stripesubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripesubscription',
            name='cancel_at_end',
            field=models.BooleanField(default=False),
        ),
    ]
