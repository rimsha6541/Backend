from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from .models import *
from user_details.models import UserDetails
import pandas as pd
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random
from decimal import Decimal



class AddProductView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        print(request.data)
        serializer = AddProductSerializer(data=request.data)
        image = request.data['p_image']
        if serializer.is_valid():
            # print('into for Loop')
            # print(request.data['ac_capacity'])
            category_name = request.data['category']
            category = Category.objects.get(cat_name = category_name)
            # sub_cat_name = request.data['sub_category']
            # sub_cat = SubCategory.objects.get(sub_name = sub_cat_name)
            inverter = request.data['ac_inverter']
            invert = False
            if inverter == "true":
                invert = True
            else:
                invert = False
            user = UserDetails.objects.get(id = request.data['user_data'], is_seller=True)
            product = Product.objects.create(
                    p_name = request.data['p_name'],
                    p_image = request.data['p_image'],
                    p_brand = request.data['p_brand'],
                    p_status = request.data['p_status'],
                    p_des = request.data['p_des'],
                    p_price = request.data['p_price'],
                    disc_price = request.data['disc_price'],
                    discount = request.data['discount'],
                    category = category,
                    # sub_category = sub_cat_name,
                    user_data = user,
                    created_at = timezone.now(),
                    updated_at = timezone.now()
                )
            product.save()
            if category_name == 'Phones':  
                mobile = MobilePhones.objects.create(
                    category = category,
                    # sub_category = sub_cat_name,
                    product = product,
                    mobile_processor = request.data['mobile_processor'],
                    mobile_battery = request.data['mobile_battery'],
                    mobile_memory = request.data['mobile_memory'],
                    mobile_display = request.data['mobile_display'],
                    mobile_camera = request.data['mobile_camera']
                )
                mobile.save()
            elif category_name == 'Laptops':
                laptops = Laptops.objects.create(
                    category = category,
                    # sub_category = sub_cat_name,
                    product = product,
                    laptop_processor = request.data['laptop_processor'],
                    laptop_battery = request.data['laptop_battery'],
                    laptop_memory = request.data['laptop_memory'],
                    laptop_display = request.data['laptop_display'],
                    laptop_generation = request.data['laptop_generation']
                )
                laptops.save()
            elif category_name == 'LCD':
                lcd = LCD.objects.create(
                    category = category,
                    # sub_category = sub_cat_name,
                    product = product,
                    lcd_display = request.data['lcd_display'],
                    lcd_power_consumption = request.data['lcd_power_consumption'],
                    lcd_audio = request.data['lcd_audio'],
                    lcd_chip = request.data['lcd_chip']
                )
                lcd.save()
            elif category_name == 'AC':
                ac = AC.objects.create(
                    category = category,
                    # sub_category = sub_cat_name,
                    product = product,
                    ac_capacity = request.data['ac_capacity'],
                    ac_type = request.data['ac_type'],
                    ac_inverter = invert,
                    ac_warranty = request.data['ac_warranty'],
                    ac_energy_efficiency = request.data['ac_energy_efficiency']
                )
                ac.save()
            variation = Variation.objects.create(
                product = product,
                color = request.data['color'],
                quantity = request.data['quantity']
            )
            variation.save()
            return Response({
                'error' : False,
                'msg' : 'Product Added Successfully'
            })
        return Response({
            'error' : True,
            'msg' : 'Cannot Add Product',
        })
class ProductView(APIView):

    def get(self, request):
        allProducts = self.get_allproducts()
        latest = self.get_latest()
        discounted = self.get_discounted()
        if allProducts is not None or latest is not None or discounted is not None:
            return Response({
                'allproducts' : allProducts,
                'latest' : latest,
                'special' : discounted,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data'
        })

    def get_allproducts(self):
        product = Product.objects.all()
        if product is not None:
            serializer = ProductSerializer(product, many=True)
            return serializer.data
        return []
  
    def get_latest(self):
        latest_products = Product.objects.all().order_by('created_at')[:5]
        if latest_products is not None:
            serializer = ProductSerializer(latest_products, many=True)
            return serializer.data
        return []

    def get_discounted(self):
        discounted_products = Product.objects.all().order_by('-disc_price')[:5]
        if discounted_products is not None:
            serializer = ProductSerializer(discounted_products, many=True)
            return serializer.data
        return []

