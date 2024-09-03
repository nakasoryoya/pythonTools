import pyautogui
import pygetwindow as gw
from pywinauto.application import Application


def send_key(key, window_title=None):
    if window_title:
        activate_window(window_title)
    pyautogui.write(key)


def activate_window(window_title):
    all_windows = gw.getAllTitles()
    matching_windows = [title for title in all_windows if window_title in title]
    if matching_windows:
        # 最初に見つかったウィンドウをアクティブにする
        window_title = matching_windows[0]
        window = gw.getWindowsWithTitle(window_title)[0]
        app = Application().connect(handle=window._hWnd)
        app.top_window().set_focus()
