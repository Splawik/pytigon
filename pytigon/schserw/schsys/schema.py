from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.conf import settings
import graphene
import importlib
from pytigon_lib.schdjangoext.django_init import AppConfigMod

"""
query {
      users {
        id,
        username,
        email
      }
}

mutation { 
    updateUser(
        username:"xyz", 
        email:"xyz@pytigon.cloud"
    ) { user { id, username, email } }
}
"""


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, id="0"):
        idd = int(id)
        if idd > 0:
            _user = get_user_model().objects.get(pk=idd)
        else:
            _user = get_user_model()()
        _user.username = username
        _user.email = email
        _user.save()
        return UserMutation(user=_user)


class _Query:
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()


class _Mutation:
    pass


class PublicQuery(graphene.ObjectType, _Query):
    pass


class PublicMutation(graphene.ObjectType, _Mutation):
    pass


public_schema = graphene.Schema(query=PublicQuery, mutation=PublicMutation)

for app in settings.INSTALLED_APPS:
    if isinstance(app, AppConfigMod):
        pos = app.name
    else:
        pos = app
        if (
            pos.startswith("django")
            or pos.startswith("debug")
            or pos.startswith("registration")
            or pos.startswith("bootstrap_admin")
            or pos.startswith("channels")
            or pos.startswith("django_bootstrap5")
        ):
            continue
    module_name = "%s.schema" % str(pos)
    try:
        m = importlib.import_module(module_name)
        if hasattr(m, "extend_query"):
            _Query = m.extend_query(_Query)
        if hasattr(m, "extend_mutation"):
            _Mutation = m.extend_mutation(_Mutation)
    except ModuleNotFoundError:
        pass


class Query(graphene.ObjectType, _Query):
    pass


class Mutation(graphene.ObjectType, _Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

if settings.GRAPHENE_PUBLIC:
    public_schema = schema
