from otkernel.applib.core_api import mp_input, mp_control, mp_com, mp_state
from otkernel.models import *
from django.db import transaction

@transaction.atomic
def move_control_to_state(control_mp_id, state_mp_id, description, json_data):
    state = None
    object_list = MPointControlQueue.objects.select_for_update().filter(mp_id=control_mp_id).order_by("id")
    for obj in object_list:
        if obj.title == title and obj.json_data == json_data:
            state = mp_state(state_mp_id, description, json_data)
            obj.delete()
    return state

def append_to_input(mp_id, json_data):
    obj = MPointInputQueue()
    obj.mp_id = mp_id
    obj.json_data = json_data
    obj.save()
    return obj
        
def append_to_control(mp_id, description, json_data):
    obj = MPointControlQueue()
    obj.mp_id = mp_id
    obj.description = description
    obj.json_data = json_data
    obj.save()
    return obj

def append_to_output(mp_id, json_data):
    obj = MPointOutputQueue()
    obj.mp_id = mp_id
    obj.json_data = json_data
    obj.save()
    return obj

@transaction.atomic
def pop_input(mp_id):
    object_list = MPointInputQueue.objects.select_for_update().filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]
        obj.delete()
        return obj.json_data if obj.json_data else {}
    else:
        return None
    
def get_inputs(mp_id):
    object_list = MPointInputQueue.objects.filter(mp_id=mp_id).order_by("id")
    return object_list
    
@transaction.atomic
def pop_output(mp_id):
    object_list = MPointOutputQueue.objects.select_for_update().filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]
        obj.delete()
        return obj.json_data if obj.json_data else {}
    else:
        return None
    
def get_outputs(mp_id):
    object_list = MPointOutputQueue.objects.filter(mp_id=mp_id).order_by("id")
    return object_list

@transaction.atomic
def pop_control(mp_id):
    object_list = MPointControlQueue.objects.select_for_update().filter(mp_id=mp_id).order_by("id")
    if object_list.count() > 0:
        obj = object_list[0]
        obj.delete()
        return { 'description': obj.description, 'data': obj.json_data }
    else:
        return None

def get_controls(mp_id):
    object_list = MPointControlQueue.objects.filter(mp_id=mp_id).order_by("id")
    return object_list

def create_task(mp_id, task_name, json_data):
    pass
    
def send_to_event_log(mp_id, text):
    pass

def add_feature(mp_id, json_data):
    obj = Feature()
    obj.json_data = json_data
    obj.save()
    return obj
    
def add_operation(json_data, previous_operation_id=None):
    obj = Operation()
    if previous_operation_id:
        operation.previous_operation_id = previous_operation_id
    operation.json_data = json_data
    operation.save()
    return operation
        
def add_to_inventory(feature_id, operation_id, location_id, product_id=None, product_external_id=None, rfid=None, amount=1):
    obj = Inventory()
    if product_id:
        product = Product.objects.get(pk=product_id, active=True)
    elif product_external_id:
        product = Product.objects.filter(external_id = product_external_id, active=True).first()
    else:
        product = None    
    if product:
        obj.product = product
        obj.location_id = location_id
        obj.amount = amount
        obj.rfid = rfid
        obj.feature_id = feature_id
        obj.last_operation_id = operation_id
        obj.save()
        return obj
    else:
        return None
    
def append_to_log(mp_id, attr, amount):
    obj = Log()
    obj.mp_id = mp_id
    obj.attr = attr
    obj.amount = amount
    obj.save()
    return obj
    
def append_to_extended_log(mp_id, attr, data):
    obj = ExtendedLog()
    obj.mp_id = mp_id
    obj.attr = attr
    obj.json_data = data
    obj.save()
    return obj

def get_inventory(product_id=None, product_external_id=None, rfid=None, location=None):
    obj = None
    if rfid:
        obj = Inventory.objects.get(rfid=rfid)
    else:    
        if product_id:
            product = Product.objects.get(pk=product_id, active=True)
        elif product_external_id:
            product = Product.objects.filter(external_id = product_external_id, active=True).first()
        else:
            product = None    
        if product:
            if location:
                object_list = Inventory.objects.get(product = product, location_id = location)
            else:
                object_list = Inventory.objects.get(product = product, location_id = location)
            if object_list.count()==1:
                obj = object_list[0]
            else:
                return None
    return obj

def update_inventory(product_id=None, product_external_id=None, rfid=None, location=None, new_location=None, operation_json_data=None, input_mp_id=None):
    obj = get_inventory(product_id, product_external_id, rfid, location)
    if obj:
        save = False
        if new_location:
            obj.location_id = new_location
            save = True
        if operation_json_data:
            opr = add_operation(operation_json_data, previous_operation_id=obj.last_operation)
            obj.last_operation = opr
            save = True
        if save:
            obj.save()
        return obj
    return None
