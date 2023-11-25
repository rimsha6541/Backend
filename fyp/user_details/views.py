from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import *
from cart_details.models import *
from cart_details.serializers import *
from product_details.models import *
from product_details.serializers import *
from order_details.models import *
from order_details.serializers import *
from django.utils import timezone
import random
import string
from django.core.mail import send_mail
from datetime import datetime
from django.db.models import Count
from django.shortcuts import HttpResponse
from django.views import View
from math import sqrt
import numpy as np
# Create your views here.

from .serializers import *

def generate_random_code(length):
    characters = string.digits  # Use digits for a numeric code
    code = ''.join(random.choice(characters) for _ in range(length))
    return code 

class UserDetailsView(APIView):
    def get(self, request, id):
        user = UserDetails.objects.filter(id=id)
        if user is not None:
            serializer = UserSerializer(user, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })
    
    def post(self,request, id):
        user = UserDetails.objects.get(id=id)
        created_at = user.created_at
        if user is not None:
            name = request.data['username']
            phone_no = request.data['phone_no']
            email = request.data['email']
            address = request.data['address']
            user.username = name
            user.phone_no = phone_no
            user.email = email
            user.address = address
            user.updated_at = timezone.now()
            user.created_at = created_at
            user.save()
            serializer = UserSerializer(user)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })


class SignupView(APIView):

    def post(self, request):
        data = request.data
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = UserDetails.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                phone_no = request.data['phone_no'],
                verified = 0,
                created_at = timezone.now(),
                updated_at = timezone.now()
            )
            user.set_password(request.data['password'])
            user.save()
            
            reset_code = generate_random_code(6)
            otp = OTP.objects.create(
                otp = reset_code,
                user = user
            )
            otp.save()

            subject = "Password Reset Code"
            message = f"Your password reset code is: {reset_code}"
            from_email = "EasyBay <mabuhurairah07@gmail.com>" 
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response({'data': serializer.data,'code' : reset_code, 'error' : False, 'msg' : 'Account Created Successfully'},status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status.HTTP_400_BAD_REQUEST, {'error' : True, 'msg' : 'Error Creating Account'})
        
class LoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, User or Password Incorrect'},status.HTTP_201_CREATED)
            else:
                user_data_fetch = UserDetails.objects.get(username=username)
                if user_data_fetch.verified == 1:
                # serializer_data = UserSerializer(user_data_fetch)
                    response_data = {
                        'id' : user_data_fetch.id,
                        'username' : user_data_fetch.username,
                    }
                    return Response({ 'data' : response_data , 'error' : False, 'msg' : 'Logged In Successfully'},status.HTTP_201_CREATED)
                else:
                    return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Please Verify your Email'},status.HTTP_201_CREATED)
class SellerSignupView(APIView):

    def post(self, request):
        data = request.data
        serializer = SellerSignupSerializer(data=data)
        if serializer.is_valid():
            user = UserDetails.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                phone_no = request.data['phone_no'],
                created_at = timezone.now(),
                updated_at = timezone.now(),
                is_seller = True   
            )
            user.set_password(request.data['password'])
            user.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Seller Account Created Successfully'},status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status.HTTP_400_BAD_REQUEST, {'error' : True, 'msg' : 'Error Creating Seller Account'})
        
class SellerLoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = SellerLoginSerializer(data = data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            seller = True
            if user is None:
                return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_HTTP_201_CREATED)
            elif user is not None:
                user_data_fetch = UserDetails.objects.get(username=username, is_seller=seller)
                if user_data_fetch is None:
                   return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_201_CREATED) 
                else :
                    response_data = {
                        'id' : user_data_fetch.id,
                        'username' : user_data_fetch.username,
                    }
                return Response({'data' : response_data, 'error' : False, 'msg' : 'Seller Logged In Successfully'},status.HTTP_201_CREATED) 
                

class AdminSignupView(APIView):

    def post(self, request):
        data = request.data
        serializer = AdminSignupSerializer(data=data)
        if serializer.is_valid():
            user = UserDetails.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                phone_no = request.data['phone_no'],
                created_at = timezone.now(),
                updated_at = timezone.now(),
                is_seller = True,
                is_admin = True   
            )
            user.set_password(request.data['password'])
            user.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Admin Account Created Successfully'},status.HTTP_201_CREATED)
        else:
           return Response(serializer.data, status.HTTP_400_BAD_REQUEST, {'error' : True, 'msg' : 'Error Creating Admin Account'})
        
class AdminLoginView(APIView):

    def post(self, request):
        data = request.data
        print(data)
        serializer = AdminLoginSerializer(data = data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_201_CREATED)
            elif user is not None:
                user_data_fetch = UserDetails.objects.get(username=username)
                if user_data_fetch is None:
                   return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_201_CREATED) 
                else :
                    response_data = {
                        'id' : user_data_fetch.id,
                        'username' : user_data_fetch.username,
                    }
                return Response({'data' : response_data, 'error' : False, 'msg' : 'Admin Logged In Successfully'},status.HTTP_201_CREATED) 
            
