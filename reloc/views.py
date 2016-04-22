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
            travel_time = map_service(latlong, rt.geo)
            rest = {}
            rest['name'] = rt.name
            rest['sla'] = travel_time
            if rt.ch:
                rest['chain_name'] = rt.ch.chain_name
            items = []
            for item in MenuItem.objects.filter(rt=rt, is_active=True):
                items.append({'item':item.item, 'price':item.price})
            rest['items'] = items
            data.append(rest)

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

        rids = MenuItem.objects.filter(pk__in=item_ids).values_list('restaurant__pk').distinct()

        try:
            restaurant = Restaurant.objects.get(pk=rids[0])
        except Restaurant.DoesNotExist:
            valid = False

        if not valid:
            response['status'] = 'error'
            response['message'] = 'invalid data'
            return JsonResponse(response, status=400)
 
        #checkif cart has all items from same restaurant

        if len(rids) > 1:
            response['status'] = 'error'
            response['message'] = 'cart contains items from more than one restaurant'
            return JsonResponse(response, status=400)

        travel_time = map_service(latlong, restaurant.pk)
        prep_time = 0
        #assuming parallel preparation
        #adding highest item prep time to travel-time for sla
        for item_id in item_ids:
            item_prep = MenuItem.objects.get(pk=item_id).prep_time
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
        try:
            restaurant = Restaurant.objects.get(pk=rid)
        except Restaurant.DoesNotExist:
            valid = False

        valid = True
        if None in [latlong, rid]:
            valid = False

        if not valid:
            response['status'] = 'error'
            response['message'] = 'invalid data'
            return JsonResponse(response, status=400)

        sla_conf = get_sla_conf()
        travel_time = map_service(latlong, rid)
        data = []

        #checking if restaurant is in sensitive item radius or not
        sense_high = True
        sense_med = True
        sense_high_radius = sla_conf['sensitive']
        sense_mid_radius = sla_conf['sensitive_med']

        rts = geo_nearby(latlong, sense_med_radius)
        for rt in rts:
            if rt.pk == rid:
                sense_med = False
                sense_high = False

        if sense_high:
            rts = geo_nearby(latlong, sense_high_radius)
            for rt in rts:
                if rt.pk == rid:
                    sense_high = False

        data = []
        max_sla = sla_conf['sla']

        for item in MenuItem.objects.filter(rt=restaurant):
            feasible = True
            if item.sensitive == 0 and sense_med == False:
                data.append({'item': item.item, 'item_id': item.pk, 'feasible': False})
            elif item.sensitive == 1 and sense_high == False:
                data.append({'item': item.item, 'item_id': item.pk, 'feasible': False})
            else:
                if travel_time + item.prep_time > max_sla:
                    feasible = False
                data.append({'item': item.item, 'item_id':item.pk, 'feasible': feasible})

        response['data'] = data
        response['status'] = "success"

        return JsonResponse(response, status=200)
    else:
        response['status'] = "error"
        response['message'] = "method not allowed"
        return JsonResponse(response, status=405)