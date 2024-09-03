import myutil.excelutil as excel
import tkinter as tk


class Workbook:
    def __init__(self, name, is_saved):
        self.Name = name
        self.IsSaved = is_saved


def show_workbook_list(workbook_list):
    root = tk.Tk()
    root.title('Excelブック一覧')
    root.geometry('800x400')
    # チェックボックス付きのリストボックスを作成
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    for workbook in workbook_list:
        listbox.insert(tk.END, ('' if workbook.is_saved() else ' * ') + workbook.name)
    listbox.pack(fill=tk.BOTH, expand=True)

    # ウィンドウを閉じるボタン

    # ブックを閉じるボタン
    close_button = tk.Button(root, text='閉じる',
                             command=lambda: close_workbooks(workbook_list, listbox.curselection(), True, root))

    force_close_button = tk.Button(root, text='強制的に閉じる',
                                   command=lambda: close_workbooks(workbook_list, listbox.curselection(), False, root))
    force_close_button.pack()
    close_button.pack()

    root.mainloop()


def close_workbooks(workbook_list, selected_indices, is_force, root):
    for index in selected_indices:
        workbook_list[index].close(is_force)

    root.destroy()
    main()


def main():
    # 開いているブックの一覧を取得
    workbook_list = excel.get_open_book_list()
    show_workbook_list(workbook_list)


if __name__ == "__main__":
    main()
