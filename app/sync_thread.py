#!/usr/bin/python
import threading
from synchronization import Synchronization
from modules.common import info

class SyncThread(threading.Thread):
    """Threaded Synchronize Account from Line to S3"""

    def __init__(self, queue, lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock

    def run(self):
        while True:
            # gets the account_id from the queue
            account_id = self.queue.get()
            name = threading.currentThread().getName()
            info('Thread ' + name + ' process ' + account_id)
            sync_account = Synchronization(account_id, self.lock)
            sync_account.synchronize()
            self.queue.task_done()

