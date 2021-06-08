# Generated by Django 3.2 on 2021-06-08 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_alter_product_product_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=400)),
                ('ingredients', models.TextField(null=True)),
                ('instructions', models.TextField(null=True)),
                ('publish_date', models.DateTimeField(help_text='Date used to determine loading date and user access.', null=True)),
                ('featured_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
    ]
