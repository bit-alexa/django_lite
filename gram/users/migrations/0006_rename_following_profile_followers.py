# Generated by Django 3.2 on 2022-12-12 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='following',
            new_name='followers',
        ),
    ]