class ProductDetailsView(APIView):

    def get(self, request, id):
        product = Product.objects.get(p_id=id)
        if product is not None:
            serializer = ProductSerializer(product)
            return Response({
                'data' : serializer.data,
                'error' : False,
            })
        return Response({
            'error' : True,
            'msg' : 'Product No Found'
        })
            

class WishlistView(APIView):


    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            if not UserDetails.objects.get(id = user_id):
                return Response({'error' : True, 'data' : serializer.data, 'msg' : 'Related user or Product not Found. Login to Your Account'}, status.HTTP_204_NO_CONTENT)
            product_instance = Product.objects.get(p_id = product_id)
            product_serializer = ProductSerializer(product_instance)
            user_instance = UserDetails.objects.get(id=user_id)
            wishlist, created = Wishlist.objects.get_or_create(product = product_instance , user_data = user_instance)
            if created:
                return Response({'data' : product_serializer.data, 'error' : False, 'msg' : 'Product Added in Wishlist'}, status.HTTP_202_ACCEPTED)
            else:
                return Response({'data' : product_serializer.data, 'error' : True, 'msg' : 'Product Already in Wishlist'}, status.HTTP_207_MULTI_STATUS)
            
        return Response({'data' : serializer.data, 'error' : True, 'msg' : 'Cannot Add Products To Wishlist'}, status.HTTP_204_NO_CONTENT)
    
    def get(self,request,id):
        wishlist = Wishlist.objects.filter(user_data = id)
        if wishlist is not None:
            serializer = ShowWishlistSerializer(wishlist, many=True)
            for products in wishlist:
                p = products.product
                print(p.category.cat_name)
                if p.category.cat_name == 'Phones':
                    phone = MobilePhones.objects.get(product=p)
                    phone_serializer = MobileSerializer(phone)
                    print(phone_serializer.data)
                elif p.category.cat_name == 'LCD':
                    lcd = LCD.objects.get(product=p)
                    lcd_serializer = LCDSerializer(lcd)
                    print(lcd_serializer.data)
                elif p.category.cat_name == 'Laptops':
                    laptops = Laptops.objects.get(product=p)
                    laptop_serializer = LaptopSerializer(laptops)
                    print(laptop_serializer.data)
                elif p.category.cat_name == 'AC':
                    ac = AC.objects.get(product=p)
                    ac_serializer = ACSerializer(ac)
                    print(ac_serializer.data)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'error' : True,
            'msg' : 'There is no Product to Show'
        })

