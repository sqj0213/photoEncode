#!/bin/env python
#coding=utf8
from datetime import *
import os,sys,time
from pgmagick import Image,Blob,Color,Geometry,ImageList,GravityType
from pgmagick import CompositeOperator as co
from inc import proto,commFunc
"""基于GraphicsMagick官方推荐的python扩展pgmagick来开发
pgmagick通过boost.python进行封装，提供较全面的文档与用例

"""
class dynamicPhoto(object):
    #按照指定的宽与高缩略后再按照指定的宽与高进行裁剪
    @staticmethod
    def resize( srcFile="", destFile="", w=200,h=200 ):
        imgs = ImageList()
        imgs.readImages(srcFile)
        imgs.scaleImages("%dx%d"%(w,h))
        imgs.writeImages(destFile)
        return "True"
        #CONVERT_RESIZE_SIMPLE_WITH_WIDTH = "%s -resize '%d" + "x>'" + " %s"
    #源图宽或高大于目标图宽或高时才缩略
    @staticmethod
    def resize0( srcFile="", destFile="", w=200,h=200 ):
        imgs = ImageList()
        imgs.readImages( srcFile )
        imgs.scaleImages("%dx>"%w)

        imgs.writeImages(destFile)
        return "True"

    #忽略宽高比缩放
    @staticmethod
    def resize2( srcFile="", destFile="", w=200, h=200, Ignore=False ):
        imgs = ImageList()
        imgs.readImages( srcFile )
        if ( h != -1 ):
            imgs.scaleImages("%dx%d!" % (w,h))
        else:
            imgs.scaleImages("%dx!" % w )
        imgs.writeImages(destFile)
        return "True"

    #    #CONVERT_RESIZE_GREATER_ONLY = "%s -resize '%d" + "x" + "%d>' %s"
    @staticmethod
    def resize3( srcFile="", destFile="", w=200, h=200, Ignore=False ):
        imgs = ImageList()
        imgs.readImages(srcFile)
        imgs.scaleImages("%dx%d>"%(w,h))
        imgs.writeImages(destFile)
        return "True"
        #CONVERT_RESIZE_SMALLER_ONLY = "%s -resize '%d" + "x" + "%d<' %s"
    #源图宽或高小于目标图宽或高时进行拉伸
    @staticmethod
    def resize4( srcFile="", destFile="", w=200,h=200 ):
        imgs = ImageList()
        imgs.readImages( srcFile )
        imgs.scaleImages("%dx%d<" % (int(w),int(h)))
        """
        gifFrame0 = imgs.__getitem__(0)

        sw = gifFrame0.columns()
        sh = gifFrame0.rows()
        #小于指定的宽高时才拉伸,notice是等比缩放，目标尺寸不成比例时不会达到目标尺寸
        if ( sw < w or sh < h ):
            imgs.scaleImages("%dx%d" % (int(w),int(h)))
        """
        imgs.writeImages(destFile)
        return "True"


    #CONVERT_RESIZE_CROP = "%s -resize %d" + "x" + " -crop %d" + "x" + "%d" + "+0+0 +repage %s"
    #按照指定宽度等比缩放后按高与宽进行截剪
    #长小高大变为长大高小时有问题
    #
    #按照指定宽度等比缩放后按高与宽进行截剪
    #长小高大变为长大高小时有问题
    #
    @staticmethod
    def resize5( srcFile="", destFile="", w=200,h=200 ):
        imgs = ImageList()
        outImgs = ImageList()
        imgs.readImages( srcFile )
        gifFrameLen = len( imgs )
        #取得gif的第0帧
        img = imgs.__getitem__( 0 )
        #sw源图宽度
        sw = img.columns()
        sh = img.rows()
        #要缩略的宽度
        rw = w
        #要缩略的高度
        rh = h

        #源图的宽高比
        sratio = float(sw)/float(sh)
        #目标图的宽高比
        rratio = float(rw)/float(rh)

        if ( sw>w ):
            imgs.scaleImages( "%dx"%w)
        #
        #??长大高小的图片处理问题:1600x94 转换为160x298按照宽度等比缩放
        #??长大高小的图片处理问题:1600x94 转换为522x294
        #若源图的宽高比大于目标图的宽高比时，则按照高进行缩放后再裁剪宽度
        else:
            if ( sratio > rratio ):
                hscale = float(rh)/float(sh)
                w = int(sw*hscale)
                h = int(sh*hscale)
                #print (sw,sh,w,h,rw,rh,hscale)
                #就高缩放
                imgs.scaleImages( "%dx"%(w) )

            #若源图的宽高比小于目标图的宽高比时，则按照宽进行缩放后再裁剪高度
            else:
                wscale = float(rw)/float(sw)

                w = int(sw*wscale)
                h = int(sh*wscale)
                #print (sw,sh,w,h,rw,rh,wscale)
                #就宽缩放
                imgs.scaleImages("%dx%d"%(w,h))
                #缩放完后遍历裁剪
            for i in range( gifFrameLen ):
                tmpImg = imgs.__getitem__( i )
                tmpImg.crop(Geometry( rw,rh,0,0 ) )
                tmpImg.profile("*", Blob())
                outImgs.append( tmpImg )
                #(102, 900, 160, 1411, 160, 298)
                #print( sw,sh,w,h,rw,rh)

        if ( len( outImgs ) > 0 ):
            outImgs.writeImages(destFile)
        else:
            imgs.writeImages(destFile)
        return "True"
        #img.quality(100)#图片的压缩质量，与图片大小相关，消耗cpu
        #img.filterType(FilterTypes.SincFilter)#图片处理滤镜，消耗cpu
        #scalePara = "'%d" +'x'+ "%d" % (int(w),int(h))
        #img.scale(scalePara)
        #img.sharpen(1.0)#图片锐化处理加强图片单元里的物件轮廓与线条，开启后会消耗cpu
        #img.write(dstfile)


    #按照指定的宽与高缩略或放大后再按照指定的宽与高从中心进行裁剪
    @staticmethod
    def resize6( srcFile="", destFile="", w=200,h=200 ):
        imgs = ImageList()

        imgs.readImages(srcFile)
        gifFrameLen = len(imgs)

        #若只有一帧直接调用静态方法输出
        if ( gifFrameLen == 1 ):
            return staticPhoto.resize6(srcFile,destFile,w,h)

        outImg = ImageList()

        #取得第0帧
        gifFrame0 = imgs.__getitem__(0)

        #sw源图宽度
        sw = gifFrame0.columns()
        sh = gifFrame0.rows()
        #如果宽高比大小于倍则转成静态图片
        if ( int(sw/sh) > 5 ):
            return staticPhoto.resize1(srcFile,destFile,w,h)

        #要缩略的宽度
        rw = w
        #要缩略的高度
        rh = h

        #源图的宽高比
        sratio = float(sw)/float(sh)
        #目标图的宽高比
        rratio = float(rw)/float(rh)

        #若源图的宽高比大于目标图的宽高比时，则按照高进行缩放后再裁剪宽度
        if ( sratio > rratio ):
            hscale = float(rh)/float(sh)
            w = int(sw*hscale)
            h = int(sh*hscale)
            #print (sw,sh,w,h,rw,rh,hscale)
            #就高缩放
            imgs.scaleImages("%dx%d"%(w,h))

            #计算裁剪宽的部分的横坐标,超出的宽的部分进行裁剪
            tmpRowsPos = int((sw*hscale - rw)/2)
            #imgs.coalesceImags(Geometry( rw,rh,tmpRowsPos,0 ))
            for i in range( gifFrameLen ):
                tmpImg = imgs.__getitem__(i)
                #print w,h,sw,sh,rw,rh,tmpRowsPos,i,gifFrameLen,tmpImg.columns(),tmpImg.rows()
                #594 260 320 140 132 260 231 0 145 320 140

                if ( sw == tmpImg.columns() and sh == tmpImg.rows() and tmpRowsPos > 0 ):
                    return staticPhoto.resize1(srcFile,destFile,rw,rh)
                tmpImg.crop(Geometry( rw,rh,tmpRowsPos,0 ) )
                tmpImg.profile("*", Blob())
                outImg.append(tmpImg)
            outImg.writeImages(destFile)
            return "True"
        #若源图的宽高比小于目标图的宽高比时，则按照宽进行缩放后再裁剪高度
        else:
            wscale = float(rw)/float(sw)
            w = int(sw*wscale)
            h = int(sh*wscale)
            #print (sw,sh,w,h,rw,rh,wscale)
            #就宽缩放
            imgs.scaleImages("%dx%d"%(w,h))
            tmpColsPos = int((sh*wscale-rh)/2 )

            for i in range(gifFrameLen):
                if ( i == 0 ):
                    tmpImg = gifFrame0
                else:
                    tmpImg = imgs.__getitem__(i)
                if ( sw == tmpImg.columns() and sh == tmpImg.rows() and tmpColsPos > 0 ):
                    return staticPhoto.resize1(srcFile,destFile,rw,rh)
                tmpImg.crop( Geometry( rw,rh,0,tmpColsPos ) )
                tmpImg.profile("*", Blob())
                outImg.append(tmpImg)
            outImg.writeImages(destFile)
            return "True"
        return "True"

