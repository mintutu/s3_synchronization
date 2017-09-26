from datetime import datetime

# return the date with YYYYMMDD format
def get_today_str():
    return datetime.today().strftime("%Y%m%d")

# this method support to generate file name pattern: {prefix}_{accountId}_{yyyyMMdd}_{H}_{num}.{extension}
def generate_file_name(prefix, accountId, counter, extension):
    hour_current_str = datetime.today().strftime("%H")
    today_str = datetime.today().strftime("%Y%m%d")
    file_name = prefix + '_' + str(accountId) + '_' + today_str + \
        '_' + hour_current_str + '_' + str(counter) + extension
    return file_name
