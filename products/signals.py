from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import ProductReview, Product

@receiver([post_save, post_delete], sender=ProductReview)
def update_product_rating(sender, instance, **kwargs):
    """Update product rating cache when reviews change"""
    product = instance.product
    approved_reviews = product.reviews.filter(is_approved=True)
    
    if approved_reviews.exists():
        avg_rating = approved_reviews.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        product.average_rating = round(avg_rating, 2)
        product.review_count = approved_reviews.count()
    else:
        product.average_rating = None
        product.review_count = 0
    
    # Save only rating fields to avoid recursion
    Product.objects.filter(id=product.id).update(
        average_rating=product.average_rating,
        review_count=product.review_count
    )