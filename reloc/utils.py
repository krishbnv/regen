from reloc.models import Restaurant
import json

def map_service(latlong, rest_id):
    """
    Takes latlong of consumer, restaurant id as input
    returns time taken for travelling taking traffic into account
    """
    import random
    ttime = random.randrange(20, 35)
    return ttime


def geo_nearby(latlong, radius):
    """
    Takes latlong of consumer and radius as input
    returns list of restaurants in the georadius 
    """
    rts = Restaurant.objects.filter(is_active=True)
    return rts


def get_sla_conf():
    sla_conf = json.load(open('sla_conf.json'))
    return sla_conf