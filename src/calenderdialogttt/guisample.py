import tkinter
from datetime import datetime
from tkinter import ttk
from tkinter.simpledialog import Dialog

from tkcalendar import Calendar


class CalenderDialog(Dialog):
    """
    日付選択ダイアログ
    """
    _date: str
    _time: str
    _disp_mode: str
    _initial_value: datetime
    _input_time: ttk.Spinbox
    _calendar: Calendar
    result: bool

    def __init__(self, master: tkinter.Tk = None, title: str = None, disp_mode: str = "date",
                 initial_value: datetime = datetime.now()):
        """

        :param master:tkinter.Tk 親画面
        :param title:str タイトル
        :param disp_mode:str 表示モード "date": 日付のみ "datetime": 日時
        :param initial_value:datetime 初期値
        """
        self._date = ""
        self._time = ""
        self._disp_mode = disp_mode
        self._initial_value = initial_value
        super().__init__(parent=master, title=title)

    def body(self, master) -> None:
        # 初期値設定
        initial_year, initial_month, initial_day = self._initial_value.year, self._initial_value.month, self._initial_value.day
        self._calendar = Calendar(master, showweeknumbers=False, year=initial_year, month=initial_month,
                                  day=initial_day, date_pattern="yyyy/mm/dd")
        self._calendar.grid(sticky="w", row=0, column=0)
        if self._disp_mode == "datetime":
            self._input_time = ttk.Spinbox(master)
            self._input_time.insert(0, self._initial_value.strftime("%H:%M:%S"))
            self.map_event()
            self._input_time.grid(sticky="w", row=1, column=0)

    def map_event(self):
        """各イベント設定"""
        self._input_time.bind("<Key>", self._on_key_press)
        self._input_time.bind("<ButtonRelease-1>", self._on_input_time_click)
        # スピンボタン押下時
        self._input_time.bind("<<Increment>>", lambda e: self._increment_time(1))
        self._input_time.bind("<<Decrement>>", lambda e: self._increment_time(-1))

    def apply(self):
        self._date = self._calendar.get_date()
        if self._disp_mode == "datetime":
            self._time = self._input_time.get()
        else:
            self._time = "00:00:00"

    def ok(self, event=None):
        super().ok(event)
        self.result = True

    def cancel(self, event=None):
        super().cancel(event)
        self.result = False

    def get_date(self) -> datetime:
        return datetime.strptime(self._date, "%Y/%m/%d")

    def get_time(self) -> datetime:
        return datetime.strptime(self._time, "%H:%M:%S")

    def get_datetime(self) -> datetime:
        return datetime.strptime(f"{self._date} {self._time}", "%Y/%m/%d %H:%M:%S")

    def get_datetime_str(self, format="%Y/%m/%d %H:%M:%S") -> str:
        return self.get_datetime().strftime(format)

    def _on_input_time_click(self, event):
        self._edit_time()

    def _edit_time(self):
        cursor_index = self._get_cursor_index()
        start = (cursor_index // 3) * 3
        self._input_time.selection_range(start, start + 2)

        self._input_time.icursor(self._input_time.index(tkinter.SEL_LAST))

    def _on_key_press(self, event):
        key_action_map = {
            "digit": lambda e: self._update_time_digit(int(e.char)),
            "Left": lambda e: self._move_selection(e.keysym),
            "Right": lambda e: self._move_selection(e.keysym),
            "Up": lambda e: self._increment_time(1),
            "Down": lambda e: self._increment_time(-1),
            "Escape": self.cancel,
            "else": lambda e: "break"
        }
        key = "digit" if event.char.isdigit() else event.keysym if event.keysym in key_action_map else "else"

        key_action_map[key](event)
        return "break"

    def _update_time_digit(self, digit):
        selection_start, selection_end = self._get_selection_index()
        selection_val = int(self._input_time.selection_get())
        max_val = 23 if selection_start == 0 else 59

        new_val = selection_val * 10 + digit
        if new_val > max_val:
            new_val = digit

        self._replace_selection(str(new_val).zfill(2))
        self._edit_time()

    def _increment_time(self, increment):
        start, end = self._get_selection_index()
        if self._get_selection_index() == (0, 0):
            self._input_time.icursor(2)
            self._edit_time()

        val = int(self._input_time.selection_get())
        val = (val + increment) % (24 if start == 0 else 60)

        val = str(val).zfill(2)

        self._replace_selection(val)

        self._edit_time()
        return "break"

    def _move_selection(self, vector):
        self._input_time.icursor(self._get_cursor_index() + (3 if vector == "Right" else -3))
        self._edit_time()

    def _get_cursor_index(self):
        return self._input_time.index(tkinter.INSERT)

    def _get_selection_index(self):
        try:
            return self._input_time.index(tkinter.SEL_FIRST), self._input_time.index(tkinter.SEL_LAST)
        except tkinter.TclError:
            return 0, 0

    def _replace_selection(self, val):
        start = self._input_time.index(tkinter.SEL_FIRST)
        self._input_time.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        self._input_time.insert(start, val)


if __name__ == '__main__':
    date = CalenderDialog(disp_mode="datetime")
    if date.result:
        print(date.get_date())
        print(date.get_time())
        print(date.get_datetime_str())
