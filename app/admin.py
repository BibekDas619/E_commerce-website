from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app.models import Product,Contact,Order,CustomUser
# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CustomUser)