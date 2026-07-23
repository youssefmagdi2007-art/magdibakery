from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from bakery.views import (
    CanCakeView, HomePageView, MiniTreatsView, SugarFreeView, FavoritesView,
    TortesView, OrientalSweetsView, CakesView, IceCreamTortesView,
    SaltySnacksView, SavoryShareableBoxesView
)
import os

# ----- Health check endpoint for Railway -----
def health_check(request):
    return JsonResponse({'status': 'ok'})

# ----- Logo and PDF views -----
def logo_view(request):
    logo_path = os.path.join(os.path.dirname(__file__), 'images', 'MagdisBakery-logo.png')
    with open(logo_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')

def pdf_view(request):
    pdf_path = os.path.join(os.path.dirname(__file__), 'PDFs', 'Customized-Cake.pdf')
    with open(pdf_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='application/pdf')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bakery.urls')),  # all bakery API endpoints
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('logo/', logo_view, name='logo'),
    path('Customized-Cake.pdf', pdf_view, name='customized_cake_pdf'),

    # ----- Health check for Railway -----
    path('health/', health_check, name='health_check'),

    # Frontend pages
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
     path('health/', health_check, name='health_check'),
    path('checkout/', TemplateView.as_view(template_name='checkout.html'), name='checkout'),
    path('signin/', TemplateView.as_view(template_name='signin.html'), name='signin'),
    path('register-step1/', TemplateView.as_view(template_name='register_step1.html'), name='register_step1'),
    path('register-step2/', TemplateView.as_view(template_name='register_step2.html'), name='register_step2'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)