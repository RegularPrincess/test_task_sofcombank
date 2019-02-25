import json
import logging

import requests

from db.db import DB
from models.region import Region
from search_sheadule import SearchShedule
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


def square_search(cadastral):
    res = requests.post('https://egrp365.ru/reestr?egrp={}'.format(cadastral), headers=utils.HEADERS)
    html = res.text
    pattern = 'Площадь — '
    index = html.find(pattern)
    if index != -1:
        index += len(pattern)
        square = ''
        i = 0
        c = html[index + i]
        while c != ' ':
            square += c
            i += 1
            c = html[index + i]
        return square


def search_house(search_form, request_id):
    payload = utils.create_form_data(search_form.__dict__)
    res = requests.post('https://extra.egrp365.ru/api/extra/index.php', data=payload.encode('utf-8'),
                        headers=utils.HEADERS)
    try:
        json_data = json.loads(res.text)
        if json_data['success']:
            db = DB()
            for x in json_data['data']:
                result = Result()
                result.cadastral = x['cn']
                result.adress = x['address']
                result.cadastral_map = 'https://egrp365.ru/map/?kadnum={}'.format(result.cadastral)
                db.insert(result, 'result')
        else:
            SEARCH_SHEDULE.append_request(request_id)

    except Exception as e:
        logging.error('Search error. Response text: ' + res.text)
        raise e


def search_flat(search_form, request_id):
    payload = utils.create_form_data(search_form.__dict__)
    res = requests.post('https://extra.egrp365.ru/api/extra/index.php', data=payload.encode('utf-8'),
                        headers=utils.HEADERS)
    try:
        json_data = json.loads(res.text)
        if json_data['success']:
            db = DB()
            for x in json_data['data']:
                result = Result()
                result.cadastral = x['cn']
                result.adress = x['address']
                result.floor = x['floor']
                result.square = square_search(result.cadastral)
                db.insert(result, 'result')
        else:
            SEARCH_SHEDULE.append_request(request_id)
    except Exception as e:
        logging.error('Search error. Response text: ' + res.text)
        raise e


def search_in_region(request, cur_region_code):
    districts = get_or_downlod_districts(cur_region_code)
    dists = []
    for d in districts:
        dist = lv.distance(request.city, d.name)
        dists.append((dist, d.value, d.name))
    s = min(dists, key=lambda p: p[0])
    if s[0] < 2:
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
            search_house(search_form, request.id)
        else:
            search_flat(search_form, request.id)
    else:
        # it mean that locality too small and need specify district(область) of region
        pass


def search_in_city(request, cur_region_code):
    search_form = SearchForm()
    search_form.macroRegionId = cur_region_code
    search_form.street = request.street
    search_form.house = request.house
    search_form.building = request.block
    search_form.apartment = request.flat
    if request.kind_premises == 'Дом':
        search_house(search_form, request.id)
    else:
        search_flat(search_form, request.id)


def search(request):
    db = DB()
    db.increase_try_num(request.try_num)
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


def search_all():
    db = DB()
    requests = db.get_all_requests()
    for request in requests:
        search(request)


def search_by_id(request_id):
    db = DB()
    request = db.get_request_by_id(request_id)
    search(request)


SEARCH_SHEDULE = SearchShedule(searcher=search)
SEARCH_SHEDULE.start()