class DeleteWishlistView(APIView):
    def post(self, request):
        serializer = WishlistSerializer(data= request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            wishlist = Wishlist.objects.get(product_id = product_id, user_data_id = user_id)
            wishlist.delete()
            return Response({
                'error' : False,
                'msg' : 'Product Deleted'
            })
        return Response({
            'error': True,
            'msg' : serializer.errors
        }) 

             
class AddCompareView(APIView):
    
    # def post(self, request):
    #     serializer = AddCompareSerializer(data=request.data)
    #     if serializer.is_valid():
    #         product_id = request.data['product_id']
    #         user_id = request.data['user_id']
    #         if not Product.objects.filter(p_id = product_id) or not UserDetails.objects.filter(id = user_id):
    #             return Response({'msg' : 'Related user or Product not Found', 'error' : True})
    #         existing = CompareProducts.objects.filter(user_data = user_id).first()
    #         print(CompareProducts.objects.filter(user_data = user_id).first())
    #         count = CompareProducts.objects.filter(user_data = user_id).count()
    #         product_instance1 = Product.objects.get(p_id = product_id)
    #         if count >= 2 :
    #             return Response({'msg' : 'Already Two Products In Comparing', 'error' : True})
    #         product_val = '' 
    #         if existing is not None:
    #             product_val = existing.product.p_id
    #             product_instance = Product.objects.get(p_id = product_val)
    #             cat_id = product_instance.category
    #             cat_id1 = product_instance1.category
    #             if cat_id != cat_id1:
    #                 return Response({'msg' : 'Products Category Must Be Same', 'error' : True})
    #         product_serializer = ProductSerializer(product_instance1)
    #         user_instance = UserDetails.objects.get(id=user_id)
    #         compare, created = CompareProducts.objects.get_or_create(product = product_instance1 , user_data = user_instance)
    #         if created:
                
    #             return Response({'data' : product_serializer.data, 'error' : False, 'msg' : 'Product Added in Compare'}, status.HTTP_202_ACCEPTED)
    #         elif compare:
    #             return Response({'data' : product_serializer.data, 'error' : True, 'msg' : 'Product Already in Compare'}, status.HTTP_207_MULTI_STATUS)
            
    #     return Response({ 'data' : serializer.errors ,'error' : True, 'msg' : 'Cannot Add Products To Compare'}, status.HTTP_204_NO_CONTENT)
    
    def post(self, request):
        # Assuming you receive p_id and p_id1 in request.data
        p_id = request.data.get('p_id')
        p_id1 = request.data.get('p_id1')

        if p_id is None or p_id1 is None:
            return Response({
                'error': True,
                'msg': 'Minimum two products required'
            }, status=status.HTTP_200_OK)

        # Check if the products exist in the Product model
        products = Product.objects.filter(p_id__in=[p_id, p_id1])

        if not products:
            return Response({
                'error': True,
                'msg': 'The specified products do not exist'
            }, status=status.HTTP_200_OK)

        data_list = []
        data_cat = []

        for product in products:
            cat = product.category.cat_name

            if cat == 'LCD':
                lcd = LCD.objects.get(product=product)
                lcd_serializer = LCDSerializer(lcd)
                data_list.append(lcd_serializer.data)
                if 'LCD' not in data_cat:
                    data_cat.append('LCD')
            elif cat == 'AC':
                ac = AC.objects.get(product=product)
                ac_serializer = ACSerializer(ac)
                data_list.append(ac_serializer.data)
                if 'AC' not in data_cat:
                    data_cat.append('AC')
            elif cat == 'Laptops':
                laptops = Laptops.objects.get(product=product)
                laptop_serializer = LaptopSerializer(laptops)
                data_list.append(laptop_serializer.data)
                if 'Laptops' not in data_cat:
                    data_cat.append('Laptops')
            elif cat == 'Phones':
                phones = MobilePhones.objects.get(product=product)
                phone_serializer = MobileSerializer(phones)
                data_list.append(phone_serializer.data)
                if 'Phones' not in data_cat:
                    data_cat.append('Phones')

        serializer = ProductSerializer(products, many=True)

        data = {
            'details': data_list,
            'product': serializer.data,
            'category': data_cat
        }

        return Response({
            'data': data,
            'msg': 'Description retrieved successfully',
            'error': False
        }, status=status.HTTP_200_OK)

    def get(self,request, id):
        compare = CompareProducts.objects.filter(user_data = id)
        # count = CompareProducts.objects.filter(user_data = id).count()
        cat = 'Null'
        p_id1 = 0
        data_list = [] 
        data_cat = []
        # if compare is not None:
        #     serializer = ShowCompareSerializer(compare, many=True)
        #     return Response({
        #         'data' : serializer.data,
        #         'error' : False
        #     })
        # return Response({
        #     'error' : True,
        #     'msg' : 'There is no Product to Show'
        # })
        if compare is not None:
                # print(count)
            serializer = ShowCompareSerializer(compare, many=True)  
            # if count == 2:
            for products in compare:
                cat = products.product.category.cat_name
                p_id = products.product.p_id
                
                if cat == 'LCD':
                    lcd = LCD.objects.get(product_id=p_id)
                    lcdserializer = LCDSerializer(lcd)
                    data_list.append(lcdserializer.data)
                    if len(data_cat) == 0:
                        data_cat.append(cat)
                elif cat == 'AC':
                    ac = AC.objects.get(product_id=p_id)
                    acserializer = ACSerializer(ac)
                    data_list.append(acserializer.data)
                    if len(data_cat) == 0:
                        data_cat.append(cat)
                elif cat == 'Laptops':
                    laptops = Laptops.objects.get(product_id=p_id)
                    laptopSerializer = LaptopSerializer(laptops)
                    data_list.append(laptopSerializer.data)
                    if len(data_cat) == 0:
                        data_cat.append(cat)
                elif cat == 'Phones':
                    phones = MobilePhones.objects.get(product_id=p_id)
                    phoneserializer = MobileSerializer(phones)
                    data_list.append(phoneserializer.data)
                    if len(data_cat) == 0:
                        data_cat.append(cat)
                data = {
                    'details' : data_list,
                    'product' : serializer.data,
                    'category' : data_cat
                }
                return Response({
                    'data': data,
                    'msg': 'Descripted Successfully',
                    'error': False
                }, status.HTTP_202_ACCEPTED) 
        return Response({
            'error' : True,
            'msg' : 'There is no Details to Show'
        }, status.HTTP_200_OK)             
                
class DeleteCompareView(APIView):
    def post(self, request):
        serializer = AddCompareSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            compare = CompareProducts.objects.get(product_id = product_id, user_data_id = user_id)
            compare.delete()
            return Response({
                'error' : False,
                'msg' : 'Product Deleted'
            })
        return Response({
            'error': True,
            'msg' : serializer.errors
        })

class AddCategoryView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        cat_image = request.data['cat_image']
        if serializer.is_valid():
            cat_name = request.data['cat_name']
            category = Category.objects.create(
                cat_name = cat_name,
                cat_image = cat_image
            )
            return Response({
                'error' : False,
                'data' : serializer.data,
                'msg' : 'Category Added'
            })
        return Response({
            'error' : True,
            'data' : serializer.errors,
            'msg' : 'Cannot Add Category'
        })
    def get(self, request):
        category = Category.objects.all()
        if category is not None:
            serializer = CategorySerializer(category, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False,
            })
        return Response({
            'error' : True,
            'msg' : 'category No Found'
        })
    
