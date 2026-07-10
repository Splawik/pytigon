import importlib

import graphene
import graphql_jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

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
        fields = ["id", "username", "email"]


# Define the UserMutation which allows updating or creating a user
class UserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, id="0"):
        idd = int(id)
        if idd > 0:
            try:
                _user = get_user_model().objects.get(pk=idd)
            except get_user_model().DoesNotExist:
                _user = get_user_model()()
        else:
            _user = get_user_model()()
        _user.username = username
        _user.email = email
        _user.save()
        return UserMutation(user=_user)


# Define the base Query class
class _Query:
    ping = graphene.String(description="graphql api test")


# Define the base Mutation class
class _Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


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
        if any(pos.startswith(p) for p in settings.SKIP_APPS_PREFIXES):
            continue
    module_name = f"{str(pos)}.schema"
    try:
        m = importlib.import_module(module_name)
        if hasattr(m, "extend_query"):
            _Query = m.extend_query(_Query)
        if hasattr(m, "extend_mutation"):
            _Mutation = m.extend_mutation(_Mutation)
    except ModuleNotFoundError:
        pass


class Query(graphene.ObjectType, _Query):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()


class Mutation(graphene.ObjectType, _Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

if settings.GRAPHENE_PUBLIC:
    public_schema = schema
