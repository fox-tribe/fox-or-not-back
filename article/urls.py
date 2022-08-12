from django.urls import path
from article import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    #article/
    path('', views.ArticleView.as_view()),
    path('<obj_id>/comment/', views.CommentView.as_view()),
    path('pagination/', views.ArticlePagination.as_view()),
    path('pagination/comment/', views.CommentPagination.as_view()),
    path('search/', views.SearchResult.as_view()),
    path('likeCount/', views.MostLikedArticleView.as_view()),
    path('voteCount/', views.MostVotedArticleView.as_view()),
    path('voteCount/board/', views.MostVotedArticleByBoardView.as_view()),
    path('comment/likeCount/', views.MostLikedCommentView.as_view()),
    path('board/', views.ArticleByBoard.as_view()),
    path('<obj_id>/', views.ArticleView.as_view()),
    path('<obj_id>/detail/', views.ArticleDetailView.as_view()),
    path('<comment_id>/comment/like/', views.CommentLikeView.as_view()),
    path('<article_id>/article/like/', views.ArticleLikeView.as_view()),
    path('<article_id>/article/vote/', views.ArticleVoteBridgeView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)