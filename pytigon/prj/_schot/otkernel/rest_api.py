from django.urls import path
from django.core import serializers
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response

from otkernel.applib.api import pub, prv

@api_view(['POST', "DELETE",])
def measurement(request, mp_id):
    if request.method == 'POST':
        ret = pub.push_measurement(mp_id, request.data["data"])        
        if ret:
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    elif request.method == 'DELETE':
        return Response(pub.clear_all_input_items(mp_id))
    return Response({ "ok": False })


@api_view(['GET', 'PUT',])
def measurement_point_state(request, mp_id):
    if request.method == 'GET':
        ret = pub.get_measurement_point_state(mp_id)        
        if ret:
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    elif request.method == 'PUT':
        ret = pub.set_measurement_point_state(mp_id, request.data["description"],  request.data["data"])        
        if ret:
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['GET', 'POST', 'DELETE',])    
def control_cmd(request, mp_id):
    if request.method == 'GET':
        ret = pub.get_all_control_cmds(mp_id)
        if ret != None:
            d = serializers.serialize("json", ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    elif request.method == 'POST':
        ret = pub.push_control_cmd(mp_id, request.data["description"],  request.data["data"])        
        if ret:
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    elif request.method == 'DELETE':
        ret = pub.clear_all_control_cmds(mp_id)
        if ret != None:
            return Response(ret)
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['GET',])
def pop_control_cmd(request, mp_id):
    if request.method == 'GET':
        ret = pub.pop_control_cmd(mp_id)        
        if ret:
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['GET',])
def get_first_control_cmd(request, mp_id):
    if request.method == 'GET':
        ret = pub.get_first_control_cmd(mp_id)
        if ret:
            if type(ret) == dict:
                d = ret
            else:
                d = model_to_dict(ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['DELETE',])    
def clear_control_cmd(request, mp_id):
    if request.method == 'DELETE':
        ret = pub.clear_control_cmd(mp_id, request.data["description"],  request.data["data"])        
        if ret:
            return Response(ret)
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['GET', 'DELETE',])    
def output_item(request, mp_id):
    if request.method == 'GET':
        ret = pub.get_all_output_items(mp_id)
        if ret != None:
            d = serializers.serialize("json", ret)
            return Response({ "ok": True, "data": d })
        else:
            return Response({ "ok": False })
    elif request.method == 'DELETE':
        ret = pub.clear_all_output_items(mp_id)        
        if ret:
            return Response(ret)
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['GET',])
def pop_output_item(request, mp_id):
    if request.method == 'GET':
        ret = pub.pop_output_item(mp_id)
        if ret:
            return Response(ret)
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['GET',])
def get_first_output_item(request, mp_id):
    if request.method == 'GET':
        ret = pub.get_first_output_item(mp_id)
        if ret:
            return Response(ret)
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


@api_view(['DELETE',])
def clear_output_item(request, mp_id):
    if request.method == 'DELETE':
        ret = pub.clear_output_item(mp_id,  request.data["data"])
        if ret:
            return Response(ret)
        else:
            return Response({ "ok": False })
    return Response({ "ok": False })


urlpatterns = [
    path("<int:mp_id>/measurement/", measurement, name="measurement"),
    path("<int:mp_id>/measurement_point_state/", measurement_point_state, name="measurement_point_state"),

    path("<int:mp_id>/control_cmd/", control_cmd, name="control_cmd"),
    
    path("<int:mp_id>/control_cmd/pop/", pop_control_cmd, name="pop_control_cmd"),
    path("<int:mp_id>/control_cmd/get_first/", get_first_control_cmd, name="get_first_control_cmd"),
    path("<int:mp_id>/control_cmd/clear/", clear_control_cmd, name="clear_control_cmd"),

    path("<int:mp_id>/output_item/", output_item, name="output_item"),
    path("<int:mp_id>/output_item/pop/", pop_output_item, name="pop_output_item"),
    path("<int:mp_id>/output_item/get_first/", get_first_output_item, name="get_first_output_item"),    
    path("<int:mp_id>/output_item/clear/", clear_output_item, name="clear_output_item"),
]
