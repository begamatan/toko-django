from dataclasses import fields
from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Order, OrderDetail

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = (
            "id",
            "product",
            "price",
            "quantity"
        )

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total",
            "created_at",
            "order_details",
        )

    def create(self, validated_data):
        order_details = validated_data.pop('order_details')
        order = Order.objects.create(**validated_data)
        for order_detail in order_details:
            OrderDetail.objects.create(order=order, **order_detail)

        return order
