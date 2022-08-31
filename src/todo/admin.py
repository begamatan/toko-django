from django.contrib import admin

from .models import Category, Post

# Register your models here.

# class PostInline(admin.StackedInline):
#     model = Post
#     extra = 1

# class CategoryAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['title']}),
#         ('Description', {'fields': ['description']})
#     ]

#     inlines = [PostInline]

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category_name')

#     def category_name(self, obj):
#         return obj.category_id

#     category_name.short_description = 'Category'

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Post, PostAdmin)