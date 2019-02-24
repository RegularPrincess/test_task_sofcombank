from openpyxl import load_workbook
import logging
from models.Request import Request
from db import DB
import config as cfg


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
        db.insert_request(r)
        i+=1
        next_str = sheet_ranges[i]


def main(argv):
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    db = DB()
    if db.request_table_is_empty():
        logging.info('Table request is empty. Filling...')
        xslx_to_db()


if __name__ == '__main__':
    import sys
    main(sys.argv[0:])
