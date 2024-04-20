from django.contrib import admin
from product_mngmnt.models import *

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','detail']
    list_filter=['brand']

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display=['name','mobile_number']

@admin.register(UserDetail)
class VisitorAdmin(admin.ModelAdmin):
    list_display=['name','mobile_number','email']