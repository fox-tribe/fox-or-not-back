# Generated by Django 4.0.6 on 2022-07-11 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sign_out_date',
            field=models.DateTimeField(null=True, verbose_name='탈퇴일'),
        ),
    ]
