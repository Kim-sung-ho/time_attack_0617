import numbers
from urllib import response
from django.shortcuts import render
# DRF 퍼미션 클래스 를 사용하기 위해  APIView를 임포트해서 상속받아야한다.
from rest_framework.views import APIView
from rest_framework import permissions  # 권한 설정 해주는 permissions 클래스
from rest_framework.response import Response  # Response를 임포트해서 사용할 것이다.
# 로그인 및 로그아웃에 사용
from django.contrib.auth import login, authenticate, logout

# FBV
# def user(request):
#     if request.method == 'GET':
#         #조회
#         pass
#     if request.method == 'POST':
#         #생성
#         pass


# def sum_numbers(a, b):
#     return a + b
def sum_numbers(*args):
    return sum(args)

# CBV


class UserView(APIView):
    ###### 권한 설정 해주는 permissions 클래스#######
    permission_classes = [permissions.AllowAny]  # 모두 사용가능
    # parmission_classes = [permissions.IsAuthenticated] #로그인 된 사용자만
    # parmission_classes = [permissions.IsAdminUser] # 어드민 유저만

    def get(self, request):
        # 사용자 정보 조회

        # request.data
        '''
        {
            'a' : 5,
            'b' : 10
        }
        '''
        # result = sum_numbers(**request.data)
        # == 제이슨 형식은 키 벨류 값을 가지고 있다.
        # Python의 tuple을 JSON으로 변환하면 JSON object가 되며,
        # 이를 다시 Python으로 재변환하면 tuple이 된다.
        '''
        result = sum_numbers(a = 5 , b = 5)
        '''
        # print(request.data)
        # print(sum_numbers(**request.data))
        # * 를 써보려면 리스트형식으로 벨류값을 받아와야 된다.
        numbers = request.data.get("a", [])
        result = sum_numbers(*numbers)
        return Response({'message': f'post method is {result}'})

    # 로그인
    def post(self, request):

        return Response({'message': '로그인 성공!!'})

    def put(self, request):
        # 회원 정보 수정
        return Response({'message': 'put method'})

    def delete(self, request):
        # 회원탈퇴
        return Response({'message': 'delete method'})


class UserAPIView(APIView):
    ###### 권한 설정 해주는 permissions 클래스#######
    permission_classes = [permissions.AllowAny]  # 모두 사용가능

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        # 변수 user에는 인증에 성공하면 user가 담기고, 인증 실패하면 None이 담긴다.
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({'message': '아이디 또는 비밀번호가 올바르지 않습니다.'})
        login(request, user)
        return Response({'message': '로그인 성공!!'})
