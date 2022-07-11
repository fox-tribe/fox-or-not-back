from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.jwt_claim_serializer import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import (
    User as UserModel,
)
from user.serializers import (
    UserSerializer,
)

class UserView(APIView):
    # permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)

    # 회원가입
    def post(self, request):
        password = request.data.pop("password")
        password2 = request.data.pop("password2")

        if password == password2:
            user = UserModel(**request.data)
            user.set_password(password)
            user.save()
            return Response({"message": "회원가입 완료!!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "비밀번호가 일치하지 않습니다."})

    def put(self, request):
        return Response({'message': 'put method!!'})


    def delete(self, request):
        return Response({'message': 'delete method!!'})



class UserApiView(APIView):
    # permission_classes = [permissions.AllowAny]
    
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user)
            return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)

    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!!"}, status=status.HTTP_200_OK)


# jwt 토큰
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# 인가된 사용자만 접근할 수 있는 View 생성
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})
