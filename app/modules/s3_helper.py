#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import boto.s3
import configuration
from time import sleep
from boto.s3.key import Key
from common import error, info

class S3Helper:

    def __init__(self):
        self.MAX_RETRY = 3
        self.bucket_name = configuration.AWS_BUCKET_NAME
        self.conn = boto.connect_s3(configuration.AWS_ACCESS_KEY_ID, configuration.AWS_SECRET_ACCESS_KEY)

    def put_file_to_s3(self, source_file, s3_file_name, retry_number=0):
        try:
            info('put file ' + source_file + ' to s3')
            bucket = self.conn.get_bucket(self.bucket_name, validate=False)
            k = Key(bucket)
            k.key = s3_file_name
            k.set_contents_from_filename(source_file)
        except Exception, e:
            error(e)
            if retry_number < self.MAX_RETRY:
                retry_number += 1
                sleep(1)
                self.put_file_to_s3(source_file, s3_file_name, retry_number)
