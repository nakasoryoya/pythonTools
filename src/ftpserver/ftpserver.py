import customtkinter
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
from customtkinter import CTk
from myutil.fileutil import Directory
from myutil.threadutil import ClosableThread


class App(CTk):

    def __init__(self, server):
        super().__init__()

        self.server = server
        self.button = None
        self.input_user = None
        self.input_password = None

        # メンバー変数の設定
        self.geometry(f'300x100')

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        # テキストボックスを表示する
        self.input_user = customtkinter.CTkEntry(master=self, placeholder_text="ユーザ", width=100)
        self.input_user.grid(row=0, column=0, padx=10, pady=5)

        self.input_password = customtkinter.CTkEntry(master=self, placeholder_text="パスワード", width=100)
        self.input_password.grid(row=0, column=1, padx=10, pady=5)

        # ボタンを表示する
        self.button = customtkinter.CTkButton(master=self, text="追加", command=self.button_function, width=70,
                                              height=10)
        self.button.grid(row=1, column=0, padx=10, pady=5)

    def button_function(self):
        add_user(self.server.handler, self.input_user.get(), self.input_password.get())


def add_user(handler, user, password):
    if handler.authorizer.has_user(user):
        print(f'User {user} already exists')
        return

    root_dir = Directory(f'C:\\tmp\\ftphost\\{user}')
    if not root_dir.exists():
        root_dir.create()

    handler.authorizer.add_user(user, password, root_dir.path, perm='elradfmw')
    print(f'User {user} added')


def ftp_server():
    # 個々の接続を管理するハンドラーを作る
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = pyftpdlib.authorizers.DummyAuthorizer()

    add_user(handler, 'user', 'password')

    # FTPサーバーを立ち上げる
    server = pyftpdlib.servers.FTPServer(("172.30.224.1", 21), handler)
    return server


def main():
    server = ftp_server()
    # FTPサーバーを立ち上げる
    thread = ClosableThread(target=server.serve_forever)
    thread.start()

    app = App(server)
    app.mainloop()
    # サーバーを終了する
    thread.close()


if __name__ == '__main__':
    main()
