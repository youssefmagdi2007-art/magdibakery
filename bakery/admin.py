from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem, User, Like, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'show_on_homepage', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['show_on_homepage']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'is_featured', 'is_bestseller', 'in_stock']
    list_filter = ['category', 'is_featured', 'is_bestseller']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_featured', 'is_bestseller']
    prepopulated_fields = {'slug': ('name',)}
    
    def in_stock(self, obj):
        return obj.stock > 0
    in_stock.boolean = True
    in_stock.short_description = 'In Stock'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'get_full_name', 'total', 'get_payment_method', 
                    'get_delivery_method', 'order_status', 'payment_status', 'placed_at']
    list_filter = ['payment_status', 'order_status', 'payment_method', 'delivery_method']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'address']
    readonly_fields = ['order_number', 'total', 'placed_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Customer'
    
    def get_payment_method(self, obj):
        return obj.get_payment_method_display()
    get_payment_method.short_description = 'Payment Method'
    
    def get_delivery_method(self, obj):
        return obj.get_delivery_method_display()
    get_delivery_method.short_description = 'Delivery Method'
    
    def items_summary(self, obj):
        return ", ".join([f"{item.product.name} x{item.quantity}" for item in obj.items.all()][:3])
    items_summary.short_description = 'Items (first 3)'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'get_item_count']
    readonly_fields = ['id']
    search_fields = ['user__username', 'id']

    def get_item_count(self, obj):
        return obj.items.count()
    get_item_count.short_description = 'Items'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_order_manager']
    list_filter = ['is_staff', 'is_order_manager']
    search_fields = ['username', 'email']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'created_at']
    list_filter = ['user', 'product']
    search_fields = ['user__username', 'product__name']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'area', 'phone']
    search_fields = ['user__username', 'city', 'area']