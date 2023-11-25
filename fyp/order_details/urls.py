from django.urls import path
from .views import *

urlpatterns = [
    path('show_shipment/<id>', ShowShipmentView.as_view(), name="view_shipment"),
    path('order/', OrderView.as_view(), name='order'),
    path('b2b_order/', B2BOrderView.as_view(), name='order_b2b'),
    path('seller_order/<id>', SellerOrderView.as_view(), name='seller_order'),
    path('order_details/<id>', OrderDetailsView.as_view(), name='order_details'),
    path('update_status/', UpdateStatusView.as_view(), name='updatestatus'),
    path('delete_order/', DeleteOrderView.as_view(), name='delete'),
]