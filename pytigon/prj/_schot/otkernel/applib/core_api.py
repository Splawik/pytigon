from otkernel.models import *

class Api():
    def __init__(self):
        pass
    
    def register_api(self, namespace, api_obj):
        setattr(self, namespace, api_obj)

API = Api()

def push_measurement_default(mp_id, json_data):
    obj = MPointInputQueue()
    obj.mp_id = mp_id
    obj.json_data = json_data
    obj.save()
    return obj

def push_control_cmd_default(mp_id, description, json_data):
    obj = MPointControlQueue()
    obj.mp_id = mp_id
    obj.description = description
    obj.json_data = json_data
    obj.save()
    return obj

def set_measurement_point_state_default(mp_id, description, json_data):
    mp = MeasurementPoint.objects.get(mp_id)
    state = mp.measurementpointstate
    state.description = description
    state.json_data = json_data
    state.save()
    return state

def _proc(mp_id, command, json_data, **argv):
    global API
    obj = MeasurementPoint.objects.get(pk=mp_id)
    input_str = getattr(obj, command)
    if input_str:
        make_proc_str = (
            "def proc(obj, json_data, api, **argv):\n"
                + "\n".join(["    " + pos for pos in input_str.split("\n")])
                + "\n"
        )    
        exec(make_proc_str)
        return locals()["proc"](obj, json_data, API, **argv)
    else:
        if command == "input_proc":
            return push_measurement_default(mp_id, json_data)
        elif command == "control_proc":
            return push_control_cmd_default(mp_id, argv['description'], json_data)
        elif command == "state_proc":
            return set_measurement_point_state_default(mp_id, json_data)

def mp_input(mp_id, json_data):
    return _proc(mp_id, "input_proc", json_data)

def mp_control(mp_id, description, json_data):
    return _proc(mp_id, "control_proc", json_data, description=description)
    
def mp_com(mp_id, json_data):
    return _proc(mp_id, "com_proc", json_data)

def mp_state(mp_id, description, json_data):
    return _proc(mp_id, "state_proc", json_data, description=description)
