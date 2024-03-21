from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def custom_validation(data):
    email = data['email'].strip()
    first_name = data['first_name'].strip()
    last_name = data['last_name'].strip()
    password = data['password'].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('choose a different email')

    if not password or len(password) < 8:
        raise ValidationError('choose a different password, min 8 characters')

    if not first_name:
        raise ValidationError('first name not excepted')

    if not last_name:
        raise ValidationError('last name not excepted')

    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True


def validate_first_name(data):
    first_name = data['first_name'].strip()
    if not first_name:
        raise ValidationError('a first name is needed')
    return True


def validate_last_name(data):
    last_name = data['last_name'].strip()
    if not last_name:
        raise ValidationError('a last name is needed')
    return True


def validate_password(data):
    password = data['password'].strip()
    if not password or len(password) < 8:
        raise ValidationError('a password is needed, min 8 characters')
    return True

