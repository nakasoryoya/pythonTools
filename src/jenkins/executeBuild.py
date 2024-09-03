import time
import tkinter as tk

import requests


def show_input_dialog():
    root = tk.Tk()
    root.title('環境設定')
    root.geometry('400x100')
    input_db_server_label = tk.Label(text='DBサーバー名')
    input_db_server_label.grid(row=1, column=1, padx=10)

    input_db_server = tk.Entry(width=30)
    input_db_server.grid(row=1, column=2)

    input_db_port_label = tk.Label(text='ポート')
    input_db_port_label.grid(row=1, column=3, padx=10)

    input_db_port = tk.Entry(width=4)
    input_db_port.grid(row=1, column=4)

    input_sys_db_label = tk.Label(text='システムデータベース')
    input_sys_db_label.grid(row=2, column=1, padx=10)

    input_sys_db = tk.Entry(width=30)
    input_sys_db.grid(row=2, column=2)

    input_tenant_db_label = tk.Label(text='テナントデータベース')
    input_tenant_db_label.grid(row=3, column=1, padx=10)

    input_tenant_db = tk.Entry(width=30)
    input_tenant_db.grid(row=3, column=2)

    button = tk.Button(text='ビルド実行', command=lambda: main(input_db_server.get(), input_db_port.get(), input_sys_db.get(), input_tenant_db.get(), root))
    button.place(x=180, y=70)

    root.mainloop()


def main(db_server, db_port, sys_db, tenant_db, root):
    base_url = 'http://172.23.144.171:8091'
    jenkins_user = 'admin'
    api_key = '11487ddf7b071f43bfe9605e74d1e80b88'
    imm_job_name = 'local_build_imm'
    war_job_name = 'local_build_war'
    url = f'{base_url}/job/{imm_job_name}/buildWithParameters'
    auth = (jenkins_user, api_key)
    param = {
        'token': 'token',
        'databasehost': db_server,
        'databaseport': db_port,
        'databasenamesystem': sys_db,
        'databasenametenant': tenant_db
    }

    # root内にある全てのウィジェットを取得
    widgets = root.winfo_children()
    for widget in widgets:
        widget.destroy()

    # rootにメッセージを表示
    building = tk.Label(root, text='ビルド中です...')
    building.pack()
    root.update()

    requests.post(url, auth=auth, params=param)

    url = f'{base_url}/queue/api/json'
    res = requests.get(url, auth=auth).json()
    queue_id = None
    for tasks in res['items']:
        if tasks['task']['name'] == 'local_build_imm':
            queue_id = tasks['id']
            break

    url = f'{base_url}/queue/item/{queue_id}/api/json'
    while True:
        res = requests.get(url, auth=auth).json()
        if 'executable' in res:
            imm_build_no = res['executable']['number']
            break
        time.sleep(1)

    url = f'{base_url}/job/{imm_job_name}/{imm_build_no}/api/json'
    while True:
        res = requests.get(url, auth=auth).json()
        if res['building'] is False:
            build_status = res['result']
            break
        time.sleep(10)

    # ビルドが失敗した場合は終了
    if build_status == 'FAILURE':
        building.destroy()
        tk.Label(root, text='ビルドに失敗しました。').pack()
        root.attributes('-topmost', True)
        root.update()
        return

    while True:
        url = f'{base_url}/job/{war_job_name}/api/json'
        res = requests.get(url, auth=auth).json()
        last_build_no = res['lastBuild']['number']
        url = f'{base_url}/job/{war_job_name}/{last_build_no}/api/json'
        res = requests.get(url, auth=auth).json()
        if res['building'] is True:
            war_build_no = last_build_no
            break
        time.sleep(1)

    url = f'{base_url}/job/{war_job_name}/{war_build_no}/api/json'
    while True:
        res = requests.get(url, auth=auth).json()
        if res['building'] is False:
            build_status = res['result']
            break
        time.sleep(10)

    if build_status == 'SUCCESS':
        url = f'{base_url}/job/{war_job_name}/{war_build_no}/artifact/kpportal.war'
        res = requests.get(url, auth=auth)
        with open('kpportal.war', 'wb') as f:
            f.write(res.content)

    building.destroy()
    tk.Label(root, text='ビルドが完了しました。').pack()
    root.attributes('-topmost', True)
    root.update()


if __name__ == "__main__":
    show_input_dialog()
