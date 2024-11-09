from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

# Others
import json
import random

# Custom Imports
from api import serilaizer as api_serializer
from api import models as api_models


class CategoryListApiView(generics.ListAPIView):
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Category.objects.all()


class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category = self.kwargs['category_slug']
        category = api_models.Category.objects.get(slug=category)
        return api_models.Post.objects.filter(category=category, status='Published')


class PostListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Post.objects.filter(status='Published')


class PostDetailsListAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
  
    def get_object(self):
        
        slug = self.kwargs['slug']
        post = api_models.Post.objects.get(slug=slug, status='Published')
        post.view += 1
        post.save()
        return post

class LikePostView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='post id'),
            }
        )
    )
    def post(self , request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        
        user = api_models.User.objects.get(id=user_id)
        post = api_models.Post.objects.get(id=post_id)
        
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message' : 'post Dislike'} ,status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            
            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type='like'
            )
            
            return Response({'message':'Post Liked'} , status=status.HTTP_201_CREATED)
        
        
class PostCommentAPIView(APIView):
    def post_id(self , request):
        post_id = request.data['post_id']
        