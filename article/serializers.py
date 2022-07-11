from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from user.models import User as User


class CommentSerializer(serializers.ModelSerializer):
    comments_related_article = serializers.SerializerMethodField()

    def get_comments_related_article(self,obj):
        return obj.article.id

    # custum update
    def update(self, instance, validated_data):        
        for key, value in validated_data.items():
            if key == "comment_authour":
                instance.user(value)
                continue
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta :
        model = CommentModel
        fields = ['id', 'article', 'comment_authour', 'comment_contents', 'comments_related_article']


class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)

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
        fields = ['id','article_author','article_title','article_image',
        'article_contents','article_post_date',
        'article_exposure_date','comment_set'
        ]

