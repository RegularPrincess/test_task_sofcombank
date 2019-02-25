import json
import logging

import requests

from db.db import DB
from models.region import Region
from models.result import Result
from to_db_utils import district_to_db
import Levenshtein as lv
from models.search_form import SearchForm
import utilits as utils


def get_or_downlod_districts(region_code):
    db = DB()
    if db.region_has_districts(region_code):
        return db.get_all_districts_by_region(region_code)
    else:
        district_to_db(region_code)
        return db.get_all_districts_by_region(region_code)


def search_house(search_form):
    payload = utils.create_form_data(search_form.__dict__)
    res = requests.post('https://extra.egrp365.ru/api/extra/index.php', data=payload.encode('utf-8'), headers=utils.HEADERS)
    try:
        json_data = json.loads(res.text)
        if json_data['success']:
            db = DB()
            for x in json_data['data']:
                result = Result()
                result.cadastral = x['cn']
                result.adress = x['address']
                db.insert(result, 'result')
                result.cadastral_map = get_house_detaile(result.cadastral)
    except Exception as e:
        logging.error('Region loading error. Response text: ' + res.text)
        raise e
    pass


def search_flat(search_form):
    pass


def search_in_region(request, cur_region_code):
    districts = get_or_downlod_districts(cur_region_code)
    dists = []
    for d in districts:
        dist = lv.distance(request.city, d.name)
        dists.append((dist, d.value, d.name))
    s = min(dists, key=lambda p: p[0])
    if s[0] > 2:
        logging.info('Not found match for "{}"\n'.format(request.city))
        # start search on the main page
        return
    logging.info('Found match for "{}" is "{}" with dist = {}\n'.format(request.city, s[2], s[0]))
    cur_distinct_code = s[1]
    search_form = SearchForm()
    search_form.macroRegionId = cur_region_code
    search_form.regionId = cur_distinct_code
    search_form.street = request.street
    search_form.house = request.house
    search_form.building = request.block
    search_form.apartment = request.flat
    if request.kind_premises == 'Дом':
        search_house(search_form)
    else:
        search_flat(search_form)


def search_in_city(request, cur_region_code):
    pass


def search(request):
    db = DB()
    regions = db.get_all_regions()
    cur_region = request.region
    dists = []
    for r in regions:
        dist = lv.distance(cur_region, r.name)
        dists.append((dist, r.value, r.name))
    s = min(dists, key=lambda p: p[0])
    logging.info('Found match for "{}" is "{}" with dist = {}'.format(cur_region, s[2], s[0]))
    cur_region_code = s[1]
    if ' г' in cur_region:
        search_in_city(request, cur_region_code)
    else:
        search_in_region(request, cur_region_code)

    # cur_region.name = cur_region.name.replace(' г', '', 1)


def search_all():
    db = DB()
    requests = db.get_all_requests()
    for request in requests:
        search(request)


def search_by_id(request_id):
    db = DB()
    request = db.get_request_by_id(request_id)
    search(request)

