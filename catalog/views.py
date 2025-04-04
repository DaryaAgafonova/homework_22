from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from .models import Product, Category, Contact
from .forms import ProductForm, ContactForm

def home(request):
    products = Product.objects.filter(status='published').order_by('-created_at')[:8]
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    contacts = Contact.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('contacts')
    else:
        form = ContactForm()
    
    return render(request, 'catalog/contacts.html', {'contacts': contacts, 'form': form})

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and (
            self.request.user.is_staff or 
            self.request.user.groups.filter(name='Модератор продуктов').exists()
        ):
            return queryset
        return queryset.filter(status='published')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and (
            self.request.user.is_staff or 
            self.request.user.groups.filter(name='Модератор продуктов').exists() or
            queryset.filter(owner=self.request.user).exists()
        ):
            return queryset
        return queryset.filter(status='published')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')
    login_url = '/users/login/'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')
    login_url = '/users/login/'
    
    def test_func(self):
        product = self.get_object()
        return (product.owner == self.request.user or 
                self.request.user.has_perm('catalog.change_product'))
    
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этого продукта.')
        return redirect('product_detail', pk=self.get_object().pk)
    
    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    login_url = '/users/login/'
    
    def test_func(self):
        product = self.get_object()
        return (product.owner == self.request.user or 
                self.request.user.groups.filter(name='Модератор продуктов').exists() or
                self.request.user.has_perm('catalog.delete_product'))
    
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого продукта.')
        return redirect('product_detail', pk=self.get_object().pk)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)

@login_required(login_url='/users/login/')
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'draft'
    product.save()
    messages.success(request, f'Продукт "{product.name}" снят с публикации.')
    return redirect('product_detail', pk=pk)

@login_required(login_url='/users/login/')
def publish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        messages.error(request, 'У вас нет прав для публикации этого продукта.')
        return redirect('product_detail', pk=pk)
    
    product.status = 'published'
    product.save()
    messages.success(request, f'Продукт "{product.name}" опубликован.')
    return redirect('product_detail', pk=pk)

@login_required(login_url='/users/login/')
def change_product_status(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.status == 'published' and not request.user.has_perm('catalog.can_unpublish_product'):
        messages.error(request, 'У вас нет прав для снятия продукта с публикации.')
        return redirect('product_detail', pk=pk)
    
    if product.owner != request.user and not request.user.has_perm('catalog.change_product'):
        messages.error(request, 'У вас нет прав для изменения статуса этого продукта.')
        return redirect('product_detail', pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [status[0] for status in Product.STATUS_CHOICES]:
            product.status = new_status
            product.save()
            messages.success(request, f'Статус продукта "{product.name}" изменен на "{dict(Product.STATUS_CHOICES)[new_status]}".')
        
        return redirect('product_detail', pk=pk)
    
    return render(request, 'catalog/change_status.html', {'product': product})