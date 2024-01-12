# -*- coding: utf-8 -*-

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from .models import SmsVerifyCode, EmailVerifyCode

from wybj_drf.settings import REGEX_MOBILE, REGEX_EMAIL, TIME_ZONE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    短信序列化器
    """

    mobile = serializers.CharField(max_length=11)

    # 验证手机号码
    def validate_mobile(self, mobile):
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if SmsVerifyCode.objects.filter(
            add_time__gt=one_mintes_ago, mobile=mobile
        ).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class EmailSerializer(serializers.Serializer):
    """
    邮箱序列化器
    """

    email = serializers.EmailField()

    # 验证邮箱
    def validate_email(self, email):
        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱号码非法")

        return email


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    """
    短信注册
    """

    code = serializers.CharField(
        required=True,
        write_only=True,
        max_length=4,
        min_length=4,
        label="验证码",
        error_messages={
            "blank": "请输入验证码",
            "required": "请输入验证码",
            "max_length": "验证码格式错误",
            "min_length": "验证码格式错误",
        },
        help_text="验证码",
    )
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        help_text="密码",
        label="密码",
        write_only=True,
    )

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        verify_records = SmsVerifyCode.objects.filter(
            mobile=self.initial_data["username"]
        ).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class EmailUserRegSerializer(serializers.ModelSerializer):
    """
    邮箱注册
    """

    code = serializers.CharField(
        required=True,
        write_only=True,
        max_length=4,
        min_length=4,
        label="验证码",
        error_messages={
            "blank": "请输入验证码",
            "required": "请输入验证码",
            "max_length": "验证码格式错误",
            "min_length": "验证码格式错误",
        },
        help_text="验证码",
    )
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        help_text="密码",
        label="密码",
        write_only=True,
    )

    # 校验验证码
    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 取出最新的记录
        verify_records = EmailVerifyCode.objects.filter(
            # email=self.initial_data["username"]
            email=self.initial_data["email"]
        ).order_by("-add_time")

        if verify_records:
            last_record = verify_records[0]

            one_hour_ago = datetime.now() - timedelta(hours=1, minutes=0, seconds=0)
            if one_hour_ago > last_record.add_time.replace(tzinfo=None):
                raise serializers.ValidationError(f"验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        # attrs["email"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "email", "password")
