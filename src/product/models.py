from io import BytesIO
from PIL import Image

from django.conf import settings
from django.core.files import File
from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.slug}/"
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnail_uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}/"

    def get_image(self):
        if self.image:
            return settings.APP_URL + self.image.url

        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return settings.APP_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return settings.APP_URL + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumb_name = image.name.split('/')[-1]
        thumbnail = File(thumb_io, name=thumb_name)

        return thumbnail





