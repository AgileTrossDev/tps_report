from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from temperature_api.consumers import TemperatureConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/temperature/', TemperatureConsumer.as_asgi()),
    ]),
})