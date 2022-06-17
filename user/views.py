from collections import UserList
import datetime
import email
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from .models import User, UserType, UserLog

# from user.models import UserLog


class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    # 사용자 정보 조회

    def get(self, request):
        return Response({"message": "get method"})

    # 회원가입
    def post(self, request):
        user_type = request.data.get('user_type', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        usertype = UserType.objects.get(user_type=user_type)
        User(user_type=usertype, email=email,
             password=make_password(password)).save()

        return Response({"message": "post method!!"})

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})

    # 회원 탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})


class UserAPIView(APIView):
    # 로그인
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        now = datetime.datetime.now()
        UserLog.objects.create(user=user, last_login_date=now.strftime(
            '%Y-%m-%d'))  # 유저로그생성
        return Response({"message": "login success!!"})
    # 로그아웃

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})
