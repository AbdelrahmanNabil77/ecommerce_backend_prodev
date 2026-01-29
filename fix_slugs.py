# fix_slugs.py
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product

def fix_category_slugs():
    categories = Category.objects.filter(slug='')
    for category in categories:
        if not category.slug:
            slug = slugify(category.name)
            original_slug = slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(id=category.id).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            category.slug = slug
            category.save()
            print(f"Fixed slug for category: {category.name} -> {category.slug}")

def fix_product_slugs():
    products = Product.objects.filter(slug='')
    for product in products:
        if not product.slug:
            slug = slugify(product.name)
            original_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            product.slug = slug
            product.save()
            print(f"Fixed slug for product: {product.name} -> {product.slug}")

if __name__ == '__main__':
    print("Fixing category slugs...")
    fix_category_slugs()
    print("\nFixing product slugs...")
    fix_product_slugs()
    print("\nDone!")