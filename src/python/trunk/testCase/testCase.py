#!/bin/env python
#coding=utf8
import os,time,sys

from ImageConvert import ImageConvert
from myGraphicsMagick import myGraphicsMagick
from myGraphicsMagick import myGraphicsMagick10

from inc import proto,commFunc
#源图片路径
SRCPICPATH="./testPIC/srcPic"
#命令行转换后输出图片路径
BINCONVERTPATH="./testPIC/binConvert/"
#lib转换后输出图输出图片路径
LIBCONVERTPATH="./testPIC/libConvert/"

#lib10转换后输出图输出图片路径
LIBCONVERTPATH10="./testPIC/libConvert10/"
proto.protocal['appName'] = 'testCase'
proto.protocal['ver'] = 1
proto.protocal['cmdSN'] = '123456'
proto.protocal['type'] = 1
proto.protocal['cmdData'] = 'json_data'


def getFileList(jpgPath=""):
    import glob
    return glob.glob(jpgPath)


srcPicFileList = list()

"""
用例图：
    changgaodouda.jpg
    changdagaoxiao.jpg
    changxiaogaoda.jpg
    changgaodouxiao.jpg

meitu
    197x146_1
    160x298_3
    600x
zipai
    160x298_3
    160x298_5
    600x_3
    600x
bizhi
    140x104_1
    140x104_3
    600x
fengmian
    100x100
    600x
touxiang
    100x100
    200x200

kongjianpifu
//  _5 格式于老图片（没有宽高数据），新图片都是没有_5的
    522x294_5
    522x
    256x144_5
    256x
    167x104_5
    167x
    600x
    600x_3
    pifu
    260x132_5
    600x_3
    600x

avatar
    60x60
    200x200
"""

def getBaseFileName( filename='' ):
    return os.path.splitext(os.path.basename(filename))

def getDestFileName( targetDestPath='', srcFile='', format='100x100_3' ):
    w=-1
    h=-1
    type=0

    destFile = targetDestPath

    if ( format.find('x_') != -1 ):
        (w,type) = format.split('x_')
    elif ( format.find('_') != -1 ):
        (wh,type) = format.split('_')
        (w,h) = wh.split('x')
    elif ( format.endswith('x') ):
        w = format.strip('x')
    else:
        (w,h) = format.split('x')

    (fileName,extName) = getBaseFileName( srcFile )

    destFile = destFile + '/' + fileName +'_' +format+extName

    return ( w, h, type, destFile )

