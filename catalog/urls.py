from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/publish/', views.publish_product, name='publish_product'),
    path('product/<int:pk>/unpublish/', views.unpublish_product, name='unpublish_product'),
    path('product/<int:pk>/change-status/', views.change_product_status, name='change_product_status'),
]