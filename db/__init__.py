import config as cfg
import db.sql as s
import psycopg2

CONN_STR = "host={} dbname={} user={} password={}" \
    .format(cfg.host, cfg.dbname, cfg.user, cfg.password)

with psycopg2.connect(CONN_STR) as connection:
    cursor = connection.cursor()
    sql = s.create_request
    cursor.execute(sql)

    sql = s.create_region_code
    cursor.execute(sql)

    sql = s.create_district_code
    cursor.execute(sql)

    sql = s.create_localy_code
    cursor.execute(sql)

    sql = s.create_notify_func
    cursor.execute(sql)

    sql = s.drop_notify_trigger
    cursor.execute(sql)

    sql = s.create_notify_trigger
    cursor.execute(sql)

    sql = s.create_result_table
    cursor.execute(sql)
    connection.commit()

    cursor.close()
