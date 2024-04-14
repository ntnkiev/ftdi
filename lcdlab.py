import time
import datetime
import pyftdi.i2c
from find_ft232h import find_ft232h

# LCD thru I2C PCF8574 pinout:
# D0: RS
# D1: RW
# D2: E
# D3: Backlight
# D4: D4
# D5: D5
# D6: D6
# D7: D7

RS = 0x01
RW = 0x02
E = 0x04
BL = 0x08

COLUMNS = 16
ROWS = 2
LCD_ADDRESS = 0x27  # LCD

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

I2C_CLOCK = 100000


class LCD:
    def __init__(self, url):

        self.i2c = pyftdi.i2c.I2cController()
        self.i2c.configure(url, frequency=I2C_CLOCK)
        self.port = self.i2c.get_port(LCD_ADDRESS)

        self.column = 0
        self.row = 0
        self.command = bytearray(1)
        self.init_sequence = True

        time.sleep(.05)

        for i in range(3):
            self._command(FUNCTIONSET | _8BITMODE)
            time.sleep(.01)
        self._command(FUNCTIONSET | _2LINE)
        self.init_sequence = False

        self.on()
        self.clear()

        self._command(ENTRYMODESET | ENTRYLEFT | ENTRYSHIFTDECREMENT)

        self.set_cursor(0, 0)

    def on(self, cursor=False, blink=False):
        if cursor is False and blink is False:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSOROFF | BLINKOFF)
        elif cursor is False and blink is True:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSOROFF | BLINKON)
        elif cursor is True and blink is False:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSORON | BLINKOFF)
        elif cursor is True and blink is True:
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

    def backlight(self, state):
        if state:
            self.port.write([BL])
        else:
            self.port.write([0])

    def cursor(self, state):
        if state:
            self._command(DISPLAYCONTROL | CURSORON | BLINKON | DISPLAYON)
        else:
            self._command(DISPLAYCONTROL | CURSOROFF | BLINKOFF | DISPLAYON)

    def write(self, s):
        lcd_data = []
        for i in range(len(s)):
            if s[i] == '\n':
                self.set_cursor(0, self.row + 1)
                continue
            data = ord(s[i])
            wdata = (data & 0xF0) | BL | RS
            lcd_data.append(wdata | E)
            lcd_data.append(wdata)
            wdata = (data << 4) & 0xF0 | BL | RS
            lcd_data.append(wdata | E)
            lcd_data.append(wdata)
        try:
            self.port.write(lcd_data)
        except pyftdi.i2c.I2cNackError:
            print('I2C Nack Error')
        self.column = self.column + 1
        if self.column >= COLUMNS:
            self.set_cursor(0, self.row + 1)

    def _command(self, value):
        self.command = value
        try:
            wcommand = (self.command & 0xF0) | BL
            self.port.write([wcommand | E])
            self.port.write([wcommand])
            if not self.init_sequence:
                wcommand = (self.command << 4) & 0xF0 | BL
                self.port.write([wcommand | E])
                self.port.write([wcommand])
        except pyftdi.i2c.I2cNackError:
            print('I2C Nack Error')
        time.sleep(.001)


if __name__ == '__main__':
    display = LCD(find_ft232h())
    display.on()
    display.clear()
    display.set_cursor(0, 0)
    display.write('Hello, World!')
    # display.write(datetime.date.today().strftime('%Y-%m-%d'))
    # display.set_cursor(0, 1)
    # display.write(time.strftime('%H:%M:%S'))
    # display.on()
