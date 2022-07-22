from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    반환되는 토큰에 유저의 email과 username 정보를 담습니다.
    djangorestframework-sumplejwt 라이브러리의
    TokenObtainPairSerializer를 오버라이딩 합니다.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        return token
