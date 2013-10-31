#!/bin/env python
#coding=utf8

from pgmagick import ImageList,Image,Geometry,ImageType
"""
-rw-r--r-- 1 root root 1089472 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DX6Q2R4VdiABCfwP0OA-o539.gif
-rw-r--r-- 1 root root 1056394 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DX6Q2RBvZmABAeim0uJTQ292.gif
-rw-r--r-- 1 root root 3411611 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DX6Q3CGkx-ADQOmxGk_JA500.gif
-rw-r--r-- 1 root root 1080596 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DX6Q3Q0HjVABB9FCiDbJw805.gif
-rw-r--r-- 1 root root  975008 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DX6QzxQXCPAA7goGinVHQ886.gif
-rw-r--r-- 1 root root  482451 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DX6Qzzv59oAAdck3FTTWM317.gif
-rw-r--r-- 1 root root   63206 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXEY3wz5A5AAD25q_eynY225.gif
-rw-r--r-- 1 root root  467051 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXKGXCYf-jAAcga70JhF4929.gif
-rw-r--r-- 1 root root  468960 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXKKGzkytwAAcn4BZ0VCc690.gif
-rw-r--r-- 1 root root  479438 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXKKHyBrRSAAdQzkyjClk043.gif
-rw-r--r-- 1 root root   49983 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXrCqwaqv0AADDPz_aAUY584.gif
-rw-r--r-- 1 root root   35241 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXrEqhu0EcAACJqRzHzsk573.gif
-rw-r--r-- 1 root root   53148 12月 29 21:04 ../testPIC/srcPic/srcPic.bak/rBABE1DXrEqyEwS2AADPnJe2Too116.gif
"""

srcGifFrame0 = "./testGif/rBABE1DX6Q3CGkx-ADQOmxGk_JA500.gif"
#srcGifFrame0 = "./testGif/rBABE1DX6Q2R4VdiABCfwP0OA-o539.gif"
srcGifFrame1 = "./testGif/rBABE1DX6Q2R4VdiABCfwP0OA-o539.gif[1]"
srcGifFrame2 = "./testGif/rBABE1DX6Q2R4VdiABCfwP0OA-o539.gif[2]"

#imgFrame0 = Image( srcGifFrame0 )
#imgFrame1 = Image( srcGifFrame1 )
#imgFrame2 = Image( srcGifFrame2 )

#imgFrame2.write('aaaa.gif')
imgs = ImageList(  )
outImage = ImageList()
#imgs.append(imgFrame0)
#imgs.append(imgFrame1)
#imgs.append(imgFrame2)
#imgs.animationDelayImages(100)
a = ImageType()

imgs.readImages(srcGifFrame0)
imgs.scaleImages( "550x550")
img = imgs.__getitem__( 0 )
print img.columns(),img.rows()

print len( imgs )
#imgs.animationDelayImages(100)
imgs.writeImages( './test.gif' )

"""
from pgmagick import Image, ImageList, Geometry, Color



imgs = ImageList()

for color in ('red', 'blue', 'green', 'black', 'yellow'):

    imgs.append(Image(Geometry(200, 200), Color(color)))

imgs.animationDelayImages(100)

imgs.scaleImages(Geometry(100, 100))

print len(imgs)

imgs.writeImages('output.gif')

"""""