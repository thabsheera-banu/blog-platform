from rest_framework import serializers
# from .models import BlogPost,UserProfile,Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Register
class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('username taken')
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()  
        return validated_data

    
# Login

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('This Account is not Exisist')
        return data
    def get_jwt_token(self , data):
        user = authenticate(username = data['username'],
                            password = data['password'])
        print(f"User object: {user}")
        print(user)
        if not user:
            return {
                'message ' : 'invalid credential',
                'data' : {}
            }
        refresh = RefreshToken.for_user(user)
        return {'message' : 'login success' ,
                 'data' : {'token':{'refresh': str(refresh),
                                   'access': str(refresh.access_token)}}}
    
    
        
    
