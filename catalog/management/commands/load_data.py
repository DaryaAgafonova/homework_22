from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Загрузить из fixtures'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write('Удаление существующих данных...')
            Product.objects.all().delete()
            Category.objects.all().delete()

            self.stdout.write('Загрузка категорий...')
            call_command('loaddata', 'categories')
            
            self.stdout.write('Загрузка продуктов...')
            call_command('loaddata', 'products')

            categories_count = Category.objects.count()
            products_count = Product.objects.count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно загружено {categories_count} категорий и {products_count} продуктов'
                )
            )

            for product in Product.objects.all():
                self.stdout.write(
                    f'Продукт: {product.name}, Категория: {product.category.name}'
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке данных: {str(e)}')
            )
            raise