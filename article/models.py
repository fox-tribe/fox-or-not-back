from contextlib import nullcontext
from django.db import models
from django.utils import timezone


        
class Article(models.Model):
    article_author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    board = models.ForeignKey('Board', verbose_name="해당 게시판", on_delete=models.CASCADE)
    article_category = models.ForeignKey('Category', verbose_name="카테고리 종류", on_delete=models.CASCADE, null=True)
    article_title = models.CharField('게시물 제옥', max_length=50)
    article_contents = models.TextField('게시물 내용', max_length=500)
    article_image = models.ImageField('이미지', upload_to="", blank=True)
    article_post_date = models.DateField('게시 일자', auto_now_add=True)
    article_exposure_date = models.DateField('게시 만료 일자', blank=True)
    
    def __str__(self):
        return f"{self.article_author.username} 님이 {self.board}에 {self.article_category}태그로 작성한 글입니다."

class Comment(models.Model):
    comment_author = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    comment_contents = models.TextField("내용", max_length=100)
    comment_created_at = models.DateTimeField("생성시간", auto_now_add=True)
    comment_updated_at = models.DateTimeField("수정시간",auto_now = True)

    def __str__(self):
       return f"{self.comment_author.username} 님이 작성하신 댓글입니다."

class Like(models.Model):
    like = models.BooleanField("공감여부")
    like_category = models.CharField("공감종류", max_length=50, default="")
    like_comment = models.ManyToManyField(Comment, related_name="comment_likes")
    like_article = models.ManyToManyField(Article, related_name="article_likes")

    def __str__(self, request):
       return f"{self.article_author.username}{self.comment_author.username}님이 {self.like_comment}{self.like_article}에 {self.like_category}공감했습니다."
    
class Vote(models.Model):
    vote_user = models.ForeignKey('user.User', verbose_name="투표한 유저", on_delete=models.CASCADE)
    vote_article = models.ForeignKey('Article', verbose_name="투표한 게시글", on_delete=models.CASCADE)
    vote = models.BooleanField("투표여부")
    vote_category = models.CharField("투표 종류", max_length=50)

    def __str__(self):
       return f"{self.vote_user.username}님이 {self.vote_article}에 {self.vote_category}투표했습니다."

class Board(models.Model):
    name = models.CharField("게시판 이름", max_length=50, default="")

    def __str__(self):
       return f"{self.name}"

class Category(models.Model):
    name = models.CharField("카테고리 이름", max_length=50, default="")

    def __str__(self):
       return f"{self.name}"