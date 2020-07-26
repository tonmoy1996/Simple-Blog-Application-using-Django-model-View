from django.contrib import admin
from .models import *
from django import forms

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields= ['author','title', 'text', 'created_date', 'publish_date']
    search_fields = ['title','text']
    list_display=['title', 'text', 'created_date', 'publish_date']
    list_filter=['title','created_date','publish_date']
    list_per_page = 2

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
