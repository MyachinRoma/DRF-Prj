from rest_framework.serializers import ValidationError


def validate_links(value):
    if "youtube.com" not in value:
        raise ValidationError("Материалы могут содержать ссылки только на youtube.com")
    return value
