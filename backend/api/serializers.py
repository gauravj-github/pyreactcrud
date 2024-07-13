from django.db.models import fields
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class Userserializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
     
    class Meta:
        model = User
        fildes =['id','_id','username','name','isAdmin']

    def get(self , obj):
         return obj.id
        
    def get_isAdmin(self , obj):
        return obj.is_staff
        
    def get_name(self , obj):
        name = obj.first_name
        if name == "":
            name = obj.email 
            return name
            
class UserserializerWithToken(Userserializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','_id','username','name','isAdmin','token']

        def get_token(self,obj):
            token = RefreshToken.for_user(obj)
            return str(token.access_token)

class Reviewserializer(serializers.ModelSerializer):
    class Meta:
        models = Review
        fields = '__all__'

class Productserializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        models = Product
        fields = '__all__'

    def get_review(self , obj):
        reviews = obj.reviews_set.all()
        serializer = Reviewserializer(reviews,many=True)
        return serializer.data

class ShippingAddressserializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields ='__all__'

class OrderItemserializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class Orderserializer(serializers.ModelSerializer):     
    orderitems = serializers.SerializerMetaclass(read_only=True)
    shippingaddress = serializers.SerializerMetaclass(read_only=True)
    user = serializers.SerializerMetaclass(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        
    def get_orderitems(self , obj):
        items = obj.orderitems_set.all()
        serializer = OrderItemserializer(items,many=True)
        return serializer.data

    def get_shippingAddress(self,obj):
        try:
            address = ShippingAddressserializer(obj.shippingaddress,many=False).data
        except:
            address = False
        return address

    def get_User(self,obj):
        items = obj.user
        serializer = Userserializer(items,many=False)
        return serializer.data
