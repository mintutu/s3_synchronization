import sys
import json
from modules import S3Helper
from modules import LineHelper
from modules import constants
from modules.common import get_today_str, generate_file_name


def synchronize_report_data(accountId, url, prefix):
    start_index = 1
    counter = 0
    line_helper = LineHelper(url, max_result=20000)

    while(True):
        payload = {'startDate': get_today_str(), 'endDate': get_today_str(),
                   'accounts': [accountId], 'reportType': 'CAMPAIGN', 'start': start_index, 'results': line_helper.max_result}

        response = line_helper.get_data_from_line(payload)
        decoded_response = response.text.encode("utf-8")

        if len(decoded_response.split('\n')) <= 2:
            print 'finish'
            break

        counter += 1
        file_name = generate_file_name(prefix, accountId, counter, '.tsv')
        file_path = '/tmp/' + file_name

        # write file and push to S3
        with open(file_path, 'wb') as f:
            f.write(decoded_response)
        print 'push file ' + file_name
        # put_file_to_s3(file_path, PREFIX + '/' + file_name)
        start_index += line_helper.max_result


def synchronize_structure_data(accountId, url, prefix):
    start_index = 1
    counter = 0
    line_helper = LineHelper(url)
    s3_helper = S3Helper()

    while(True):
        counter += 1
        payload = {'accountId': accountId, 'removed': False, 'start': start_index,
                   'results': line_helper.max_result, 'sortType': 'ASC', 'sortKey': 'ID'}
        response = line_helper.get_data_from_line(payload)
        decoded_response = response.json()
        current_records = len(decoded_response["operands"])

        file_name = generate_file_name(prefix, accountId, counter, '.json')
        file_path = '/tmp/' + file_name

        # write file and push to S3
        with open(file_path, 'wb') as out:
            json.dump(decoded_response, out, sort_keys=True,
                      indent=4, separators=(',', ': '))
        print 'push file ' + file_name
        s3_helper.put_file_to_s3(file_path, prefix + '/' + file_name)
        start_index += line_helper.max_result

        if current_records < line_helper.max_result:
            print 'finish'
            break


if __name__ == '__main__':
    synchronize_report_data(
        1256, constants.REPORT_CAMPAIGN_URL, constants.REPORT_CAMPAIGN_PREFIX)
    synchronize_structure_data(
        1256, constants.MEDIA_URL, constants.MEDIA_PREFIX)
