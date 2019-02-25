import os
from threading import Thread
import select
import psycopg2
import psycopg2.extensions
import config as cfg
import logging


class Insertlistner(Thread):
    def __init__(self, listen_function):
        Thread.__init__(self)
        self.listner = listen_function

    def run(self):
        CONN_STR = "host={} dbname={} user={} password={}" \
            .format(cfg.host, cfg.dbname, cfg.user, cfg.password)
        conn = psycopg2.connect(CONN_STR)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        curs = conn.cursor()
        curs.execute("LISTEN insert_notify;")

        logging.info("Waiting for notifications on channel 'insert_notify'")
        while 1:
            if select.select([conn], [], [], 5) == ([], [], []):
                pass
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    this_pid = os.getpid()
                    if notify.pid != this_pid:
                        logging.info("Got NOTIFY: pid: {}, channel: {}, id = {}".format(notify.pid, notify.channel, notify.payload))
                        row_id = int(notify.payload)
                        self.listner(row_id)
