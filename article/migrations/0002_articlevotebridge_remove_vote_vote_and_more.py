# Generated by Django 4.0.6 on 2022-07-13 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleVoteBridge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=50, verbose_name='게시글 공감 카테고리 이름')),
            ],
        ),
        migrations.RemoveField(
            model_name='vote',
            name='vote',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='vote_article',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='vote_category',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='vote_user',
        ),
        migrations.AddField(
            model_name='article',
            name='article_vote',
            field=models.ManyToManyField(through='article.ArticleVoteBridge', to='article.vote'),
        ),
        migrations.AddField(
            model_name='vote',
            name='category',
            field=models.CharField(default='', max_length=50, verbose_name='공감종류'),
        ),
        migrations.AddField(
            model_name='articlevotebridge',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article'),
        ),
        migrations.AddField(
            model_name='articlevotebridge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articlevotebridge',
            name='vote',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.vote'),
        ),
    ]