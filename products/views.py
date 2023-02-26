from django.shortcuts import render
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.shortcuts import render,get_object_or_404, redirect
from .forms import *    
from users.utils import code_generator
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponse
from rest_framework import serializers
import qrcode
# from tkinter import *
# from tkinter import messagebox



class ProductDetail(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        products = Product.objects.filter(product_id = pk)
        # if not products :
        #     getLocation(request)
        
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

    