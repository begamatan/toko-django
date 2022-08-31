from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from todo.models import Category, Post

# Create your tests here.

def create_category(title, description):
    return Category.objects.create(title=title, description=description)

def create_post(category, title, body):
    return Post.objects.create(title=title, body=body, category_id=category)

def create_user(username, email, password):
    return User.objects.create_superuser(username, email, password)

class CategoryIndexViewTests(TestCase):
    def test_no_category(self):
        response = self.client.get(reverse('todo:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['category_list'], [])

    def test_has_category(self):
        category = create_category('Kategori 1', 'deskripsi')
        response = self.client.get(reverse('todo:index'))
        
        self.assertQuerysetEqual(response.context['category_list'], [category])

class CategoryDetailViewTests(TestCase):
    def test_category_detail(self):
        category = create_category('Kategori 1', 'deskripsi')
        response = self.client.get(reverse('todo:category_detail', args=(category.id,)))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, category.description)
        self.assertContains(response, category)
        self.assertContains(response, 'Belum ada post')

    def test_category_detail_has_posts(self):
        category = create_category('Kategori 1', 'deskripsi')
        post = create_post(category, 'Post 1', 'body')

        response = self.client.get(reverse('todo:category_detail', args=(category.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Belum ada post')
        self.assertContains(response, post)

    def test_submit_post(self):
        category = create_category('Kategori 1', 'deskripsi')
        response = self.client.post(reverse('todo:store_post', args=(category.id,)), data={'title': 'Title', 'body': 'Body'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('todo:category_detail', args=(category.id,)))
        post = Post.objects.first()
        self.assertEqual(post.title, 'Title')

class ApiCategoryTests(TestCase):
    def test_get_category(self):
        user = create_user('root', 'admin@admin.com', 'root')
        category = create_category('Kategori', 'Desc')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/todo/api/category/')  

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, category)
