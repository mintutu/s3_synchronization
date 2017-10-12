#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configuration
from slackclient import SlackClient

class SlackHelper:

    def __init__(self):
        self.client = SlackClient(configuration.SLACK_API_TOKEN)
        pass

    def send_msg(self, msg, channel = '#p4l_supervisor_dev'):
        try:
            self.client.api_call('chat.postMessage', username='S3-Sync-Bot', icon_emoji=':robot_face:', channel=channel,
                                 text='[S3-Sync] ' + msg)
        except Exception, e:
            print e

