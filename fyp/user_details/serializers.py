from rest_framework import serializers
from .models import UserDetails
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class AdminDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'phone_no']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'phone_no', 'address']
        
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'password', 'phone_no']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if not username or not password:
            raise serializers.ValidationError("Both Fields are required")
        return data
    
class SellerSignupSerializer(serializers.Serializer):
    username = serializers.CharField()     
    password = serializers.CharField(write_only=True)
    email = serializers.CharField() 
    phone_no = serializers.CharField() 

class SellerLoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if not username or not password:
            raise serializers.ValidationError("Both Fields are required")
        return data
    
class AdminSignupSerializer(serializers.Serializer):
    username = serializers.CharField()     
    password = serializers.CharField(write_only=True)
    email = serializers.CharField() 
    phone_no = serializers.CharField() 

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if not username or not password:
            raise serializers.ValidationError("Both Fields are required")
        return data
    
class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['email']

class CodeSerializer(serializers.Serializer):
    code = serializers.CharField()     

class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserDetails
        fields = ['password']
    
class DCustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField()

