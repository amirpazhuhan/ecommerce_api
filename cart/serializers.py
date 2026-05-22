from rest_framework import serializers

from .models import Cart, Item, Product

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields= ['id', 'item', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = ItemSerializer(many=True, read_only=True)

    def get_total_price(self,obj):
        return obj.get_total_price()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']



class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        # This is custom validation!
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("This product does not exist.")
        return value
