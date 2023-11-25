from django.db import models

# Create your models here.
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    panel = models.IntegerField(default=1)