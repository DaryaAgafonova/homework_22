from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Создание групп пользователей и назначение им прав'

    def handle(self, *args, **options):
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        
        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)
        
        # Получаем права для модели Product
        can_unpublish_product = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=product_content_type
        )
        can_delete_product = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type
        )
        
        # Назначаем права группе модераторов
        moderator_group.permissions.add(can_unpublish_product)
        moderator_group.permissions.add(can_delete_product)
        
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана'))
        
        # Дополнительное задание: создаем группу "Контент-менеджер"
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        
        try:
            # Получаем ContentType для модели BlogPost
            blog_content_type = ContentType.objects.get_for_model(BlogPost)
            
            # Получаем все права для модели BlogPost
            blog_permissions = Permission.objects.filter(content_type=blog_content_type)
            
            # Назначаем права группе контент-менеджеров
            for permission in blog_permissions:
                content_manager_group.permissions.add(permission)
            
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" успешно создана'))
        except:
            self.stdout.write(self.style.WARNING('Модель BlogPost не найдена. Группа "Контент-менеджер" создана без прав.'))

