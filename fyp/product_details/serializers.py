from rest_framework import serializers
from .models import *
from user_details.models import UserDetails

class AddProductSerializer(serializers.Serializer):
    p_image = serializers.ImageField()
    p_name = serializers.CharField(max_length=250)
    p_brand = serializers.CharField(max_length=250)
    p_status = serializers.IntegerField()
    p_des = serializers.CharField(max_length=5000)
    p_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    disc_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.IntegerField()
    category = serializers.CharField(max_length=250)
    # sub_category = serializers.CharField(max_length=250)
    user_data = serializers.CharField(max_length=250)
    if category == 'Phones':
            mobile_processor = serializers.CharField(max_length=500)
            mobile_battery = serializers.CharField(max_length=500)
            mobile_memory = serializers.CharField(max_length=500)
            mobile_display = serializers.CharField(max_length=500)
            mobile_camera = serializers.CharField(max_length=500)
    elif category == 'Laptops':
            laptop_processor = serializers.CharField(max_length=500)
            laptop_battery = serializers.CharField(max_length=500)
            laptop_memory = serializers.CharField(max_length=500)
            laptop_display = serializers.CharField(max_length=500)
            laptop_generation = serializers.IntegerField()
    elif category == 'AC':
            ac_capacity = serializers.CharField(max_length=500)
            ac_type = serializers.CharField(max_length=500)
            ac_inverter = serializers.BooleanField(default=True)
            ac_warranty = serializers.IntegerField()
            ac_energy_efficiency = serializers.IntegerField()
    elif category =='LCD':
            lcd_display = serializers.CharField(max_length=500)
            lcd_power_consumption = serializers.CharField(max_length=500)
            lcd_audio = serializers.CharField(max_length=500)
            lcd_chip = serializers.CharField(max_length=500)
    color = serializers.CharField(max_length=250)
    quantity = serializers.IntegerField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubCategory
#         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    # sub_category = SubCategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'

class MobileSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    # sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=MobilePhones
        exclude = ['product', 'category']

class LaptopSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    # sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=Laptops
        exclude = ['product', 'category']

class LCDSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    # sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=LCD
        exclude = ['product', 'category']

class ACSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    # sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=AC
        exclude = ['product', 'category']

class WishlistSerializer(serializers.Serializer):
    # product = ProductSerializer()
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        product_id = data.get("product_id", "")
        user_id = data.get("user_id", "")
        if not user_id or not product_id:
            raise serializers.ValidationError("Both User and Product ID's  are required")
        return data

class ShowWishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Wishlist
        fields = '__all__'

class AddCompareSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        product_id = data.get("product_id", "")
        user_id = data.get("user_id", "")
        if not user_id or not product_id:
            raise serializers.ValidationError("Both User and Product ID's  are required")
        return data

class ShowCompareSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CompareProducts
        fields = '__all__'

class VariationSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Variation
        fields = '__all__'

class FeedBackSerializer(serializers.Serializer):
     product = serializers.CharField()
     user = serializers.IntegerField()
     stars = serializers.DecimalField(max_digits=5, decimal_places=2)   
    
class DProductSerializer(serializers.Serializer):
     p_id = serializers.IntegerField()