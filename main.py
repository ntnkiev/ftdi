import tkinter as tk
from tkinter import PhotoImage
from find_ft232h import find_ft232h
from lcd_i2c import LCD
import datetime

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

backlight_var = tk.IntVar()
backlight = tk.Checkbutton(win, text="Backlight", font=("Arial", 12), variable=backlight_var,
                           command=lambda: display.backlight(backlight_var.get()))
cursor_var = tk.IntVar()
cursor = tk.Checkbutton(win, text="Cursor", font=("Arial", 12), variable=cursor_var,
                        command=lambda: display.cursor(cursor_var.get()))


def text_send():
    display.clear()
    display.set_cursor(0, 0)
    display.write(text.get("1.0", "end-1c"))


text = tk.Text(win, font=("Cascadia Mono", 12), width=16, height=2)
text.place(x=10, y=70)
text.bind("<Key>", on_input)
button_send = tk.Button(win, text="Send", font=("Arial", 12), command=text_send)
button_send.place(x=107, y=120)

cursor.place(x=10, y=40)
backlight.select()
backlight.place(x=10, y=10)

win.mainloop()