class testOldConvert(object):
    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

    meitu
        197x146_1
        160x298_3
        600x
    """
    @staticmethod
    def testMeiTu( _srcPic = '/meitu/changgaodouda.jpg' ):
        format = '197x146_1'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/meitu/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/meitu/changgaodouda_172x146_1.jpg
        re = ImageConvert.ImageConvert.convert_resize_gravity(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '160x298_3'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/meitu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/meitu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllMeiTu():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testMeiTu(SRCPICPATH+'/meitu/'+srcPicFileList[i])
        eTime = time.time()
        #print "testAllMeiTu totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        zipai
        160x298_3
        160x298_5
        600x_3
        600x
    """
    @staticmethod
    def testZiPai( _srcPic = '/zipai/changgaodouda.jpg' ):
        format = '160x298_3'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/zipai/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/zipai/changgaodouda_160x298_3.jpg
        re = ImageConvert.ImageConvert.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '160x298_5'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/zipai/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_crop(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x_3'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/zipai/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/zipai/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllZiPai():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testZiPai(SRCPICPATH+'/zipai/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllZiPai totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg


        bizhi
        140x104_1
        140x104_3
        600x
    """

    @staticmethod
    def testBiZhi( _srcPic = '/bizhi/changgaodouda.jpg' ):
        format = '140x104_1'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/bizhi/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/meitu/changgaodouda_172x146_1.jpg
        re = ImageConvert.ImageConvert.convert_resize_gravity(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '140x104_3'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/bizhi/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/bizhi/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllBiZhi():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testBiZhi(SRCPICPATH+'/bizhi/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllBiZhi end!\ttotalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        fengmian
        100x100
        600x
    """

    @staticmethod
    def testFengMian( _srcPic = '/meitu/changgaodouda.jpg' ):

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/fengmian/', _srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_split(srcfile=_srcPic, dstpath=BINCONVERTPATH+'/fengmian/',
            truefile=destFile,
            split='100x100', w=100, h=100)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllFengMian():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testFengMian(SRCPICPATH+'/fengmian/'+srcPicFileList[i])
        eTime = time.time()
        #print "testAllFengMian end! totalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        touxiang
        100x100
        200x200
    """

    @staticmethod
    def testTouXiang( _srcPic = '/touxiang/changgaodouda.jpg' ):

        format = '100x100'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/touxiang/', _srcPic, format )
        #print w,h
        #os.sys.exit(1)
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        format = '200x200'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/touxiang/', _srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllTouxiang():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testTouXiang(SRCPICPATH+'/touxiang/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllTouxiang end! totalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        avatar
        60x60
        200x200
    """

    @staticmethod
    def testAvatar( _srcPic = '/avatar/changgaodouda.jpg' ):

        format = '60x60'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/avatar/', _srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        format = '200x200'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/avatar/', _srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllAvatar():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testAvatar(SRCPICPATH+'/avatar/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllAvatar end! totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        kongjianpifu
        //  _5 格式于老图片（没有宽高数据），新图片都是没有_5的
        522x294_5
        522x
        256x144_5
        256x
        167x104_5
        167x
        pifu
        260x132_5
        600x_3
        600x
    """

    @staticmethod
    def testPiFu( _srcPic = '/pifu/changgaodouda.jpg' ):
        format = '522x294_5'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )

        t1 = time.time()

        #生成./testPIC/binConvert/zipai/changgaodouda_160x298_3.jpg
        re = ImageConvert.ImageConvert.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '522x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,   need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '256x144_5'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '256x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '167x104_5'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '167x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '260x132_5'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x_3'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_greater(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)

        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllPiFu():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testPiFu(SRCPICPATH+'/pifu/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllPiFu end! totalTime:%s" % (eTime-bTime)


    @staticmethod
    def testAllFormat(srcPic):
        _srcPic = srcPic


        t1 = time.time()
        format = '132x260_0'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        t1 = time.time()
        format = '132x260_1'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_gravity(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_2'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_exactly(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_3'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_greater(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_4'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_smaller(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_5'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_6'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_coalesce(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_7'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_gif_thumbnail_frame0(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_8'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_gif_thumbnail_frame0_g(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_9'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_thumbinal(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()


        t1 = time.time()
        format = '30000x'
        ( w,h,type, destFile ) = getDestFileName(BINCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = ImageConvert.ImageConvert.convert_resize_simple_with_width_at(srcfile=_srcPic, dstfile=destFile,
            w=w, need_return=False)
        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllFormatRun():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testOldConvert.testAllFormat(SRCPICPATH+'/allFormat/'+srcPicFileList[i])
        eTime = time.time()


    @staticmethod
    def runTestPic():
        testOldConvert.testAllMeiTu()
        testOldConvert.testAllZiPai()
        testOldConvert.testAllBiZhi()
        #testOldConvert.testAllFengMian()
        testOldConvert.testAllTouxiang()
        testOldConvert.testAllAvatar()
        testOldConvert.testAllPiFu()

class testNewConvert(object):
    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

    meitu
        197x146_1
        160x298_3
        600x
    """
    @staticmethod
    def testMeiTu( _srcPic = '/meitu/changgaodouda.jpg' ):
        format = '197x146_1'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/meitu/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/meitu/changgaodouda_172x146_1.jpg
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_gravity(srcfile=srcPic, dstfile=destFile,w=w, h=h, need_return=False)

        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '160x298_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/meitu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/meitu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllMeiTu():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testMeiTu(SRCPICPATH+'/meitu/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllMeiTu totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        zipai
        160x298_3
        160x298_5
        600x_3
        600x
    """
    @staticmethod
    def testZiPai( _srcPic = '/zipai/changgaodouda.jpg' ):
        format = '160x298_3'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/zipai/', srcPic, format )

        t1 = time.time()

        #生成./testPIC/binConvert/zipai/changgaodouda_160x298_3.jpg
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '160x298_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/zipai/', srcPic, format )

        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/zipai/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/zipai/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllZiPai():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testZiPai(SRCPICPATH+'/zipai/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllZiPai totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg


        bizhi
        140x104_1
        140x104_3
        600x
    """

    @staticmethod
    def testBiZhi( _srcPic = '/bizhi/changgaodouda.jpg' ):
        format = '140x104_1'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/bizhi/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/meitu/changgaodouda_172x146_1.jpg
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_gravity(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '140x104_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/bizhi/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/bizhi/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllBiZhi():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testBiZhi(SRCPICPATH+'/bizhi/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllBiZhi end!\ttotalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        fengmian
        100x100
        600x
    """

    @staticmethod
    def testFengMian( _srcPic = '/meitu/changgaodouda.jpg' ):

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/fengmian/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,   need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_split(srcfile=_srcPic, dstpath=LIBCONVERTPATH+'/fengmian/',
            truefile=destFile,
            split='3x3', w=100, h=100)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllFengMian():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testFengMian(SRCPICPATH+'/fengmian/'+srcPicFileList[i])
        eTime = time.time()
        #print "testAllFengMian end! totalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        touxiang
        100x100
        200x200
    """

    @staticmethod
    def testTouXiang( _srcPic = '/touxiang/changgaodouda.jpg' ):

        format = '100x100'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/touxiang/', _srcPic, format )
        ##print w,h
        #os.sys.exit(1)
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)

        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '200x200'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/touxiang/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)

        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllTouxiang():

        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testTouXiang(SRCPICPATH+'/touxiang/'+srcPicFileList[i])

        eTime = time.time()

        #print "testAllTouxiang end! totalTime:%d" % (eTime-bTime)

    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        avatar
        60x60
        200x200
    """

    @staticmethod
    def testAvatar( _srcPic = '/avatar/changgaodouda.jpg' ):

        format = '60x60'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/avatar/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '200x200'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/avatar/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllAvatar():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testAvatar(SRCPICPATH+'/avatar/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllAvatar end! totalTime:%d" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        kongjianpifu
        //  _5 格式于老图片（没有宽高数据），新图片都是没有_5的
        522x294_5
        522x
        256x144_5
        256x
        167x104_5
        167x
        pifu
        260x132_5
        600x_3
        600x
    """

    @staticmethod
    def testPiFu( _srcPic = '/pifu/changgaodouda.jpg' ):
        format = '522x294_5'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )

        t1 = time.time()

        #生成./testPIC/binConvert/zipai/changgaodouda_160x298_3.jpg
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '522x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '256x144_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '256x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '167x104_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '167x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '260x132_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllPiFu():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testPiFu(SRCPICPATH+'/pifu/'+srcPicFileList[i])
        eTime = time.time()
        #print "testAllPiFu end! totalTime:%d" % (eTime-bTime)

    @staticmethod
    def testAllFormat(srcPic):
        _srcPic = srcPic

        t1 = time.time()
        format = '132x260_0'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_1'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_gravity(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_2'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_exactly(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        t1 = time.time()
        format = '132x260_4'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_smaller(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_6'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_coalesce(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_7'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_gif_thumbnail_frame0(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_8'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_gif_thumbnail_frame0_g(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_9'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_thumbinal(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        t1 = time.time()
        format = '132x260_30000'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width_at(srcfile=_srcPic, dstfile=destFile,
            w=type,need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllFormatRun():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert.testAllFormat(SRCPICPATH+'/allFormat/'+srcPicFileList[i])
        eTime = time.time()

    @staticmethod
    def runTestPic():
        testNewConvert.testAllMeiTu()
        testNewConvert.testAllZiPai()
        testNewConvert.testAllBiZhi()
        #testNewConvert.testAllFengMian()
        testNewConvert.testAllTouxiang()
        testNewConvert.testAllAvatar()
        testNewConvert.testAllPiFu()



class testNewConvert10(object):
    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

    meitu
        197x146_1
        160x298_3
        600x
    """
    @staticmethod
    def testMeiTu( _srcPic = '/meitu/changgaodouda.jpg' ):
        format = '197x146_1'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/meitu/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/meitu/changgaodouda_172x146_1.jpg
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_gravity(srcfile=srcPic, dstfile=destFile,w=w, h=h, need_return=False)

        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '160x298_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/meitu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/meitu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllMeiTu():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testMeiTu(SRCPICPATH+'/meitu/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllMeiTu totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        zipai
        160x298_3
        160x298_5
        600x_3
        600x
    """
    @staticmethod
    def testZiPai( _srcPic = '/zipai/changgaodouda.jpg' ):
        format = '160x298_3'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/zipai/', srcPic, format )

        t1 = time.time()

        #生成./testPIC/binConvert/zipai/changgaodouda_160x298_3.jpg
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '160x298_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/zipai/', srcPic, format )

        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_crop(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/zipai/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/zipai/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllZiPai():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testZiPai(SRCPICPATH+'/zipai/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllZiPai totalTime:%s" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg


        bizhi
        140x104_1
        140x104_3
        600x
    """

    @staticmethod
    def testBiZhi( _srcPic = '/bizhi/changgaodouda.jpg' ):
        format = '140x104_1'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/bizhi/', srcPic, format )

        t1 = time.time()
        #生成./testPIC/binConvert/meitu/changgaodouda_172x146_1.jpg
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_gravity(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '140x104_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/bizhi/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_greater(srcfile=srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/bizhi/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllBiZhi():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testBiZhi(SRCPICPATH+'/bizhi/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllBiZhi end!\ttotalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        fengmian
        100x100
        600x
    """

    @staticmethod
    def testFengMian( _srcPic = '/meitu/changgaodouda.jpg' ):

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/fengmian/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,   need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_split(srcfile=_srcPic, dstpath=LIBCONVERTPATH10+'/fengmian/',
            truefile=destFile,
            split='3x3', w=100, h=100)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllFengMian():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testFengMian(SRCPICPATH+'/fengmian/'+srcPicFileList[i])
        eTime = time.time()
        #print "testAllFengMian end! totalTime:%s" % (eTime-bTime)


    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        touxiang
        100x100
        200x200
    """

    @staticmethod
    def testTouXiang( _srcPic = '/touxiang/changgaodouda.jpg' ):

        format = '100x100'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/touxiang/', _srcPic, format )
        ##print w,h
        #os.sys.exit(1)
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)

        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '200x200'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/touxiang/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)

        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllTouxiang():

        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testTouXiang(SRCPICPATH+'/touxiang/'+srcPicFileList[i])

        eTime = time.time()

        #print "testAllTouxiang end! totalTime:%d" % (eTime-bTime)

    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        avatar
        60x60
        200x200
    """

    @staticmethod
    def testAvatar( _srcPic = '/avatar/changgaodouda.jpg' ):

        format = '60x60'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/avatar/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '200x200'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/avatar/', _srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()

        print "%s:%s" % (destFile,(t2-t1) )


    @staticmethod
    def testAllAvatar():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testAvatar(SRCPICPATH+'/avatar/'+srcPicFileList[i])

        eTime = time.time()
        #print "testAllAvatar end! totalTime:%d" % (eTime-bTime)



    """
    用例图：
        changgaodouda.jpg
        changdagaoxiao.jpg
        changxiaokuangda.jpg
        changgaodouxiao.jpg

        kongjianpifu
        //  _5 格式于老图片（没有宽高数据），新图片都是没有_5的
        522x294_5
        522x
        256x144_5
        256x
        167x104_5
        167x
        pifu
        260x132_5
        600x_3
        600x
    """

    @staticmethod
    def testPiFu( _srcPic = '/pifu/changgaodouda.jpg' ):
        format = '522x294_5'
        srcPic = _srcPic
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )

        t1 = time.time()

        #生成./testPIC/binConvert/zipai/changgaodouda_160x298_3.jpg
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '522x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '256x144_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '256x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '167x104_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '167x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '260x132_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_greater(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        format = '600x'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/pifu/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w,  need_return=False)


        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllPiFu():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testPiFu(SRCPICPATH+'/pifu/'+srcPicFileList[i])
        eTime = time.time()
        #print "testAllPiFu end! totalTime:%d" % (eTime-bTime)

    @staticmethod
    def testAllFormat(srcPic):
        _srcPic = srcPic

        t1 = time.time()
        format = '132x260_0'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width(srcfile=_srcPic, dstfile=destFile,
            w=w, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_1'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_gravity(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_2'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_exactly(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_3'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_greater(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        t1 = time.time()
        format = '132x260_4'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_smaller(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_5'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_crop(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_6'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_coalesce(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_7'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_gif_thumbnail_frame0(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_8'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_gif_thumbnail_frame0_g(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

        t1 = time.time()
        format = '132x260_9'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_thumbinal(srcfile=_srcPic, dstfile=destFile,
            w=w, h=h, need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )


        t1 = time.time()
        format = '132x260_30000'
        ( w,h,type, destFile ) = getDestFileName(LIBCONVERTPATH10+'/allFormat/', srcPic, format )
        t1 = time.time()
        re = myGraphicsMagick10.myGraphicsMagick10.convert_resize_simple_with_width_at(srcfile=_srcPic, dstfile=destFile,
            w=type,need_return=False)
        t2 = time.time()
        print "%s:%s" % (destFile,(t2-t1) )

    @staticmethod
    def testAllFormatRun():
        bTime = time.time()
        fileLength = len( srcPicFileList )
        for i in range(fileLength):
            testNewConvert10.testAllFormat(SRCPICPATH+'/allFormat/'+srcPicFileList[i])
        eTime = time.time()

    @staticmethod
    def runTestPic():
        testNewConvert10.testAllMeiTu()
        testNewConvert10.testAllZiPai()
        testNewConvert10.testAllBiZhi()
        #testNewConvert.testAllFengMian()
        testNewConvert10.testAllTouxiang()
        testNewConvert10.testAllAvatar()
        testNewConvert10.testAllPiFu()


if __name__ == '__main__':
    t1 = time.time()
    testOldConvert.runTestPic()
    t2 = time.time()


    t3 = time.time()
    testNewConvert.runTestPic()
    t4 = time.time()
    print "old convert end! runTIme:%s" % (t2-t1)
    print "lib convert end! runTIme:%s" % (t4-t3)

"""
/usr/bin/convert /home/sunshare/NetBeansProjects/i.gexing.com/src/trunk/gearman_convert_worker/testPIC/binConvert//fengmian//changgaodouda_600x.jpg -crop 100x100 +repage +adjoin /home/sunshare/NetBeansProjects/i.gexing.com/src/trunk/gearman_convert_worker/testPIC/binConvert//fengmian//changgaodouda.%d.jpg
"""
