from django.shortcuts import render
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from django.shortcuts import render,get_object_or_404, redirect
from .forms import *    
from users.utils import code_generator
from django.http import HttpResponseRedirect
from django.urls import reverse

import qrcode
from tkinter import *
from tkinter import messagebox



class ProductDetail(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        products = Product.objects.filter(product_id = pk)
        print(products)
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
        barcode = generateCode(obj.product_name,'http://192.168.1.102:8000/product/'+product_id)
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


def generateCode(name,text):
    qr = qrcode.QRCode(version = 1,
            box_size = 10,
            border = 5)
    qr.add_data(text) 
    qr.make(fit = True) 
    img = qr.make_image()
    fileDirec = f'media/qrcodes/{name}'
    img.save(f'{fileDirec}.png') 