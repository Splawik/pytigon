from otkernel.applib.core_api import mp_input, mp_control, mp_com, mp_state
from otkernel.models import *

def push_measurement(mp_id, json_data):
    return mp_input(mp_id, json_data)

def set_measurement_point_state(mp_id, description, json_data):
    return mp_state(mp_id, description, json_data)

def get_measurement_point_state(mp_id):
    return MeasurementPointState.objects.filter(parent__id = mp_id).first()

def clear_all_input_items(mp_id):
    object_list = MPointInputQueue.objects.filter(mp_id=mp_id)
    return object_list.delete()
    
def push_control_cmd(mp_id, description, json_data):
    return mp_control(mp_id, description, json_data)

def pop_control_cmd(mp_id):
    object_list = MPointControlQueue.objects.filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]        
        obj.delete()
        return { 'description': obj.description, 'data': obj.json_data }
    else:
        return None
    
def get_first_control_cmd(mp_id):
    object_list = MPointControlQueue.objects.filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]        
        return { 'description': obj.description, 'data': obj.json_data }
    else:
        return None
    
def get_all_control_cmds(mp_id):
    object_list = MPointControlQueue.objects.filter(mp_id=mp_id).order_by("id")
    return object_list
    
def clear_control_cmd(mp_id, description, json_data):
    object_list = MPointControlQueue.objects.filter(mp_id=mp_id)
    for obj in object_list:
        if obj.json_data == json_data:
            if not description or description == obj.description:
                return obj.delete()
    return None
    
def clear_all_control_cmds(mp_id):
    object_list = MPointControlQueue.objects.filter(mp_id=mp_id)
    return object_list.delete()
    
def pop_output_item(mp_id):
    object_list = MPointOutputQueue.objects.filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]        
        obj.delete()
        return obj.json_data if obj.json_data else {}
    else:
        return None
    
def get_first_output_item(mp_id):
    object_list = MPointOutputQueue.objects.filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]        
        return obj.json_data if obj.json_data else {}
    else:
        return None
    
def get_all_output_items(mp_id):
    object_list = MPointOutputQueue.objects.filter(mp_id=mp_id).order_by("id")
    return object_list
    
def clear_output_item(mp_id, json_data):
    object_list = MPointOutputQueue.objects.filter(mp_id=mp_id)
    for obj in object_list:
        if obj.json_data == json_data:
            return obj.delete()
    return None
        
def clear_all_output_items(mp_id):
    object_list = MPointOutputQueue.objects.filter(mp_id=mp_id)
    return object_list.delete()
    
