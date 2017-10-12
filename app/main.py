#!/usr/bin/python
import time
import argparse
import threading
from sync_thread import SyncThread
from modules import SMDBHelper
from synchronization import Synchronization
from modules.common import info
from modules import SlackHelper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a S3 sync tool')
    parser.add_argument('-i','--input', help='Input account Id (default is all account)',required=False)
    parser.add_argument('-n','--number', help='number of thread (default is 4)',required=False)
    args = parser.parse_args()

    threads_num = 4 #default number thread
    if args.number:
        threads_num = int(args.number)

    start = time.time()
    slack = SlackHelper()
    #Using lock to prevent multiple thread change Line Access Token at the same time, check the line_helper.py
    lock = threading.Lock()

    if args.input:
        account_id = args.input
        info('Starting download account ' + account_id)
        sync = Synchronization(account_id, lock)
        sync.synchronize()
        info('Finish')
    else:
        msg = 'Starting download report and structure data of all accounts'
        slack.send_msg(msg)
        info(msg)
        smdb_helper = SMDBHelper()
        accounts = smdb_helper.get_all_account_data()
        for i in range(threads_num):
            t = SyncThread(accounts, lock)
            t.setDaemon(True)
            t.start()
        accounts.join()
        end = time.time()
        duration = round((end - start) / 60, 2)
        msg = 'Finish task in {0} minute'.format(duration)
        info(msg)
        slack.send_msg(msg)
