from threading import Thread
import logging
import time

from db.db import DB


class SearchShedule(Thread):
    def __init__(self, searcher):
        Thread.__init__(self)
        self.queue = []
        self.searcher = searcher

    def append_request(self, request_id):
        db = DB()
        request = db.get_request_by_id(request_id)
        if request.try_num < 3:
            logging.info('Add request to shedule id: ' + str(request_id))
            self.queue.append(request)
        else:
            db.set_not_found(request_id)

    def run(self):
        while 1:
            for q in self.queue:
                logging.info('Run sheduled search for id: ' + str(q.id))
                self.searcher(q)
            time.sleep(60)
