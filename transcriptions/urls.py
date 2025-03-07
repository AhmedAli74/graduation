from django.urls import path
from . import views
app_name='transcriptions'
urlpatterns = [
    path("", views.index, name="index"),
    path('text-to-speech/', views.text_to_speech, name='text_to_speech')
]