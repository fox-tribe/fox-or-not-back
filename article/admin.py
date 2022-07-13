from django.contrib import admin
from article.models import Article, ArticleVoteBridge, Comment, Category, CommentLikeBridge, Vote, ArticleLike, CommentLike, Board, ArticleLikeBridge


admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(ArticleLike)
admin.site.register(CommentLike)
admin.site.register(ArticleLikeBridge)
admin.site.register(CommentLikeBridge)
admin.site.register(ArticleVoteBridge)
admin.site.register(Board)