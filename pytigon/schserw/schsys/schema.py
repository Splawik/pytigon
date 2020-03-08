from graphene_django import DjangoObjectType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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
        model = User

class UserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, id="0"):
        idd = int(id)
        if idd > 0:
            _user = User.objects.get(pk=idd)
        else:
            _user = User()
        _user.username = username
        _user.email = email
        _user.save()
        return UserMutation(user=_user)

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    update_user = UserMutation.Field()

for app in settings.INSTALLED_APPS:
    if isinstance(app, AppConfigMod):
        pos = app.name
    else:
        pos = app
        if pos.startswith('django') or pos.startswith('debug') or pos.startswith('registration') \
        or pos.startswith('bootstrap_admin') or pos.startswith('channels')\
        or pos.startswith('bootstrap4'):
            continue
    module_name = '%s.schema' % str(pos)
    try:
        m = importlib.import_module(module_name)
        if hasattr(m, 'extend_query'):
            Query = m.extend_query(Query)
        if hasattr(m, 'extend_mutation'):
            Mutation = m.extend_mutation(Mutation)
    except ModuleNotFoundError:
        pass

schema = graphene.Schema(query=Query, mutation=Mutation)