class SellerProductDetailsView(APIView):

    def get(self, request, id):
        product = Product.objects.filter(user_data_id=id)
        if product is not None:
            serializer = ProductSerializer(product,many=True)
            return Response({
                'data' : serializer.data,
                'error' : False,
            })
        return Response({
            'error' : True,
            'msg' : 'Product No Found'
        })
            

class FeedBackView(APIView):

    def post(self, request):
        print(request.data)
        serializer = FeedBackSerializer(data=request.data)
        if serializer.is_valid():
            product = request.data['product']
            productData = Product.objects.get(p_id = product)
            user = request.data['user']
            userData = UserDetails.objects.get(id = user)
            stars = request.data['stars']
            if userData is not None:
                check = Feedback.objects.filter(user=userData, product = productData)
                if check:
                    return Response({
                        'msg' : 'Product Already Rated',
                        'error' : True
                    })
            feedback = Feedback.objects.create(
                stars = stars,
                product = productData,
                user = userData
            )
            feedback.save()
            feed = Feedback.objects.filter(product=product)
            count = feed.count()
            total = 0
            for rate in feed:
                total += rate.stars
            avg = total / count
            productData.rating = avg
            productData.save()
            return Response({
                'msg' : 'Thanks for the Feedback',
                'error' : False
            })
        return Response({
                'msg' : 'Please Try Again',
                'error' : True
            })
    
