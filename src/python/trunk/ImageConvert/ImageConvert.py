#!/bin/evn python
#coding=utf8
from datetime import *
"""
Created on 2012-7-27
@author: Wang chunsheng<chunshengster@gmail.com>
"""

GM_COMMAND = r'/usr/bin/convert '
#旋转
#"convert {$tmpFile} -rotate 90 {$trueFile}";
#"convert {$tmpFile} -rotate 180 {$trueFile}";
#"convert {$tmpFile} -rotate -90 {$trueFile}";
CONVERT_ROTATE = "%s -rotate %d %s"
#分割
#"convert {$tmpFile2} -crop 100x100  +repage  +adjoin  {$cachePath}/{$basename}.%d.{$extend}";
CONVERT_CROP_SEGMENTATION_SEC_ONE = "%s -crop " + "%d" + "x" + "%d +repage +adjoin %s/%s" + '.'
CONVERT_CROP_SEGMENTATION_SEC_TWO = '%d'  #for %d
CONVERT_CROP_SEGMENTATION_SEC_THREE = '%s' # for extend

#裁剪
#"convert {$tmpFile}[0] -crop {$w}x{$h}+0+0 +repage {$tmpFile2}";
CONVERT_CROP_SHAPE = "%s -crop %d" + 'x' + "%d" + "+0+0 +repage %s"

#缩略
#"convert {$tmpFile}[0] -thumbnail '{$v}x{$v}>' -background white -gravity center -extent {$v}x{$v} {$truePath}{$v}.jpg";
CONVERT_RESIZE_THUMBNAIL = "%s" + "[0] -thumbnail %d" + "x" + "%d" + "> -background white -gravity center -extent %d" + "x" + "%d %s"

#"convert {$sourceFile}[0] -resize 200x200^ -gravity center -extent 200x200 {$targetFile}";
#"convert {$srcFile}[0] -resize {$size}^ -gravity center -extent {$size} $dstFile";
CONVERT_RESIZE_GRAVITY = "%s" + "[0] -resize %d" + "x" + "%d" + "^ -gravity center -extent %d" + "x" + "%d" + " %s"

#"convert {$srcFile}  -resize {$size}\! $dstFile";
CONVERT_RESIZE_EXACTLY = "%s -resize %d" + "x" + "%d! %s"
#type为3,大于目标像素才缩略
#"convert {$srcFile}  -resize {$size}\> $dstFile";
CONVERT_RESIZE_GREATER_ONLY = "%s -resize '%d" + "x" + "%d>' %s"
#type为4,小于目标像素才放大
#"convert {$srcFile}  -resize {$size}\< $dstFile";
CONVERT_RESIZE_SMALLER_ONLY = "%s -resize '%d" + "x" + "%d<' %s"

#"convert {$srcFile}  -resize {$width}x -crop {$size}+0+0 +repage $dstFile";
CONVERT_RESIZE_CROP = "%s -resize %d" + "x" + " -crop %d" + "x" + "%d" + "+0+0 +repage %s"
#"convert {$srcFile}  -coalesce -sample {$size}^ -gravity center -extent {$size} $dstFile";
CONVERT_RESIZE_COALESCE = "%s -coalesce -sample %d" + "x" + "%d" + "^ -gravity center -extent %d" + "x" + "%d %s"
#"convert {$srcFile}  -resize {$size} $dstFile";
CONVERT_RESIZE_SIMPLE = "%s -resize %d" + "x" + "%d %s"
CONVERT_RESIZE_SIMPLE_WITH_WIDTH = "%s -resize '%d" + "x>'" + " %s"
CONVERT_RESIZE_SIMPLE_WITH_WIDTH_AT = "%s -resize '%d" + "@>'" + " %s"
#GIF
##"convert {$from} -coalesce -sample '{$w}x{$h}>^' -gravity center -extent {$w}x{$h} {$to}";
#CONVERT_GIF_COALESCE = "%s -coalesce -sample '%dx%d>^' -gravity center -extent %dx%d %s"
#"convert {$from}[0] -thumbnail '{$w}x{$h}>^' -extent {$w}x{$h} {$to}";
#只处理第0帧，目标gif只有第一帧
CONVERT_GIF_THUMBNAIL_FRAME0 = "%s" + "[0] -thumbnail '%d" + "x" + "%d" + ">^' -extent %d" + "x" + "%d %s"
#"convert {$from}[0] -thumbnail '{$w}x{$h}>^' -gravity center -extent {$w}x{$h} {$to}";
#只处理第0帧，目标gif只有第一帧
CONVERT_GIF_THUMBNAIL_FRAME0_G = "%s" + "[0] -thumbnail '%d" + "x" + "%d" + ">^' -gravity center -extent %d" + "x" + "%d %s"

#把大的缩略图处理成小的缩略图
#convert ./aa.gif -coalesce -thumbnail '140x110<'  -layers optimize ./bb.gif
#coalesce保证每一帧的尺寸一致
#-layers optimize删除重复像素
CONVERT_GIF_THUMBNAIL = "%s" + " -coalesce -thumbnail '%d" + "x" + "%d" + ">^' -layers optimize %s"

from inc import proto
import os, sys,time
from inc import commFunc

#from PIL import Image

