oled.py

このスクリプトは、作成途中のものを git 管理しているので動く状態のものではありません。

moOde player で再生中の極情報などを Adafruit 社 OLED モジュール(128x64ピクセル)に
表示するサンプルスクリプトです。

*■対応するプレーヤソフト*
Moode Audio Player  
http://moodeaudio.org  

3.7 Release 2017-05-25 で動作を確認中です。
/var/local/www/currentsong.txt のメタデータファイル作成可能なバージョンであれば
問題なく動くと思われます。

*■使用した OLED モジュール*
adafruit  
PRODUCT ID: 326  
Monochrome 0.96" 128x64 OLED graphic display  

このサンプルプログラムは raspberry pi と SPI 接続で使用するものです。
接続方法などの解説ページを参考にして SPI 接続の配線を行ってください。   
https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black

*■使用した DAC ボード*
「じんそんのぶにっき」さんが設計された  
TDA1387 DAC for Raspberry pi zero  
を使用しています。  

頒布ページ
https://www.switch-science.com/catalog/3282/  
https://www.telnet.jp/~mia/sb/log/eid213.html  
スクリプトサンプルのサポートページ  
https://www.telnet.jp/~mia/sb/log/eid220.html  
https://www.telnet.jp/~mia/sb/log/eid218.html  

