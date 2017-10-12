#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from modules import S3Helper
from modules import LineHelper
from modules import constants
from modules.common import get_today_str, generate_file_name, generate_file_path, info, error

class Synchronization:

    def __init__(self, account_id, lock):
        self.account_id = account_id
        self.lock = lock

    def synchronize_report_data(self, url, prefix, path, report_type):
        response = None
        payload = None
        try:
            start_index = 1
            counter = 0
            s3_helper = S3Helper()
            line_helper = LineHelper(url, self.lock, max_result=20000)

            while True:
                payload = {'startDate': get_today_str(), 'endDate': get_today_str(),
                           'accounts': [self.account_id], 'reportType': report_type, 'start': start_index,
                           'results': line_helper.max_result}

                response = line_helper.get_data_from_line(payload)
                if response is None:
                    break
                decoded_response = response.text.encode("utf-8")
                if len(decoded_response.split('\n')) <= 2:
                    break
                counter += 1
                file_name = generate_file_name(prefix, self.account_id, counter, '.tsv')
                file_path = '/tmp/' + file_name

                # write file and push to S3
                with open(file_path, 'wb') as out:
                    out.write(decoded_response)
                s3_helper.put_file_to_s3(file_path, path + '/' + file_name)
                os.remove(file_path)
                start_index += line_helper.max_result
        except Exception, e:
            response_content = '' if response is None else response.content
            error('Cannot download {0} with {1} response {2} because {3}'.format(url, str(payload), str(response_content) , str(e)))

    def synchronize_structure_data(self, url, prefix, path):
        response = None
        payload = None
        try:
            start_index = 1
            counter = 0
            line_helper = LineHelper(url, self.lock)
            s3_helper = S3Helper()
            while True:
                counter += 1
                payload = {'accountId': self.account_id, 'removed': False, 'start': start_index,
                           'results': line_helper.max_result, 'sortType': 'ASC', 'sortKey': 'ID'}
                response = line_helper.get_data_from_line(payload)
                if response is None:
                    break
                decoded_response = response.text.encode("utf-8")
                decoded_json_response = json.loads(decoded_response, encoding='utf8')
                current_records = len(decoded_json_response["operands"])

                file_name = generate_file_name(prefix, self.account_id, counter, '.json')
                file_path = '/tmp/' + file_name

                # write file and push to S3
                if current_records > 0:
                    json_string = json.dumps(decoded_json_response, ensure_ascii=False, indent=4, sort_keys=True).encode('utf8')
                    with open(file_path, 'wb') as out:
                        out.write(json_string)
                    s3_helper.put_file_to_s3(file_path, path + '/' + file_name)
                    os.remove(file_path)
                    start_index += line_helper.max_result

                if current_records < line_helper.max_result:
                    break
        except Exception, e:
            response_content = '' if response is None else response.content
            error('Cannot download {0} with {1} response {2}: {3}'.format(url, str(payload), str(response_content) , str(e)))

    def synchronize(self):
        self.synchronize_report_data(constants.REPORT_URL, constants.REPORT_AD_MEDIA_PREFIX,
                                     generate_file_path(constants.REPORT_AD_MEDIA_PATH), 'AD_MEDIA')

        self.synchronize_structure_data(constants.MEDIA_URL, constants.MEDIA_PREFIX,
                                        generate_file_path(constants.MEDIA_PATH))
        self.synchronize_structure_data(constants.CREATIVE_URL, constants.CREATIVE_PREFIX,
                                        generate_file_path(constants.CREATIVE_PATH))
        self.synchronize_structure_data(constants.AD_URL, constants.AD_PREFIX,
                                        generate_file_path(constants.AD_PATH))
        self.synchronize_structure_data(constants.AD_GROUP_URL, constants.AD_GROUP_PREFIX,
                                        generate_file_path(constants.AD_GROUP_PATH))
        self.synchronize_structure_data(constants.CAMPAIGN_URL, constants.CAMPAIGN_PREFIX,
                                        generate_file_path(constants.CAMPAIGN_PATH))