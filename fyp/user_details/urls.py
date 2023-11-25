from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='SignUp'),
    path('login/', LoginView.as_view(), name='Login'),
    path('seller_signup/', SellerSignupView.as_view(), name='seller SignUp'),
    path('seller_login/', SellerLoginView.as_view(), name='seller Login'),
    path('admin_login/', AdminLoginView.as_view(), name='Admin Login'),
    path('admin_signup/', AdminSignupView.as_view(), name='Admin Signup'),
    path('all_users/', TotalUsersView.as_view(), name='Total_users'),
    path('admin/<int:id>/', AdminDetailsView.as_view(), name='AdminDetails'),
    path('seller/<int:id>/', SellerDetailsView.as_view(), name='SellerDetails'),
    path('user/<int:id>', UserDetailsView.as_view(), name='UserDetails'),
    path('forget_password/', ForgotPasswordView.as_view(), name='Forgot_Password'),
    path('validate/', CheckCodeView.as_view(), name='Validate'),
    path('delete/', DeleteCustomerView.as_view(), name='delete'),
    path('update_password/<id>', UpdatePasswordView.as_view(), name='update'),
    path('dashboard/<id>', DashboardView.as_view(), name='dashboard'),
    path('sellerdashboard/<id>', SellerDashboardView.as_view(), name='seller_dashboard'),
    path('customer/<id>', UserDetailsView.as_view(), name='customer'),
    path('sales/<id>', SellerSalesView.as_view(), name='sales'),
    path('recommend/<id>', RecommendationView.as_view(), name='recommend'),

    
]