from rest_framework import serializers
from .models import Tag, Product, Picture, Comment, Like

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'picture', 'created_at', 'replies', 'like_count', 'user_has_liked']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True).data

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class ProductSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'location', 'label', 
            'tags', 'pictures', 'comments', 'created_at', 
            'updated_at', 'creator', 'status', 'views_count'
        ]