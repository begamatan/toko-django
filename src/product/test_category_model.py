from django.test import TestCase

from .models import Category

# Create your tests here.
def create_category(title, description, slug):
    return Category.objects.create(title=title, description=description, slug=slug)

class CategoryModelTests(TestCase):
    def test_get_absolute_url(self):
        category = create_category('Kategori', 'Deskripsi', 'kategori')

        self.assertEqual(category.get_absolute_url(), f"/kategori/")