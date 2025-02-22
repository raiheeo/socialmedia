from rest_framework import routers
from .views import *
from django.urls import path, include


router = routers.SimpleRouter()

router.register(r'post_like', PostLikeViewSet, basename='post_like_list')
router.register(r'comment_like', CommentLikeViewSet, basename='comment_like_list'),
router.register(r'saved', SavedViewSet, basename='saved_list'),
router.register(r'saved_item', SavedItemViewSet, basename='saved_item_list'),


urlpatterns = [
    path('', include(router.urls)),
    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('post_create/', PostCreateAPIView.as_view(), name='post_create'),

    path('users/', UserProfileListAPIView.as_view(), name='users_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),

    path('follows/', FollowListAPIView.as_view(), name='follow_list'),

    path('stories/', StoryListAPIView.as_view(), name='stories_list'),
    path('story/<int:pk>/', StoryDetailAPIView.as_view(), name='story_detail'),
    path('story_create/', StoryCreateAPIView.as_view(), name='story_create'),

    path('comment/', CommentListAPIView.as_view(), name='comment_list'),
    path('comment/<int:pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    path('comment_create/', CommentCreateAPIView.as_view(), name='comment_create'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]