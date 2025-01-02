from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Product, Comment, Tag
from .serializers import ProductSerializer, CommentSerializer, TagSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def add_picture(self, request, pk=None):
        product = self.get_object()
        if product.pictures.count() >= 5:
            return Response({"error": "Maximum pictures reached"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        product = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Product.status.field.choices):
            product.status = new_status
            product.save()
            return Response({'status': new_status})
        return Response({'error': 'Invalid status'}, status=400)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        
        like, created = Like.objects.get_or_create(user=user, comment=comment)
        if not created:
            like.delete()
            return Response({"status": "unliked"})
        return Response({"status": "liked"})

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]