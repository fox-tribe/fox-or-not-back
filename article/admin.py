from django.contrib import admin
from article.models import Article, Comment, Category, Vote, Like, Board


admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Like)
admin.site.register(Board)