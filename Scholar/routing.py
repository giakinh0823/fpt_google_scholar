from django.urls import path

from . import consumers

ws_urlpatterns = [
    path('ws/wordcloud/<str:room_name>/', consumers.WordCloudConsumer.as_asgi()),
]