#!/usr/bin/env python
# -*- mode:python; encoding:utf-8 -*-

import os
import locale

photoExt = ['.JPG', '.JPEG', '.PNG']

for path, dir, file in os.walk('/mnt/SDCARD'):
    if len(dir) == 0:
        dirPath = os.path.relpath(path, '/mnt')
        dirName = os.path.basename(dirPath)
        fileNames = []
        for fname in file:
            ext = os.path.splitext(fname)
            ext = ext[1]
            ext = ext.upper()
            if ext not in photoExt:
                fileName = os.path.join(dirPath, fname)
                fileName = fileName.decode('UTF8')
                fileNames.append(fileName)
        fileNames.sort()
        writefileName = '/var/lib/mpd/playlists/' + dirName + '.m3u'
        fno = open(writefileName, 'w') 
        for i in fileNames:
            fno.write(i.encode('UTF8'))
            fno.write('\n')
        fno.close()

# ---------------------------------------------------
# -- Written by Masahiro Kusunoki
# -- http://mkusunoki.net
# -- http://em9system.com
# -- 3 jul 2017 v0.1
# ---------------------------------------------------
