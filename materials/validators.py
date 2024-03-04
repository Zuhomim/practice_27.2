from rest_framework import serializers

ALLOWED_LINK = "https://www.youtube.com"


class ScamLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.lower().split()
        if ALLOWED_LINK not in url:
            raise serializers.ValidationError("Запрещено использовать сторонние ссылки")
