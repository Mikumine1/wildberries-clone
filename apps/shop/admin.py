from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Likes)
admin.site.register(Comment)
admin.site.register(ProductImage)
admin.site.register(Company)
admin.site.register(Banner)
admin.site.register(ShippingAddress)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}