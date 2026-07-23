from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string
import json
import logging

from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem, Like, Profile
)
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, 
    CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer,
    OrderSerializer, CreateOrderSerializer
)

logger = logging.getLogger(__name__)
User = get_user_model()

# ============================================================
# TEST ENDPOINT
# ============================================================
def test_json(request):
    return JsonResponse({'message': 'JSON is working!'})

# ============================================================
# FRONTEND VIEWS (category pages)
# ============================================================

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_categories'] = Category.objects.filter(show_on_homepage=True, is_active=True)
        bestseller_products = Product.objects.filter(is_bestseller=True)
        if not bestseller_products.exists():
            bestseller_products = Product.objects.filter(is_featured=True)
            if not bestseller_products.exists():
                bestseller_products = Product.objects.all().order_by('?')[:8]
        context['bestseller_products'] = bestseller_products[:8]
        context['categories'] = Category.objects.filter(is_active=True)
        default_category = Category.objects.filter(slug='cakes').first()
        if default_category:
            carousel_products = Product.objects.filter(category=default_category)
        else:
            carousel_products = Product.objects.all().order_by('?')
        context['carousel_products'] = carousel_products
        return context

class MiniTreatsView(TemplateView):
    template_name = 'mini-treats.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='mini-treats')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class SugarFreeView(TemplateView):
    template_name = 'sugar-free.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='sugar-free')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class TortesView(TemplateView):
    template_name = 'tortes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='tortes')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class OrientalSweetsView(TemplateView):
    template_name = 'oriental-sweets.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='oriental-sweets-boxes')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class CakesView(TemplateView):
    template_name = 'cakes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='cakes')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class CanCakeView(TemplateView):
    template_name = 'can-cake.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='can-cake')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class IceCreamTortesView(TemplateView):
    template_name = 'ice_cream_tortes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='ice-cream-tortes')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class SaltySnacksView(TemplateView):
    template_name = 'salty_snacks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='salty-snacks')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class SavoryShareableBoxesView(TemplateView):
    template_name = 'savory_shareable_boxes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Category.objects.get(slug='savory-shareable-boxes')
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class FavoritesView(TemplateView):
    template_name = 'favorites.html'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_likes = Like.objects.filter(user=self.request.user)
        liked_product_ids = user_likes.values_list('product_id', flat=True)
        context['products'] = Product.objects.filter(id__in=liked_product_ids)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

# ============================================================
# AUTHENTICATION VIEWS (with CSRF exemption)
# ============================================================

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')
            
            if not email or not password:
                return JsonResponse({'success': False, 'error': 'Email and password required'}, status=400)

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({
                        'success': True,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                        }
                    })
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid email or password'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid email or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method in ('POST', 'GET'):
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

# ============================================================
# API VIEWS (likes, categories, products, carts, orders)
# ============================================================

class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        like, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            like.delete()
            total_likes = Like.objects.filter(user=request.user).count()
            return Response({
                'liked': False,
                'message': 'Unliked',
                'total_likes': total_likes
            }, status=status.HTTP_200_OK)
        else:
            total_likes = Like.objects.filter(user=request.user).count()
            return Response({
                'liked': True,
                'message': 'Liked',
                'total_likes': total_likes
            }, status=status.HTTP_201_CREATED)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category__slug', 'is_featured', 'is_bestseller']
    search_fields = ['name', 'description']
    permission_classes = [AllowAny]

class CartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        cart = Cart.objects.create()
        return Response({'id': cart.id}, status=status.HTTP_201_CREATED)
    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, id=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    def destroy(self, request, pk=None):
        cart = get_object_or_404(Cart, id=pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = get_object_or_404(Cart, id=pk)
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=['patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, pk=None, item_id=None):
        cart = get_object_or_404(Cart, id=pk)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data)
    @action(detail=True, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        cart = get_object_or_404(Cart, id=pk)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data)
    @action(detail=True, methods=['delete'], url_path='clear')
    def clear_cart(self, request, pk=None):
        cart = get_object_or_404(Cart, id=pk)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(f"Order validation error: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_id = serializer.validated_data.get('cart_id')
        if not cart_id:
            return Response({'error': 'Cart ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = get_object_or_404(Cart, id=cart_id)
        
        with transaction.atomic():
            order_number = f"MB-{random.randint(10000, 99999)}-{''.join(random.choices(string.digits, k=4))}"
            order = Order.objects.create(
                cart=cart,
                order_number=order_number,
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                email=serializer.validated_data.get('email', ''),
                phone=serializer.validated_data.get('phone', ''),
                address=serializer.validated_data.get('address', ''),
                city=serializer.validated_data.get('city', ''),
                notes=serializer.validated_data.get('notes', ''),
                total=cart.get_total(),
                is_guest=serializer.validated_data.get('is_guest', True),
                payment_status='P',
                payment_method=serializer.validated_data.get('payment_method', 'card'),
                delivery_method=serializer.validated_data.get('delivery_method', 'home'),
            )
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
            
            # Create order items and collect for email
            order_items = []
            for cart_item in cart.items.all():
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                order_items.append(order_item)
                # Reduce stock
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()
            
            cart.items.all().delete()
            
            # ====== SEND CONFIRMATION EMAILS ======
            try:
                self._send_order_confirmation_emails(order, order_items, request)
            except Exception as e:
                logger.error(f"Error sending order emails: {str(e)}")
                # Continue even if email fails
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, order_number=pk)
        if not request.user.is_authenticated or (order.user and order.user != request.user):
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def _send_order_confirmation_emails(self, order, order_items, request):
        """Send emails to customer and order managers."""
        # Build order items list for email
        items_list = []
        for item in order_items:
            items_list.append({
                'name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.price),
                'total': str(item.quantity * item.price),
            })
        
        # Build delivery info
        if order.delivery_method == 'home':
            delivery_info = f"Home Delivery to: {order.address}, {order.city}"
        else:
            # For pickup, address holds the store name
            delivery_info = f"Store Pickup at: {order.address}"
        
        # ====== 1. Email to Customer ======
        customer_subject = f"Your Order #{order.order_number} has been Confirmed!"
        customer_context = {
            'order': order,
            'items': items_list,
            'delivery_info': delivery_info,
            'customer_name': f"{order.first_name} {order.last_name}",
            'delivery_days': '3-5 business days' if order.delivery_method == 'home' else 'ready for pickup in 3-5 business days',
        }
        customer_html = render_to_string('email/customer_order_confirmation.html', customer_context)
        customer_plain = strip_tags(customer_html)
        
        send_mail(
            subject=customer_subject,
            message=customer_plain,
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[order.email],
            html_message=customer_html,
            fail_silently=False,
        )
        
        # ====== 2. Email to Order Managers ======
        managers = User.objects.filter(is_order_manager=True, is_active=True)
        if managers.exists():
            manager_subject = f"New Order #{order.order_number} has been placed"
            manager_context = {
                'order': order,
                'items': items_list,
                'delivery_info': delivery_info,
                'customer_name': f"{order.first_name} {order.last_name}",
                'customer_email': order.email,
                'customer_phone': order.phone,
            }
            manager_html = render_to_string('email/manager_order_notification.html', manager_context)
            manager_plain = strip_tags(manager_html)
            
            recipient_list = [manager.email for manager in managers]
            send_mail(
                subject=manager_subject,
                message=manager_plain,
                from_email=None,
                recipient_list=recipient_list,
                html_message=manager_html,
                fail_silently=False,
            )

# ============================================================
# CHECKOUT VIEWS (protected)
# ============================================================

@login_required(login_url='/signin/')
def checkout_view(request):
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None
    initial_data = {}
    if profile:
        initial_data = {
            'address_line1': profile.address_line1,
            'address_line2': profile.address_line2,
            'compound': profile.compound,
            'building_number': profile.building_number,
            'city': profile.city,
            'area': profile.area,
            'postal_code': profile.postal_code,
            'phone': profile.phone,
        }
    return render(request, 'checkout.html', {
        'user': user,
        'profile': profile,
        'initial_data': initial_data,
    })

@csrf_exempt
@login_required(login_url='/signin/')
def save_address_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        logger.info(f"Received address data: {data}")

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.address_line1 = data.get('address_line1', '').strip()
        profile.address_line2 = data.get('address_line2', '').strip()
        profile.compound = data.get('compound', '').strip()
        profile.building_number = data.get('building_number', '').strip()
        profile.city = data.get('city', '').strip()
        profile.area = data.get('area', '').strip()
        profile.postal_code = data.get('postal_code', '').strip()
        profile.country = data.get('country', 'Egypt').strip()
        profile.phone = data.get('phone', '').strip()
        profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Address saved successfully!',
            'profile': {
                'address_line1': profile.address_line1,
                'address_line2': profile.address_line2,
                'compound': profile.compound,
                'building_number': profile.building_number,
                'city': profile.city,
                'area': profile.area,
                'postal_code': profile.postal_code,
                'country': profile.country,
                'phone': profile.phone,
            }
        })
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Error saving address: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)