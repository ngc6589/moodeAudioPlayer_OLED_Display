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

# アイコン定義
icon1 = [
    '                                                          ',
    '  *********      *********      *********      *********  ',
    ' *         *    *         *    *         *    *         * ',
    '*    *      *  *    *      *  *    *      *  *           *',
    '*   * *     *  *   * *   * *  *   * *     *  *           *',
    '* **  *     *  * **  *   * *  * **  *     *  *           *',
    '* *   * *   *  * *   * * * *  * *   * * * *  *           *',
    '* *   * *   *  * *   * * * *  * *   *  *  *  *           *',
    '* *   * *   *  * *   * * * *  * *   * * * *  *           *',
    '* **  *     *  * **  *   * *  * **  *     *  *           *',
    '*   * *     *  *   * *   * *  *   * *     *  *           *',
    '*    *      *  *    *      *  *    *      *  *           *',
    ' *         *    *         *    *         *    *         * ',
    '  *********      *********      *********      *********  '
    ]

icon2 = [
    '                                                          ',
    '  *********      *********      *********      *********  ',
    ' *         *    *         *    *         *    *         * ',
    '*   *       *  *           *  *           *  *           *',
    '*   **      *  *   ** **   *  *           *  *           *',
    '*   ***     *  *   ** **   *  *   *****   *  *           *',
    '*   ****    *  *   ** **   *  *   *****   *  *           *',
    '*   *****   *  *   ** **   *  *   *****   *  *           *',
    '*   ****    *  *   ** **   *  *   *****   *  *           *',
    '*   ***     *  *   ** **   *  *   *****   *  *           *',
    '*   **      *  *   ** **   *  *           *  *           *',
    '*   *       *  *           *  *           *  *           *',
    ' *         *    *         *    *         *    *         * ',
    '  *********      *********      *********      *********  '
    }

icon3 = [
    '                                                          ',
    '  *********      *********      *********      *********  ',
    ' *         *    *         *    *         *    *         * ',
    '*  *    *   *  *   *    *  *  *           *  *           *',
    '*  **   *   *  *   *   **  *  *           *  *           *',
    '*  ***  *   *  *   *  ***  *  *           *  *           *',
    '*  **** *   *  *   * ****  *  *           *  *           *',
    '*  ******   *  *   ******  *  *           *  *           *',
    '*  **** *   *  *   * ****  *  *           *  *           *',
    '*  ***  *   *  *   *  ***  *  *           *  *           *',
    '*  **   *   *  *   *   **  *  *           *  *           *',
    '*  *    *   *  *   *    *  *  *           *  *           *',
    ' *         *    *         *    *         *    *         * ',
    '  *********      *********      *********      *********  '
    ]


# メタデータファイル
metaDataFileName = '/var/local/www/currentsong.txt'
#metaDataFileName = 'currentaudio.txt'
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
    if lastModTimeNow > lastModTImeSave:
        # メタデータファイルを読んで変数更新
        for line in open(metaDataFileName, 'r'):
            itemList = line[:-1].split('=')
            str01 = itemList[1]
            str01 = str01.decode('UTF8')
            print itemList[0], str01
            if itemList[0] == 'title':
                str01 = itemList[1]
                str01 = str01.decode('UTF8')
                titleStr = str01
            if itemList[0] == 'album':
                str01 = itemList[1]
                str01 = str01.decode('UTF8')
                albumStr = str01
            if itemList[0] == 'artist':
                str01 = itemList[1]
                str01 = str01.decode('UTF8')
                artistStr = str01

        #titleStr = '洋酒といえば、誰でも最初に思い浮かべるのがウイスキー。いわば洋酒のシンボル的な存在'
        #titleStr = titleStr.decode('UTF8')
        titleImageSize = font12.getsize(titleStr)

        # テキスト描画イメージ幅を120ピクセルの整数倍となるようにアライメント
        rowCount = titleImageSize[0] / 120
        if titleImageSize[0] % 120 > 0:
            rowCout = rowCount + 1
        if rowCount < 2:
            rowCount = 2
        titleImageSize = (rowCount * 120, titleImageSize[1])

        # タイトルの文字列を描画
        titleImageWK = Image.new('1', titleImageSize)
        titledrawWK = ImageDraw.Draw(titleImageWK)
        titledrawWK.text((0, 0), titleStr, font=font12, fill=255)

        # 描画した文字列を縦スクロール用イメージに貼り付ける
        titleImage = Image.new('1', (120, ((rowCount + 4) * 12)))
        for i in range(rowCount):
            region = titleImageWK.crop((i * 120, 0, i * 120 + 120, 12))
            titleImage.paste(region, (0, i * 12 + 24, 120, i * 12 + 36))

        # アルバムの文字列を描画
        albumImageSize = font12.getsize(albumStr)
        albumImageWK = Image.new('1', albumImageSize)
        albumdrawWK = ImageDraw.Draw(albumImageWK)
        albumdrawWK.text((0, 0), albumStr, font=font12, fill=255)

        # アーティストの文字列を描画
        artistImageSize = font12.getsize(artistStr)
        artistImageWK = Image.new('1', artistImageSize)
        artistdrawWK = ImageDraw.Draw(artistImageWK)
        artistdrawWK.text((0, 0), artistStr, font=font12, fill=255)

        lastModTImeSave = lastModTimeNow


    # タイトル文字イメージを OLED 用キャンバスに貼り付け
    region = titleImage.crop((0, scrollCount + 0, 120, scrollCount + 24))
    image.paste(region,(8, 0))

    # スクロール終了位置判定
    # カウンターの範囲をみて、スクロールしないタイミングなど実装すると見やすくなるかも
    scrollCount = scrollCount + 1
    if scrollCount > (rowCount + 2) * 12:
        scrollCount = 0


    # アルバム文字列をキャンバスに貼る
    region = albumImageWK.crop((0, 0, 120, 12))
    image.paste(region,(8, 24))
    
    # アーティスト文字列をキャンバスに貼る
    region = artistImageWK.crop((0, 0, 120, 12))
    image.paste(region,(8, 36))
    
    # OLED に出力
    disp.image(image)
    disp.display()
    time.sleep(0.1)


# ..*....1....*....2....*....3....*....4....*....5....*....6....*....7....*....8....*....9....*....A....*....B....*....C..
#
# python 入門者のコードのため冗長な書き方が多いです。
# Written by Masahiro Kusunoki http://mkusunoki.net http://em9system.net
#
