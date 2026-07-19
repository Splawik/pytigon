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
        if not info.context.user.is_authenticated:
            raise Exception("Authentication required")
        idd = int(id)
        if idd > 0:
            if info.context.user.id != idd and not info.context.user.is_superuser:
                raise Exception("Not authorized to modify this user")
            try:
                _user = get_user_model().objects.get(pk=idd)
            except get_user_model().DoesNotExist:
                _user = get_user_model()()
        else:
            if not info.context.user.is_superuser:
                raise Exception("Only superusers can create new users")
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
        """Return all users. Restricted to authenticated staff members.

        Exposing every account (including email addresses) to any logged-in
        user would leak PII. Require ``is_staff`` so that only privileged
        operators can enumerate the user directory.
        """
        user = info.context.user
        if not (user.is_authenticated and user.is_staff):
            return []
        return get_user_model().objects.all()


class Mutation(graphene.ObjectType, _Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

if settings.GRAPHENE_PUBLIC:
    public_schema = schema
