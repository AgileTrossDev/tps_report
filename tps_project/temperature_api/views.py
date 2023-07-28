from django.shortcuts import render

from graphene_django.views import GraphQLView
from .schema import schema

class CustomGraphQLView(GraphQLView):
    graphiql = True  # Enable the GraphiQL interface for testing in the browser
    schema = schema
