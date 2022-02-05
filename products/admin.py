from django.contrib import admin
from products.models import ProductVariant,Product,ProductImage,Category,SubCategory
# Register your models here.

admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
