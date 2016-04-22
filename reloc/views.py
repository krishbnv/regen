from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from reloc.models import Restaurant, MenuItem
import json
from reloc.utils import map_service, geo_nearby, get_sla_conf


def rest_sla(request):
    """
    Send list of restaurants in delivery radius along with SLAs
    """
    response = {}
    if request.method == "GET":
        if request.GET.get('latlong') == None:
            response['status'] = "error"
            response['message'] = "expected data not provided"
            return JsonResponse(response, status=400)

        #get restaurants in the georadius
        sla_conf = get_sla_conf()
        latlong = request.GET.get('latlong')
        rts = geo_nearby(latlong, sla_conf["delivery_radius"])

        #calculate SLAs for each restaurant in delivery radius
        #assuming map_service has realtime traffic data
        data = []
        for rt in rts:
            travel_time = map_service(latlong, rt.latlong) 
            item = {}
            item['name'] = rt.name
            item['sla'] = travel_time
            data.append(item)

        #sort by sla
        sorted_data = sorted(data, key=lambda k : k['sla'])

        response['data'] = data
        response['message'] = "success"
        return JsonResponse(response, status=200)
    else:
        response['status'] = "error"
        response['message'] = "method not allowed"
        return JsonResponse(response, status=405)


@csrf_exempt
def cart_sla(request):
    response = {}
    if request.method == "POST":
        response['data'] = {}
        post_data = json.loads(request.body)
        item_ids = post_data.get('item_ids') #cart item ids
        latlong = post_data.get('latlong')

        #data validation
        valid = True
        if None in [item_ids, latlong]:
            valid = False

        if type(item_ids) != list:
            valid = False

        if not valid:
            response['status'] = 'error'
            response['message'] = 'invalid data'
            return JsonResponse(response, status=400)
 
        #checkif cart has all items from same restaurant
        rids = MenuItem.objects.filter(pk__in=item_ids).values_list('restaurant__pk').distinct()
        if len(rids) > 1:
            response['status'] = 'error'
            response['message'] = 'cart contains items from more than one restaurant'
            return JsonResponse(response, status=400)

        restaurant = Restaurant.objects.get(pk=rids[0])

        travel_time = map_service(latlong, restaurant.pk)
        prep_time = 0
        #assuming parallel preparation
        #adding highest item prep time to travel-time for sla
        for item_id in item_ids:
            item_prep = Item.objects.get(pk=item_id).prep_time
            if item_prep > prep_time:
                prep_time = item_prep

        sla = prep_time + travel_time
        response['data']['sla'] = sla

        #check if sla is getting breached
        sla_conf = get_sla_conf()
        max_sla = sla_conf['sla']

        if sla > max_sla:
            response['data']['breach'] = True
        return JsonResponse(response, status=200)
    else:
        response['status'] = "error"
        response['message'] = "method not allowed"
        return JsonResponse(response, status=405)


@csrf_exempt
def allow_items(request):
    """
    Send list of listof(item, allow_boolean) for a given restaurant
    """
    response = {}
    if request.method == "POST":
        post_data = json.loads(request.body)
        latlong = post_data.get('latlong')
        rid = post_data.get('rid')

        valid = True
        if None in [latlong, rid]:
            valid = False

        if not valid:
            response['status'] = 'error'
            response['message'] = 'invalid data'
            return JsonResponse(response, status=400)

        return JsonResponse(response, status=200)
    else:
        response['status'] = "error"
        response['message'] = "method not allowed"
        return JsonResponse(response, status=405)