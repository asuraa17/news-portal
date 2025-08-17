from django.contrib.auth.models import Group, User
from rest_framework import serializers

from newspaper.models import Advertisement, Post, Tag, Category, Newsletter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'first_name', 'last_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'description']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'featured_image',
            'status',
            'category', 
            'tag',
            # read only
            'author',
            'views_count',
            'published_at',
            ]
        extra_kwargs = {
            'author': {"read_only": True},
            'views_count': {"read_only": True},
            'published_at': {"read_only": True},
        }

    def validate(self, data):
            data["author"] = self.context["request"].user
            return data


class PostPublishSerializer(serializers.Serializer):
    id = serializers.IntegerField()

        
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'image']

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = "__all__"
