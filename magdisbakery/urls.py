from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from bakery.views import (
    CanCakeView, HomePageView, MiniTreatsView, SugarFreeView, FavoritesView,
    TortesView, OrientalSweetsView, CakesView, IceCreamTortesView,
    SaltySnacksView, SavoryShareableBoxesView,
    checkout_view, save_address_view, CartViewSet
)
import os

def health_check(request):
    return JsonResponse({'status': 'ok'})

def logo_view(request):
    logo_path = os.path.join(os.path.dirname(__file__), 'images', 'MagdisBakery-logo.png')
    with open(logo_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')

def pdf_view(request):
    pdf_path = os.path.join(os.path.dirname(__file__), 'pdfs', 'customizedCake.pdf')
    with open(pdf_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='application/pdf')

urlpatterns = [
    path('admin/', admin.site.urls),

    # ----- Manual cart add_item route (matches UUID with dashes) -----
    # This is checked FIRST, before the api/ include
    re_path(r'^api/carts/(?P<pk>[0-9a-f-]+)/add_item/$', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),

    path('api/', include('bakery.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('logo/', logo_view, name='logo'),
    path('health/', health_check, name='health_check'),
    path('Customized-Cake.pdf', pdf_view, name='customized_cake_pdf'),
    path('', HomePageView.as_view(), name='home'),
    path('mini-treats/', MiniTreatsView.as_view(), name='mini_treats'),
    path('sugar-free/', SugarFreeView.as_view(), name='sugar_free'),
    path('tortes/', TortesView.as_view(), name='tortes'),
    path('oriental-sweets/', OrientalSweetsView.as_view(), name='oriental_sweets'),
    path('cakes/', CakesView.as_view(), name='cakes'),
    path('can-cake/', CanCakeView.as_view(), name='can_cake'),
    path('ice-cream-tortes/', IceCreamTortesView.as_view(), name='ice_cream_tortes'),
    path('salty-snacks/', SaltySnacksView.as_view(), name='salty_snacks'),
    path('savory-shareable-boxes/', SavoryShareableBoxesView.as_view(), name='savory_shareable_boxes'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('category/<slug:slug>/', TemplateView.as_view(template_name='category_detail.html'), name='category'),
    path('product/<slug:slug>/', TemplateView.as_view(template_name='product_detail.html'), name='product_detail'),
    path('cart/', TemplateView.as_view(template_name='cart.html'), name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('signin/', TemplateView.as_view(template_name='signin.html'), name='signin'),
    path('register-step1/', TemplateView.as_view(template_name='register_step1.html'), name='register_step1'),
    path('register-step2/', TemplateView.as_view(template_name='register_step2.html'), name='register_step2'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)