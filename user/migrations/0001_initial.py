# Generated by Django 4.0.6 on 2022-07-11 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='회원')),
                ('email', models.EmailField(max_length=100, verbose_name='이메일 주소')),
                ('password', models.CharField(max_length=128, verbose_name='비밀번호')),
                ('nickname', models.CharField(max_length=30, verbose_name='닉네임')),
                ('birth', models.DateTimeField(max_length=20, verbose_name='생년월일')),
                ('gender', models.CharField(max_length=20, verbose_name='성별')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='가입일')),
                ('sign_out_date', models.DateTimeField(null=True, verbose_name='탈퇴일')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
                ('introduction', models.TextField(verbose_name='소개')),
                ('profile_image', models.ImageField(null=True, upload_to='', verbose_name='프로필사진')),
            ],
        ),
    ]
