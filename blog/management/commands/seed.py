from django.core.management.base import BaseCommand
from blog.models import CustomUser, Post


class Command(BaseCommand):
    help = 'Seed database with test data'

    def handle(self, *args, **kwargs):
        CustomUser.objects.filter(username__in=['poster_user', 'reader_user']).delete()
        Post.objects.all().delete()

        admin_user = CustomUser.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin',
            )

        poster = CustomUser.objects.create_user(
            username='poster_user',
            email='poster@example.com',
            password='poster123',
            role='poster',
        )

        CustomUser.objects.create_user(
            username='reader_user',
            email='reader@example.com',
            password='reader123',
            role='user',
        )

        posts = [
            ('Django для начинающих', 'Django — это высокоуровневый Python веб-фреймворк, который позволяет быстро создавать безопасные и поддерживаемые веб-сайты.', admin_user),
            ('Как работает ORM', 'ORM (Object-Relational Mapping) позволяет работать с базой данных через объекты Python вместо написания SQL-запросов вручную.', admin_user),
            ('Шаблоны в Django', 'Система шаблонов Django предоставляет мощный и гибкий способ генерировать HTML, разделяя логику и представление.', poster),
            ('Class-based Views', 'Классовые представления позволяют переиспользовать код и организовывать логику обработки запросов более структурированно.', poster),
            ('Деплой Django проекта', 'Деплой Django приложения включает настройку сервера, статических файлов, базы данных и переменных окружения.', admin_user),
        ]

        for title, content, author in posts:
            Post.objects.create(title=title, content=content, author=author)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми данными'))
