# Generated by Django 4.0.6 on 2022-07-18 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=50, verbose_name='게시물 제옥')),
                ('article_contents', models.TextField(max_length=500, verbose_name='게시물 내용')),
                ('article_image', models.ImageField(blank=True, upload_to='', verbose_name='이미지')),
                ('article_post_date', models.DateField(auto_now_add=True, verbose_name='게시 일자')),
                ('article_exposure_date', models.DateField(blank=True, verbose_name='게시 만료 일자')),
                ('article_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_category', models.CharField(default='', max_length=50, verbose_name='공감종류')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='게시판 이름')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='게시글 카테고리 이름')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_contents', models.TextField(max_length=100, verbose_name='내용')),
                ('comment_created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시간')),
                ('comment_updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article', verbose_name='게시글')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_category', models.CharField(default='', max_length=50, verbose_name='공감종류')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=50, verbose_name='공감종류')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLikeBridge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=50, verbose_name='코멘트 공감 카테고리 이름')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.comment')),
                ('like', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.commentlike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_like',
            field=models.ManyToManyField(through='article.CommentLikeBridge', to='article.commentlike'),
        ),
        migrations.CreateModel(
            name='ArticleVoteBridge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=50, verbose_name='게시글 투표 카테고리 이름')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.vote')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLikeBridge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=50, verbose_name='게시글 공감 카테고리 이름')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
                ('like', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.articlelike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='article_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.category', verbose_name='카테고리 종류'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_like',
            field=models.ManyToManyField(through='article.ArticleLikeBridge', to='article.articlelike'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_vote',
            field=models.ManyToManyField(through='article.ArticleVoteBridge', to='article.vote'),
        ),
        migrations.AddField(
            model_name='article',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.board', verbose_name='해당 게시판'),
        ),
    ]
