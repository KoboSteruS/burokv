"""
Команда для добавления услуг в базу данных.
"""
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from landing.models import Service


class Command(BaseCommand):
    """
    Команда для добавления услуг компании в базу данных.
    """
    help = 'Добавляет услуги компании в базу данных'

    def handle(self, *args, **options):
        """
        Основной метод выполнения команды.
        """
        # Определяем путь к статическим файлам
        from django.conf import settings
        base_dir = settings.BASE_DIR
        static_dir = os.path.join(base_dir, 'static', 'images')
        
        # Список услуг с описаниями
        services_data = [
            {
                'title': 'Предпродажная консультация',
                'description': 'Подготовим стратегию для выгодной продажи квартиры, дома, земли.',
                'icon_file': 'uslugi1.png',
                'order': 1
            },
            {
                'title': 'Размещение рекламы',
                'description': 'Эффективно разместим объявления на всех площадках.',
                'icon_file': 'uslugi2.png',
                'order': 2
            },
            {
                'title': 'Юридическое сопровождение',
                'description': 'Проверим чистоту сделки, подготовим документы и договоры.',
                'icon_file': 'uslugi3.png',
                'order': 3
            },
            {
                'title': 'Оценка недвижимости',
                'description': 'Проведем оценку стоимости квартиры, дома или участка.',
                'icon_file': 'uslugi4.png',
                'order': 4
            },
            {
                'title': 'Срочный выкуп',
                'description': 'Быстро купим комнату, квартиру или дом в Петрозаводске.',
                'icon_file': 'uslugi5.png',
                'order': 5
            },
            {
                'title': 'Кадастровая съемка',
                'description': 'Проведем кадастровую съемку и подготовим документы.',
                'icon_file': 'uslugi6.png',
                'order': 6
            },
            {
                'title': 'Межевание',
                'description': 'Услуги межевания земельных участков.',
                'icon_file': 'uslugi7.png',
                'order': 7
            },
            {
                'title': 'План границ',
                'description': 'Разработаем межевые и технические планы участка.',
                'icon_file': 'uslugi8.png',
                'order': 8
            },
            {
                'title': 'Регистрация недвижимости',
                'description': 'Оформим права на жилую и коммерческую недвижимость.',
                'icon_file': 'uslugi9.png',
                'order': 9
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for service_data in services_data:
            icon_path = os.path.join(static_dir, service_data['icon_file'])
            
            # Проверяем существование файла иконки
            if not os.path.exists(icon_path):
                self.stdout.write(
                    self.style.WARNING(
                        f'Иконка {service_data["icon_file"]} не найдена. Пропускаем услугу "{service_data["title"]}"'
                    )
                )
                continue
            
            # Проверяем, существует ли уже такая услуга
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'order': service_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                # Если услуга создана, загружаем иконку
                with open(icon_path, 'rb') as f:
                    service.icon.save(
                        service_data['icon_file'],
                        File(f),
                        save=True
                    )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Создана услуга: "{service_data["title"]}"'
                    )
                )
            else:
                # Если услуга уже существует, обновляем её
                service.description = service_data['description']
                service.order = service_data['order']
                service.is_active = True
                
                # Обновляем иконку, если её нет
                if not service.icon:
                    with open(icon_path, 'rb') as f:
                        service.icon.save(
                            service_data['icon_file'],
                            File(f),
                            save=True
                        )
                
                service.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'↻ Обновлена услуга: "{service_data["title"]}"'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Создано: {created_count}, Обновлено: {updated_count}'
            )
        )

