import psycopg2
from models.request import Request
import logging
import config as cfg

CONN_STR = "host={} dbname={} user={} password={}" \
    .format(cfg.host, cfg.dbname, cfg.user, cfg.password)

with psycopg2.connect(CONN_STR) as connection:
    cursor = connection.cursor()
    sql = """create table IF NOT EXISTS request
        (
	    id serial not null
		    constraint request_pkey
			primary key,
	    kind_premises varchar(10) not null,
	    post_code varchar(10),
	    region varchar(50),
	    city_type varchar(10),
	    city varchar(50),
	    street_type varchar(10),
	    street varchar(50),
	    house varchar(50),
	    block varchar(10),
	    flat varchar(10),
	    adress varchar,
	    try_num integer default 0
        );"""
    cursor.execute(sql)

    sql = """create table IF NOT EXISTS region_code
(
	value integer not null
		constraint region_codes_pkey
			primary key,
	name varchar not null
)
;
"""
    cursor.execute(sql)

    sql = """create table IF NOT EXISTS district_code
(
	value integer not null
		constraint district_codes_pkey
			primary key,
	name varchar not null,
	region_value integer not null
		constraint region_value
			references region_code
				on update cascade on delete cascade
)
;
"""
    cursor.execute(sql)

    sql = """create table IF NOT EXISTS locality_code
(
	value integer not null
		constraint locality_code_pkey
			primary key,
	name varchar not null,
	district_value integer not null
		constraint district_value
			references district_code
				on update cascade on delete cascade
)
;"""
    cursor.execute(sql)
    connection.commit()


class DB(object):
    def __init__(self):
        try:
            self._db_connection = psycopg2.connect(CONN_STR)
            self._db_cur = self._db_connection.cursor()
        except psycopg2.Error as e:
            logging.error('Error in connection string or other connection error')
            raise e

    def query(self, query, params):
        res = self._db_cur.execute(query, params)
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
            requests.append(request)
            row = self._db_cur.fetchone()
        return requests

    def table_is_empty(self, table_name):
        self._db_cur.execute('select not exists (select 1 from {})'.format(table_name))
        return self._db_cur.fetchone()[0]

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()
