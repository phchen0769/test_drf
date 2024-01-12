from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from wybj_drf.settings import DEFAULT_FROM_EMAIL

from .serializers import (
    SmsSerializer,
    EmailSerializer,
    EmailUserRegSerializer,
    UserDetailSerializer,
)
from wybj_drf.settings import APIKEY
from utils.yunpian import YunPian
from .models import SmsVerifyCode, EmailVerifyCode

# 导入权限
from rest_framework.decorators import action
from rest_framework_roles.granting import is_self

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            # 重载ModelBackend模块的 authenticate方法，增加了mobile和email登录方式。
            user = User.objects.get(
                Q(username=username) | Q(mobile=username) | Q(email=username)
            )
            # user = UserModel._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """

    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        # 生成验证码
        code = get_random_string(length=6, allowed_chars="1234567890")

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response(
                {"mobile": sms_status["msg"]}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            code_record = SmsVerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)


class EmailCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """

    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            # 生成验证码
            code = get_random_string(length=4, allowed_chars="1234567890")

            # 创建或更新验证码实例
            EmailVerifyCode.objects.update_or_create(
                email=email, defaults={"code": code, "add_time": timezone.now()}
            )

            # 发送邮件
            send_mail(
                "Your Email Verification Code",
                f"Your verification code is {code}.",
                f"{DEFAULT_FROM_EMAIL}",
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "Verification code sent successfully!"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(
    CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    用户
    """

    serializer_class = EmailUserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (
        JWTAuthentication,
        authentication.SessionAuthentication,
    )

    # get方法的序列化器
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return EmailUserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        # 取出json数据初始化到serializer中
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 调用serializer保存方法
        user = self.perform_create(serializer)

        # 向前端返回refresh token、access token 以及serializer中的对象
        refresh = RefreshToken.for_user(user)
        re_dict = serializer.data
        re_dict["refresh"] = str(refresh)
        re_dict["access"] = str(refresh.access_token)
        # re_dict["username"] = user.username if user.name else user.username
        re_dict["username"] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    # 保存serializer到数据库中
    def perform_create(self, serializer):
        return serializer.save()
