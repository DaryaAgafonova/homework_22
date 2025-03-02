from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Добавить тестовые продукты'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category1 = Category.objects.create(name="Электроника", description="Электронные устройства")
        category2 = Category.objects.create(name="Книги", description="Печатные издания")

        Product.objects.create(
            name="Смартфон",
            description="Мощный смартфон с отличной камерой",
            category=category1,
            price=999.99
        )
        Product.objects.create(
            name="Ноутбук",
            description="Легкий и производительный ноутбук",
            category=category1,
            price=1499.99
        )
        Product.objects.create(
            name="Научная фантастика",
            description="Увлекательный роман о будущем",
            category=category2,
            price=19.99
        )

        self.stdout.write(self.style.SUCCESS('Successfully added test products'))
        