class RecommendationView(APIView):
    def get(self, request, user_id):
        # Fetch all feedback data
        feedback_data = Feedback.objects.all()

        # If there is no feedback data, recommend a random product
        if not feedback_data.exists():
            random_product = Product.objects.order_by('?').first()
            reSerializer = ProductSerializer(random_product)
            return Response({'recommendation': reSerializer.data}, status=status.HTTP_200_OK)

        feedback_df = pd.DataFrame(list(feedback_data.values()))
        
        # Create a user-item matrix (pivot table)
        user_item_matrix = feedback_df.pivot_table(index='user_id', columns='product_id', values='stars')

        # Fill missing values with 0
        user_item_matrix = user_item_matrix.fillna(0)

        # Calculate cosine similarity between products
        cosine_sim = cosine_similarity(user_item_matrix.T)

        # Create a DataFrame to store product similarity scores
        product_similarity_df = pd.DataFrame(cosine_sim, index=user_item_matrix.columns, columns=user_item_matrix.columns)

        # Get the product IDs rated by the user
        user_rated_products = feedback_df[feedback_df['user_id'] == user_id]['product_id']

        # Initialize a dictionary to store recommendations
        recommendations = {}

        # Initialize a list to store recommended products
        recommended_products = []

        # Create a dictionary to map product IDs to their index in the product_similarity_df
        product_id_to_index = {product_id: i for i, product_id in enumerate(product_similarity_df.index)}
        
        # Iterate through the products rated by the user
        for product_id in user_rated_products:
            
            try:
                # Get the category of the user's rated product
                user_rated_product = Product.objects.get(p_id=product_id)
                

                # Filter products by category
                similar_products = product_similarity_df.loc[product_id].sort_values(ascending=False)

                

                # Exclude products already rated by the user
                similar_products = similar_products[~similar_products.index.isin(user_rated_products)]
                

                # Check if there are similar products available
                if not similar_products.empty:
                    top_similar_product_id = similar_products.index[0]
                    recommendations[product_id] = top_similar_product_id
                    recommended_products.append(top_similar_product_id)
                else:
                    # If there are no similar products, recommend a random product not already rated
                    random_product = Product.objects.exclude(p_id=product_id).exclude(p_id__in=recommended_products).order_by('?').first()
                    recommendations[product_id] = random_product.p_id
                    recommended_products.append(random_product.p_id)
            except Product.DoesNotExist:
                # Handle the case where the product doesn't exist
                recommendations[product_id] = None
            if recommended_products:
                for product_id in recommended_products:
                    try:
                        product = Product.objects.get(p_id=product_id)
                        # Now, 'product' contains the Product object for the recommended product
                        # You can apply your logic to 'product' here
                        serializer = ProductSerializer(product)
                        # Rest of your logic here
                        return Response({'data' : serializer.data}, status=status.HTTP_200_OK)
                    except Product.DoesNotExist:
                        # Handle the case where the product doesn't exist
                        return Response({'data' : serializer.data}, status=status.HTTP_200_OK)


                return Response({'data' : serializer.data}, status=status.HTTP_200_OK)

class DeleteProductView(APIView):

    def post(self, request):
        serializer = DProductSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data['p_id'])
            product = Product.objects.get(p_id=request.data['p_id'])
            product.delete()
            return Response({'error': False, 'msg': 'Product deleted successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': True, 'msg': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class UserCountView(APIView):
    def get(self, request,id):
        product = Product.objects.get(p_id=id)
        count = Feedback.objects.filter(product=product).count()
        return Response({'error': False, 'msg': 'Reviews', 'data' : count}, status=status.HTTP_200_OK)


    
