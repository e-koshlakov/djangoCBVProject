import re
from django.core.exceptions import ValidationError

def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    if not pattern.match(field):
        raise ValidationError("Must contain A-Z, a-z letters and 0-9 numbers")
    if not 8 <= len(field) <= 12:
        raise ValidationError("Password length must be between 8 and 12 characters")