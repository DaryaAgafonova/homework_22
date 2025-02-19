from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Contact

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(f"Product: {product.name}, Price: {product.price}")
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение: {name}, номер: {phone}. Оставил сообщение: {message}!')
        return JsonResponse({'status': 'success'})
    contact_info = Contact.objects.first()
    return render(request, 'catalog/contacts.html', {'contact_info': contact_info})