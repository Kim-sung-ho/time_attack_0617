from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an username')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model


class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=50, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일 주소", max_length=100,
                              unique=True)  # unique=True 추가
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateField("가입일", auto_now_add=True)
    user_type = models.ForeignKey(
        "UserType", verbose_name="유저타입", on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # email

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username} / {self.email} / {self.fullname}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Hobby(models.Model):
    name = models.CharField("취미 이름", max_length=20)

    def __str__(self):
        return self.name

# user detail info table


class UserProfile(models.Model):
    # user = models.ForeignKey(User, verbose_name="유저", on_delete=models.CASCADE, unique=True)
    user = models.OneToOneField(
        User, verbose_name="유저", on_delete=models.CASCADE)
    introduction = models.TextField("자기소개", null=True, blank=True)
    birthday = models.DateField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField(Hobby, verbose_name="취미")

    def __str__(self):
        return f"{self.user.username} 님의 프로필입니다."


class UserType(models.Model):
    name = models.CharField("유저 타입 이름", max_length=20)

    def __str__(self):
        return self.name


class UserLog(models.Model):
    user = models.ForeignKey(User, verbose_name="유저", on_delete=models.CASCADE)
    login_date = models.DateTimeField("로그인 일짜", auto_now_add=True)
    apply_date = models.DateTimeField("지원날짜", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} 님의 로그인 내역입니다."
