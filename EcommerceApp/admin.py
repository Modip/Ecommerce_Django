from django.contrib import admin

# Register your models here.
from EcommerceApp.models import Categories, SubCategories

admin.site.register(Categories)
admin.site.register(SubCategories)
