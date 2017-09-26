#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import boto
import boto.s3
from time import sleep
from boto.s3.key import Key


class S3Helper:

    def __init__(self):
        AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
        AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
        self.MAX_RETRY = 3
        self.bucket_name = 'p4l-development'
        self.conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    def put_file_to_s3(self, source_file, s3_file_name, retry_number=0):
        try:
            bucket = self.conn.get_bucket(self.bucket_name, validate=False)
            k = Key(bucket)
            k.key = s3_file_name
            k.set_contents_from_filename(source_file)
        except Exception, e:
            print e
            if retry_number < self.MAX_RETRY:
                retry_number += 1
                sleep(1)
                self.put_file_to_s3(source_file, s3_file_name, retry_number)
