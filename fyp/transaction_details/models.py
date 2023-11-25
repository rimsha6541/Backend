from django.db import models

# Create your models here.
class Transaction(models.Model):
    t_id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=200)
    order = models.ForeignKey("order_details.Order", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)
