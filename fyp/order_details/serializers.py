from rest_framework import serializers
from .models import *
from product_details.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderDetails
        fields = "__all__"



class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = "__all__"

class AddOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    payment_type = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip = serializers.CharField()
    address = serializers.CharField()
    p_address = serializers.CharField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    o_panel = serializers.IntegerField()
    if payment_type == 'Stripe':
        card_number = serializers.IntegerField()
        exp_month = serializers.IntegerField()
        exp_year = serializers.IntegerField()
        cvc = serializers.IntegerField()

class ViewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_type', 'total_bill', 'bill_payed', 'discount', 'o_panel']

class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['o_id', 'o_status']

class DorderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()