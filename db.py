import psycopg2
import models.Request
import logging
import config as cfg

CONN_STR = "host={} dbname={} user={} password={}"\
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

    def insert_request(self, request):
        fields_dict = request.__dict__
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
        sql = "INSERT INTO request {};".format(part_of_sql)
        logging.info(sql)
        logging.info('; '.join(str(x) for x in values))
        self.query(sql, values)

    def get_requests(self):
        self._db_cur.execute('SELECT * FROM "request"', ())
        d = self._db_cur.fetchone()
        print(d)

    def request_table_is_empty(self):
        self._db_cur.execute('select not exists (select 1 from request)')
        return self._db_cur.fetchone()[0]

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()
