import psycopg2
from models.request import Request
from models.region import Region
from models.district import District

import logging
import config as cfg
from models.result import Result


class DB(object):
    def __init__(self):
        conn_str = "host={} dbname={} user={} password={}" \
            .format(cfg.host, cfg.dbname, cfg.user, cfg.password)
        try:
            self._db_connection = psycopg2.connect(conn_str)
            self._db_cur = self._db_connection.cursor()
        except psycopg2.Error as e:
            logging.error('Error in connection string or other connection error')
            raise e

    def _row_to_request(self, row):
        request = Request()
        request.id = row[0]
        request.kind_premises = row[1]
        request.post_code = row[2]
        request.region = row[3]
        request.city_type = row[4]
        request.city = row[5]
        request.street_type = row[6]
        request.street = row[7]
        request.house = row[8]
        request.block = row[9]
        request.flat = row[10]
        request.adress = row[11]
        request.try_num = row[12]
        return request

    def query(self, query, params):
        self._db_cur.execute(query, params)
        self._db_connection.commit()

    def insert(self, obj, table_name):
        fields_dict = obj.__dict__
        part_of_sql = "({}) VALUES({})"
        i = 0
        values = ()
        for key, value in fields_dict.items():
            i += 1
            values += (value,)
            if i < len(fields_dict):
                part_of_sql = part_of_sql.format(key + ', {}', '%s' + ', {}')
            else:
                part_of_sql = part_of_sql.format(key, '%s')
        sql = "INSERT INTO {} {};".format(table_name, part_of_sql)
        logging.info(sql)
        logging.info('; '.join(str(x) for x in values))
        self.query(sql, values)

    def get_all_requests(self):
        self._db_cur.execute('SELECT * FROM request', ())
        requests = []
        row = self._db_cur.fetchone()
        while row:
            request = self._row_to_request(row)
            requests.append(request)
            row = self._db_cur.fetchone()
        return requests

    def get_request_by_id(self, id):
        self._db_cur.execute('SELECT * FROM request WHERE id = %s', (id,))
        row = self._db_cur.fetchone()
        request = self._row_to_request(row)
        return request

    def table_is_empty(self, table_name):
        self._db_cur.execute('select not exists (select 1 from {})'.format(table_name))
        return self._db_cur.fetchone()[0]

    def region_has_districts(self, region_value):
        self._db_cur.execute('select exists (select 1 from district_code d WHERE d.region_value = %s)', (region_value,))
        return self._db_cur.fetchone()[0]

    def get_all_regions(self):
        self._db_cur.execute('SELECT * FROM region_code', ())
        regions = []
        row = self._db_cur.fetchone()
        while row:
            region = Region(row[0], row[1])
            regions.append(region)
            row = self._db_cur.fetchone()
        return regions

    def get_all_districts_by_region(self, region_value):
        self._db_cur.execute('SELECT * FROM district_code d WHERE d.region_value = %s', (region_value,))
        districts = []
        row = self._db_cur.fetchone()
        while row:
            district = District(row[0], row[1], row[2])
            districts.append(district)
            row = self._db_cur.fetchone()
        return districts

    def increase_try_num(self, request_id):
        self.query('UPDATE request SET try_num = request.try_num + 1 WHERE id = %s;', (request_id,))

    def set_not_found(self, request_id):
        self.query('UPDATE request SET not_found = TRUE WHERE id = %s;', (request_id,))

    def count_of_found(self):
        self._db_cur.execute('SELECT count(*) FROM request r WHERE not r.not_found')
        res = self._db_cur.fetchone()
        return res[0]

    def count_of_not_found(self):
        self._db_cur.execute('SELECT count(*) FROM request r WHERE r.not_found')
        res = self._db_cur.fetchone()
        return res[0]

    def get_all_results(self):
        self._db_cur.execute('SELECT * FROM result', ())
        results= []
        row = self._db_cur.fetchone()
        while row:
            result = Result()
            result.request_id = row[1]
            result.adress = row[3]
            result.square = row[6]
            result.region_id = row[8]
            results.append(result)
            row = self._db_cur.fetchone()
        return results

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()

