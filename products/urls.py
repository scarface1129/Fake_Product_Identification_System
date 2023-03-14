from django.urls import path
from .views import *



app_name = 'products'

urlpatterns = [
    path('update/<slug>/', UpdateProduct.as_view(), name=('product_update')),
    path('search/', search, name=('search')),
    # path('getlocation/', getLocation, name=('location')),
    path('create/', CreateProduct.as_view(), name=('product_create')),
    path('fake/', Fake, name=('fake')),
    path('map', Map, name=('map')),
    path('update_fake', updateFakeProduct, name=('update_fake')),
    path('fake_products/', FakeProductList.as_view(), name=('fake_list')),
    path('<pk>/', ProductDetail.as_view(), name=('product_detail')),
    
]