from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

# -------------------------------
# REGISTER / SIGNUP SERIALIZER
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    # Ensure email is unique and required for the crypto dashboard
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # We still include username because Django's default User model requires it,
        # but your frontend can just auto-generate it or use the email prefix.
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# -------------------------------
# LOGIN SERIALIZER (Email Only)
# -------------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # 1. Lookup the user by email to get the username for authenticate()
            try:
                # Use iexact to avoid case-sensitivity issues during login
                user_obj = User.objects.get(email__iexact=email)
                username = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")

            # 2. Authenticate using the retrieved username and provided password
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        # 3. Pass the user object back so the view can generate JWT tokens
        attrs['user'] = user
        return attrs