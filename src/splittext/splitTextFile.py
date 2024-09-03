import math
import os
import sys

import customtkinter
import pyautogui

FONT_TYPE = "meiryo"


class App(customtkinter.CTk):

    def __init__(self, file_path):
        super().__init__()

        self.button = None
        self.textbox = None
        self.canvas = None
        self.file_path = file_path

        # メンバー変数の設定
        self.fonts = (FONT_TYPE, 15)
        x, y = pyautogui.position()
        self.geometry(f'120x70+{x}+{y}')
        self.wm_overrideredirect(True)

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.canvas = customtkinter.CTkCanvas(master=self, highlightthickness=2, highlightbackground="black")
        self.canvas.pack(fill="both", expand=True)

        # テキストボックスを表示する
        self.textbox = customtkinter.CTkEntry(master=self.canvas, placeholder_text="行数", font=(self.fonts, 15),
                                              width=100)
        self.textbox.grid(row=0, column=0, padx=10, pady=5)

        # ボタンを表示する
        self.button = customtkinter.CTkButton(master=self.canvas, text="実行", command=self.button_function,
                                              font=(self.fonts, 15), width=70, height=10)
        self.button.grid(row=1, column=0, padx=10, pady=5)

        self.focus_force()
        self.textbox.focus()

        self.textbox.bind("<FocusOut>", lambda e: self.destroy())
        self.textbox.bind("<Return>", lambda e: self.button_function())
        self.textbox.bind("<Escape>", lambda e: self.destroy())

    def button_function(self):
        line_num = self.textbox.get()
        self.update()
        try:
            split_text_file(self.file_path, line_num)
        except ValueError:
            self.textbox.delete(0, "end")
            return
        self.destroy()


# 入力ダイアログを表示
def show_input_dialog(file_path):
    app = App(file_path)
    app.mainloop()


def split_text_file(file_path, line_num):
    try:
        line_num = int(line_num)
    except ValueError:
        raise ValueError()

    target_directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name = file_name.split('.')[0] + '_{i}.' + file_name.split('.')[1]
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), line_num):
            with open(os.path.join(target_directory, file_name.format(i=math.ceil(i / line_num) + 1)), 'w') as wf:
                wf.writelines(lines[i:i + line_num])


def main():
    if len(sys.argv) == 1:
        sys.exit(1)
    show_input_dialog(sys.argv[1])


if __name__ == "__main__":
    main()
