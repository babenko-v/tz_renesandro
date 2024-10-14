from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'username',  'password')
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False}
        }

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Пароли не совпадают."})
    #
    #     # Проверка уникальности email
    #     if User.objects.filter(email=attrs['email']).exists():
    #         raise serializers.ValidationError({"email": "Пользователь с таким email уже существует."})
    #
    #     # Проверка уникальности username
    #     if User.objects.filter(username=attrs['username']).exists():
    #         raise serializers.ValidationError({"username": "Пользователь с таким никнеймом уже существует."})
    #
    #     return attrs

    def create(self, validated_data):

        # Создаем пользователя
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            # programming_area=validated_data['programming_area']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']