class AdminDetailsView(APIView):
    def get(self, request, id):
        admin = UserDetails.objects.filter(id=id, is_admin=True)
        if admin is not None:
            serializer = AdminDetailsSerializer(admin, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })
    
    def post(self,request, id):
        admin = UserDetails.objects.get(id=id, is_admin=True)
        created_at = admin.created_at
        if admin is not None:
            name = request.data['username']
            phone_no = request.data['phone_no']
            email = request.data['email']
            check = UserDetails.objects.get(email=email)
            phoneCheck = UserDetails.objects.get(phone_no=phone_no)
            if check or phoneCheck:
                return Response({
                    'data'  : 'There is already a user with same email'
                })
            admin.username = name
            admin.phone_no = phone_no
            admin.email = email
            admin.updated_at = timezone.now()
            admin.created_at = created_at
            admin.save()
            serializer = AdminDetailsSerializer(admin)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })



class TotalUsersView(APIView):
    def get(self, request):
        allseller = self.get_allseller()
        allcustomers = self.get_allcustomers()
        if allseller is not None or allcustomers is not None:
            return Response({
                'allseller' : allseller,
                'allcustomers' : allcustomers,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data'
        })

    def get_allseller(self):
        seller = UserDetails.objects.filter(is_seller=True)
        if seller is not None:
            serializer = UserSerializer(seller, many=True)
            return serializer.data
        return []
  
    def get_allcustomers(self):
        customers = UserDetails.objects.filter(is_seller=False,is_admin=False)
        customers_count = UserDetails.objects.filter(is_seller=False,is_admin=False).count()
        if customers is not None:
            serializer = UserSerializer(customers, many=True)
            return {
                'data' : serializer.data,
                'count' : customers_count
            }
        return []


class DashboardView(APIView):
    def get(self, request, id):
            current_month = timezone.now().month
            current_year = timezone.now().year
            current_date = timezone.now().date()
            user = UserDetails.objects.get(id=id, is_admin=True)
            if user is None:
                return Response({
                'error' : True,
                'data' : 'User Not Found'
            })
            else:
                order = Order.objects.all()
                todayOrders = Order.objects.filter(updated_at__date=current_date)
                monthOrder = Order.objects.filter(updated_at__month=current_month, updated_at__year=current_year)
                monthCustomers = UserDetails.objects.filter(is_admin=False, is_seller=False, is_active=True, updated_at__month=current_month, updated_at__year=current_year)
                todayCustomers = UserDetails.objects.filter(is_admin=False, is_seller=False, is_active=True, updated_at__date=current_date)
                customer = UserDetails.objects.filter(is_admin=False, is_seller=False, is_active=True)
                processing = Order.objects.filter(o_status='In Process')
                delivered = Order.objects.filter(o_status='Delivered')
                deliveredcount = delivered.count()
                processingcount = processing.count()
                customercount = customer.count()
                ordercount = order.count()
                monthordercount = monthOrder.count()
                monthcustomercount = monthCustomers.count()
                todaycustomercount = todayCustomers.count()
                todayordercount = todayOrders.count()
                if order and customer is not None:
                    data = {
                        'ordercount' : ordercount,
                        'customercount' : customercount,
                        'monthorders' : monthordercount,
                        'monthcustomers' : monthcustomercount,
                        'todayorders' : todayordercount,
                        'todaycustomers' : todaycustomercount,
                        'processing' : processingcount,
                        'delivered' : deliveredcount
                    }
                    return Response({
                        'data' : data,
                        'error' : False,
                    })
                return Response({
                    'error' : True,
                    'msg' : 'No info Found'
                })
            
