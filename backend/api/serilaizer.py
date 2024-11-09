from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models as api_models



class CategorySerializer(serializers.ModelSerializer):
    def get_post_count(self , category):
        return category.posts.count()
    class Meta:
        model = api_models.Category
        fields = "__all__"
        



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Comment
        fields = "__all__"
    
    def __init__(self , *args, **kwargs):
        super(CommentSerializer , self).__init__( *args, **kwargs)
        request = self.context.get('request')
        if request and request == 'POST':
            self.Meta.depth = 0
        else :
            self.Meta.depth = 1



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Post
        fields = "__all__"
    
    def __init__(self , *args, **kwargs):
        super(PostSerializer , self).__init__( *args, **kwargs)
        request = self.context.get('request')
        if request and request == 'POST':
            self.Meta.depth = 0
        else :
            self.Meta.depth = 1

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Bookmark
        fields = "__all__"
    
    def __init__(self , *args, **kwargs):
        super(BookmarkSerializer , self).__init__( *args, **kwargs)
        request = self.context.get('request')
        if request and request == 'POST':
            self.Meta.depth = 0
        else :
            self.Meta.depth = 1


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Notification
        fields = "__all__"
    
    def __init__(self , *args, **kwargs):
        super(NotificationSerializer , self).__init__( *args, **kwargs)
        request = self.context.get('request')
        if request and request == 'POST':
            self.Meta.depth = 0
        else :
            self.Meta.depth = 1


class AuthprSerializer(serializers.Serializer):
    views = serializers.IntegerField(default=0)
    posts = serializers.IntegerField(default=0)
    likes = serializers.IntegerField(default=0)
    bookmarks = serializers.IntegerField(default=0)