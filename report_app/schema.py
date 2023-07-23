import graphene
from graphene_django.types import DjangoObjectType
from .models import TimeSeries


class TimeSeriesType(DjangoObjectType):
    class Meta:
        model = TimeSeries


class Query(graphene.ObjectType):
    all_timeseries = graphene.List(TimeSeriesType)

    def resolve_all_timeseries(self, info):
        return TimeSeries.objects.all()


schema = graphene.Schema(query=Query)
