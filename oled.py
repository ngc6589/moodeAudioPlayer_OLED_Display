#!/usr/bin/env python
# -*- mode:python; encoding:utf-8 -*-

import os
import time
import subprocess
import locale
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# メタデータファイル
# metaDataFileName = '/var/local/www/currentaudio.txt'
metaDataFileName = 'currentaudio.txt'
lastModTImeSave = 0
lastModTImeNow = 0

# OLED モジュール設定
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=16000000))

# OLED モジュール初期化・画面クリア
disp.begin()
disp.clear()
disp.display()

# image は OLED モジュールと同じピクセルサイズでキャンバスの感じ
width = 128
height = 64
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# 日本語フォントの登録
font12 = ImageFont.truetype('PixelMplus12-Regular.ttf', 12, encoding='unic')

# 変数
scrollCount = 0
rowCount = 0

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # メタデータファイルが変更されたら OLED に表示するデータ更新
    lastModTimeNow = os.stat(metaDataFileName).st_mtime
    if lastModTimeNow > lastModTimeSave:
        # メタデータファイルを読んで変数更新

        titleStr = '洋酒といえば、誰でも最初に思い浮かべるのがウイスキー。いわば洋酒のシンボル的な存在'
        titleStr = titleStr.decode('UTF8')
        titleImageSize = font12.getsize(titleStr)

        # テキスト描画イメージ幅を120ピクセルの整数倍となるようにアライメント
        rowCount = titleImageSize[0] / 120
        if titleImageSize[0] % 120 > 0:
            rowCout = rowCount + 1
        if rowCount < 2:
            rowCount = 2
        titleImageSize[0] = rowCount * 120
        # titleImageSize = (titleImageSize[0], 12 + titleImageSize[1] + 12)

        # タイトルの文字列を描画
        titleImageWK = Image.new('1', titleImageSize)
        titledrawWK = ImageDraw.Draw(titleImageWK)
        titledrawWK.text((0, 0), titleStr, font=font12, fill=255)

        # 描画した文字列を縦スクロール用イメージに貼り付ける
        titleImage = Image.new('1', (120, (rowCount + 4 * 12)))
        for i in range(rowCount):
            region = titleImageWK.crop((rowCount * 120, 0, rowCount * 120 + 120, 12))
            titleImage.paste(region, (0, rowCount * 12 + 24, 120, rowCount * 12 + 36))

        lastModTimeSave = lastModTimeNow



    # タイトル文字イメージを OLED 用キャンバスに貼り付け
    region = titleImage.crop((0, scrollCount + 0, 120, scrollCount + 24))
    image.paste(region,(8, 0))

    # スクロール終了位置判定
    # カウンターの範囲をみて、スクロールしないタイミングなど実装すると見やすくなるかも
    scrollCount = scrollCount + 1
    if scroolCount > (rowCount + 2) * 12:
        scrollCOunt = 0
        
    # OLED に出力
    disp.image(image)
    disp.display()
    time.sleep(0.1)


# ..*....1....*....2....*....3....*....4....*....5....*....6....*....7....*....8....*....9....*....A....*....B....*....C..
#
# python 入門者のコードのため冗長な書き方が多いです。
# Written by Masahiro Kusunoki http://mkusunoki.net http://em9system.net
#
