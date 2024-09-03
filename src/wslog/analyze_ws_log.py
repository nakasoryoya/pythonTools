import os
import sys
import xml.etree.ElementTree as et
from datetime import datetime

import myutil.excelutil as excelutil
import pytz
from myutil.fileutil import Directory


def get_log_info_list(files):
    log_info_list = []
    for file in files:
        log_data = file.get_text()
        root = et.fromstring(log_data)
        namespace = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
        log_user = root.find(".//ns:Data[@Name='TargetUserName']", namespace).text
        log_time = root.find(".//ns:TimeCreated", namespace).attrib['SystemTime'][:19]
        # ログオン時刻を日本時間に変換
        log_time_timezone = datetime.strptime(log_time + "+0000", "%Y-%m-%dT%H:%M:%S%z").astimezone(
            pytz.timezone('Asia/Tokyo'))

        # RenderingInfoタグ配下にあるTaskタグの値を取得
        log_task = root.find(".//ns:RenderingInfo/ns:Task", namespace).text

        log_info_list.append(
            {'log_user': log_user, 'log_time': log_time_timezone, 'log_task': log_task}
        )

    return log_info_list


def group_log_info_list_by_user(log_info_list):
    log_info_dict = dict()
    for log_info in log_info_list:
        if log_info['log_user'] not in list(log_info_dict.keys()):
            log_info_dict[log_info['log_user']] = []

        log_info_dict[log_info['log_user']].append({'log_time': log_info['log_time'], 'log_task': log_info['log_task']})

    return log_info_dict


def group_log_time_by_hour(log_time_list):
    before_log_time = None
    log_start_time = None
    log_time_group = []
    for log_time in log_time_list:
        if not before_log_time:
            log_start_time = log_time['log_time']
        else:
            if (log_time['log_time'] - before_log_time).seconds > 3600:
                log_time_group.append({
                    'log_start_time': log_start_time.strftime('%Y/%m/%d %H:%M:%S'),
                    'log_end_time': before_log_time.strftime('%Y/%m/%d %H:%M:%S')
                })
                log_start_time = log_time['log_time']
            elif log_time_list.index(log_time) == len(log_time_list) - 1:
                log_time_group.append({
                    'log_start_time': log_start_time.strftime('%Y/%m/%d %H:%M:%S'),
                    'log_end_time': log_time['log_time'].strftime('%Y/%m/%d %H:%M:%S')
                })

        before_log_time = log_time['log_time']

    return log_time_group


def main():
    # 第一引数のパスよりログファイルを取得
    files = Directory(sys.argv[1]).get_text_files('txt')
    log_info_list = get_log_info_list(files)
    log_info_dict = group_log_info_list_by_user(log_info_list)

    wb = excelutil.WorkBook()
    for user in log_info_dict.keys():
        log_time_list = log_info_dict[user]
        log_time_list.sort(key=lambda x: x['log_time'])
        log_time_group = group_log_time_by_hour(log_time_list)
        wb.create_worksheet(user).output_dictionary_to_excel(log_time_group)

    wb.delete_worksheet('Sheet')
    out_path = f'{os.path.dirname(os.path.abspath(sys.argv[0]))}/out'
    if not os.path.exists(f'{out_path}'):
        os.makedirs(f'{out_path}')

    out_file_name = f'{out_path}/アクセスログ_ユーザ別_{datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")}.xlsx'
    wb.save(out_file_name)
    print('処理が完了しました。')


if __name__ == '__main__':
    main()
