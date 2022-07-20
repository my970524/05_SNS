# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSignupSerializer


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 성공적으로 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": "회원가입에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
