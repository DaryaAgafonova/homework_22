from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import BlogPost  # Предполагаем, что у вас есть модель BlogPost

class Command(BaseCommand):
    help = 'Создание групп и назначение разрешений'

    def handle(self, *args, **options):
        # Получаем или создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует'))
        
        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)
        
        # Получаем разрешения для модели Product
        can_unpublish_product = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=product_content_type
        )
        can_delete_product = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type
        )
        
        # Назначаем разрешения группе "Модератор продуктов"
        moderator_group.permissions.add(can_unpublish_product)
        moderator_group.permissions.add(can_delete_product)
        
        self.stdout.write(self.style.SUCCESS('Разрешения назначены группе "Модератор продуктов"'))
        
        # Дополнительное задание: Создаем группу "Контент-менеджер"
        try:
            content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
            if created:
                self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана'))
            else:
                self.stdout.write(self.style.WARNING('Группа "Контент-менеджер" уже существует'))
            
            # Получаем ContentType для модели BlogPost
            blog_post_content_type = ContentType.objects.get_for_model(BlogPost)
            
            # Получаем разрешения для модели BlogPost
            can_add_blog_post = Permission.objects.get(
                codename='add_blogpost',
                content_type=blog_post_content_type
            )
            can_change_blog_post = Permission.objects.get(
                codename='change_blogpost',
                content_type=blog_post_content_type
            )
            can_delete_blog_post = Permission.objects.get(
                codename='delete_blogpost',
                content_type=blog_post_content_type
            )
            
            # Назначаем разрешения группе "Контент-менеджер"
            content_manager_group.permissions.add(can_add_blog_post)
            content_manager_group.permissions.add(can_change_blog_post)
            content_manager_group.permissions.add(can_delete_blog_post)
            
            self.stdout.write(self.style.SUCCESS('Разрешения назначены группе "Контент-менеджер"'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Ошибка при настройке группы "Контент-менеджер": {e}'))