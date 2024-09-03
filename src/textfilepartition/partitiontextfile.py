import myutil.fileutil
from tkinter import simpledialog


def main():
    file_path = simpledialog.askstring('ファイルパス入力', 'ファイルパスを入力してください')
    file_path = file_path.replace('\n', '')
    partition_size = int(simpledialog.askstring('分割行数入力', '分割行数を入力してください'))

    current_line=0
    # ファイルを1行ずつ読み込み、partition_size行ごとにファイルを分割する
    with open(file_path, 'r') as f:
        while True:
            text_file = myutil.fileutil.TextFile(f'{file_path}_{current_line//partition_size}.txt')
            text_data = ''
            for i in range(partition_size):
                line = f.readline()
                if not line:
                    break
                text_data += line

            text_file.set_text(text_data)
            text_file.save()

            if not line:
                break

            current_line += partition_size


if __name__ == "__main__":
    main()
