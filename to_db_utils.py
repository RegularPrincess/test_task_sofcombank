import json

import logging
import requests
from openpyxl import load_workbook

import config as cfg
from db.db import DB
from models.district import District
from models.region import Region
from models.request import Request
import utilits as utils


def regions_to_db():
    fields = {'method': 'getRegionsList'}
    payload = utils.create_form_data(fields)
    res = requests.post('https://extra.egrp365.ru/api/extra/index.php', data=payload, headers=utils.HEADERS)
    try:
        json_data = json.loads(res.text)
        if json_data['success']:
            db = DB()
            for x in json_data['data']:
                region = Region(value=x['value'], name=x['name'])
                db.insert(region, 'region_code')
    except Exception as e:
        logging.error('Region loading error. Response text: ' + res.text)
        raise e


def xslx_to_db():
    wb = load_workbook(filename=cfg.request_xls_file_path)
    sheet_ranges = wb.get_active_sheet()
    i = 2
    next_str = sheet_ranges[i]
    while next_str[0].value:
        r = Request()
        r.kind_premises = next_str[0].value
        r.post_code = next_str[1].value
        r.region = next_str[2].value
        r.city_type = next_str[3].value
        r.city = next_str[4].value
        r.street_type = next_str[5].value
        r.street = next_str[6].value
        r.house = next_str[7].value
        r.block = next_str[8].value
        r.flat = next_str[9].value
        r.adress = next_str[10].value
        db = DB()
        db.insert(r, 'request')
        i += 1
        next_str = sheet_ranges[i]


def district_to_db(region_value):
    fields = {'method': 'getRegionsList',
              'region': region_value}
    payload = utils.create_form_data(fields)
    res = requests.post('https://extra.egrp365.ru/api/extra/index.php', data=payload, headers=utils.HEADERS)
    try:
        json_data = json.loads(res.text)
        if json_data['success']:
            db = DB()
            for x in json_data['data']:
                district = District (value=x['value'], name=x['name'], region_value=region_value)
                db.insert(district, 'district_code')
    except Exception as e:
        logging.error('District loading error. Response text: ' + res.text)
        raise e
