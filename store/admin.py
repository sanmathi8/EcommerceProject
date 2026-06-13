from django.contrib import admin
from .models import Category, Product, Profile, Cart, CartItem, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'zip_code')
    search_fields = ('user__username', 'user__email', 'phone', 'city')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_total_price',)

    def get_total_price(self, instance):
        return instance.get_total_price()
    get_total_price.short_description = 'Total Price'

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'items_count', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_id')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price', 'get_total_price')

    def get_total_price(self, instance):
        return instance.get_total_price()
    get_total_price.short_description = 'Total Price'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'email', 'total', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('customer', 'email', 'address', 'city')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('created',)

# Register models in admin panel
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)

# Customize Admin Site Titles
admin.site.site_header = "LuxCart Administration"
admin.site.site_title = "LuxCart Admin Portal"
admin.site.index_title = "Welcome to LuxCart Management Dashboard"