from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from reloc.models import Restaurant, MenuItem
import json
from regen.settings import sla_conf
from reloc.utils import map_service, geo_nearby


def rest_sla(request):
    response = {}
    if request.method == "GET":
        if request.GET.get('latlong') == None:
            response['status'] = "error"
            response['message'] = "expected data not provided"
            return JsonResponse(response, status=400)

        sla = sla_conf['sla']

        response['data'] = []
        response['message'] = "success"
        return JsonResponse(response, status=200)
    else:
        response['status'] = "error"
        response['message'] = "method not allowed"
        return JsonResponse(response, status=405)


def cart_sla(request):
    response = {}
    return JsonResponse(response, status=200)


def allow_item(request):
    response = {}
    return JsonResponse(response, status=200)