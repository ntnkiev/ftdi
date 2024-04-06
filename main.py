import tkinter as tk
from tkinter import PhotoImage
from find_ft232h import find_ft232h
from lcd_i2c import LCD

display = LCD(find_ft232h())

win = tk.Tk()
win.title("LCD I2C")
win.geometry("800x600")
win.resizable(False, False)
icon = PhotoImage(file="1602.png")
win.iconphoto(False, icon)

backlight_var = tk.IntVar()
backlight = tk.Checkbutton(win, text="Backlight", font=("Arial", 12), variable=backlight_var,
                           command=lambda: display.backlight(backlight_var.get()))
backlight.select()
backlight.place(x=10, y=10)

win.mainloop()
