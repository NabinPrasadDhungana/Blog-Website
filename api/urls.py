from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SessionLoginView#, UserAPIView,UserViewSet, CategoryViewSet, BlogViewSet, CommentViewSet, LikeViewSet, 
from .views import UserListCreateAPIView, UserDetailAPIView, CategoryListCreateAPIView, CategoryDetailAPIView, BlogListCreateAPIView, BlogDetailAPIView
from . import views

# router = DefaultRouter()
# router.register('users', UserViewSet, basename='user')
# router.register('categories', CategoryViewSet, basename='category')
# router.register('blogs', BlogViewSet, basename='blog')
# router.register('comments', CommentViewSet, basename='comment')
# router.register('likes', LikeViewSet, basename='likes')

urlpatterns = [
    path('login/', SessionLoginView.as_view(), name='api_login'),

    #users
    # path('user/create/', UserCreateAPIView.as_view(), name='create_user'),
    # path('users/', UserListAPIView.as_view(), name='list_users'),
    # path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='retrieve_user'),
    # path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    # path('user/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='delete_user'),
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    #category
    # path('category/create/', views.CategoryCreateAPIView.as_view(), name='create_category'),
    # path('categories/', views.CategoryListAPIView.as_view(), name='list_category'),
    # path('category/<slug:slug>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_delete_category'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('category/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    #blog
    # path('blogs/', views.BlogListCreateAPIView.as_view(), name='create_blog'),
    # path('blog/<int:pk>/', views.BlogUpdateRetrieveDestroyAPIView.as_view(), name='update_retrieve_delete_blog)'),
    path('blogs/', views.BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('blog/<int:pk>/', views.BlogDetailAPIView.as_view(), name='blog-detail'),

    #comment
    path('comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comment/<int:pk>', views.CommentDetailAPIView.as_view(), name='comment-detail'),

    #like
    path('likes/', views.LikeListCreateAPIView.as_view(), name='list_create_like'),
    
]

# urlpatterns += router.urls
