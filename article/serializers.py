from rest_framework import serializers
from article.models import (
    Article as ArticleModel,
    Comment as CommentModel,
    CommentLikeBridge,
    ArticleVoteBridge,
)
from user.models import User as User
from user.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    comments_related_article = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_comments_related_article(self,obj):
        return obj.article.id
    def get_author(self,obj):
        return obj.comment_author.username

    def get_count(self,obj):
        like_count = CommentLikeBridge.objects.filter(comment_id=obj.id).count()
        return like_count

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
        fields = ['id', 'article', 'author', 'comment_created_at', 'comment_contents', 'comments_related_article', 'count']

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()

    def get_category(self,obj):
        return obj.article_category.name
    def get_author(self,obj):
        return obj.article_author.username

    def get_vote(self,obj):
        votes = ArticleVoteBridge.objects.filter(article_id=obj.id)
        votes = list(votes.values())
        vote_count = dict(fox=0, green=0, miss=0)
        for vote in votes:
            if vote['category'] == '폭스입니다':
                vote_count['fox'] += 1
            elif vote['category'] == '그린라이트':
                vote_count['green'] += 1
            else:
                vote_count['miss'] += 1
        return vote_count

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
        fields = ['id','author','article_title','category','article_image', 'board', 'vote',
        'article_contents','article_post_date',
        'article_exposure_date','comment_set'
        ]

