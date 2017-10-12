#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from slack_helper import SlackHelper

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename='/var/log/s3_sync.log')
slack = SlackHelper()

def get_year_str():
    return datetime.today().strftime("%Y")

def get_month_str():
    return datetime.today().strftime("%m")

# return the date with YYYYMMDD format
def get_today_str():
    return datetime.today().strftime("%Y%m%d")

def generate_file_path(path):
    return path + '/' + get_year_str() + '/' + get_month_str()

# this method support to generate file name pattern: {prefix}_{accountId}_{yyyyMMdd}_{H}_{num}.{extension}
def generate_file_name(prefix, account_id, counter, extension):
    hour_current_str = datetime.today().strftime("%H")
    today_str = datetime.today().strftime("%Y%m%d")
    file_name = "{0}_{1}_{2}_{3}_{4}{5}".format(prefix, today_str, hour_current_str, str(counter).zfill(2), account_id, extension)
    return file_name

def debug(msg):
    print msg
    logging.debug(msg)

def info(msg):
    print msg
    logging.info(msg)

def error(msg):
    print msg
    #do not need to send the notification message because there are many unused accounts
    if "can't access to accountId with your token." not in msg:
        slack.send_msg(msg)
    logging.error(msg)