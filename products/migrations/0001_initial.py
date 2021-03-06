# Generated by Django 3.2 on 2021-04-29 16:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=600)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('county', models.CharField(blank=True, max_length=40, null=True)),
                ('company_url', models.URLField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.IntegerField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=600)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('texture', models.CharField(blank=True, max_length=254, null=True)),
                ('flavour', models.CharField(blank=True, max_length=254, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.company')),
            ],
        ),
    ]
