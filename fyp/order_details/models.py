from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=200)
    total_bill = models.CharField(max_length=200)
    bill_payed = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)
    user_id = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    o_status = models.CharField(default='In Process', max_length=200)
    o_panel = models.IntegerField(default=1)

class OrderDetails(models.Model):
    od_id = models.AutoField(primary_key=True)
    actual_price = models.CharField(max_length=200)
    sale_price = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)
    order = models.ForeignKey("order_details.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    variation = models.ForeignKey("product_details.Variation", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)


class ShipmentDetails(models.Model):
    s_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=1000)
    p_address = models.CharField(max_length=1000, default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    user_id = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, default='')
    # last_name = models.CharField(max_length=50, default='')
    order = models.ForeignKey("order_details.Order", on_delete=models.CASCADE)
