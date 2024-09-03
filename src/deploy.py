import paramiko
import scp
import sys


def main(args):
    # 入力を受け付け
    print("日付を入力してください。（形式：YYYYMMDD）:")
    deploy_date = input()
    print("ビルド番号を数値で入力してください。:")
    build_number = input()

    with paramiko.SSHClient() as sshc:
        rsa_key = paramiko.RSAKey.from_private_key_file('c:\\Users\\tie306883\\.ssh\\id_rsa1')
        sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshc.connect(hostname='172.23.144.171', pkey=rsa_key)

        # SSHClient()の接続設定を合わせてあげる
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.get('c:\\jenkins_home\\jobs\\tis_kic_it_build_war\\builds\\%buildNo%\\archive\\kpportal.war',
                     f'C:\\deploy\\{deploy_date}#{build_number}\\kpportal.war')


if __name__ == "__main__":
    main(sys.argv)
