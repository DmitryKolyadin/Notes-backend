from django.contrib import admin


# Регестрируем модели в админке
from api.models import JWT_token, Note

admin.site.register(JWT_token)
admin.site.register(Note)

