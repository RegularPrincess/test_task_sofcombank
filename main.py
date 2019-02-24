from openpyxl import load_workbook
import logging
from models.request import Request
from models.region import Region
from db.db import DB
from db.insert_listner import Insertlistner
import config as cfg
import json
import requests


def regions_to_db():
    body = {
        'method': 'getRegionsList',
    }
    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"method\"\r\n\r\ngetRegionsList"
    files = {'file': (None, payload),}
    header = {
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryZMdp8iiQktcHpQah',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Origin': 'https://egrp365.ru',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.96 Safari/537.36'
    }

    res = requests.post('https://extra.egrp365.ru/api/extra/index.php', data=payload, headers=header)
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
        i+=1
        next_str = sheet_ranges[i]


def search(request):
    print('ACCEPT ID: ')
    print(request)


def main(argv):
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    db = DB()
    if db.table_is_empty('request'):
        logging.info('Table request is empty. Filling...')
        xslx_to_db()
    # if db.table_is_empty('region_code'):
    #     logging.info('Table region_code is empty. Filling...')
    #     regions_to_db()
    insert_listner = Insertlistner(search)
    insert_listner.start()
    insert_listner.join()


if __name__ == '__main__':
    import sys
    main(sys.argv[0:])
