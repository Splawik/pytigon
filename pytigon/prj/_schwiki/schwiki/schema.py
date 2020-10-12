from .models import PageObjectsConf

from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType


class _PageObjectsConf(DjangoObjectType):
    class Meta:
        model = PageObjectsConf
        interfaces = ( Node, )
        filter_fields = {
            'app': ['exact', 'icontains', 'istartswith'],
            'name': ['exact', 'icontains', 'istartswith'],
        }


def extend_query(query_class):
    class query(query_class):        
        pageobjectsconf = Node.Field(_PageObjectsConf)
        all_pageobjectsconf = DjangoFilterConnectionField(_PageObjectsConf)

    return query

def extend_mutation(mutation_class):
    return mutation_class
    