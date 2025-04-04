from django import forms
from .models import Product
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название продукта'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание продукта'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Введите цену продукта'
            elif field_name == 'status':
                field.widget.attrs['class'] = 'form-select'

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 
                          'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        
        for word in forbidden_words:
            if re.search(r'\b' + re.escape(word) + r'\b', name.lower()):
                raise forms.ValidationError(
                    f'Название не должно содержать запрещенное слово "{word}"'
                )
        
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 
                          'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        
        for word in forbidden_words:
            if re.search(r'\b' + re.escape(word) + r'\b', description.lower()):
                raise forms.ValidationError(
                    f'Описание не должно содержать запрещенное слово "{word}"'
                )
        
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if not image:
            return image
        
        if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError('Разрешены только файлы формата JPEG или PNG')
        
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Размер файла не должен превышать 5 МБ')
        
        return image

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваше сообщение'}))