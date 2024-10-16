from django.contrib import admin

from dogs.models import Category, Dog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    ordering = ('pk', 'name')

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    ordering = ( 'name', )