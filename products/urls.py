# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/toggle-status/', views.ProductViewSet.as_view({'post': 'toggle_status'})),
    path('products/<int:pk>/add-picture/', views.ProductViewSet.as_view({'post': 'add_picture'})),
    path('comments/<int:pk>/like/', views.CommentViewSet.as_view({'post': 'like'})),
]