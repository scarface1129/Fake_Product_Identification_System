from django import forms
from .models import *
# from profiles.tasks import sleepy

from django.contrib.auth import get_user_model

class ProductCreate(forms.ModelForm):
    class Meta:
        model = Product 
        fields = [
            
            'product_name',
            # 'product_manufacturer',
            'product_image',
			'production_date',
			'expiry_date',
            'product_description',
            
        ]

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcodes 
        fields = [             
            'barcode',
            'product',
			          
        ]

