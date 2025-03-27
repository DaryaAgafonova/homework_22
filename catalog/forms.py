from django import forms
from .models import Product
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
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