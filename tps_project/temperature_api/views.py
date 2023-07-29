from django.shortcuts import render

from graphene_django.views import GraphQLView
from .schema import schema

from django.views.generic import TemplateView
from .consumers import TemperatureConsumer

class CustomGraphQLView(GraphQLView):
    graphiql = True  # Enable the GraphiQL interface for testing in the browser
    schema = schema


class TemperatureView(TemplateView):
    template_name = 'temperature_view.html'

    async def get(self, request, *args, **kwargs):
      # Create a TemperatureConsumer instance and connect to the external WebSocket server
      consumer = TemperatureConsumer()
      
      await consumer.connect()

      # The consumer will keep running and receiving data from the WebSocket
      return await super().get(request, *args, **kwargs)