from graphene_django import DjangoObjectType
import graphene
from .models import SChAppSet

class _SChAppSet(DjangoObjectType):
    class Meta:
        model = SChAppSet

def extend_query(query_class):
    class query(query_class):
        app_sets = graphene.List(_SChAppSet)
        
        def resolve_app_sets(self, info):
            return SChAppSet.objects.all()

    return query

def extend_mutation(mutation_class):
    return mutation_class

