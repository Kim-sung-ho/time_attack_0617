import email
from ntpath import join
from unicodedata import name
from django.db import models
# 커스텀 유저 모델을 만들기 위해서 BaseUserManager와 AbstractBaseUser를 import
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
# custom user model 사용 시 UserManager 클래스와 create_user,
# create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    # auto_now_add=True로 최초 생성시 시간을 자동으로 입력해 준다.
    join_data = models.DateTimeField(auto_now_add=True)

    # is_active는 사용자가 이용할 수 있는지 여부를 표시하는 필드이다.
    is_active = models.BooleanField(default=True)
    # is_admin 은 관리자인지 여부를 표시하는 필드이다.
    is_admin = models.BooleanField(default=False)

    # 사용자가 로그인할 때 사용하는 id로 어떤 것을 사용 할 때에 지정을 해준 것.
    # 여기선 username 을 지정 했고, 다른 값으로도 사용 가능하다.
    USERNAME_FIELD = 'username'

    # 슈퍼계정을 생성 할 때, 입력해야 할 값들을 지정 할 수 있다.
    # 빈값을 입력하면 사용하지 않을 수 있지만 선언은 꼭 해야 된다.
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False

    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        return True
    # admin 권한 설정

    @property
    def is_staff(self):
        return self.is_admin


# User Profile model
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, verbose_name="사용자", on_delete=models.CASCADE)
    introduction = models.TextField("자기소개")
    birth = models.DateField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField("Hobby", verbose_name="취미")

    def __str__(self):
        return f'{self.user.username} 님의 프로필'

# Hobby model


class Hobby(models.Model):
    name = models.CharField("취미 이름", max_length=50)

    def __str__(self):
        return self.name
