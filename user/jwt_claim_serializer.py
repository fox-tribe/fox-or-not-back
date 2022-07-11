from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# TokenObtainPairSerializer를 상속하여 클레임 설정
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 생성된 토큰 가져오기
        token = super().get_token(user)

        # 사용자 지정 클레임 설정하기
        token['id'] = user.id

        # 로그인 하는 id
        token['username'] = user.username

        # 더 넣고 싶은 정보
        return token