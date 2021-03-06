from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stocks', 'selling_price',)
    list_filter = ('name', 'stocks',)
    search_fields = ['name', 'stocks']
    prepopulated_fields = {'slug': ('name',), }

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)