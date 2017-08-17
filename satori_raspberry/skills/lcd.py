"""
Follow the instruction to setup.
I2C interface: https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/appendix-1-i2c-configuration-sensor-kit-v2-0-for-b-plus.html

LCD: Sunfounder LCD1602
"""
import time
import smbus2

from satori_raspberry.skills.base import Skill as BaseSkill

BUS = smbus2.SMBus(1)

class Skill(BaseSkill):
    LINE_LEN = 16

    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel
        self.lcd = LCD1602()

    def plug(self, address):
        # Run in console i2cdetect -y 1 to get the address.
        # Address should be 0xXX where XX is digital number.
        # Example: 0x27
        self.lcd.init(address, 1)	# init(slave address, background light)
        return self
    
    def write(self, offset, line, message):
        self.lcd.write(offset, line, message)
    
    def message(self, message, sleep=1):
        while len(message) > 0:
            self.clear()
            line1 = message[0:self.LINE_LEN]
            line2 = message[self.LINE_LEN:self.LINE_LEN * 2]
            self.write(0, 0, line1)
            self.write(0, 1, line2)
            time.sleep(sleep)
            message = message[self.LINE_LEN*2:]
    
    def clear(self):
        self.lcd.clear()


class LCD1602():
    def write_word(self, addr, data):
        global BLEN
        temp = data
        if BLEN == 1:
            temp |= 0x08
        else:
            temp &= 0xF7
        BUS.write_byte(addr ,temp)

    def send_command(self, comm):
        # Send bit7-4 firstly
        buf = comm & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.write_word(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(LCD_ADDR ,buf)

        # Send bit3-0 secondly
        buf = (comm & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.write_word(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(LCD_ADDR ,buf)

    def send_data(self, data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.write_word(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(LCD_ADDR ,buf)

        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.write_word(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(LCD_ADDR ,buf)

    def init(self, addr, bl):
    #	global BUS
    #	BUS = smbus.SMBus(1)
        global LCD_ADDR
        global BLEN
        LCD_ADDR = addr
        BLEN = bl
        try:
            self.send_command(0x33) # Must initialize to 8-line mode at first
            time.sleep(0.005)
            self.send_command(0x32) # Then initialize to 4-line mode
            time.sleep(0.005)
            self.send_command(0x28) # 2 Lines & 5*7 dots
            time.sleep(0.005)
            self.send_command(0x0C) # Enable display without cursor
            time.sleep(0.005)
            self.send_command(0x01) # Clear Screen
            BUS.write_byte(LCD_ADDR, 0x08)
        except:
            return False
        else:
            return True

    def clear(self):
        self.send_command(0x01) # Clear Screen
    
    def shift_right(self):
        self.send_command(0x1C) # Move entire display right
    
    def shift_left(self):
        self.send_command(0x18) # Move entire display left

    def openlight(self):  # Enable the backlight
        BUS.write_byte(0x27,0x08)
        BUS.close()

    def write(self, x, y, str):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y <0:
            y = 0
        if y > 1:
            y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)

        for chr in str:
            self.send_data(ord(chr))
        