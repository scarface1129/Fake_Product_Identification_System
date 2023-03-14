from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save


User = settings.AUTH_USER_MODEL



class Product(models.Model):
    product_name        = models.CharField(max_length=100,blank=False, null=False)
    product_manufacturer= models.CharField(max_length=100,blank=False, null=False)
    product_id          = models.CharField(max_length=50,blank=False, null=False)
    product_image       = models.FileField(upload_to='media',blank=False, null=False)
    production_date     = models.CharField(max_length=12,blank=True, null=True)
    product_type        = models.CharField(max_length=100,blank=True, null=True)
    expiry_date         = models.CharField(max_length=12,blank=True, null=True)
    product_description = models.TextField(max_length=500)
    barcode             = models.FileField(upload_to='media',blank=False, null=False, default='image')
    slug                = models.SlugField(null=True, blank=True)
    
    

    def __str__(self):
        return self.product_name
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={'pk':self.product_id})
    # def __unicode__(self):
    #     return 
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	instance.slug = instance.product_id


pre_save.connect(rl_pre_save_receiver, sender=Product)

class FakeProductManager(models.Manager):
    def create_fakeProduct(self, latitude,longitude,time):
        fakeProduct = self.create(latitude = latitude,longitude = longitude,time = time)
        # do something with the book
        return fakeProduct
class FakeProduct(models.Model):
    longitude    = models.CharField(max_length=1000)
    latitude    = models.CharField(max_length=1000)
    time        = models.DateTimeField(auto_now_add=True)
    detained    = models.BooleanField(default=False)
    
    objects = FakeProductManager()