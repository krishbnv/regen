from reloc.models import Restaurant


def map_service(latlong, rest_id):
    """
    Takes latlong of consumer, restaurant id as input
    returns time taken for travelling taking traffic into account
    """
    ttime = 0
    return ttime


def geo_nearby(latlong, radius):
    """
    Takes latlong of consumer and radius as input
    returns list of restaurants in the georadius 
    """
    rts = Restaurants.objects.filter(is_active=True)
    return rts


def get_sla_conf():
    sla_conf = json.load(open('sla_conf.json'))
    return sla_conf