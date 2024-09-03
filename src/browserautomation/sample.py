import time
import tkinter as tk
from tkinter import Label

from selenium import webdriver  # Webブラウザを自動操作する（python -m pip install selenium)
from selenium.webdriver.chrome.options import Options  # オプションを使うために必要

global is_black_window_shown


def show_black_window():
    global black_window
    global label
    black_window = tk.Tk()
    black_window.attributes('-fullscreen', True)
    black_window.attributes('-topmost', True)
    black_window.configure(bg='black')

    label = Label(black_window, text="Loading", bg='black', fg='white', font=("Helvetica", 22))
    label.pack(expand=True)
    black_window.update()


def hide_black_window():
    global black_window
    black_window.destroy()


def update_label(text):
    global black_window
    global label
    label['text'] = text


option = Options()  # オプションを用意
option.add_argument('--incognito')  # シークレットモードの設定を付与
option.add_experimental_option("detach", True)

show_black_window()
driver = webdriver.Chrome(options=option)  # Chromeを準備(optionでシークレットモードにしている）

driver.get('https://www.google.com/')  # Googleを開く
driver.fullscreen_window()  # フルスクリーン表示
hide_black_window()
time.sleep(3)  # 3秒待機
show_black_window()
update_label("Loading...")
driver.get('https://www.yahoo.co.jp/')  # Yahooを開く
driver.fullscreen_window()  # フルスクリーン表示

hide_black_window()
