#!/usr/bin/env python
# -*- mode:python; encoding:utf-8 -*-

import os
import time
import subprocess
import locale
import RPi.GPIO as GPIO
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
    ]

icon3 = [
    '                                                          ',
    '  *********      *********      *********      *********  ',
    ' *         *    *         *    *         *    *         * ',
    '*  *    *   *  *   *    *  *  *     *     *  *           *',
    '*  *   **   *  *   **   *  *  *     *     *  *           *',
    '*  *  ***   *  *   ***  *  *  *   * * *   *  *           *',
    '*  * ****   *  *   **** *  *  *  *  *  *  *  *           *',
    '*  ******   *  *   ******  *  * *   *   * *  *           *',
    '*  * ****   *  *   **** *  *  * *       * *  *           *',
    '*  *  ***   *  *   ***  *  *  * *       * *  *           *',
    '*  *   **   *  *   **   *  *  *  *     *  *  *           *',
    '*  *    *   *  *   *    *  *  *   *   *   *  *           *',
    ' *         *    *         *    *   ***   *    *         * ',
    '  *********      *********      *********      *********  '
    ]

icon4 = [
    '                                                          ',
    '  *********      *********      *********      *********  ',
    ' *         *    *         *    *         *    *         * ',
    '*           *  *           *  *    ***    *  *           *',
    '*     *     *  *           *  *   *   *   *  *           *',
    '*    * *    *  * *       * *  *  *     *  *  *           *',
    '*   *   *   *  *  *     *  *  * *       * *  *           *',
    '*  *     *  *  *   *   *   *  * *       * *  *           *',
    '* *       * *  *    * *    *  * *       * *  *           *',
    '*           *  *     *     *  *  *     *  *  *           *',
    '*           *  *           *  *   *   *   *  *           *',
    '*           *  *           *  *    ***    *  *           *',
    ' *         *    *         *    *         *    *         * ',
    '  *********      *********      *********      *********  '
    ]


icon1ysize = len(icon1)
icon1xsize = len(icon1[0])
icon1image = Image.new('1', (icon1xsize, icon1ysize))
for y in range(icon1ysize):
    char01 = icon1[y]
    for x in range(icon1xsize):
        if char01[x] != ' ':
            icon1image.putpixel((x, y), 1)

icon2ysize = len(icon2)
icon2xsize = len(icon2[0])
icon2image = Image.new('1', (icon2xsize, icon2ysize))
for y in range(icon2ysize):
    char01 = icon2[y]
    for x in range(icon2xsize):
        if char01[x] != ' ':
            icon2image.putpixel((x, y), 1)

icon3ysize = len(icon3)
icon3xsize = len(icon3[0])
icon3image = Image.new('1', (icon3xsize, icon3ysize))
for y in range(icon3ysize):
    char01 = icon3[y]
    for x in range(icon3xsize):
        if char01[x] != ' ':
            icon3image.putpixel((x, y), 1)

icon4ysize = len(icon4)
icon4xsize = len(icon4[0])
icon4image = Image.new('1', (icon4xsize, icon4ysize))
for y in range(icon4ysize):
    char01 = icon4[y]
    for x in range(icon4xsize):
        if char01[x] != ' ':
            icon4image.putpixel((x, y), 1)

iconMode = 0