class SellerDashboardView(APIView):
    def get(self, request, id):
            current_month = timezone.now().month
            current_year = timezone.now().year
            current_date = timezone.now().date()
            user = UserDetails.objects.get(id=id, is_seller=True)
            if user is None:
                return Response({
                'error' : True,
                'data' : 'User Not Found'
            })
            else:
                order = OrderDetails.objects.filter(product__user_data__id=id)
                revenue = int(0)
                for bill in order:
                    revenue += float(bill.order.bill_payed)
                todayOrders = OrderDetails.objects.filter(product__user_data__id=id , updated_at__date=current_date)
                todayRevenue = int(0)
                for bill in todayOrders:
                    todayRevenue += float(bill.order.bill_payed)
                monthOrder = OrderDetails.objects.filter(product__user_data__id=id , updated_at__month=current_month, updated_at__year=current_year)
                monthRevenue = int(0)
                for bill in monthOrder:
                    monthRevenue += float(bill.order.bill_payed)

                processing = OrderDetails.objects.filter(product__user_data__id=id , order__o_status='In Process')
                delivered = OrderDetails.objects.filter(product__user_data__id=id , order__o_status='Delivered')
                deliveredcount = delivered.count()
                processingcount = processing.count()
                ordercount = order.count()
                monthordercount = monthOrder.count()
                todayordercount = todayOrders.count()
                if order is not None:
                    data = {
                        'ordercount' : ordercount,
                        'revenue' : revenue,
                        'monthorders' : monthordercount,
                        'monthRevenue' : monthRevenue,
                        'todayorders' : todayordercount,
                        'todayRevenue' : todayRevenue,
                        'processing' : processingcount,
                        'delivered' : deliveredcount
                    }
                    return Response({
                        'data' : data,
                        'error' : False,
                    })
                return Response({
                    'error' : True,
                    'msg' : 'No info Found'
                })
            
 


class ForgotPasswordView(APIView):


    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                print(request.data)
                user = UserDetails.objects.get(email=request.data['email'])
            except UserDetails.DoesNotExist:
                return Response({
                    'error': True,
                    'msg': 'User with this email does not exist.'
                }, status=status.HTTP_404_NOT_FOUND)

            reset_code = generate_random_code(6)
            otp = OTP.objects.create(
                otp = reset_code,
                user = user
            )
            otp.save()

            subject = "Password Reset Code"
            message = f"Your password reset code is: {reset_code}"
            from_email = "EasyBay <mabuhurairah07@gmail.com>"  # Replace with your email
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response({
                'error': False,
                'msg': 'Password reset code has been sent to your email.',
                'code' : reset_code,
            }, status=status.HTTP_200_OK)

        return Response({
            'error': True,
            'msg': 'Invalid data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class CheckCodeView(APIView):

    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            code = request.data['code']
            otp = OTP.objects.get(otp=code)
            # request.session['id'] = otp.user.id
            if otp is not None:
                user_id = otp.user.id
                user = UserDetails.objects.get(id = user_id)
                user.verified = 1
                user.save()
                otp.delete()
                return Response({
                    'data' : 'Validated',
                    'id' : user_id,
                    'error' : False,
                })
            elif otp is None:

                return Response({
                    'data' : 'Invalid Code Please Enter Right Code',
                    'error' : True
                })
            
class UpdatePasswordView(APIView):

    def post(self, request, id):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # id  = request.session.get('id')
            # print(id)
            try:
                user = UserDetails.objects.get(id=id)
                user.set_password(request.data['password'])
                user.save()
                return Response({
                    'error': False,
                    'msg': 'Password has been Updated'
                })
            except UserDetails.DoesNotExist:
                return Response({
                    'error': True,
                    'msg': 'Please Enter A Valid Password'
                }, status=status.HTTP_404_NOT_FOUND)
            
class SellerSalesView(APIView):
    def get(self, request, id):
            current_month = timezone.now().month
            current_year = timezone.now().year
            current_date = timezone.now().date()
            user = UserDetails.objects.get(id=id, is_seller=True)
            if user is None:
                return Response({
                'error' : True,
                'data' : 'User Not Found'
            })
            else:
                order = OrderDetails.objects.filter(product__user_data__id=id)
                if order is not None:
                    serializer = OrderDetailsSerializer(order, many=True)
                    return Response({
                        'data' : serializer.data,
                        'error' : False,
                    })
                return Response({
                    'error' : True,
                    'msg' : 'No info Found'
                })
            
class UserDetailsView(APIView):
    def get(self, request, id):
        user = UserDetails.objects.filter(id=id)
        if user is not None:
            serializer = UserDetailsSerializer(user, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })
    
    def post(self,request, id):
        user = UserDetails.objects.get(id=id)
        created_at = user.created_at
        if user is not None:
            name = request.data['username']
            phone_no = request.data['phone_no']
            email = request.data['email']
            address = request.data['address']
            check = UserDetails.objects.get(email=email)
            phoneCheck = UserDetails.objects.get(phone_no=phone_no)
            if check or phoneCheck:
                return Response({
                    'data'  : 'There is already a user with same email'
                })
            user.username = name
            user.phone_no = phone_no
            user.email = email
            user.address = address
            user.updated_at = timezone.now()
            user.created_at = created_at
            user.save()
            serializer = UserDetailsSerializer(user)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })

