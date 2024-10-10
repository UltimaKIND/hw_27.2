import re

from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:
    """
    проверяет что ссылка ведет только на YouTube
    """

    def __init__(self, field="link_to_video", message="Ссылка ведет не на YouTube"):
        self.field = field
        self.message = message

    def __call__(self, value):
        mask = re.compile(r"(http(s)?://)?(www\.)?(youtube\.com)/\w+")
        link = value.get(self.field)
        if link:
            if not mask.match(link):
                raise ValidationError({self.field: [self.message]})
        return
