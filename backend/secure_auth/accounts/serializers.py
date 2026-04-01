from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    username=serializers.CharField(
        required=True,
    )
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password=serializers.CharField(
        required=True,
        read_only=True,
        validators=[validate_password]
    )
    password2=serializers.CharField(
        required=True,
        write_only=True,
    )
    class Meta:
        model=User
        fields=['username','password','password2','email']
        def validate(self,attrs):
            if attrs['password'] != attrs['passwrod2']:
                raise serializers.ValidationError({"password":"Password fields didn't match."})
            return attrs
        def create(self,validated_data):
            validated_data.pop('password2')
            user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(
        required=True,
    )
    password=serializers.CharField(
        required=True,
        write_only=True,
    )
    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        if email and password:
            try:
                user=User.objects.get(email_iexact=email)
                username=user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError({"email":"User with this email does not exist."})
            user=authenticate(username=username,password=password)
            if not user:
                raise serializers.ValidationError({"password":"Incorrect password."})
            else:
                raise serializers.ValidationError({"non_field_errors":"Unable to log in with provided credentials."})
        attrs['user']=user
        return attrs 