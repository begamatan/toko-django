import calendar
from datetime import datetime
from io import BytesIO
from PIL import Image
from rest_framework.test import APITestCase

from django.conf import settings
from django.core.files import File
from django.urls import reverse

from .models import Category, Product

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

def get_image(img_name = ''):
    img = Image.open(str(settings.MEDIA_ROOT) + '/uploads/test_product.jpg')

    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=100)

    name = img_name if img_name else get_file_name()
    image = File(img_io, name=name)
    return image

def get_file_name():
    date = datetime.utcnow()
    return str(calendar.timegm(date.utctimetuple())) + '.jpg'

# Create your tests here.
class LatestProductsListTests(APITestCase):
    def test_get_latest_product_list(self):
        response = self.client.get(reverse('product:latest_products'))
        self.assertEqual(response.data, [])

        category = create_category('Manga', 'manga', 'manga')
        product = create_product(category, 'One Piece', 'one piece', 'one-piece', 10000)

        response_with_product = self.client.get(reverse('product:latest_products'))
        
        self.assertEqual(response_with_product.data[0]['title'], 'One Piece')

    def test_get_product_detail(self):
        response = self.client.get(reverse('product:product_detail', args=('manga', 'one-piece')))
        self.assertEqual(response.status_code, 404)

        category = create_category('Manga', 'manga', 'manga')
        product = create_product(category, 'One Piece', 'one piece', 'one-piece', 10000)
        response = self.client.get(reverse('product:product_detail', args=('manga', 'one-piece')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'One Piece')

class CategoryDetailTests(APITestCase):
    def test_category_detail_not_found(self):
        response = self.client.get(reverse('product:category_detail', args=('manga',)))
        self.assertEqual(response.status_code, 404)

    def test_category_detail_with_no_product(self):
        category = create_category('Novel', 'novel', 'novel')
        response = self.client.get(reverse('product:category_detail', args=('novel',)))

        fields = {
            'title': 'Novel',
            'description': 'novel',
            'get_absolute_url': '/novel/' 
        }

        self.assertEqual(response.status_code, 200)
        for field in fields:
            self.assertEqual(response.data[field], fields[field])

        self.assertEqual(response.data['products'], [])

    def test_category_detail_with_no_product(self):
        category = create_category('Novel', 'novel', 'novel')
        product = create_product(category, 'Buku', 'deskripsi buku', 'buku', 10000)
        response = self.client.get(reverse('product:category_detail', args=('novel',)))

        fields = {
            'title': 'Novel',
            'description': 'novel',
            'get_absolute_url': '/novel/' 
        }

        product_fields = {
            'title': 'Buku',
            'description': 'deskripsi buku',
            'get_absolute_url': '/novel/buku/'
        }

        self.assertEqual(response.status_code, 200)
        for field in fields:
            self.assertEqual(response.data[field], fields[field])

        for product_field in product_fields:
            self.assertEqual(response.data['products'][0][product_field], product_fields[product_field])


class ProductListTests(APITestCase):
    def test_product_list_is_empty(self):
        response = self.client.get(reverse('product:product_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_product_list_is_not_empty(self):
        category = create_category('Novel', 'deskripsi', 'novel')
        product = create_product(category, 'Novel 1', 'deskripsi novel 1', 'novel-1', 10000)
        response = self.client.get(reverse('product:product_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], 'Novel 1')

        # test search
        product_2 = create_product(category, 'Buku', 'buku', 'buku', 10000)
        response = self.client.get(f"{reverse('product:product_list')}?search=novel")

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Novel 1')
        