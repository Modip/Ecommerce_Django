from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CostomUser(AbstractUser):
    user_type_choices = ((1, "Admin"), (2, "Staff"), (3, "Merchant"), (4, "Costomer"))
    user_type = models.CharField(max_length=255, choices=user_type_choices, default=1)


class AdminUser(models.Model):
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

class StaffUser(models.Model):
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantUser(models.Model):
    profile_pic = models.FileField(default="")
    company_name = models.CharField(max_length=255)
    gst_detail = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class CostomerUser(models.Model):
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    description = models.TextField()


class SubCategories(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    description = models.TextField()

class Products(models.Model):
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_discount_price = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description = models.TextField()
    is_active = models.IntegerField(default=1)

class ProductDetails(models.CharField):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    title_details = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductAbout(models.CharField):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductTags(models.CharField):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductQuestions(models.CharField):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    is_active = models.IntegerField(default=1)


class ProductReviews(models.CharField):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CostomerUser, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5)
    review = models.TextField(max_length=255)
    is_active = models.IntegerField(default=1)


class ProductReviewVoting(models.CharField):
    product_review_id = models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user_id_voting = models.ForeignKey(CostomerUser, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5)
    review = models.TextField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductVarient(models.CharField):
    title = models.TextField(max_length=255)

class ProductVarientItems(models.CharField):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.TextField(max_length=255)
