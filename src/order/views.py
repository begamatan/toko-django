from midtransclient import Snap
from rest_framework import generics, permissions
from rest_framework.response import Response

from django.conf import settings

from order.models import Order
from order.serializers import OrderSerializer

# Create your views here.
class Checkout(generics.CreateAPIView):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_midtrans_url(self, order):
        snap = Snap(server_key=settings.MIDTRANS_SERVER_KEY)

        param = {
            "transaction_details": {
                "order_id": order['id'],
                "gross_amount": order['total']
            }
        }

        transaction = snap.create_transaction(param)
        return transaction

    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        midtrans = self.get_midtrans_url(response.data)
        return Response({
            'status': response.status_code,
            'data': {
                'order': response.data,
                'url': midtrans['redirect_url'],
            }
        })

class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)