#!/bin/env python
#coding=utf8
from datetime import *
import os,sys,time
from inc import proto,commFunc

CONVERT_SPX_TO_RAW="/usr/local/bin/simpleSpeexDecode %s < %s"
CONVERT_RAW_TO_WAV="/usr/bin/sox -V -r 8000 -b 16 -c 1 -s %s %s"
CONVERT_WAV_TO_MP3="/usr/bin/lame -V3 %s %s"
class mySoundConvert(object):
    @staticmethod
    def binCmd(command='', need_return=False):
        """

        """
        t1 = time.time()

        sys.stdout.flush()
        r = os.popen(command)
        #notice r=None后才可以进行t2=time.time()进行计时，否则时间无效
        ret =  r.read()
        r = None
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+
            "binCmd appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command:%s pipret:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],proto.protocal['type'],proto.protocal['cmdData'], command, ret, (t2-t1)) )
        if need_return:
            return ret
        else:
            return str(True)
    @staticmethod
    def convertSPXTOMP3( srcFile="",destFile=""):
        if ( len( srcFile ) == 0 or len( destFile ) == 0 ):
            return "False"
        rawTmpFile = destFile+".raw"
        wavTmpFile = destFile+".wav"
        t1 = time.time()
        convertRawBin = CONVERT_SPX_TO_RAW % ( rawTmpFile, srcFile )
        mySoundConvert.binCmd( convertRawBin )
        convertWavBin = CONVERT_RAW_TO_WAV % ( rawTmpFile, wavTmpFile )
        mySoundConvert.binCmd( convertWavBin )
        convertMp3Bin = CONVERT_WAV_TO_MP3 %( wavTmpFile, destFile)
        mySoundConvert.binCmd( convertMp3Bin )
        mySoundConvert.binCmd( "/bin/rm -f %s %s" % ( rawTmpFile, wavTmpFile ) )
        t2 = time.time()
        sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"soundConvert appName:%s ver:%s cmdSN:%s type:%s cmdData:%s command : "
                              "convertSPXTOMP3 srcfile:%s dstfile:%s runTime:%s\n" % ( proto.protocal['appName'],proto.protocal['ver'],proto.protocal['cmdSN'],
                                proto.protocal['type'],proto.protocal['cmdData'], srcFile,destFile,(t2-t1)) )
        sys.stdout.flush()
        return "True"
    pass
