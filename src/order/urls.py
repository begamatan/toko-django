from django.urls import path

from . import views

app_name='order'
urlpatterns = [
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('list/', views.OrderList.as_view(), name='list'),
    path('midtrans/notification/', views.MidtransNotification.as_view(), name='midtrans_notification')
]
