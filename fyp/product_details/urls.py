from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    # path('add_product/', AddProductView.as_view(), name='Add Products'),
    path('product_display/', ProductView.as_view(), name="Products"),
    path('wishlist/', WishlistView.as_view(), name="Wishlist"),
    path('wishlist/<id>', WishlistView.as_view(), name="Wishlist"),
    path('details/<id>', ProductDetailsView.as_view(), name="details"),
    path('reviews/<id>', UserCountView.as_view(), name="reviews"),
    path('seller_products/<id>', SellerProductDetailsView.as_view(), name="seller_products"),
    path('delete_wishlist/', DeleteWishlistView.as_view(), name="Wishlist_delete"),
    path('compare/', AddCompareView.as_view(), name="Compare"),
    path('delete_product/', DeleteProductView.as_view(), name="Delete"),
    path('compare/<id>', AddCompareView.as_view(), name="Compare_details"),
    path('delete_compare/', DeleteCompareView.as_view(), name="Delete_compare"),
    path('add_category/', AddCategoryView.as_view(), name="add_Category"),
    path('add_product/', AddProductView.as_view(), name="add_product"),
    path('feedback/', FeedBackView.as_view(), name="add_product"),
    path('recommendations/<int:user_id>', RecommendationView.as_view(), name='product-recommendations'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)