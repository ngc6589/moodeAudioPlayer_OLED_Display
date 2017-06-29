# ラズパイ DAC で OLED 液晶画面に曲名などを表示する python スクリプト  

moode audio player しばりになりますが、再生中の曲情報などを Adafruit 社 OLED モジュールに
表示するサンプルスクリプトです。
コントローラ: SSD1306  
描画サイズ: 128x64 ピクセル
で SPI 接続対応可能であれば、そのまま当スクリプト流用可能かと思います。  

*当スクリプトは python 2.7 で動作確認しています*  

## ■対応するプレーヤソフト  

Moode Audio Player  
<http://moodeaudio.org>  

3.7 Release 2017-05-25 で動作を確認中です。
/var/local/www/currentsong.txt のメタデータファイル作成可能なバージョンであれば
問題なく動くと思われます。

ブラウザから moode audio player の画面を開いて、設定→ｘｘｘｘｘ を有効にしてください。


## ■使用した OLED モジュール  

adafruit  
PRODUCT ID: 326  
Monochrome 0.96" 128x64 OLED graphic display  

このサンプルプログラムは raspberry pi と SPI 接続で使用するものです。
下記解説ページを参考にして SPI 接続の配線、ラズパイに必要な adafruit の液晶制御モジュールをインストールしてください。   

<https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black>


```
$ sudo apt-get update
$ sudo apt-get install build-essential python-dev python-pip
$ sudo pip install RPi.GPIO 
$ sudo apt-get install python-imaging python-smbus
$ sudo apt-get install git
$ git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
$ cd Adafruit_Python_SSD1306
$ sudo python setup.py install
```




## ■使用した DAC ボード  
「じんそんのぶにっき」さんの web サイトの主が作られた  
TDA1387 DAC for Raspberry pi zero  
を使用しています。  

頒布ページ  
https://www.switch-science.com/catalog/3282/  
https://www.telnet.jp/~mia/sb/log/eid213.html  
スクリプトサンプルのサポートページ  
https://www.telnet.jp/~mia/sb/log/eid220.html  
https://www.telnet.jp/~mia/sb/log/eid218.html  


DAC ボード依存はありませんので、他の DAC ボードでも SPI ポートが配線できれば問題ありません

## ■フォントの配置  

OLED に表示する文字フォントは、下記アドレスからダウンロードした
12ドット等幅 TrueType フォントを使用しています。


PixelMplus（ピクセル・エムプラス） ‥ 8bitビットマップふうフリーフォント  
<http://itouhiro.hatenablog.com/entry/20130602/font>  


ダウンロードした zip を展開して PixelMplus12-Regular.ttf を適当なディレクトリに配置して下さい。
oled.py 内の下記場所のパス名を書き換えてください。
`# 日本語フォントの登録`  
`font12 = ImageFont.truetype('/home/pi/PixelMplus12-Regular.ttf', 12, encoding='unic')`  



12ドット等幅フォントであれば、他のフォントでも表示可能と思います。お好みのフォントに差し替えてみるのもよいかと思います。

## ■自動起動の方法  

/etc/rc.local の exit の前に下記コマンドを追加してください。  

nohup python /home/pi/oled.py > /dev/null 2>&1 &  


