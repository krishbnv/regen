from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from reloc.models import Restaurant, MenuItem
import json
# Create your views here.

def restaurants(request):
    response = {}
    response['data'] = []
    response['message'] = "success"
    return JsonResponse(response, status=200)