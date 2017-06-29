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
「じんそんのぶにっき」さんの web サイトの主が作られた  
TDA1387 DAC for Raspberry pi zero  
を使用しています。  

頒布ページ  
https://www.switch-science.com/catalog/3282/  
https://www.telnet.jp/~mia/sb/log/eid213.html  
スクリプトサンプルのサポートページ  
https://www.telnet.jp/~mia/sb/log/eid220.html  
https://www.telnet.jp/~mia/sb/log/eid218.html  

*■フォントの配置*

OLED に表示する文字フォントは、下記アドレスからダウンロードした
12ドット等幅 TrueType フォントを使用しています。


PixelMplus（ピクセル・エムプラス） ‥ 8bitビットマップふうフリーフォント
http://itouhiro.hatenablog.com/entry/20130602/font


ダウンロードした zip を展開して PixelMplus12-Regular.ttf を oled.py と同じディレクトリにおいてください。
oled.py のフォントファイル名のところをフルパスで記述してください。

例 フォントを /home/pi/ に配置したときは、
`# 日本語フォントの登録`  
`font12 = ImageFont.truetype('/home/pi/PixelMplus12-Regular.ttf', 12, encoding='unic')`  
としてください。


12ドット等幅フォントであれば、たのフォントでも表示可能と思います。お好みのフォントに差し替えてみるのもよいかと思います。

*■自動起動の方法*  

/etc/rc.local の exit の前に下記コマンドを追加してください。  

nohup python /home/pi/oled.py > /dev/null 2>&1 &  


