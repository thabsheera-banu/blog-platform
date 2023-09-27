from rest_framework import serializers
from . models import BlogPost,UserProfile

class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'