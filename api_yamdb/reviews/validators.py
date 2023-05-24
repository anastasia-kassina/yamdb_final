from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка года."""
    if value > timezone.now().year:
        raise ValidationError(
            'Такой год %(value)s еще не наступил!',
            params={'value': value},
        )
    return value
