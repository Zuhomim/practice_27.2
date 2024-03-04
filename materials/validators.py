from rest_framework import serializers
import re

ALLOWED_LINK = "https://www.youtube.com"


class ScamLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data_url = dict(value).get(self.field)
        if data_url:
            if bool(re.match(r'https://www.youtube.com/', data_url)) is False:
                raise serializers.ValidationError("Запрещено использовать сторонние ссылки")
