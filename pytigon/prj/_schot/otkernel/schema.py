import graphene
from graphene.types.generic import GenericScalar
from . import models
from pytigon_lib.schdjangoext.graphql import add_graphql_to_class
from otkernel.applib.api import pub, prv
from django.forms.models import model_to_dict
    
def extend_query(query_class):        
    #for model_name in dir(models):
    #    model = getattr(models, model_name)
    #    if hasattr(model, "_meta") and hasattr(model, "filter_fields"):
    #        add_graphql_to_class(model, getattr(model, "filter_fields"), query_class)    
    
    class _QueryClass(query_class):                
        get_first_control_cmd = GenericScalar        
        def resolve_get_first_control_cmd(root, info, mp_id) :
            return pub.get_first_control_cmd(mp_id)

        get_first_output_item = GenericScalar        
        def resolve_get_first_output_item(root, info, mp_id) :
            return pub.get_first_output_item(mp_id)
    
        get_all_control_cmds=graphene.List(GenericScalar, mp_id = graphene.Int())        
        def resolve_all_control_cmds(root, info, mp_id) :
            ret = pub.get_all_control_cmds(mp_id)             
            if ret:
                return [ model_to_dict(obj) for obj in ret ]
            else:
                return []

        get_all_output_items=graphene.List(GenericScalar, mp_id = graphene.Int())        
        def resolve_get_all_output_items(root, info, mp_id) :
            ret = pub.get_all_output_items(mp_id)
            if ret:
                return [ model_to_dict(obj) for obj in ret ]
            else:
                return []

    return _QueryClass

class PushMeasurment(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
        data = GenericScalar()
        
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id, data):
        ret = pub.push_measurement(mp_id, data)        
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return PushMeasurment(ok=ok, data=d)

class SetMeasurementPointState(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
        description = graphene.String()
        data = GenericScalar()
        
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id, description, data):
        ret = pub.set_measurement_point_state(mp_id, description, data) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return SetMeasurementPointState(ok=ok, data=d)


class ClearAllInputItems(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id):
        ret = pub.clear_all_input_items(mp_id) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return ClearAllInputItems(ok=ok, data=d)

class PushControlCmd(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
        description = graphene.String()
        data = GenericScalar()

    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id, description, data):
        ret = pub.push_control_cmd(mp_id, description, data)        
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return PushControlCmd(ok=ok, data=d)


class PopControlCmd(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id):
        ret = pub.pop_control_cmd(mp_id) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return PopControlCmd(ok=ok, data=d)



class ClearControlCmd(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
        description = graphene.String()
        data = GenericScalar()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id, description, data):
        ret = pub.clear_control_cmd(mp_id, description, data) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return ClearControlCmd(ok=ok, data=d)


class ClearAllControlCmds(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id):
        ret = pub.clear_all_control_cmds(mp_id) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return ClearAllControlCmds(ok=ok, data=d)

class PopOutputItem(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id):
        ret = pub.pop_output_item(mp_id) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return PopOutputItem(ok=ok, data=d)

class ClearOutputItem(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
        data = GenericScalar()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id, data):
        ret = pub.clear_output_item(mp_id, data) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return ClearOutputItem(ok=ok, data=d)


class ClearAllOutputItems(graphene.Mutation):
    class Arguments:
        mp_id = graphene.Int()
                
    ok = graphene.Boolean()
    data = GenericScalar()

    def mutate(root, info, mp_id):
        ret = pub.clear_all_output_items(mp_id) 
        if ret:
            ok = True
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
        else:
            ok = False
            d = None
        return ClearAllOutputItems(ok=ok, data=d)


def extend_mutation(mutation_class):
    mutation_class.push_measurment = PushMeasurment.Field()
    mutation_class.set_measurement_point_state = SetMeasurementPointState.Field()
    mutation_class.clear_all_input_items = ClearAllInputItems.Field()
    mutation_class.push_control_cmd = PushControlCmd.Field()
    mutation_class.pop_control_cmd = PopControlCmd.Field()
    mutation_class.clear_control_cmd = ClearControlCmd.Field()
    mutation_class.clear_all_control_cmds = ClearAllControlCmds.Field()
    mutation_class.pop_output_item = PopOutputItem.Field()
    mutation_class.clear_output_item = ClearOutputItem.Field()
    mutation_class.clear_all_output_items = ClearAllOutputItems.Field()
    return mutation_class
