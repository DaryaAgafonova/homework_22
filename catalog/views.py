from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Contact
from .forms import ProductForm

def home(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 6)  # Показывать 6 товаров на странице
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение: {name}, номер: {phone}. Оставил сообщение: {message}!')
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('contacts')
    
    contact_info = Contact.objects.first()
    return render(request, 'catalog/contacts.html', {'contact_info': contact_info})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})