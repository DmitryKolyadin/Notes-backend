from django.contrib import admin
from django.urls import include, path

from api import views

# Методы:

# /api/v0.1/auth/login/password

# /api/v0.1/notes
# - GET — получение
# - POST — создание

# /api/v0.1/note
# - GET — получение
# - PUT — обновление
# - DELETE — удаление


urlpatterns_v0_1 = [
    path('auth/login/password', views.login_password),
    path('notes', views.notes),
    path('note/<note_id>', views.note),
]

urlpatterns = [
    path('v0.1/', include(urlpatterns_v0_1)),
]
