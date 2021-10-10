from django.urls import path
from .views import Home, single_product, category_items, About, Contact, SearchView

urlpatterns = [
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('product/<int:id>/', single_product, name='single_product'),
    path('product/<int:id>/<slug:slug>/',
         category_items, name='category_items'),
    path('search/', SearchView, name='SearchView'),


]
