from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return self.title
