from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Changed to allow blank
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                             null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
    

class Product(models.Model):
    PRODUCT_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Changed to allow blank
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                       null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2,
                                    null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                null=True, related_name='products')
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, 
                            default='draft')
    featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  null=True, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['price']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})
    
    @property
    def is_in_stock(self):
        return self.quantity > 0
    
    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return round(((self.compare_price - self.price) / self.compare_price) * 100, 1)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                              related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_default', 'created_at']

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                              related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']
        indexes = [
            models.Index(fields=['product', 'is_approved']),
            models.Index(fields=['rating']),
        ]