class ImageConvert(object):
    def __init__(self):
        """

        """
        pass

    @staticmethod
    def execute_convert(command='', need_return=False):
        """

        """
        t1 = time.time()

        sys.stdout.flush()
        r = os.popen(command)
	#notice r=None后才可以进行t2=time.time()进行计时，否则时间无效
        ret =  r.read()
        r = None
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"binconvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command:%s pipret:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], command, ret, (t2-t1)) )
        if need_return:
            return ret
        else:
            return str(True)

    @staticmethod
    def execute_split(srcfile='', dstpath='', w=100, h=100, basename='', image_ext='jpg'):
        args_sec_one = CONVERT_CROP_SEGMENTATION_SEC_ONE % (srcfile, int(w), int(h), dstpath, basename)
        args_sec_three = CONVERT_CROP_SEGMENTATION_SEC_THREE % image_ext
        args = args_sec_one + CONVERT_CROP_SEGMENTATION_SEC_TWO + args_sec_three
        return ImageConvert.execute_convert(GM_COMMAND + args)

    @staticmethod
    def convert_rotate(srcfile='', dstfile='', rotate=90, need_return=False):
        """
        srcfile:
        dstfile:
        rotate:  90  180  270
        """
        args = CONVERT_ROTATE % (srcfile, int(rotate), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    #    @staticmethod
    #    def convert_crop_segmentation(srcfile='', dstfile='', need_return=False):
    #        args = CONVERT_CROP_SEGMENTATION % (srcfile, dstfile)
    #        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    #    @staticmethod
    #    def convert_crop_shape(srcfile='', dstfile='', w=200, h=200, need_return=False):
    #        args = CONVERT_CROP_SHAPE % (srcfile, int(w), int(h), dstfile)
    #        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_thumbinal(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_THUMBNAIL % (srcfile, int(w), int(h), int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_gravity(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_GRAVITY % (srcfile, int(w), int(h), int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_exactly(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_EXACTLY % (srcfile, int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_greater(srcfile='', dstfile='', w=200, h=200, need_return=False):
        if ( h == -1 ):
            args =  CONVERT_RESIZE_SIMPLE_WITH_WIDTH % (srcfile, int(w), dstfile)
        else:
            args = CONVERT_RESIZE_GREATER_ONLY % (srcfile, int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_smaller(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_SMALLER_ONLY % (srcfile, int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)


    @staticmethod
    def convert_resize_crop(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_CROP % (srcfile, int(w), int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_coalesce(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_COALESCE % (srcfile, int(w), int(h), int(w), int(h), dstfile)
        return  ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_simple(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_RESIZE_SIMPLE % (srcfile, int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_simple_with_width(srcfile='', dstfile='', w=200, need_return=False):
        args = CONVERT_RESIZE_SIMPLE_WITH_WIDTH % (srcfile, int(w), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_resize_simple_with_width_at(srcfile='', dstfile='', w=200, need_return=False):
        args = CONVERT_RESIZE_SIMPLE_WITH_WIDTH_AT % (srcfile,int(w),dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args,need_return)

    @staticmethod
    def convert_gif_thumbnail_frame0(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_GIF_THUMBNAIL_FRAME0 % (srcfile, int(w), int(h), int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_gif_thumbnail_frame0_g(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args = CONVERT_GIF_THUMBNAIL_FRAME0_G % (srcfile, int(w), int(h), int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    @staticmethod
    def convert_gif_thumbnail(srcfile='', dstfile='', w=200, h=200, need_return=False):
        args =  CONVERT_GIF_THUMBNAIL % (srcfile, int(w), int(h), dstfile)
        return ImageConvert.execute_convert(GM_COMMAND + args, need_return)

    #cmdData:{"src":"\/data2\/www\/itmp\/fengmian\/20130106\/1820\/50e94fd42dacf.jpg","dstPath":"\/data2\/www\/imggx\/i\/fengmian\/20130106\/1820",
    # "trueFile":"\/data2\/www\/imggx\/i\/fengmian\/20130106\/1820\/50e94fd42dacf.jpg","w":100,"h":100,"split":"5x4"}
    @staticmethod
    def convert_split(srcfile='', dstpath='', truefile='', split='3x3', w=100, h=100):
        """
        目前仅用作封面频道
        """
        try:
            (sp_x, sp_y) = split.split('x')
            (file_name, image_ext) = os.path.splitext(os.path.basename(srcfile))

            #im = Image.open(srcfile,mode='r')
            #(iw,ih) = im.size
            #cw = int(round(iw/100 + 0.5)) * 100
            #ch = int(round(ih/100 + 0.5)) * 100
            cw = int(sp_x) * int(w)
            ch = int(sp_y) * int(h)
            #tmpfile_name = os.path.splitext(srcfile)[0] + '.tmp' + image_ext
            #sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"tmpfile_name : %s \n" % truefile)
            re = ImageConvert.convert_gif_thumbnail_frame0_g(srcfile=srcfile, dstfile=truefile, w=cw, h=ch,
                need_return=False)
            if re == 'True':
            #re = ImageConvert.convert_split(srcfile=tmpfile_name, dstpath=dstpath, split=split, w=w, h=h)
                re = ImageConvert.execute_split(srcfile=truefile, dstpath=dstpath,
                    w=w, h=h, basename=file_name, image_ext=image_ext)
                #r = dict()
                #r['re'] = re
                #r['tmpfile'] = truefile
                return re
            else:
                return str(False)
        except Exception as e:
            sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+ 'binconvert convert_split error:%s %s\n', (e.args,e.message) )
#        finally:
#            if im:
#                im = None

