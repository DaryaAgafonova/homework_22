from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение: {name}, номер: {phone}. Оставил сообщение: {message}!')
        return HttpResponse('Спасибо за ваше сообщение!')
    return render(request, 'catalog/contacts.html')