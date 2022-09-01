from unittest.mock import patch

from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.urls import reverse

from .views import Checkout
from product.models import Category, Product

# Create your tests here.

def create_user(username, email, password):
    return User.objects.create(username=username, email=email, password=password)

def create_category(title, description, slug):
    return Category.objects.create(title=title, description=description, slug=slug)

def create_product(category, title, description, slug, price, image = ''):
    return Product.objects.create(
        category=category,
        title=title,
        description=description,
        slug=slug,
        price=price,
        image=image
    )

class OrderViewTests(APITestCase):
    def mock_get_midtrans_url(self, order):
        return {
            'redirect_url': 'url'
        }

    @patch.object(Checkout, 'get_midtrans_url', mock_get_midtrans_url)
    def test_checkout_success(self):
        user = create_user('agung', 'agung@test.test', 'agung')
        category = create_category('Novel', 'deskripsi', 'novel')
        product = create_product(category, 'Novel 1', 'deskripsi novel 1', 'novel-1', 10000)

        data = {
            'total': 10000,
            'order_details': [{
                'product': product.id,
                'price': product.price,
                'quantity': 1
            }]
        }
        
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('order:checkout'), data=data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['url'], 'url')