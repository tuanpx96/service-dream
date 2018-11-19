from rest_framework import serializers
from django.conf import settings
from dream_users import models as user_models


class LoginEmailValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)


class LoginFacebookValidator(serializers.Serializer):
    fb_access_token = serializers.CharField(required=True, allow_blank=False)


class LoginLineValidator(serializers.Serializer):
    line_access_token = serializers.CharField(required=True, allow_blank=False)


class RegisterEmailValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            'id', 'username', 'email', 'user_type', 'status',
            'facebook_id', 'line_id', 'created_at', 'updated_at'
        )


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expired_time = serializers.DateTimeField()
    user = UserSerializer(read_only=True)


class ResetPasswordValidator(serializers.Serializer):
    reset_token = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=16, )
    confirm_password = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Confirm password must equal password.")
        if not any(char.isalpha() for char in data['password']):
            raise serializers.ValidationError("Password must contain at least 1 letter.")
        return data


class UserUpdateValidator(serializers.Serializer):
    username = serializers.CharField(required=False)


class UserUpdatePasswordValidator(serializers.Serializer):
    old_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False)


class RatingValidator(serializers.Serializer):
    num_stars = serializers.IntegerField(required=True, min_value=1, max_value=5)
    comment = serializers.CharField(required=True, allow_blank=True)


class RetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Rating
        fields = ('id', 'user_id', 'num_stars', 'comment')


class ForgotPasswordValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
