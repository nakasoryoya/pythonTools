import tkinter as tk
import pyautogui
import pygetwindow as gw
from pywinauto.application import Application


# 指定したウィンドウにキーを送信する
def send_key(input_window_title, input_sen_key):
    window_title = input_window_title.get()
    send_str = input_sen_key.get()
    if window_title:
        activate_window(window_title)
    pyautogui.write(send_str)


# 指定したウィンドウをアクティブにする
def activate_window(window_title):
    all_windows = gw.getAllTitles()
    matching_windows = [title for title in all_windows if window_title in title]
    if matching_windows:
        # 最初に見つかったウィンドウをアクティブにする
        window_title = matching_windows[0]
        window = gw.getWindowsWithTitle(window_title)[0]
        app = Application().connect(handle=window._hWnd)
        app.top_window().set_focus()


# 入力ダイアログを表示
def show_input_dialog():
    root = tk.Tk()
    root.title('keysend')
    root.geometry('300x80')
    input_window_title_label = tk.Label(text='ウィンドウタイトル')
    input_window_title_label.grid(row=1, column=1, padx=10)

    input_window_title = tk.Entry(width=30)
    input_window_title.grid(row=1, column=2)

    input_sen_key_label = tk.Label(text='送信キー')
    input_sen_key_label.grid(row=2, column=1, padx=10)

    input_sen_key = tk.Entry(width=30)
    input_sen_key.grid(row=2, column=2)

    button = tk.Button(text='送信', command=lambda: send_key(input_window_title, input_sen_key))
    button.place(x=140, y=50)

    root.mainloop()


# メイン処理
def main():
    show_input_dialog()


if __name__ == "__main__":
    main()
