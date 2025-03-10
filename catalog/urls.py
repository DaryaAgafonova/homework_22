from django.urls import path
from .views import HomeView, ProductDetailView, ProductCreateView, ContactsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-product/', ProductCreateView.as_view(), name='add_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]