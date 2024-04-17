import tkinter as tk
from tkinter import PhotoImage
from find_ft232h import find_ft232h
from lcd_i2c import LCD
import datetime
import time

display = LCD(find_ft232h())


def on_input(event):
    current_text = text.get("1.0", "end-1c")
    lines = current_text.split('\n')
    if len(lines[-1]) > 16:  # перевірка довжини останньої строки
        text.insert("end", "\n")  # автоматично перевести строку


win = tk.Tk()
win.title("LCD I2C")
win.geometry("800x600")
win.resizable(False, False)
icon = PhotoImage(file="1602.png")
win.iconphoto(False, icon)


def datetime_send():
    if datetime_var.get() == 1:  # Перевірка, чи чекбокс все ще відмічений
        display.set_cursor(0, 0)
        display.write(f"{datetime.date.today().strftime('%Y-%m-%d')}\n{time.strftime('%H:%M:%S')}")
        win.after(100, datetime_send)


def toggle_datetime():
    if datetime_var.get() == 1:
        datetime_send()  # Запуск оновлення дисплею
    else:
        win.after_cancel("datetime_send")  # Спроба зупинити оновлення
        display.clear()  # Очищення дисплею, якщо чекбокс не відмічений


datetime_var = tk.IntVar(value=False)
datetime_cb = tk.Checkbutton(win, text="Show Time", font=("Arial", 12), command=toggle_datetime, variable=datetime_var)
datetime_cb.place(x=10, y=150)

backlight_var = tk.IntVar()
backlight = tk.Checkbutton(win, text="Backlight", font=("Arial", 12), variable=backlight_var,
                           command=lambda: display.backlight(backlight_var.get()))
backlight.select()
backlight.place(x=10, y=10)

cursor_var = tk.IntVar()
cursor = tk.Checkbutton(win, text="Cursor", font=("Arial", 12), variable=cursor_var,
                        command=lambda: display.cursor(cursor_var.get()))
cursor.place(x=10, y=40)


def text_send():
    display.clear()
    display.set_cursor(0, 0)
    display.write(text.get("1.0", "end-1c"))


text = tk.Text(win, font=("Cascadia Mono", 12), width=16, height=2)
text.place(x=10, y=70)
text.bind("<Key>", on_input)
button_send = tk.Button(win, text="Send", font=("Arial", 12), command=text_send)
button_send.place(x=107, y=120)

win.mainloop()
