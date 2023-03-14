from django.shortcuts import render
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.conf import settings
from django.shortcuts import render,get_object_or_404, redirect
from .forms import *    
from users.utils import code_generator
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponse
from rest_framework import serializers
import pandas as pd
import qrcode
import pandas as pd
# from tkinter import *
# from tkinter import messagebox



class ProductDetail(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        products = Product.objects.filter(product_id = pk)
        # create_product_from_nafdac(self)
        context = {'products':products}
        return render(request, 'products/product_detail.html', context )

class CreateProduct(LoginRequiredMixin,CreateView):
    template_name = 'products/create_products.html'
    form_class = ProductCreate
    login_url = '/login/'

    def form_valid(self, form):               
        obj = form.save(commit=False)
        obj.product_id = code_generator(15)
        product_id = obj.product_id
        scheme = 'https' if self.request.is_secure() else 'http'
        site = get_current_site(self.request)
        # print('%s://%s' % (scheme, site))
        obj.barcode = generateCode(obj.product_name,'%s://%s' % (scheme, site)+'/product/'+ product_id)
        obj.product_manufacturer = self.request.user
        return super(CreateProduct, self).form_valid(form)
    
class UpdateProduct(LoginRequiredMixin,UpdateView):
    template_name = 'products/update_products.html'
    form_class = ProductCreate
    login_url = '/login/'

    def get_context_data(self,*args, **kwargs):
        context = super(UpdateProduct, self).get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        Products = Product.objects.filter(product_id = slug)
        context['product'] = Products
        return context
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(product_id = slug)
    
def search(request, *args, **kwargs):
    if request.method == "POST":
        pk = request.POST['pk']
    return HttpResponseRedirect(reverse("products:product_detail", kwargs={"pk" : pk}))

def Fake(request):
    if request.method == "POST":
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        time = ''
        if longitude and latitude:
            Fproduct = FakeProduct.objects.create_fakeProduct(latitude,longitude,time)
        
    return HttpResponseRedirect(reverse("index"))
def generateCode(name,text):
    qr = qrcode.QRCode(version = 1,
            box_size = 10,
            border = 5)
    qr.add_data(text) 
    qr.make(fit = True) 
    img = qr.make_image()
    fileDirec = f'media/{name}'
    img.save(f'{fileDirec}.png') 
    return f'{name}.png'

def Map(request):
    lat_a = request.GET.get("lat", None)
    long_b = request.GET.get("long", None)
    id_ = request.GET.get("id", None)
    context = {
    "google_api_key": settings.GOOGLE_API_KEY,
    "lat_a": lat_a,
    "long_b": long_b,
    "id": id_,
    }
    return render(request, 'products/map.html', context )

class FakeProductList(LoginRequiredMixin,ListView):
     def get(self, request):	
        product = FakeProduct.objects.all().order_by('-id')
        context = {'object_list': product}
        return render(request, 'products/fake_list.html', context )
    
def updateFakeProduct(request):
    if request.method == "POST":
        id_ = request.POST['id_']
        product = FakeProduct.objects.get(id=id_)
        product.detained = True
        product.save()
    return HttpResponseRedirect(reverse("products:fake_list"))
    
    
def create_product_from_nafdac(self):
    df = pd.read_excel(r'NAFDAC.xlsx')
    for i, row in df.iterrows():
        # print(row)
        product_name = row['Product Name']
        product_manufacturer = row['Manufacturer']
        product_id    = row['Registration No.']      
        production_date    = row['Date Approved'] 
        product_type     = row['Product Type']
        expiry_date         = row['Expiry Date']
        product_description  = row['Active Ingredent']
        
        if product_name and product_id :
            product = Product.objects.filter(product_id = product_id)
            if product.exists():
                product = product
            else:
                scheme = 'https' if self.request.is_secure() else 'http'
                site = get_current_site(self.request)
                barcode = generateCode(product_id,'%s://%s' % (scheme, site)+'/product/'+ product_id)
                new_product = Product.objects.create(
                product_name = product_name,
                product_manufacturer = product_manufacturer,
                product_id    = product_id,
                production_date    = production_date,
                product_type     = product_type,
                expiry_date         = expiry_date,
                product_description  = product_description,
                barcode            = barcode
            )
                new_product.save()
        else:
            print('***')