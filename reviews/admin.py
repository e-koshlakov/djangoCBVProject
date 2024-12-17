from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'sign_of_review', 'author', 'dog']
    list_filter = ['author', 'dog']
    ordering = ['created']
