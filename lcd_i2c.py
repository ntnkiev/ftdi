import time

import pyftdi.i2c
from pyftdi.i2c import I2cController

COLUMNS = 16
ROWS = 2
LCD_ADDRESS = 0x7c  # LCD

# Instruction set
CLEARDISPLAY = 0x01

ENTRYMODESET = 0x04
ENTRYLEFT = 0x02
ENTRYRIGHT = 0x00
ENTRYSHIFTINCREMENT = 0x01
ENTRYSHIFTDECREMENT = 0x00

DISPLAYCONTROL = 0x08
DISPLAYON = 0x04
DISPLAYOFF = 0x00
CURSORON = 0x02
CURSOROFF = 0x00
BLINKON = 0x01
BLINKOFF = 0x00

FUNCTIONSET = 0x20
_5x10DOTS = 0x04
_5x8DOTS = 0x00
_1LINE = 0x00
_2LINE = 0x08
_8BITMODE = 0x10
_4BITMODE = 0x00


class LCD:
    def __init__(self, url):

        self.column = 0
        self.row = 0
        self.address = LCD_ADDRESS
        self.command = bytearray(2)
        self.i2ccontroller = I2cController()
        self.i2ccontroller.configure(url)
        self.i2c = self.i2ccontroller.get_port(LCD_ADDRESS)

        time.sleep(.05)

        for i in range(3):
            self._command(FUNCTIONSET | _2LINE)
            time.sleep(.01)

        self.on()
        self.clear()

        self._command(ENTRYMODESET | ENTRYLEFT | ENTRYSHIFTDECREMENT)

        self.set_cursor(0, 0)

    def on(self, cursor=False, blink=False):
        if cursor == False and blink == False:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSOROFF | BLINKOFF)
        elif cursor == False and blink == True:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSOROFF | BLINKON)
        elif cursor == True and blink == False:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSORON | BLINKOFF)
        elif cursor == True and blink == True:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSORON | BLINKON)

    def off(self):
        self._command(DISPLAYCONTROL | DISPLAYOFF | CURSOROFF | BLINKOFF)

    def clear(self):
        self._command(CLEARDISPLAY)
        self.set_cursor(0, 0)

    def set_cursor(self, column, row):
        column = column % COLUMNS
        row = row % ROWS
        if row == 0:
            command = column | 0x80
        else:
            command = column | 0xC0
        self.row = row
        self.column = column
        self._command(command)

    def write(self, s):
        for i in range(len(s)):
            time.sleep(.01)
            try:
                self.i2c.write(b'\x40' + s[i].encode('ascii'))
            except pyftdi.i2c.I2cNackError:
                print('I2C Nack Error')
            self.column = self.column + 1
            if self.column >= COLUMNS:
                self.set_cursor(0, self.row + 1)

    def _command(self, value):
        self.command[0] = 0x80
        self.command[1] = value
        try:
            self.i2c.write(self.command)
        except pyftdi.i2c.I2cNackError:
            print('I2C Nack Error')
        time.sleep(.001)


if __name__ == '__main__':
    display = LCD('ftdi://ftdi:232h:1:0xe/1')
    display.on()
    display.clear()
    display.set_cursor(0, 0)
    display.write('Hello World!')