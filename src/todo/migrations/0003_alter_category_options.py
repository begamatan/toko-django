# Generated by Django 4.1 on 2022-08-28 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_category_description_post_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]