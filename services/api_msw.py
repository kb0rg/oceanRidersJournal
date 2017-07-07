import os
import json
import logging
import requests
from pprint import pprint


"""
module for functions relating to calls to magicseaweed.com api
"""

"""
remember to source keys .sh file to set tokens as env variables
for each terminal session.
"""

MSW_API_KEY = os.environ['MSW_ACCESS_TOKEN']
MSW_API_URL = "http://magicseaweed.com/api/"+MSW_API_KEY+"/forecast/?spot_id="


def get_url_by_spot(spot_id):

    url_base = MSW_API_URL +str(spot_id)+"&units=us"

    return url_base


def get_swell_1(spot_base_url):

    """
    make call to magicseaweed API to get swell info for journal entry.
    """

    # TODO: reduce request to query only fields used
    url_swell1 = spot_base_url + "swell.components.primary.*"
    logging.debug('MSW url_swell1: {}'.format(url_swell1))

    # TODO: find closest relevant timestamp in resp. for now, return first
    msw_swell1_resp = requests.get(url_swell1)
    msw_swell1_first = msw_swell1_resp.json()[0]
    logging.debug(msw_swell1_first)

    return msw_swell1_first

def parse_swell_1_data(msw_swell1_first):

    swell1_primary = msw_swell1_first['swell']['components']['primary']
    swell1_dir_deg_msw = swell1_primary.get('direction')
    swell1_dir_deg_global = get_global_degrees(swell1_dir_deg_msw)

    return {
        'swell1_ht': swell1_primary.get('height'),
        'swell1_per': swell1_primary.get('period'),
        'swell1_dir_deg_msw': swell1_dir_deg_msw,
        'swell1_dir_comp': swell1_primary.get('compassDirection'),
        'swell1_dir_deg_global': swell1_dir_deg_global,
        'swell1_arrow_deg': get_arrow_degrees(swell1_dir_deg_global),
        }

def get_wind(spot_base_url):

    """
    make call to magicseaweed API to get wind info for journal entry.
    """

    url_wind = spot_base_url + "wind.speed,wind.direction,wind.compassDirection,wind.unit"
    logging.debug('MSW url_wind: {}'.format(url_wind))

    msw_wind_resp = requests.get(url_wind)
    wind_data = msw_wind_resp.json()[0]['wind']

    return wind_data

def parse_wind_data(wind_data):

    wind_dir_deg = wind_data['direction']

    return {
        'wind_speed': wind_data['speed'],
        'wind_gust': wind_data['gusts'],
        'wind_dir_deg': wind_dir_deg,
        'wind_dir_comp': wind_data['compassDirection'],
        'wind_unit': wind_data['unit'],
        'wind_arrow_deg': get_arrow_degrees(wind_dir_deg),
    }

def get_global_degrees(degrees):

    """
    convert degress from API (rotate 180)
    """

    degreesGlobal = (degrees + 180.0) % 360
    degreesGlobal = round(degreesGlobal, 2)

    return degreesGlobal

def get_arrow_degrees(degrees):

    """
    find nearest 5 degree increment to get arrow sprite from api.
    """

    if degrees % 5 == 0:
        degrees = degrees
    else:
        if degrees % 5 >= 3:
            degrees = degrees +  (5 -(degrees % 5))
        if degrees % 5 < 3:
            degrees = degrees - (degrees % 5)

    return int(degrees)
