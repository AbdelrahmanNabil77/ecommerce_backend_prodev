from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductReview

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'rating', 'title', 'created_at']
    can_delete = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'product_count']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Product Count'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'category', 'status', 'quantity', 'is_in_stock', 'created_by']
    list_filter = ['status', 'category', 'featured', 'created_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'average_rating_display']
    inlines = [ProductImageInline, ProductReviewInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'compare_price', 'cost_price', 'quantity', 'sku', 'barcode')
        }),
        ('Status & Display', {
            'fields': ('status', 'featured', 'images')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'average_rating_display')
        }),
    )
    
    def average_rating_display(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            avg = reviews.aggregate(avg=models.Avg('rating'))['avg']
            return f"{avg:.1f}/5.0 ({reviews.count()} reviews)"
        return "No reviews yet"
    average_rating_display.short_description = 'Average Rating'
    
    def is_in_stock(self, obj):
        return obj.quantity > 0
    is_in_stock.boolean = True
    is_in_stock.short_description = 'In Stock'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new product
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__email', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_reviews', 'reject_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} reviews rejected.")
    reject_reviews.short_description = "Reject selected reviews"
