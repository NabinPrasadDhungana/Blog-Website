from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, SAFE_METHODS
from accounts.models import User
from baseapp.models import Category, Blog, Comment, Like
from .serializers import UserSerializer, CategorySerializer, BlogSerializer, CommentSerializer, LikeSerializer
from .filters import BlogFilter
from .permissions import IsSelf, IsSelfOrAdmin, IsOwnerOrAdmin
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_permissions(self):
#         if self.request.method in ['GET', 'PUT', 'PATCH']:
#             return [IsAuthenticated()]
#         if self.request.method == 'POST':
#             return [AllowAny()]
#         elif self.request.method == 'DELETE':
#             return [IsAdminUser()]
#         else:
#             return [AllowAny()]
        
# class UserCreateAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

class UserListCreateAPIView(APIView):
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     elif self.request.method in ['PUT', 'PATCH']:
    #         return [IsSelfOrAdmin()]
    #     elif self.request.method == 'DELETE':
    #         return [IsAdminUser()]
    #     else:
    #         return [AllowAny()]
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'GET':
            self.permission_classes == [IsAdminUser]
        return super().get_permissions()
            
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes == [AllowAny]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsSelfOrAdmin]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class UserListAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]

# class UserRetrieveAPIView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

# class UserUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsSelfOrAdmin]

# class UserDeleteAPIView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsSelfOrAdmin]
    
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         else:
#             return [IsAdminUser()]
        
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
        
# class BlogViewSet(viewsets.ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     filterset_class = BlogFilter
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at', 'updated_at']
#     ordering = ['created_at']

#     def get_permissions(self):
#         if self.request.method in ['POST', 'PATCH', 'DELETE', 'PUT']:
#             return [IsAuthenticated()]
#         else:
#             return [AllowAny()]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

class BlogListCreateAPIView(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filterset_class = BlogFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogUpdateRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsOwnerOrAdmin()]
        

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     filterset_fields = ['blog']

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [IsAuthenticated()]
#         return [AllowAny()]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = ['blog']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

# class LikeViewSet(viewsets.ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         blog_id = request.data.get('blog')
#         if blog_id:
#             existing_like = Like.objects.filter(user=request.user, blog=blog_id).first()
#             if existing_like:
#                 existing_like.delete()
#                 return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
#         return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeListCreateAPIView(ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filterset_fields = ['blog']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        blog_id = request.data.get('blog')
        if blog_id:
            existing_like = Like.objects.filter(user=request.user, blog=blog_id).first()
            if existing_like:
                existing_like.delete()
                return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

class SessionLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    