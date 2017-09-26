#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from time import sleep


class LineHelper:

    def __init__(self, line_api_url, max_result=100):
        self.line_api_url = line_api_url
        self.max_result = max_result
        self.MAX_RETRY_TIME = 4

    def read_line_access_token(self):
        file = open(
            '/opt/pyxis/p4l/line-credential/line_access_token.conf', 'r')
        for line in file.readlines():
            if "p4l.line.accessToken" in line:
                idx = line.strip().split("p4l.line.accessToken=")
                return idx[1]

    def get_data_from_line(self, payload, retry_time=0):
        if retry_time == self.MAX_RETRY_TIME:
            return
        url = self.line_api_url
        line_token = self.read_line_access_token()

        headers = {'Authorization': 'Bearer ' +
                   line_token, 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload), stream=True)
        if response.status_code != 200:
            print response
            sleep(0.5)
            get_data_from_line(payload, retry_time + 1)
        return response
