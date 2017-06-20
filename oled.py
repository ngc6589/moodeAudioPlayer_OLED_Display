#!/usr/bin/env python
# -*- encoding:utf8 -*-

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import locale

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=16000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

font12 = ImageFont.truetype('PixelMplus12-Regular.ttf', 12, encoding='unic')

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    textStr = '洋酒といえば、誰でも最初に思い浮かべるのがウイスキー。いわば洋酒のシンボル的な存在'
    textStr = textStr.decode('UTF8')
    #draw.text((8, 0), textStr,  font=font12, fill=255)


    titleImageSize = font12.getsize(textStr)
    titleImageSize = (120 + titleImageSize[0] + 120, 12 + titleImageSize[1] + 12)
    titleImage = Image.new('1', titleImageSize)
    titledraw = ImageDraw.Draw(titleImage)
    titledraw.text((12, 12), textStr,  font=font12, fill=255)

    for x in range(titleImageSize[0]+120):
        region = titleImage.crop((x,12,x+120,24))
        image.paste(region,(8,0))
        disp.image(image)
        disp.display()
        #time.sleep(.05)
    
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
