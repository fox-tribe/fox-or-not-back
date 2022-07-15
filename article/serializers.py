from rest_framework import serializers
from article.models import (
    Article as ArticleModel,
    Comment as CommentModel,
    ArticleLike as ArticleLikeModel,
    CommentLike as CommentLikeModel,
    Vote as VoteModel,
)
from user.models import User as User
from user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    comments_related_article = serializers.SerializerMethodField()

    def get_comments_related_article(self,obj):
        return obj.article.id

    # custum update
    def update(self, instance, validated_data):        
        for key, value in validated_data.items():
            if key == "comment_author":
                instance.user(value)
                continue
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta :
        model = CommentModel
        fields = ['id', 'article', 'comment_author', 'comment_contents', 'comments_related_article']



class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self,obj):
        return obj.article_category.name

    def get_author(self,obj):
        return obj.article_author.username

    # custum update
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "article_author":
                instance.set_author(value)
                continue

            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = ArticleModel
        fields = ['id','author','article_title','category','article_image', 'board',
        'article_contents','article_post_date',
        'article_exposure_date','comment_set'
        ]
