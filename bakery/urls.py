from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import checkout_view, save_address_view, CartViewSet

# ---- Manual cart routes (all except add_item, which is handled in main urls) ----
cart_create = CartViewSet.as_view({'post': 'create'})
cart_retrieve = CartViewSet.as_view({'get': 'retrieve'})
cart_destroy = CartViewSet.as_view({'delete': 'destroy'})
cart_update_item = CartViewSet.as_view({'patch': 'update_item'})
cart_remove_item = CartViewSet.as_view({'delete': 'remove_item'})
cart_clear = CartViewSet.as_view({'delete': 'clear_cart'})

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')
router.register('orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('carts/', cart_create, name='cart-list'),
    path('carts/<uuid:pk>/', cart_retrieve, name='cart-detail'),
    path('carts/<uuid:pk>/', cart_destroy, name='cart-destroy'),
    path('carts/<uuid:pk>/items/<int:item_id>/', cart_update_item, name='cart-update-item'),
    path('carts/<uuid:pk>/items/<int:item_id>/', cart_remove_item, name='cart-remove-item'),
    path('carts/<uuid:pk>/clear/', cart_clear, name='cart-clear'),

    path('', include(router.urls)),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.test_json, name='test'),
    path('like/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/save-address/', save_address_view, name='save_address'),
]