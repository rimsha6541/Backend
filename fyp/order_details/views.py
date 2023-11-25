from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
import json 
from rest_framework.decorators import api_view
from user_details.models import UserDetails
from product_details.models import *
from transaction_details.models import Transaction
from transaction_details.serializers import TransactionSerializer
from cart_details.models import Cart
import stripe
from decimal import Decimal
import json

    
class ShowShipmentView(APIView):
    def get(self, request, id):
        user = UserDetails.objects.get(id=id)
        if user is not None:
            shipment = ShipmentDetails.objects.filter(user_id = user)
            if shipment is not None:
                serializer = ShipmentSerializer(shipment, many=True)
                return Response({'data' : serializer.data, 'error' : False}, status.HTTP_202_ACCEPTED)
        return Response({'msg' : 'No data to show', 'error' : True}, status.HTTP_204_NO_CONTENT)
    
class OrderView(APIView):

    def post(self, request):
        stripe.api_key = 'sk_test_51MpzUtLoFp1QEKARGxkOuCCDODAxX9TSy8VsNPZgN9bpFdragt0dy5yi2Lw7KXmxOoYUSXeRInCutS22rRnAMC99002om5S2rq'
        print(request.data)
        serializer = AddOrderSerializer(data=request.data)
        # print(serializer)
    #     if serializer.is_valid():
    #         user_id = request.data['user_id']
    #         user_data = get_object_or_404(UserDetails, id=user_id)
    #         cart = Cart.objects.filter(user_data=user_data)
    #         total = Decimal('0')  # Initialize total as a Decimal
    #         discount = Decimal('0')  # Initialize discount as a Decimal
    #         if cart.exists():
    #             for product in cart:
    #                 price = product.product.disc_price
    #                 quantity = int(product.quantity)
    #                 total += (price * quantity)
    #                 discount += Decimal(product.product.p_price - price)  # Convert to Decimal
    #             shipping = Decimal('500')  # Initialize shipping as a Decimal
    #             total_bill = total + shipping
    #             order = Order.objects.create(user_id=user_data, total_bill=total_bill, discount=discount, bill_payed='0', payment_type='None', created_at=timezone.now(), updated_at=timezone.now())
    #             order_name = str(order.o_id)  # Convert order.o_id to string
    #             session = stripe.checkout.Session.create(
    #                 line_items=[{
    #                     'price_data': {
    #                         'currency': 'usd',
    #                         'product_data': {
    #                             'name': order_name,
    #                         },
    #                         'unit_amount': int(total_bill * 100),  # Convert to cents
    #                     },
    #                     'quantity': 1,
    #                 }],
    #                 mode='payment',
    #                 success_url='http://localhost:3000/product',
    #                 cancel_url='http://localhost:3000/checkout'
    #             )
    #             url = session.url
    #             session_id = session.id
    #             request.session['id'] = session_id
        if serializer.is_valid():
            print(request.data)
            user_id = serializer.validated_data['user_id']
            o_panel = serializer.validated_data['o_panel']
            payment = request.data['payment_type']
            if payment == 'Stripe':
                card_number = request.data['card_number']
                exp_month = request.data['exp_month']
                exp_year = request.data['exp_year']
                cvc = request.data['cvc']
                if card_number is None or exp_month is None or  cvc is None or exp_year is None:
                        return Response({
                            'msg' : 'Please Enter Valid Card Details',
                            'error' : True
                        })
            address = request.data['address']
            p_address = request.data['address']
            city = request.data['city']
            state = request.data['state']
            zip = request.data['zip']
            firstname = request.data['firstname']
            lastname = request.data['lastname']
            user = UserDetails.objects.get(id=user_id)
            user_data = get_object_or_404(UserDetails, id=user_id)
            cart = Cart.objects.filter(user_data=user_data)
            total = Decimal('0')
            discount = Decimal('0')
            # print('Into ser')
            if cart.exists():
                # print('into if')
                for product in cart:
                    price = product.product.disc_price
                    quantity = int(product.quantity)
                    total += (price * quantity)
                    discount += Decimal(product.product.p_price - price)
                
                shipping = Decimal('500')
                total_bill = total + shipping
                if payment == 'Stripe':
                    try:
                        # Use a test token instead of card details
                        payment_method = stripe.PaymentMethod.create(
                            type="card",
                            card={
                                "token" : "tok_visa"
                            },  
                        )

                        # Continue with the payment process using the test token
                        payment_intent = stripe.PaymentIntent.create(
                            amount=int(total_bill * 100),
                            currency="usd",
                            payment_method=payment_method.id,  # Use the PaymentMethod ID
                            confirm=True,
                            return_url="http://localhost:3002/checkout"
                        )

                        order = Order.objects.create(
                            user_id=user_data,
                            total_bill=total_bill,
                            bill_payed=total_bill,
                            payment_type='Stripe',
                            discount=discount,
                            o_status='In Process',
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            o_panel = o_panel
                        )
                        order.save()
                        shipment = ShipmentDetails.objects.create(
                            address = address,
                            city = city,
                            state = state,
                            zip = zip,
                            user_id = user,
                            p_address=p_address,
                            first_name=firstname,
                            last_name=lastname,
                            order = order
                        )
                        shipment.save()
                        transaction = Transaction.objects.create(
                                transaction_id = payment_method.stripe_id,
                                order=order,
                                created_at=timezone.now(),
                                updated_at=timezone.now()
                        )
                        for q in cart: 
                            update = Variation.objects.get(product_id=product.product.p_id)
                            update.quantity -= int(q.quantity)
                            update.save()
                            details = OrderDetails.objects.create(
                            actual_price=q.product.p_price,
                            sale_price=q.product.disc_price,
                            discount = q.product.discount,
                            order = order,
                            product = q.product,
                            variation = update,
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        details.save()
                        cart.delete()
                        return Response({
                            'data': serializer.data,
                            'error': False,
                            'msg': 'Order Created and Payment Successful',
                        }, status=status.HTTP_202_ACCEPTED)

                    except stripe.error.CardError as e:
                        return Response({
                            'error': True,
                            'msg': str(e.user_message)
                        }, status=status.HTTP_400_BAD_REQUEST)
                elif payment == 'Cash':
                    order = Order.objects.create(
                            user_id=user_data,
                            total_bill=total_bill,
                            discount=discount,
                            bill_payed='0',
                            payment_type='Cash',
                            o_status='In Process',
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            o_panel = o_panel
                        )
                    order.save()
                    shipment = ShipmentDetails.objects.create(
                        address = address,
                        p_address = p_address,
                        city = city,
                        state = state,
                        zip = zip,
                        user_id = user,
                        first_name=firstname,
                        last_name=lastname,
                        order = order
                    )
                    shipment.save()
                    for q in cart: 
                        update = Variation.objects.get(product_id=product.product.p_id)
                        update.quantity -= int(q.quantity)
                        update.save()
                        details = OrderDetails.objects.create(
                            actual_price=q.product.p_price,
                            sale_price=q.product.disc_price,
                            discount = q.product.discount,
                            order = order,
                            product = q.product,
                            variation = update,
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        details.save()
                    cart.delete()
                    # orderSerializer = ViewOrderSerializer(order)
                    return Response({
                            'data': serializer.data,
                            'error': False,
                            'msg': 'Order Created Successfully',
                        }, status=status.HTTP_202_ACCEPTED)
                return Response({
                'error': True,
                'msg': 'Cannot Create Order, Your cart is empty'
            }, status=status.HTTP_202_ACCEPTED)
        return Response({
            'error': True,
            'msg': 'Cannot Create Order'
        }, status=status.HTTP_202_ACCEPTED)
    

    def get(self, request):
        order = Order.objects.all()
        if order is not None:
            serializer = OrderSerializer(order, many=True)
            return Response({
                'data' : serializer.data,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data' 
        })

class UpdateStatusView(APIView):

    def post(self, request):
        serializer = UpdateStatusSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            order_id = request.data['o_id']
            status = request.data['o_status']
            order = Order.objects.get(o_id=order_id)
            order.o_status = status
            order.bill_payed = order.total_bill
            order.save()
            return Response({
                'data' : serializer.data,
                'error' : False,
                'msg' : 'Order Status Updated SuccessFully'
            })
        return Response({
            'error' : True,
            'msg' : 'Cannot Update Order, Your Order is not Found'
        }, status.HTTP_204_NO_CONTENT) 

class DeleteOrderView(APIView):

    def post(self, request):
        serializer = DorderSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data['order_id'])
            order = Order.objects.get(o_id=request.data['order_id'])
            order.delete()
            return Response({'error': False, 'msg': 'Order deleted successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': True, 'msg': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

class SellerOrderView(APIView):
    def get(self, request, id):
        orderDetails = OrderDetails.objects.filter(product__user_data__id=id)
        orders = []
        for order in orderDetails:
            orders.append(order.order)
        if orders is not None:
            serializer = OrderSerializer(orders, many=True)
            return Response({
                'data' : serializer.data,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data' 
        })
    
class B2BOrderView(APIView):

     def post(self, request):
        stripe.api_key = 'sk_test_51MpzUtLoFp1QEKARGxkOuCCDODAxX9TSy8VsNPZgN9bpFdragt0dy5yi2Lw7KXmxOoYUSXeRInCutS22rRnAMC99002om5S2rq'
        # print(request.data)
        serializer = AddOrderSerializer(data=request.data)
        # print(serializer)
    #     if serializer.is_valid():
    #         user_id = request.data['user_id']
    #         user_data = get_object_or_404(UserDetails, id=user_id)
    #         cart = Cart.objects.filter(user_data=user_data)
    #         total = Decimal('0')  # Initialize total as a Decimal
    #         discount = Decimal('0')  # Initialize discount as a Decimal
    #         if cart.exists():
    #             for product in cart:
    #                 price = product.product.disc_price
    #                 quantity = int(product.quantity)
    #                 total += (price * quantity)
    #                 discount += Decimal(product.product.p_price - price)  # Convert to Decimal
    #             shipping = Decimal('500')  # Initialize shipping as a Decimal
    #             total_bill = total + shipping
    #             order = Order.objects.create(user_id=user_data, total_bill=total_bill, discount=discount, bill_payed='0', payment_type='None', created_at=timezone.now(), updated_at=timezone.now())
    #             order_name = str(order.o_id)  # Convert order.o_id to string
    #             session = stripe.checkout.Session.create(
    #                 line_items=[{
    #                     'price_data': {
    #                         'currency': 'usd',
    #                         'product_data': {
    #                             'name': order_name,
    #                         },
    #                         'unit_amount': int(total_bill * 100),  # Convert to cents
    #                     },
    #                     'quantity': 1,
    #                 }],
    #                 mode='payment',
    #                 success_url='http://localhost:3000/product',
    #                 cancel_url='http://localhost:3000/checkout'
    #             )
    #             url = session.url
    #             session_id = session.id
    #             request.session['id'] = session_id
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            o_panel = serializer.validated_data['o_panel']
            payment = request.data['payment_type']
            if payment == 'Stripe':
                card_number = request.data['card_number']
                exp_month = request.data['exp_month']
                exp_year = request.data['exp_year']
                cvc = request.data['cvc']
            address = request.data['address']
            city = request.data['city']
            state = request.data['state']
            zip = request.data['zip']
            firstname = request.data['firstname']
            lastname = request.data['lastname']
            user = UserDetails.objects.get(id=user_id)
            user_data = get_object_or_404(UserDetails, id=user_id)
            cart = Cart.objects.filter(user_data=user_data)
            total = Decimal('0')
            discount = Decimal('0')
            
            # print('Into ser')
            if cart.exists():
                # print('into if')
                for product in cart:
                    price = product.product.disc_price
                    quantity = int(product.quantity)
                    total += (price * quantity)
                    discount += Decimal(product.product.p_price - price)
                
                shipping = Decimal('500')
                total_bill = total + shipping
                # percent = (total_bill * 100)
                if payment == 'Stripe':
                    try:
                        # Use a test token instead of card details
                        payment_method = stripe.PaymentMethod.create(
                            type="card",
                            card={
                                "token" : "tok_visa"
                            },  
                        )

                        # Continue with the payment process using the test token
                        payment_intent = stripe.PaymentIntent.create(
                            amount=int(total_bill * 100),
                            currency="usd",
                            payment_method=payment_method.id,  # Use the PaymentMethod ID
                            confirm=True,
                        )

                        order = Order.objects.create(
                            user_id=user_data,
                            total_bill=total_bill,
                            bill_payed=total_bill,
                            payment_type='Stripe',
                            discount=discount,
                            o_status='In Process',
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            o_panel = o_panel
                        )
                        order.save()
                        shipment = ShipmentDetails.objects.create(
                            address = address,
                            city = city,
                            state = state,
                            zip = zip,
                            user_id = user,
                            last_name=lastname,
                            first_name=firstname,
                            order = order
                        )
                        shipment.save()
                        transaction = Transaction.objects.create(
                                transaction_id = payment_method.stripe_id,
                                order=order,
                                created_at=timezone.now(),
                                updated_at=timezone.now()
                        )
                        for q in cart: 
                            update = Variation.objects.get(product_id=product.product.p_id)
                            update.quantity -= int(q.quantity)
                            update.save()
                            details = OrderDetails.objects.create(
                            actual_price=q.product.p_price,
                            sale_price=q.product.disc_price,
                            discount = q.product.discount,
                            order = order,
                            product = q.product,
                            variation = update,
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        details.save()
                        cart.delete()
                        return Response({
                            'data': serializer.data,
                            'error': False,
                            'msg': 'Order Created and Payment Successful',
                        }, status=status.HTTP_202_ACCEPTED)

                    except stripe.error.CardError as e:
                        return Response({
                            'error': True,
                            'msg': str(e.user_message)
                        }, status=status.HTTP_400_BAD_REQUEST)
                elif payment == 'Cash':
                    order = Order.objects.create(
                            user_id=user_data,
                            total_bill=total_bill,
                            discount=discount,
                            bill_payed='0',
                            payment_type='Cash',
                            o_status='In Process',
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            o_panel = o_panel
                        )
                    order.save()
                    shipment = ShipmentDetails.objects.create(
                        address = address,
                        city = city,
                        state = state,
                        zip = zip,
                        user_id = user,
                        last_name=lastname,
                        first_name=firstname,\
                        order = order
                    )
                    shipment.save()
                    for q in cart: 
                        update = Variation.objects.get(product_id=product.product.p_id)
                        update.quantity -= int(q.quantity)
                        update.save()
                        details = OrderDetails.objects.create(
                            actual_price=q.product.p_price,
                            sale_price=q.product.disc_price,
                            discount = q.product.discount,
                            order = order,
                            product = q.product,
                            variation = update,
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        details.save()
                    cart.delete()
                    # orderSerializer = ViewOrderSerializer(order)
                    return Response({
                            'data': serializer.data,
                            'error': False,
                            'msg': 'Order Created Successfully',
                        }, status=status.HTTP_202_ACCEPTED)
                return Response({
                'error': True,
                'msg': 'Cannot Create Order, Your cart is empty'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'error': True,
            'msg': 'Cannot Create Order'
        }, status=status.HTTP_204_NO_CONTENT)
     

class OrderDetailsView(APIView):
    def get(self, request, id):
        orderDetails = OrderDetails.objects.filter(order__user_id__id=id)
        if orderDetails:
            serializer = OrderDetailsSerializer(orderDetails, many=True)
            return Response({
                'data': serializer.data,
                'error': False,
            })
        return Response({
            'error': True,
            'msg': 'There is an error fetching data',
        }, status=status.HTTP_404_NOT_FOUND)


