import os
import subprocess
import sys
import tempfile

from myutil.fileutil import ZipFile


def main():
    try:
        file1, file2, win_merge_path = sys.argv[1:4]
    except ValueError:
        print("使用法: getwardiff.exe <file1> <file2> <win_merge_path>")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            folder1, folder2 = tmp_dir + "/file1", tmp_dir + "/file2"
            os.mkdir(folder1)
            os.mkdir(folder2)

            print(f"{file1}を解凍しています...")
            ZipFile(file1).extract_all(folder1)
            print(f"{file2}を解凍しています...")
            ZipFile(file2).extract_all(folder2)

            kportal_jar="/WEB-INF/lib/kportal-1.0.0-main.jar"
            print("kportal-1.0.0-main.jarを解凍しています...")
            ZipFile(folder1 + kportal_jar).extract_all()
            ZipFile(folder2 + kportal_jar).extract_all()

            print("WinMergeで差分を表示します。WinMergeを終了すると展開後のファイルは削除されます。")
            subprocess.run([win_merge_path, folder1, folder2, "/r"])
            print("展開後のファイルを削除しています...")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
