from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserView, 
    UserApiView, 
    TokenObtainPairView, 
    OnlyAuthenticatedUserView,
)

urlpatterns = [
    # user/
    path('', UserView.as_view()),
    path('login/', UserApiView.as_view()),
    path('logout/', UserApiView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sparta/token/', TokenObtainPairView.as_view(), name='sparta_token'),
    path('api/authonly/', OnlyAuthenticatedUserView.as_view()),
]