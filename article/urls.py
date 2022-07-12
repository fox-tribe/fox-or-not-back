from django.urls import path
from article import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    #article/
    path('', views.ArticleView.as_view()),
    path('<obj_id>/', views.ArticleView.as_view()),
    path('<obj_id>/detail/', views.ArticleDetailView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)