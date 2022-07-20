from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSignupSerializer
from .token_serializers import MyTokenObtainPairSerializer


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 성공적으로 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": "회원가입에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
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
