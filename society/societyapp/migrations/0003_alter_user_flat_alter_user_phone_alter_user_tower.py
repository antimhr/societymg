# Generated by Django 4.0.3 on 2022-04-14 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('societyapp', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='flat',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='tower',
            field=models.IntegerField(default=0),
        ),
    ]
