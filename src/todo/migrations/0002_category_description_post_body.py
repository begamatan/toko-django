# Generated by Django 4.1 on 2022-08-26 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(null=True),
        ),
    ]