class DeleteCustomerView(APIView):

    def post(self, request):
        serializer = DCustomerSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data['id'])
            user = UserDetails.objects.get(id=request.data['id'])
            user.delete()
            return Response({'error': False, 'msg': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': True, 'msg': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class SellerDetailsView(APIView):
    def get(self, request, id):
        seller = UserDetails.objects.filter(id=id, is_seller=True)
        if seller is not None:
            serializer = AdminDetailsSerializer(seller, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })
    
    def post(self,request, id):
        seller = UserDetails.objects.get(id=id, is_seller=True)
        created_at = seller.created_at
        if seller is not None:
            name = request.data['username']
            phone_no = request.data['phone_no']
            email = request.data['email']
            check = UserDetails.objects.get(email=email)
            phoneCheck = UserDetails.objects.get(phone_no=phone_no)
            if check or phoneCheck:
                return Response({
                    'data'  : 'There is already a user with same email'
                })
            seller.username = name
            seller.phone_no = phone_no
            seller.email = email
            seller.updated_at = timezone.now()
            seller.created_at = created_at
            seller.save()
            serializer = AdminDetailsSerializer(seller)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })



def mean_squared_error(predictions, targets):
    return ((predictions - targets) ** 2).mean()

def gradient_descent(X, y, theta, learning_rate, iterations, lambda_val, max_gradient_value=0.5):
    m = len(y)
    for i in range(iterations):
        predictions = X.dot(theta)
        errors = predictions - y
        # Regularized cost function
        cost = mean_squared_error(predictions, y) + (lambda_val / (2 * m)) * np.sum(theta[1:]**2)
        print(f"Iteration {i+1}/{iterations}, Cost: {cost}")

        # Regularized gradient with clipping
        gradient = (X.T.dot(errors) + lambda_val * np.concatenate(([0], theta[1:]))) / m
        gradient = np.clip(gradient, -max_gradient_value, max_gradient_value)

        theta = theta - learning_rate * gradient

    return theta

def train_and_predict(user):
    # Extract product fields from Cart, Feedback, and Wishlist
    cart_products = Cart.objects.filter(user_data=user)
    feedback_products = Feedback.objects.filter(user=user)
    wishlist_products = Wishlist.objects.filter(user_data=user)

    # Your existing code to retrieve products
    # ...

    # Extract relevant data for linear regression
    product_data = [(product.p_id, product.rating) for product in Product.objects.all()]
    feedback_data = [(feedback.product.p_id, feedback.stars) for feedback in feedback_products]
    feed_data = [(feedback.product.p_id, feedback.stars) for feedback in Feedback.objects.all()]

    # If there are feedback products, include them in product_data
    if feedback_products.exists():
        product_data += feedback_data
    else:
        product_data += feed_data

    # If there are cart products, update X and y
    if cart_products.exists():
        cart_data = [(cart_product.product.p_id, 0) for cart_product in cart_products]
        product_data += cart_data  # Add cart products to product_data

    # If there are wishlist products, update X and y
    if wishlist_products.exists():
        wishlist_data = [(wishlist_product.product.p_id, 0) for wishlist_product in wishlist_products]
        product_data += wishlist_data  # Add wishlist products to product_data

    # Merge data and create a matrix X and target vector y
    # Convert decimal.Decimal to float in X
    X = np.array([[1, float(p_id), float(rating)] for p_id, rating in product_data])
    y = np.array([float(rating) for _, rating in product_data])

    # Normalize ratings to a common scale (optional)
    y = (y - np.mean(y)) / np.std(y)

    # Initialize theta with small random values
    theta = np.random.rand(3)

    # Perform gradient descent to learn the parameters
    learning_rate = 0.02
    iterations = 1000
    lambda_val = 0.1
    theta = gradient_descent(X, y, theta, learning_rate, iterations, lambda_val)

    # Now, use the learned parameters to make predictions for unrated products
    unrated_products = [p_id for p_id, _ in product_data if p_id not in feed_data]

    # Create a matrix X for unrated products
    X_unrated = np.array([[1, p_id, 0] for p_id in unrated_products])

    # Make predictions for unrated products
    predictions = X_unrated.dot(theta)

    # Sort products based on predicted ratings and recommend the top 5
    recommended_products = sorted(zip(unrated_products, predictions), key=lambda x: x[1], reverse=True)[:5]

    # Extract product IDs from the recommendations
    recommended_product_ids = [product_id for product_id, _ in recommended_products]
    data = []
    
    for prod in recommended_product_ids:
        if prod not in data:
            data.append(prod)
    
    return data
                
        

class RecommendationView(APIView):
    def get(self, request, id):
        try:
            user = UserDetails.objects.get(id=id)
        except UserDetails.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        response_data = train_and_predict(user)
        print(response_data)
        products_list = []

        for r in response_data:
            # Use filter to get products for each p_id
            products_for_id = Product.objects.filter(p_id=r)
            
            # Extend the products_list with the results for the current p_id
            products_list.extend(products_for_id)

        # Serialize the entire list of products
        serializer = ProductSerializer(products_list, many=True)

        # Return the serialized data
        return Response({'data': serializer.data, 'error' : False}, status=200)














            



