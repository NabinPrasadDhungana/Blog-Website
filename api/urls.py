from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, BlogViewSet, CommentViewSet, LikeViewSet, SessionLoginView
from .views import UserCreateAPIView, UserListAPIView, UserUpdateAPIView, UserDeleteAPIView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')
router.register('blogs', BlogViewSet, basename='blog')
router.register('comments', CommentViewSet, basename='comment')
router.register('likes', LikeViewSet, basename='likes')

urlpatterns = [
    path('login/', SessionLoginView.as_view(), name='api_login'),

    path('user/create/', UserCreateAPIView.as_view(), name='create_user'),
    path('users/', UserListAPIView.as_view(), name='list_users'),
    path('user/<int:pk>', UserUpdateAPIView.as_view(), name='retrieve_user'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('user/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='delete_user'),
]

urlpatterns += router.urls
