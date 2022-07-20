from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    커스텀 유저모델을 위한 매니저 입니다.

    create_user : 유저를 생성해주는 메소드 입니다.
    create_superuser : 관리자 유저를 생성해주는 메소드 입니다.
    """

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have a email address.")
        if not username:
            raise ValueError("User must have username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField("이메일", max_length=320, unique=True)
    username = models.CharField("유저이름", max_length=200)
    password = models.CharField("비밀번호", max_length=100)
    date_joined = models.DateTimeField("가입날짜", auto_now_add=True)
    updated_at = models.DateTimeField("수정날짜", auto_now=True)
    is_admin = models.BooleanField("관리자여부", default=False)

    objects = UserManager()

    """로그인할 때, 이메일을 username 대신 받습니다."""
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """admin페이지에서 유저 객체를 이메일로 나타냅니다."""
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
