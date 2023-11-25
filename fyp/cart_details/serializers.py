from rest_framework import serializers
from .models import Cart
from product_details.models import Product
from product_details.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Cart
        fields = ['cart_id', 'user_data', 'product', 'quantity','panel']

class CartUpdateSerializer(serializers.Serializer):
    user_data = serializers.IntegerField()
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    panel = serializers.IntegerField()

class AddtoCartSerializer(serializers.Serializer):
    user_data = serializers.IntegerField()
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    panel = serializers.IntegerField()

class DSerializer(serializers.Serializer):
    user_data = serializers.CharField()
    product = serializers.CharField()