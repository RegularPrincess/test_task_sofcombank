import logging
from db.db import DB
from db.insert_listner import Insertlistner

from search import search_all, search_by_id
from to_db_utils import xslx_to_db, regions_to_db


def main(argv):
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    db = DB()
    if db.table_is_empty('request'):
        logging.info('Table request is empty. Filling...')
        xslx_to_db()
    if db.table_is_empty('region_code'):
        logging.info('Table region_code is empty. Filling...')
        regions_to_db()
    search_all()
    insert_listner = Insertlistner(search_by_id)
    insert_listner.start()
    insert_listner.join()


if __name__ == '__main__':
    import sys
    main(sys.argv[0:])
