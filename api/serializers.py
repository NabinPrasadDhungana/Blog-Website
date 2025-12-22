from rest_framework import serializers
from django.core.validators import RegexValidator
from accounts.models import User
from baseapp.models import Category, Blog, Comment, Like

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,  # Not required for updates
        style={'input_type': 'password', 'placeholder': 'Password'},
        validators=[RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*-])[A-Za-z\d!@#$%^&*-]{8,32}$',
                message='The password must be 8-32 characters, include at least one lowercase, one uppercase, one digit, and one special character. (Allowed special characters: !@#$%%^&*-).'
        )]
    )
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'avatar', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
    
    def update(self, instance, validated_data):
        # Handle password separately if provided
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug']

class BlogSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    author = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
            queryset=Category.objects.all(),
            slug_field='name'
        )
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'description', 'image', 'author', 'category', 'created_at', 'updated_at', 'likes_count', 'is_liked']

    def get_author(self, obj) -> dict:
        if not obj.author:
            return None
        
        return {
            "username": obj.author.username,
            "name": obj.author.name,
            "avatar": obj.author.avatar.url if obj.author.avatar else None
        } 
    
    def get_likes_count(self, obj) -> int:
        return obj.likes.count()

    def get_is_liked(self, obj) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'message', 'created_at', 'updated_at']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ['id','blog', 'user', 'created_at']
        