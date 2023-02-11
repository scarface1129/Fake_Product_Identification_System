from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save


User = settings.AUTH_USER_MODEL



class Product(models.Model):
    product_name    =   models.CharField(max_length=100,blank=False, null=False)
    product_manufacturer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id          = models.CharField(max_length=50,blank=False, null=False)
    product_image       = models.ImageField(blank=False, null=False)
    production_date     = models.DateField(auto_now_add=False)
    expiry_date         = models.DateField(auto_now_add=False)
    product_description = models.TextField(max_length=500)
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


class Barcodes(models.Model):
    barcode       = models.ImageField(blank=False, null=False)
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)