# Input pins:
btnA = 17
btnB = 27
btnC = 22
btnD = 25
btnMode = 0
btnPress = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(btnA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnD, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
font12 = ImageFont.truetype('/home/pi/PixelMplus12-Regular.ttf', 12, encoding='unic')

# 変数
scrollCount = 0
rowCount = 0
loopCount = 0

try:

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
                # print itemList[0], str01
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

        if btnMode != 3:
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
            image.paste(region,(8, 25))
            # アーティスト文字列をキャンバスに貼る
            region = artistImageWK.crop((0, 0, 120, 12))
            image.paste(region,(8, 37))
        else:
            # プレイリストを描画
            maxPages = len(fileNames) / 4
            for i in range(4):
                if numFileNames > (displayPageNum * 4 + i):
                    str01 = fileNames[displayPageNum * 4 + i]
                    str01 = str01.decode('UTF8')
                    if displayLineNum == i:
                        draw.text((0, i * 12), "* " + str01, font=font12, fill=255)
                    else:
                        draw.text((0, i * 12), "  " + str01, font=font12, fill=255)
                                

        # ボタン押されている間は処理スキップ
        btnAstatus = GPIO.input(btnA)
        btnBstatus = GPIO.input(btnB)
        btnCstatus = GPIO.input(btnC)
        btnDstatus = GPIO.input(btnD)

        if btnPress == True:
            if btnAstatus == 1 and btnBstatus == 1 and btnCstatus == 1 and btnDstatus == 1:
                btnPress = False
        # ボタン判定
        else:
            if btnMode == 0:
                if btnAstatus == 0:
                    #音下げ
                    os.system('mpc volume -5')
                elif btnBstatus == 0:
                    #音上げ
                    os.system('mpc volume +5')
                elif btnCstatus == 0:
                    #ミュート
                    os.system('mpc volume 0')
            elif btnMode == 1:
                if btnAstatus == 0:
                    #再生
                    os.system('mpc play')
                elif btnBstatus == 0:
                    #一時停止
                    os.system('mpc pause')
                elif btnCstatus == 0:
                    #停止
                    os.system('mpc stop')
            elif btnMode == 2:
                if btnAstatus == 0:
                    #もどる
                    os.system('mpc prev')
                elif btnBstatus ==0:
                    #次
                    os.system('mpc next')
                elif btnCstatus == 0:
                    #電源オフ
                    os.system('sudo poweroff')
            elif btnMode == 3:
                if btnAstatus == 0:
                    #上のファイル
                    if displayPageNum == 0 and displayLineNum == 0:
                        pass
                    else:
                        displayLineNum = displayLineNum - 1
                        if displayLineNum < 0:
                            displayLineNum = 3
                            displayPageNum = displayPageNum - 1
                elif btnBstatus ==0:
                    #下のファイル
                    if (displayPageNum * 4 + displayLineNum + 1) < numFileNames:
                        displayLineNum = displayLineNum + 1
                        if displayLineNum > 3:
                            if displayPageNum  == maxPages:
                                displayLineNum = 3
                            else:
                                displayLineNum = 0
                                displayPageNum = displayPageNum + 1
                elif btnCstatus == 0:
                    #プレイリスト決定
                    (file,ext) = os.path.splitext(fileNames[displayPageNum * 4 + displayLineNum])
                    str01 = "mpc load " + "'" + file + "'"
                    os.system('mpc clear')
                    os.system(str01)
                    os.system('mpc play')
                    #print str01

            if btnDstatus == 0:
                btnMode = btnMode + 1
                # プレイリスト選択モードに入るときには、ファイル一覧を更新する
                if btnMode == 3:
                    displayPageNum = 0
                    displayLineNum = 0
                if btnMode > 3:
                    btnMode = 0
        # 
        # ボタンアイコンを画面に貼る
        if btnMode == 0:
            region = icon1image.crop((0, 0, icon1xsize, icon1ysize))
            image.paste(region,(0, 50))
        if btnMode == 1:
            region = icon2image.crop((0, 0, icon2xsize, icon2ysize))
            image.paste(region,(0, 50))
        if btnMode == 2:
            region = icon3image.crop((0, 0, icon3xsize, icon3ysize))
            image.paste(region,(0, 50))
        if btnMode == 3:
            region = icon4image.crop((0, 0, icon4xsize, icon4ysize))
            image.paste(region,(0, 50))


        # 一定時間ごとに/var/lib/mpd/playlists ファイル一覧を更新する
        if loopCount == 0:
            for path, dir, file in os.walk('/var/lib/mpd/playlists'):
                fileNames = []
                absFileNames = []
                for fname in file:
                    fileNames.append(fname)
                    absFileNames.append(os.path.join(path, fname))
                    fileNames.sort()
                    absFileNames.sort()
                    numFileNames = len(fileNames)
            
        # OLED に出力
        disp.image(image)
        disp.display()
        time.sleep(0.15)
        loopCount = loopCount + 1
        if loopCount > 1000:
            loopCount = 0

except KeyboardInterrupt:
    GPIO.cleanup()

# ..*....1....*....2....*....3....*....4....*....5....*....6....*....7....*....8....*....9....*....A....*....B....*....C..
#
# python 入門者のコードのため冗長な書き方が多いです。
# Written by Masahiro Kusunoki http://mkusunoki.net http://em9system.net
