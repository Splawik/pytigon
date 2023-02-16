from django.db import models
from schlog.models import Log

def log_to_db(function, obj, description, group=None, request=None, user = None, autosave=True):    
    obj = Log()
    log.description = description
    log.group = group
    
    m = function.__module__
    x = m.split('.')
    log.app = x[0]
    
    if obj and issubclass(obj, models.Model):
        log.table = type(obj).__name__
        log.parent_id = obj.pk
        
    if user:
        log.operator = user.username
        log.operator_id = user.pk
    elif request and request.user:
        log.operator = request.user.username
        log.operator_id = request.user.pk
    
    if autosave:
        log.save()
        
    return log
