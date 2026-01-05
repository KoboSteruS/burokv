"""
Django management команда для генерации JWT токена для доступа к админ-панели.
"""
import jwt
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Генерирует JWT токен для доступа к админ-панели'

    def add_arguments(self, parser):
        parser.add_argument(
            '--expires-days',
            type=int,
            default=365,
            help='Количество дней до истечения токена (по умолчанию: 365)'
        )

    def handle(self, *args, **options):
        jwt_secret = getattr(settings, 'ADMIN_JWT_SECRET', None)
        
        if not jwt_secret:
            self.stdout.write(
                self.style.ERROR(
                    'ADMIN_JWT_SECRET не настроен в settings.py!\n'
                    'Добавьте в .env файл: ADMIN_JWT_SECRET=ваш-секретный-ключ'
                )
            )
            return
        
        expires_days = options['expires_days']
        expiration = datetime.utcnow() + timedelta(days=expires_days)
        
        payload = {
            'type': 'admin_access',
            'exp': expiration,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, jwt_secret, algorithm='HS256')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('JWT токен для админ-панели сгенерирован!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'\nТокен действителен до: {expiration.strftime("%Y-%m-%d %H:%M:%S")} UTC')
        self.stdout.write(f'\nURL для доступа к админ-панели:')
        self.stdout.write(self.style.WARNING(f'\nhttp://your-domain.com/admin/{token}/\n'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\n⚠️  ВАЖНО: Сохраните этот токен в безопасном месте!')
        self.stdout.write('⚠️  Не передавайте токен третьим лицам!\n')

