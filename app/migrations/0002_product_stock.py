# Generated by Django 3.1.2 on 2021-02-02 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.CharField(default=100, max_length=10),
        ),
    ]