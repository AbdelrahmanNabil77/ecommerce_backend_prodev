from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductReview

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ('created_at',)

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2,
                                            read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('slug', 'created_by', 'created_at', 'updated_at')