class staticPhoto(object):
    #按照指定的宽与高缩略后再按照指定的宽与高进行裁剪
    @staticmethod
    def resize( srcFile="", destFile="", w=200,h=200 ):
        blobData = Blob(open(srcFile).read())
        if ( h != -1 ):
            img = Image( blobData, Geometry(w, h))
            img.scale("%dx%d" % (w,h))
        else:
            img = Image( blobData )
            img.scale("%dx" % w )
        img.profile("*", Blob())
        img.write(destFile)
        return "True"

    @staticmethod
    def resize0( srcFile="", destFile="", w=200 ):

        img = Image(srcFile)
        sw = img.columns()
        sh = img.rows()
        if ( sw > w  ):
            tw = w
            th = sh*(float(w)/float(sw))
            img.scale("%dx%d"%(tw,th))
        img.profile("*", Blob())
        img.write(destFile)
        return "True"

    #按照指定的宽与高缩略或放大后再按照指定的宽与高从中心进行裁剪
    @staticmethod
    def resize1( srcFile="", destFile="", w=200,h=200 ):
        img = Image( srcFile )
        #sw源图宽度
        sw = img.columns()
        sh = img.rows()
        #要缩略的宽度
        rw = w
        #要缩略的高度
        rh = h

        #源图的宽高比
        sratio = float(sw)/float(sh)
        #目标图的宽高比
        rratio = float(rw)/float(rh)

        #若源图的宽高比大于目标图的宽高比时，则按照高进行缩放后再裁剪宽度
        if ( sratio > rratio ):
            hscale = float(rh)/float(sh)
            w = sw*hscale
            h = sh*hscale
            #print (sw,sh,w,h,rw,rh,hscale)
            #就高缩放
            img.scale("%dx%d"%(w,h))
            #计算裁剪宽的部分的横坐标,超出的宽的部分进行裁剪
            tmpRowsPos = int((sw*hscale - rw)/2)
            img.crop(Geometry( rw,rh,tmpRowsPos,0 ) )
        #若源图的宽高比小于目标图的宽高比时，则按照宽进行缩放后再裁剪高度
        else:
            wscale = float(rw)/float(sw)

            w = sw*wscale
            h = sh*wscale
            #print (sw,sh,w,h,rw,rh,wscale)
            #就宽缩放
            img.scale("%dx%d"%(w,h))
            tmpColsPos = int((sh*wscale-rh)/2 )
            img.crop( Geometry( rw,rh,0,tmpColsPos )  )
            #只有宽大于目标宽度的时候才进行缩略
        #elif ( sw > w ):
        #    pass
        #unicodestring.encode("utf-8")
        img.profile("*", Blob())
        img.write(destFile)
        return "True"


    #忽略高宽比缩放
    @staticmethod
    def resize2( srcFile="", destFile="", w=200,h=200 ):
        blobData = Blob(open(srcFile).read())
        if ( h != -1 ):
            img = Image( blobData, Geometry(w, h))
            img.scale("%dx%d!" % (w,h))
        else:
            img = Image( blobData )
            img.scale("%dx!" % w )
        img.profile("*",Blob())
        img.write(destFile)
        return "True"


    #宽高大于指定高宽时进行缩略
    @staticmethod
    def resize3( srcFile="", destFile="", w=200,h=200, color="", crop=False, align="center" ):

        img = Image(srcFile)
        img.scale("%dx%d>"%(w,h))
        img.profile("*",Blob())
        img.write(destFile)
        return "True"

    #源图宽或高小于目标图宽或高时进行拉伸
    @staticmethod
    def resize4( srcFile="", destFile="", w=200,h=200 ):
        img = Image(srcFile)
        img.scale("%dx%d<"%(w,h))
        img.profile("*",Blob())
        img.write(destFile)
        return "True"

    @staticmethod
    def resize5( srcFile="", destFile="", w=200,h=200 ):

        #CONVERT_RESIZE_CROP = "%s -resize %d" + "x" + " -crop %d" + "x" + "%d" + "+0+0 +repage %s"
        img = Image( srcFile )
        sw = img.columns()
        sh = img.rows()

        #源图宽高比
        sratio = float(sw)/float(sh)
        #目标图宽高比
        tratio = float(w)/float(h)

        #若源图的宽高比大于目标图的宽高比，则
        if( sratio == tratio and (w==sw) and (h==sh )):
            imb.profile("*",Blob())
            img.write(destFile)
            return "True"
        elif ( sratio > tratio ):
            hscale = float(w)/float(sw)
            tw = sw*hscale
            th = sh*hscale
            img.scale("%dx"%(tw))
            if ( th > h ):
                img.crop(Geometry(w,h))
            img.profile("*",Blob())
            img.write(destFile)
            return "True"
        elif( sratio < tratio ):
            wscale = float(w)/float(sw)

            tw = int(sw*wscale)
            th = int(sh*wscale)
            #260 132 670 502 0.388059701493 260 194

            img.scale("%dx%d"%(tw,th))
            if ( th > h ):
                img.crop(Geometry(w,h))
            img.profile("*",Blob())
            img.write(destFile)
            return "True"

        return "True"

    @staticmethod
    def resize6( srcFile="", destFile="", w=200,h=200 ):
        return staticPhoto.resize1(srcFile,destFile,w,h)

    #若源图的宽高都比目标图的宽高都大则等先缩略后裁剪
    #若源图的宽或高比目标图的宽高一项大则保证图质量进行裁剪，不足的宽或高补白后，在白画底0,0处合图像
    #若源图的宽高都比目标图的宽高都小，则在白画底0,0处合并图像
    @staticmethod
    def resize7( srcFile="", destFile="", w=200,h=200 ):
        img = Image(srcFile)

        #白色背景图
        backImg = None

        #sw源图宽度
        sw = img.columns()
        #sh源图高度
        sh = img.rows()
        #若目标图的宽或高都比源图大则不处理
        if ( sw <= w and sh <= h ):
            backImg = Image(Geometry(w,h), 'white' )
            backImg.composite(img, Geometry( sw, sh, 0, 0 ), co.OverCompositeOp)
            backImg.profile("*",Blob())
            backImg.write(destFile)
            return "True"
        #目标的宽或高都比源图的小则进行裁剪
        elif ( sw > w and sh > h ):
            #源图的宽高比
            sratio = float(sw)/float(sh)
            rratio = float(w)/float(h)
            #若源图宽高比大于目标图的宽高比的话，则就高缩放，从0,0位置裁前源图宽
            #print sratio,rratio
            if ( sratio > rratio ):
                hscale = float(h)/float(sh)
                rw = int(sw*hscale)
                rh = int(sh*hscale)
            else:
                wscale = float(w)/float(sw)
                rw = int(sw*wscale)
                rh = int(sh*wscale)
            img.scale("%dx%d"%(rw,rh))
            img.crop(Geometry(w,h,0,0))
            img.profile("*",Blob())
            img.write(destFile)
            return "True"
        elif ( sw > w ):
            backImg = Image(Geometry(w,h), 'white' )
            img.crop(Geometry(w,sh))
            backImg.composite(img,Geometry(w,h,0,0),co.OverCompositeOp )
            backImg.profile("*",Blob())
            backImg.write(destFile)
            return "True"
        elif ( sh > h ):
            backImg = Image(Geometry(w,h), 'white' )
            img.crop( Geometry(sw,h) )
            backImg.composite(img, Geometry(w,h,0,0),co.OverCompositeOp )
            backImg.profile("*",Blob())
            backImg.write(destFile)
            return "True"
        return "True"


    #按照指定宽度等比缩放后按高与宽进行截剪
    #长小高大变为长大高小时有问题
    #
    @staticmethod
    def resize8( srcFile="", destFile="", w=200,h=200 ):
        img = Image(srcFile)

        #.def("extent", (void (Magick::Image::*)(const Magick::Geometry&, const Magick::Color&, const Magick::GravityType))&Magick::Image::extent)
        #白色背景图
        backImg = None

        #sw源图宽度
        sw = img.columns()
        #sh源图高度
        sh = img.rows()
        #若目标图的宽或高都比源图大则不处理
        if ( sw <= w and sh <= h ):
            backImg = Image(Geometry(w,h), 'white' )
            backImg.composite(img, GravityType.CenterGravity, co.OverCompositeOp)
            backImg.profile("*",Blob())
            backImg.write(destFile)
            return "True"
        #目标的宽或高都比源图的小则进行裁剪
        elif ( sw > w and sh > h ):
            #源图的宽高比
            sratio = float(sw)/float(sh)
            rratio = float(w)/float(h)
            #若源图宽高比大于目标图的宽高比的话，则就高缩放，从0,0位置裁前源图宽
            #print sratio,rratio
            if ( sratio > rratio ):
                hscale = float(h)/float(sh)
                rw = int(sw*hscale)
                rh = int(sh*hscale)
            else:
                wscale = float(w)/float(sw)
                rw = int(sw*wscale)
                rh = int(sh*wscale)

            linePos = int( (rw-w)/2)
            colPos = int( (rh-h)/2)

            img.scale("%dx%d"%(rw,rh))
            img.crop(Geometry(w,h,linePos,colPos))
            img.profile("*",Blob())
            img.write(destFile)
            return "True"
        elif ( sw > w ):
            backImg = Image(Geometry(w,h), 'white' )
            img.crop(Geometry(w,sh,int((sw-w)/2)))
            backImg.composite(img,GravityType.CenterGravity,co.OverCompositeOp )
            backImg.profile("*",Blob())
            backImg.write(destFile)
            return "True"
        elif ( sh > h ):
            backImg = Image(Geometry(w,h), 'white' )
            img.crop( Geometry(sw,h,0,int((sh-h)/2) ) )
            backImg.composite(img, GravityType.CenterGravity,co.OverCompositeOp )
            backImg.profile("*",Blob())
            backImg.write(destFile)
            return "True"
        return "True"

    #CONVERT_RESIZE_THUMBNAIL = "%s" + "[0] -thumbnail %d" + "x" + "%d" + "> -background white -gravity center -extent %d" + "x" + "%d %s"
    @staticmethod
    def resize9( srcFile="", destFile="", w=200,h=200, color="", crop=False, align="center" ):
        img = Image(srcFile)

        #白色背景图
        backImg = None

        #sw源图宽度
        sw = img.columns()
        #sh源图高度
        sh = img.rows()

        #目标图与源图的宽比例
        wScale = float(w)/float(sw)
        #目标图与源图的高比例
        hScale = float(h)/float(sh)

        if ( w > sw or h > sh ):
            if (wScale == hScale ):
                tw = w
                th = h
            elif ( wScale < hScale ):
                th = h
                tw = sw*wScale
            else:
                tw = w
                th = sh*hScale
        elif( w<sw or h < sh ):
            if (wScale == hScale ):
                tw = w
                th = h
            elif ( wScale < hScale ):
                th = h
                tw = sw*wScale
            else:
                tw = w
                th = sh*hScale
        else:
            tw = sw
            th = sh
        img.scale("%dx%d"%(tw,th))
        backImg = Image(Geometry(w,h), 'white' )
        backImg.composite(img,GravityType.CenterGravity,co.OverCompositeOp )
        backImg.profile("*",Blob())
        backImg.write(destFile)
        return "True"

    #像素大于指定像素时才进行缩略
    @staticmethod
    def resize10( srcFile="", destFile="", w=200 ):
        img = Image( srcFile )
        sw = img.columns()
        sh = img.rows()
        scale = sw*sh

        if ( scale > w ):
            tw = int(sw*((float(w)/float(scale))**0.5))
            th = int(w/tw)
            img.scale("%dx%d"%(tw,th))
        img.profile("*",Blob())
        img.write(destFile)
        return "True"

        #todo:先记录日志根据运营情况来决定合并多余的函数
