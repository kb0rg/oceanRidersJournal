import os
import jinja2
import requests
import json

"""
module for functions relating to calls to magicseaweed.com api 
"""

"""
remember to source keys .sh file to set tokens as env variables
for each terminal session.
"""

MSW_API_KEY = os.environ['MSW_ACCESS_TOKEN']
# base URL for MSW API requests (adding spot_id required for all queries)
MSW_API_URL = "http://magicseaweed.com/api/"+MSW_API_KEY+"/forecast/?spot_id="

"""
api call TODO:
-> find response by time closest to time of query?
(for now, filtering out FIRST index of list from response)

More calls:
-> air temp: condition.temperature
-> wave heights: minBreakingHeight, maxBreakingHeight

Other calls (stretch goal):
-> ratings?: fadedRating, solidRating
-> ? weather icon?: condition.weather
-> charts?: charts.swell, charts.period, charts.wind
(I'd have to save and store these)

"""

def getUrlBySpot(spot_id):
    
    url_base = MSW_API_URL +str(spot_id)+"&units=us"
    print "MSW_API_URL with spot_id added is: ", url_base

    return url_base   


def getSwell1(spot_id):

    """
    make call to magicseaweed API to get swell info for journal entry.
    """

    url_base = getUrlBySpot(spot_id)
    # print "MSW_API_URL with spot_id is: ", url_base

    """
    ## example query gets all forecast for given spot_id
    # msw_resp = requests.get(url_base)
    # msw_json_list = msw_resp.json()
    # msw_json_obj = msw_json[0]
    """

    # request all attr of primary swell data
    url_swell1 = url_base + "swell.components.primary.*"
    msw_swell1_resp = requests.get(url_swell1)
    msw_swell1_json_list = msw_swell1_resp.json()
    msw_swell1_json_obj = msw_swell1_json_list[0]
    return msw_swell1_json_obj


def getWind(spot_id):

    """
    make call to magicseaweed API to get wind info for journal entry.
    """

    url_base = getUrlBySpot(spot_id)

    # request specified attr of wind data
    url_wind = url_base + "wind.speed,wind.direction,wind.compassDirection,wind.unit"
    msw_wind_resp = requests.get(url_wind)
    msw_wind_json_list = msw_wind_resp.json()
    msw_wind_json_obj = msw_wind_json_list[0]
    return msw_wind_json_obj



"""
TODO: need to source other (non MSW) APIs:
-> water temp?
-> tides (chart or info to build chart)
"""
