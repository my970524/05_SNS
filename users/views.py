from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSignupSerializer
from .token_serializers import MyTokenObtainPairSerializer


# url : POST /api/v1/users/signup
class UserSignupView(APIView):
    """
    회원가입 view 입니다.
    """

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 성공적으로 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": "회원가입에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)


# url : POST /api/v1/users/login
class UserLoginView(APIView):
    """
    로그인 view 입니다.
    입력한 정보가 유효하다면, access 토큰과 refresh 토큰을 반환합니다.
    """

    def post(self, request):
        user = authenticate(email=request.data.get("email"), password=request.data.get("password"))

        if user is None:
            return Response({"error": "존재하지 않는 계정이거나 비밀번호가 맞지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        token = MyTokenObtainPairSerializer.get_token(user)
        return Response(
            {
                "message": "로그인 되었습니다.",
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            },
            status=status.HTTP_200_OK,
        )
