from django.db import models
from user.models import User


class ArticleLike(models.Model):
    like_category = models.CharField("공감종류", max_length=50, default="")

class CommentLike(models.Model):
    like_category = models.CharField("공감종류", max_length=50, default="") 
class Vote(models.Model):
    category = models.CharField("공감종류", max_length=50, default="") 
class Article(models.Model):
    article_author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    board = models.ForeignKey('Board', verbose_name="해당 게시판", on_delete=models.CASCADE)
    article_category = models.ForeignKey('Category', verbose_name="카테고리 종류", on_delete=models.CASCADE, null=True)
    article_title = models.CharField('게시물 제옥', max_length=50)
    article_contents = models.TextField('게시물 내용', max_length=500)
    article_image = models.ImageField('이미지', upload_to="", blank=True)
    article_post_date = models.DateField('게시 일자', auto_now_add=True)
    article_exposure_date = models.DateField('게시 만료 일자', blank=True)
    article_like = models.ManyToManyField(ArticleLike, through='ArticleLikeBridge')
    article_vote = models.ManyToManyField(Vote, through='ArticleVoteBridge')

    def __str__(self):
        return f"{self.article_author.username} 님이 {self.board}에 {self.article_category}태그로 작성한 글입니다."

class Comment(models.Model):
    comment_author = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    comment_contents = models.TextField("내용", max_length=100)
    comment_created_at = models.DateTimeField("생성시간", auto_now_add=True,)
    comment_updated_at = models.DateTimeField("수정시간",auto_now = True,)
    comment_like = models.ManyToManyField(CommentLike, through='CommentLikeBridge')

    def __str__(self):
       return f"{self.comment_author.username} 님이 작성하신 댓글입니다."

class Board(models.Model):
    name = models.CharField("게시판 이름", max_length=50, default="")

    def __str__(self):
       return f"{self.name}"

class Category(models.Model):
    name = models.CharField("게시글 카테고리 이름", max_length=50, default="")

    def __str__(self):
       return f"{self.name}"

class ArticleLikeBridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    like = models.ForeignKey(ArticleLike, on_delete=models.CASCADE, null=True)
    category = models.CharField("게시글 공감 카테고리 이름", max_length=50, default="")
    

class ArticleVoteBridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, null=True)
    category = models.CharField("게시글 투표 카테고리 이름", max_length=50, default="")

class CommentLikeBridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.ForeignKey(CommentLike, on_delete=models.CASCADE, null=True)
    category = models.CharField("코멘트 공감 카테고리 이름", max_length=50, default="")