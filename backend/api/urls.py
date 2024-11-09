from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
    path('post/category/list/',api_views.CategoryListApiView.as_view()),
    path('post/category/posts/<category_slug>',api_views.PostCategoryListAPIView.as_view()),
    
    path('post/lists/',api_views.PostListAPIView.as_view()),
    path('post/details/<slug:slug>/',api_views.PostDetailsListAPIView.as_view()),
    
    path('post/like-post/',api_views.LikePostView.as_view()),
    
    
]
