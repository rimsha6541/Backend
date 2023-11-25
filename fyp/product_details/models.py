from django.db import models

# Create your models here.
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=250)
    cat_image = models.ImageField (upload_to='cat_images')

# class SubCategory(models.Model):
#     sub_id = models.AutoField(primary_key=True)
#     sub_name = models.CharField(max_length=250)
#     cat_id = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)

class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=250)
    p_image = models.ImageField(upload_to='product_images')
    p_brand = models.CharField(max_length=250)
    p_status = models.SmallIntegerField()
    p_des = models.TextField(max_length=5000)
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField()
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    # sub_category = models.CharField(max_length=250, default='No Category')
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    p_status = models.SmallIntegerField(default=1)
    rating = models.DecimalField(max_digits=5, decimal_places=2)

class Variation(models.Model):
    v_id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=250)
    quantity = models.IntegerField()
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)

class Wishlist(models.Model):
    w_id = models.AutoField(primary_key=True)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)

class CompareProducts(models.Model):
    c_id = models.AutoField(primary_key=True)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)

class MobilePhones(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    # sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    mobile_processor = models.CharField(max_length=500)
    mobile_battery = models.CharField(max_length=500)
    mobile_memory = models.CharField(max_length=500)
    mobile_display = models.CharField(max_length=500)
    mobile_camera = models.CharField(max_length=500)

class Laptops(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    # sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    laptop_processor = models.CharField(max_length=500)
    laptop_battery = models.CharField(max_length=500)
    laptop_memory = models.CharField(max_length=500)
    laptop_display = models.CharField(max_length=500)
    laptop_generation = models.IntegerField()

class LCD(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    # sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    lcd_display = models.CharField(max_length=500)
    lcd_power_consumption = models.CharField(max_length=500)
    lcd_audio = models.CharField(max_length=500)
    lcd_chip = models.CharField(max_length=500)

class AC(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    # sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    ac_capacity = models.CharField(max_length=500)
    ac_type = models.CharField(max_length=500)
    ac_inverter = models.BooleanField(default=True)
    ac_warranty = models.IntegerField()
    ac_energy_efficiency = models.IntegerField()

class Feedback(models.Model):
     stars = models.DecimalField(max_digits=5, decimal_places=2)
     user = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)
     product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)


