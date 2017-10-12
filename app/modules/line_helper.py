#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import configuration
import constants
from time import sleep
from slack_helper import SlackHelper
from common import info, error

class LineHelper:

    def __init__(self, line_api_url, lock, max_result=100):
        self.line_api_url = line_api_url
        self.max_result = max_result
        self.lock = lock
        self.MAX_RETRY_TIME = 10
        self.LINE_ACCESS_TOKEN_PATH = '/opt/pyxis/p4l/line-credential/line_access_token.conf'

    def read_line_access_token(self):
        file = open(
            '/opt/pyxis/p4l/line-credential/line_access_token.conf', 'r')
        for line in file.readlines():
            if "p4l.line.accessToken" in line:
                idx = line.strip().split("p4l.line.accessToken=")
                return idx[1]

    def check_line_access_token(self):
        line_token = self.read_line_access_token()
        payload = {'accountId': 3962}
        headers = {'Authorization': 'Bearer ' + line_token, 'Content-Type': 'application/json'}
        response = requests.post(constants.CAMPAIGN_URL, headers=headers, data=json.dumps(payload))
        print response.content
        return response.status_code == 200

    def update_line_access_token(self, new_access_token):
        try:
            line = 'p4l.line.accessToken={0}\n'.format(new_access_token)
            with open(self.LINE_ACCESS_TOKEN_PATH, 'w') as configfile:
                configfile.write(line)
        except Exception, e:
            error(e)

    def renew_line_access_token(self):
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'grant_type': 'client_credentials', 'client_id': configuration.LINE_CLIENT_ID,
                       'client_secret': configuration.LINE_CLIENT_SECRET}
            response = requests.post(configuration.LINE_ACCESS_TOKEN_URL, headers=headers, data=payload)
            result_code = response.status_code
            if result_code == 200:
                slack = SlackHelper()
                decoded_response = response.text.encode("utf-8")
                json_response = json.loads(decoded_response, encoding='utf8')
                access_token = json_response['access_token']
                notification_msg = 'Old token is invalid and new token is: {0}'.format(access_token)
                self.update_line_access_token(access_token)
                info(notification_msg)
                slack.send_msg(notification_msg)
        except Exception, e:
            error(e)

    def check_and_renew_token(self):
        self.lock.acquire()
        try:
            if self.check_line_access_token() is False:
                self.renew_line_access_token()
        finally:
            self.lock.release()

    def get_data_from_line(self, payload):
        retry_time = 0
        while True:
            if retry_time == self.MAX_RETRY_TIME:
                error('Retrying too many times, so it will stop get data of {0}'.format(str(payload)))
                return None
            url = self.line_api_url
            line_token = self.read_line_access_token()

            headers = {'Authorization': 'Bearer ' + line_token, 'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
            result_code = response.status_code

            #token is expired
            if result_code == 401:
                self.check_and_renew_token()
            #if your token cannot access accountId, it do not need to retry
            elif result_code == 200 or "can't access to accountId with your token." in response.content:
                return response
            else:
                retry_time += 1
                info('Retry at ' + str(retry_time))
                sleep(1)
