from math import perm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions

from todo.models import Category, Post
from todo.serializers import CategorySerializer, PostSerializer
class IndexView(generic.ListView):
    template_name = 'todo/index.html'

    def get_queryset(self):
        return Category.objects.all()

class DetailView(generic.DetailView):
    model = Category
    template_name = 'todo/detail.html'

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'todo/post_detail.html'

def store_post(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    post = Post(category_id=category, title=request.POST['title'], body=request.POST['body'])
    post.save()

    return HttpResponseRedirect(reverse('todo:category_detail', args=(category_id,)))

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class =  CategorySerializer
    permission_classes = [permissions.IsAuthenticated]