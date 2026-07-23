from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import checkout_view, save_address_view

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')
router.register('carts', views.CartViewSet, basename='cart')
router.register('orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.test_json, name='test'),
    path('like/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/save-address/', save_address_view, name='save_address'),
]