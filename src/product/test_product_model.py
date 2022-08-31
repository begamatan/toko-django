import calendar
from datetime import datetime
from io import BytesIO
from PIL import Image

from django.conf import settings
from django.core.files import File
from django.test import TestCase


from .models import Category, Product

# Create your tests here.
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

class ProductModelTests(TestCase):
    base_url = settings.APP_URL

    def test_get_absolute_url(self):
        category = create_category('Manga', 'manga', 'manga')
        product = create_product(
            category,
            'One Piece',
            'one piece',
            'one-piece',
            10000,
            get_image()
        )

        self.assertEqual(product.get_absolute_url(), f"/manga/one-piece/")

        product.image.delete(save=True)

    def test_get_image(self):
        category = create_category('Manga', 'manga', 'manga')
        product = create_product(
            category,
            'One Piece',
            'one piece',
            'one-piece',
            10000,
        )

        self.assertEqual(product.get_image(), '')

        img_name = get_file_name()
        product.image = get_image(img_name)
        product.save()

        self.assertEqual(product.get_image(), self.base_url + '/media/uploads/' + img_name)
        product.image.delete(save=True)

    def test_get_thumbnail(self):
        category = create_category('Manga', 'manga', 'manga')
        product = create_product(
            category,
            'One Piece',
            'one piece',
            'one-piece',
            10000,
        )

        self.assertEqual(product.get_thumbnail(), '')

        img_name = get_file_name()
        product.image = get_image(img_name)
        product.save()

        self.assertEqual(product.get_thumbnail(), self.base_url + '/media/thumbnail_uploads/' + img_name)

        # clean image
        product.image.delete(save=True)
        product.thumbnail.delete(save=True)

    def test_make_thumbnail(self):
        category = create_category('Manga', 'manga', 'manga')
        product = create_product(
            category,
            'One Piece',
            'one piece',
            'one-piece',
            10000,
        )

        img_name = get_file_name()
        product.image = get_image(img_name)
        product.save()

        thumbnail = product.make_thumbnail(product.image)
        self.assertEqual(thumbnail.name, img_name)

        # clean image
        product.image.delete(save=True)
        product.thumbnail.delete(save=True)