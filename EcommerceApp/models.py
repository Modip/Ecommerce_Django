from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class CustomUser(AbstractUser):
    user_type_choices = ((1, "Admin"), (2, "Staff"), (3, "Merchant"), (4, "Customer"))
    user_type = models.CharField(max_length=255, choices=user_type_choices, default=1)


class AdminUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class StaffUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class MerchantUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    gst_detail = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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
    url_slug = models.CharField(max_length=255)
    subCategory_id = models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_discount_price = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description = models.TextField()
    added_by_merchant = models.ForeignKey(MerchantUser, on_delete=models.CASCADE)
    in_stock_total = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

class ProductMedia(models.Model):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    media_type_choice = ((1, "image"), (2, "video"))
    media_type = models.CharField(max_length=255)
    media_type_content = models.FileField()
    is_active = models.IntegerField(default=1)

class ProductTransaction(models.Model):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    transaction_type_choices = ((1, "BUY"), (2, "SELL"))
    transaction_product_count = models.IntegerField(default=1)
    transaction_type = models.FileField(choices=transaction_type_choices, max_length=255)
    transaction_description = models.FileField(max_length=255)

class ProductDetails(models.Model):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    title_details = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductAbout(models.Model):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductTags(models.Model):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductQuestions(models.Model):
    product_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    is_active = models.IntegerField(default=1)


class ProductReviews(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    review_image = models.FileField()
    rating = models.CharField(max_length=5)
    review = models.TextField(max_length=255)
    is_active = models.IntegerField(default=1)


class ProductReviewVoting(models.Model):
    product_review_id = models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user_id_voting = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    rating = models.CharField(default="5", max_length=255)
    review = models.TextField(max_length=255)
    is_active = models.IntegerField(default=1)

class ProductVarient(models.Model):
    title = models.TextField(max_length=255)

class ProductVarientItems(models.Model):
    product_varient_id = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.TextField(max_length=255)


class CustomerOrders(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    purchase_price = models.TextField(max_length=255)
    coupon_code = models.TextField(max_length=255)
    discount_atm = models.TextField(max_length=255)
    product_status = models.TextField(max_length=255)

class OrderDeliveryStatus(models.Model):
    order_id = models.ForeignKey(CustomerOrders, on_delete=models.CASCADE)
    status = models.TextField(max_length=255)
    status_message = models.TextField(max_length=255)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type == 2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type == 3:
            MerchantUser.objects.create(auth_user_id=instance, compagny_name="", gst_detail="",address="")
        if instance.user_type == 4:
            CustomUser.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()
    if instance.user_type == 2:
        instance.staffuser.save()
    if instance.user_type == 3:
        instance.merchantuser.save()
    if instance.user_type == 4:
        instance.customuser.save()


