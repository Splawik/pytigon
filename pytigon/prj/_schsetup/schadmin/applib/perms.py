from django.conf import settings

def if_rest(user, perm):
    if user.has_perm(perm) and hasattr(settings, "REST") and settings.REST:
        return True
    else:
        return False
        
def if_graphql(user, perm):
    if user.has_perm(perm) and hasattr(settings, "GRAPHQL") and settings.GRAPHQL:
        return True
    else:
        return False

def if_oauth2(user, perm):
    return if_rest(user, perm) or if_graphql(user, perm)
    
def if_filer(user, perm):
    if user.has_perm(perm) and 'filer' in settings.INSTALLED_APPS:
        return True
    else:
        return False
    
    INSTALLED_APPS.append('filer')
