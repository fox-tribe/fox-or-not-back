# Generated by Django 4.0.6 on 2022-07-11 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateTimeField(max_length=20, null=True, verbose_name='생년월일'),
        ),
    ]