class myGraphicsMagick10(object):

    #旋转图片
    @staticmethod
    def rotate(srcFile="", destFile="", rotate=90):
        img =Image( srcFile )
        img.rotate( int(rotate) )
        img.profile("*",Blob())
        img.write( destFile )
        return "True"

    #"convert {$sourceFile}[0] -resize 200x200^ -gravity center -extent 200x200 {$targetFile}";
    #"convert {$srcFile}[0] -resize {$size}^ -gravity center -extent {$size} $dstFile";
    #CONVERT_RESIZE_GRAVITY = "%s" + "[0] -resize %d" + "x" + "%d" + "^ -gravity center -extent %d" + "x" + "%d" + " %s"

    #从中心抓取指定大小的图片
    @staticmethod
    def convert_resize_gravity(srcfile='', dstfile='', w=200, h=200, need_return=False):
        t1 = time.time()
        ret =  staticPhoto.resize1( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h))
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_gravity srcfile:%s dstfile:%s runTime:%s \n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #"convert {$tmpFile}[0] -thumbnail '{$v}x{$v}>' -background white -gravity center -extent {$v}x{$v} {$truePath}{$v}.jpg";
    #CONVERT_RESIZE_THUMBNAIL = "%s" + "[0] -thumbnail %d" + "x" + "%d" + "> -background white -gravity center -extent %d" + "x" + "%d %s"
    #宽高大于指定的宽高时才进行全缩略，不裁剪，否则不缩略，目标图尺寸一定为指定的宽与高
    #不足部分用白色填充

    @staticmethod
    def convert_resize_thumbinal(srcfile='', dstfile='', w=200, h=200, need_return=False):
        t1 = time.time()
        ret = staticPhoto.resize9( srcfile.encode("utf-8"),dstfile.encode("utf-8"),int(w), int(h), "#000000", align="center")
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_thumbinal srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #"convert {$srcFile}  -resize {$size}\! $dstFile";
    #CONVERT_RESIZE_EXACTLY = "%s -resize %d" + "x" + "%d! %s"
    #忽略宽高比进行缩略
    @staticmethod
    def convert_resize_exactly(srcfile='', dstfile='', w=200, h=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret = dynamicPhoto.resize2( srcfile.encode("utf-8"),dstfile.encode("utf-8"),int(w), int(h) )
        else:
            ret = staticPhoto.resize2( srcfile.encode("utf-8"),dstfile.encode("utf-8"),int(w), int(h))
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_exactly srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], srcfile,dstfile,(t2-t1)) )
        sys.stdout.flush()
        return ret

    #type为3,大于目标像素才缩略与convert_resize_thumbinal实现功能相同
    #"convert {$srcFile}  -resize {$size}\> $dstFile";
    #CONVERT_RESIZE_GREATER_ONLY = "%s -resize '%d" + "x" + "%d>' %s"
    @staticmethod
    def convert_resize_greater(srcfile='', dstfile='', w=200, h=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret = dynamicPhoto.resize3( srcfile.encode("utf-8"),dstfile.encode("utf-8"),int(w), int(h) )
        else:
            ret = staticPhoto.resize3(srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_greater srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #type为4,小于目标像素才放大
    #"convert {$srcFile}  -resize {$size}\< $dstFile";
    #CONVERT_RESIZE_SMALLER_ONLY = "%s -resize '%d" + "x" + "%d<' %s"
    @staticmethod
    def convert_resize_smaller(srcfile='', dstfile='', w=200, h=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret = dynamicPhoto.resize4(srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h))
        else:
            ret = staticPhoto.resize4(srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h))
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_smaller srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #"convert {$srcFile}  -resize {$width}x -crop {$size}+0+0 +repage $dstFile";
    #CONVERT_RESIZE_CROP = "%s -resize %d" + "x" + " -crop %d" + "x" + "%d" + "+0+0 +repage %s"
    #wx保持宽度
    #-crop裁剪+0+0表示从相应的坐标开始计算w与h进行裁剪
    @staticmethod
    def convert_resize_crop(srcfile='', dstfile='', w=200, h=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret = dynamicPhoto.resize5( srcfile.encode("utf-8"), dstfile.encode("utf-8"),int(w),int(h))
        else:
            ret = staticPhoto.resize5( srcfile.encode("utf-8"), dstfile.encode("utf-8"),int(w),int(h))
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_crop srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #"convert {$srcFile}  -coalesce -sample {$size}^ -gravity center -extent {$size} $dstFile";
    #CONVERT_RESIZE_COALESCE = "%s -coalesce -sample %d" + "x" + "%d" + "^ -gravity center -extent %d" + "x" + "%d %s"
    #-soalesce保证每一帧的宽高相同
    #-sample待查
    #^表示最小的宽高比
    @staticmethod
    def convert_resize_coalesce(srcfile='', dstfile='', w=200, h=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret =  dynamicPhoto.resize6( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h))
        else:
            ret =  staticPhoto.resize6( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h))

        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_coalesce srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #"convert {$srcFile}  -resize {$size} $dstFile";
    #CONVERT_RESIZE_SIMPLE = "%s -resize %d" + "x" + "%d %s"
    #不管源图什么尺寸，一律生成%dx%d的图片
    @staticmethod
    def convert_resize_simple(srcfile='', dstfile='', w=200, h=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret = dynamicPhoto.resize( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h) )
        else:
            ret = staticPhoto.resize( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_simple srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #CONVERT_RESIZE_SIMPLE_WITH_WIDTH = "%s -resize '%d" + "x>'" + " %s"
    #wx>图片宽度大于指定宽度时才截剪，高度保持不变
    @staticmethod
    def convert_resize_simple_with_width(srcfile='', dstfile='', w=200, need_return=False):
        isGifFlag = srcfile.endswith(".gif")
        t1 = time.time()
        if ( isGifFlag ):
            ret = dynamicPhoto.resize0( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w) )
        else:
            ret = staticPhoto.resize0( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_simple_with_width srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile, (t2-t1)) )
        sys.stdout.flush()
        return ret

    #大于指定像素才进行缩略，宽高比保持不变
    #w参数为像素，非宽度请注意，目的只是为了减小图片尺寸，降低带宽
    @staticmethod
    def convert_resize_simple_with_width_at(srcfile='', dstfile='', w=200, need_return=False):
        t1 = time.time()
        ret = staticPhoto.resize10( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_resize_simple_with_width_at srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'],srcfile,dstfile,(t2-t1)) )
        sys.stdout.flush()
        return ret


    #只处理第0帧，目标gif只有第一帧
    #源图大于指定的宽高尺寸时进行裁剪，保持原有图片质量,不足部分用白色补齐，目标图居左
    #CONVERT_GIF_THUMBNAIL_FRAME0 = "%s" + "[0] -thumbnail '%d" + "x" + "%d" + ">^' -extent %d" + "x" + "%d %s"
    @staticmethod
    def convert_gif_thumbnail_frame0(srcfile='', dstfile='', w=200, h=200, need_return=False):
        t1 = time.time()
        ret = staticPhoto.resize7( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_gif_thumbnail_frame0 srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], srcfile,dstfile,(t2-t1)) )
        sys.stdout.flush()
        return ret


    #只处理第0帧，目标gif只有第一帧
    #CONVERT_GIF_THUMBNAIL_FRAME0_G = "%s" + "[0] -thumbnail '%d" + "x" + "%d" + ">^' -gravity center -extent %d" + "x" + "%d %s"
    #源图大于指定的宽高尺寸时进行缩略，保持原有的宽高比缩略，不足部分用白色补齐，目标图居中
    @staticmethod
    def convert_gif_thumbnail_frame0_g(srcfile='', dstfile='', w=200, h=200, need_return=False):
        t1 = time.time()
        ret = staticPhoto.resize8( srcfile.encode("utf-8"), dstfile.encode("utf-8"), int(w), int(h) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_gif_thumbnail_frame0_g srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], srcfile,dstfile,(t2-t1)) )
        sys.stdout.flush()
        return ret

    #把大的缩略图处理成小的缩略图
    #convert ./aa.gif -coalesce -thumbnail '140x110<'  -layers optimize ./bb.gif
    #coalesce保证每一帧的尺寸一致
    #-layers optimize删除重复像素
    #CONVERT_GIF_THUMBNAIL = "%s" + " -coalesce -thumbnail '%d" + "x" + "%d" + ">^' -layers optimize %s"
    """
    尚未有此需求，暂不开发，需要逐帧处理gif图进行缩略
    """
    @staticmethod
    def convert_gif_thumbnail(srcfile='', dstfile='', w=200, h=200, need_return=False):

        return "True"

    #旋转图片
    @staticmethod
    def convert_rotate(srcfile='', dstfile='', rotate=90, need_return=False):
        """
        srcfile:
        dstfile:
        rotate:  90  180  270
        """
        t1 = time.time()
        ret = myGraphicsMagick10.rotate( srcfile.encode("utf-8"), dstfile.encode("utf-8"), rotate )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"ibconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_rotate srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], srcfile,dstfile,(t2-t1)) )
        sys.stdout.flush()
        return ret

    #cmdData:{"src":"\/data2\/www\/itmp\/fengmian\/20130106\/1820\/50e94fd42dacf.jpg","dstPath":"\/data2\/www\/imggx\/i\/fengmian\/20130106\/1820",
    # "trueFile":"\/data2\/www\/imggx\/i\/fengmian\/20130106\/1820\/50e94fd42dacf.jpg","w":100,"h":100,"split":"5x4"}
    #切割图片，用于封面图，源图即为已经带有竖线的图片(待确认)
    @staticmethod
    def convert_split(srcfile='', dstpath='', truefile='', split='3x3', w=100, h=100):
        """
        目前仅用作封面频道
        """
        srcfile = srcfile.encode("utf-8")
        dstpath = dstpath.encode("utf-8")
        truefile = truefile.encode("utf-8")
        (sp_x, sp_y) = split.split('x')
        (file_name, image_ext) = os.path.splitext(os.path.basename(srcfile))

        cw = int(sp_x) * int(w)
        ch = int(sp_y) * int(h)
        t1 = time.time()
        #生成封面列表图
        re = myGraphicsMagick10.convert_gif_thumbnail_frame0_g(srcfile=srcfile, dstfile=truefile, w=cw, h=ch,
            need_return=False)


        if re == True:
            #切割方式为从图片的左上开始逐行切割
            #目标图片文件名为：50d8059b1a822.11.jpg
            blobData = Blob(open(srcfile).read())

            try:
                num = 0#图片输出的编号
                for j in range(int(sp_y)):

                    if ( num >= ( int( sp_x )*int( sp_y ) - 1 ) ):
                        break
                    for i in range(int(sp_x)):
                        img = Image( blobData, Geometry(cw,ch) )
                        linePos = i * int(w)
                        colsPos = j * int(h)
                        #从指定的像素点进行裁剪
                        img.crop( Geometry(w,h,linePos, colsPos) )
                        destFilename = dstpath+'/%s.%d.%s' %( file_name,num,image_ext )
                        img.profile("*",Blob())
                        img.write( destFilename )
                        num = num + 1
                t2 = time.time()
                sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : convert_split srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], srcfile,dstfile,(t2-t1)) )
                sys.stdout.flush()
                return ret
            except Exception as e:
                sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"libconvert_split %s %s srcfile:%s destFilename:%s\n" % (e.args, e.message, srcfile,destFilename))
                sys.stderr.flush()
                return 'False'
        else:
            return "False"
            pass
        return 'True'
