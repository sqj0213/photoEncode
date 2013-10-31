#!/bin/env python
#coding=utf8
#import gearman.GearmanWorker
#from gearman.worker import GearmanWorker
"""
安装说明：
    环境依赖： python version >= 2.6
    python modules:
        gearman / python_daemon
    ImageMagic version >= 6.6
调整参数：
    1, gearman_worker.py : line 29
        调整 JOB_SERVER_LIST = [your job server list] . example : ['127.0.0.1:4730', ]
    2, ImageConvert. ImageConvert.py : line 8
        确认 convert 指令的路径 GM_COMMAND = r'/usr/bin/convert ' .
        ***注意***  convert 后面需要空格
"""

#TODO： 1,增加 logging 模块对日志的记录
#20120810
#增加10个进程启动运行
from datetime import *
import os, sys, multiprocessing, uuid
import gearman
from daemon.runner import *
from ImageConvert import ImageConvert
from myGraphicsMagick import myGraphicsMagick
from mySoundConvert import mySoundConvert
from inc import commFunc
from inc import proto
try:
    import json
except ImportError:
    import simplejson as json

#Define some variables
JOB_SERVER_LIST = ['172.16.2.19:4730','172.16.2.20:4730']
#JOB_SERVER_LIST = ['127.0.0.1:4730']
MAX_PROCESS = 5


class CustomGearmanWorker(gearman.worker.GearmanWorker):
    def on_job_execute(self, current_job):
    #        print "Job started"
        return super(CustomGearmanWorker, self).on_job_execute(current_job)

    def on_job_exception(self, current_job, exc_info):
    #        print "Job failed, CAN stop last gasp GEARMAN_COMMAND_WORK_FAIL"
        return super(CustomGearmanWorker, self).on_job_exception(current_job, exc_info)

    def on_job_complete(self, current_job, job_result):
    #        print "Job done"
        return super(CustomGearmanWorker, self).send_job_complete(current_job, job_result)

    def after_poll(self, any_activity):
    #        Return True if you want to continue polling, replaces callback_fxn
        return True


def task_callback(gearman_worker, job):
#    print job.data
    try:
        job_json = json.loads(job.data)
        if job_json.get('h') == 100:
            return str(job_json.get('h'))
        else:
            return "ERROR"
    except Exception as e:
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"worker_run failed:%s %s \n" % (e.args, e.message ))
        return e.message
    finally:
        pass
def do_convertSound( gearman_worker, job ):
    try:
        job_json = json.loads(job.data)

        proto.protocal['appName'] = job_json.get('appName')
        if ( proto.protocal['appName'] is None ):
            proto.protocal['appName'] = ''
        tmpVal = job_json.get('ver')
        if tmpVal is None:
            proto.protocal['ver'] = 0
        else:
            proto.protocal['ver'] = int(tmpVal)

        proto.protocal['cmdSN'] = job_json.get('cmdSN')
        if ( proto.protocal['cmdSN'] is None ):
            proto.protocal['cmdSN'] = ''

        if tmpVal is None:
            proto.protocal['type'] = 0
        else:
            if ( tmpVal == '' ):
                proto.protocal['type'] = ''
            else:
                proto.protocal['type'] = int(tmpVal)

        proto.protocal['cmdData'] = job.data
        #sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"protocal data:%s\n", job.data )
        #sys.stdout.flush()
        if ( proto.protocal['ver'] >= 1 ):
            sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"recive protocaldata:%s\n"%(job.data) )
            sys.stdout.flush()


        if ( proto.protocal['appName'] == "mobileSoundConvert" ):
           return  mySoundConvert.mySoundConvert.convertSPXTOMP3( srcFile = job_json.get( 'src' ), destFile = job_json.get( 'dst' ) )
        return True

    except Exception as e:
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"do_resize failed::%s %s protoData:%s\n" % (e.args, e.message, proto.protocalStr ))
        sys.stdout.flush()
        sys.stderr.flush()
        return "False"
    finally:
        if job_json:
            job_json = None


def do_resize(gearman_worker, job):
    try:
        job_json = json.loads(job.data)

        proto.protocal['appName'] = job_json.get('appName')
        if ( proto.protocal['appName'] is None ):
            proto.protocal['appName'] = ''
        tmpVal = job_json.get('ver')
        if tmpVal is None:
            proto.protocal['ver'] = 0
        else:
            proto.protocal['ver'] = int(tmpVal)

        proto.protocal['cmdSN'] = job_json.get('cmdSN')
        if ( proto.protocal['cmdSN'] is None ):
            proto.protocal['cmdSN'] = ''
        tmpVal = job_json.get('type')

        if tmpVal is None:
            proto.protocal['type'] = 0
        else:
	        if ( tmpVal == '' ):
		        proto.protocal['type'] = ''
	        else:
           	    proto.protocal['type'] = int(tmpVal)

        proto.protocal['cmdData'] = job.data

        if ( proto.protocal['ver'] >= 1 ):
            sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"recive protocaldata:%s\n"%(job.data) )
            sys.stdout.flush()


        if tmpVal is None:
            convert_type = -100
        else:
            if ( tmpVal == '' ):
                convert_type = -100
            else:
                convert_type  = int(tmpVal)

        if convert_type == 1:

            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_gravity(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_gravity(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 2:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_exactly(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_exactly(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 3:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_greater(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_greater(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 4:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_smaller(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_smaller(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 5:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_crop(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_crop(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 6:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_coalesce(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_coalesce(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 7:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_gif_thumbnail_frame0(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_gif_thumbnail_frame0(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        elif convert_type == 8:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_gif_thumbnail_frame0_g(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_gif_thumbnail_frame0_g(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re
        elif convert_type == 9:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_thumbinal(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_thumbinal(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re
        elif convert_type == 0:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_simple_with_width(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re
        elif convert_type == 10:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple_with_width_at(srcfile=job_json.get('src'),
                    dstfile=job_json.get('dst'),
                    w=job_json.get('w'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_simple_with_width_at(srcfile=job_json.get('src'),
            #        dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

        else:
            if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
                re = myGraphicsMagick.myGraphicsMagick.convert_resize_simple(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            #else:
            #    re = ImageConvert. ImageConvert.convert_resize_simple(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
            #        w=job_json.get('w'), h=job_json.get('h'), need_return=False)
            sys.stdout.flush()
            sys.stderr.flush()
            return re

    except Exception as e:
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"do_resize failed::%s %s protoData:%s\n" % (e.args, e.message, proto.protocalStr ))
        sys.stdout.flush()
        sys.stderr.flush()
        return "False"
    finally:
        if job_json:
            job_json = None


def do_rotate(gearman_worker, job):
    try:
        job_json = json.loads(job.data)


        proto.protocal['appName'] = job_json.get('appName')
        if ( proto.protocal['appName'] is None ):
            proto.protocal['appName'] = ''
        tmpVal = job_json.get('ver')
        if tmpVal is None:
            proto.protocal['ver'] = 0
        else:
            proto.protocal['ver'] = int(tmpVal)

        proto.protocal['cmdSN'] = job_json.get('cmdSN')
        if ( proto.protocal['cmdSN'] is None ):
            proto.protocal['cmdSN'] = ''
        tmpVal = job_json.get('type')

        if tmpVal is None:
            proto.protocal['type'] = 0
        else:
            proto.protocal['type'] = int(tmpVal)

        proto.protocal['cmdData'] = job.data
        if ( proto.protocal['ver'] >= 1 ):
            sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"recive protocaldata:%s\n"%(job.data) )
            sys.stdout.flush()

        if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
            re = myGraphicsMagick.myGraphicsMagick.rotate(srcFile=job_json.get('src'),destFile=job_json.get('dst'),rotate=job_json.get('rotate'))
        else:
            re = ImageConvert. ImageConvert.convert_rotate(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
                rotate=job_json.get('rotate'))

        return str(re)
    except Exception as e:
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"do_rotate failed::%s %s protoData:%s\n" % (e.args, e.message, proto.protocalStr ))
        sys.stderr.flush()

        return "False"
    finally:
        if job_json:
            job_json = None


def do_split(gearman_worker, job):
    """
    目前仅用作封面的切割
    """
    try:

        job_json = json.loads(job.data)


        proto.protocal['appName'] = job_json.get('appName')
        if ( proto.protocal['appName'] is None ):
            proto.protocal['appName'] = ''
        tmpVal = job_json.get('ver')
        if tmpVal is None:
            proto.protocal['ver'] = 0
        else:
            proto.protocal['ver'] = int(tmpVal)

        proto.protocal['cmdSN'] = job_json.get('cmdSN')
        if ( proto.protocal['cmdSN'] is None ):
            proto.protocal['cmdSN'] = ''
        tmpVal = job_json.get('type')

        if tmpVal is None:
            proto.protocal['type'] = 0
        else:
            proto.protocal['type'] = int(tmpVal)

        proto.protocal['cmdData'] = job.data
        if ( proto.protocal['ver'] >= 1 ):
            sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"recive protocaldata:%s\n"%(job.data) )
            sys.stdout.flush()

        if ( len(  proto.protocal['appName'] ) != 0 and  proto.protocal['ver'] >= 1 ):
	    re = ImageConvert. ImageConvert.convert_split(srcfile=job_json.get('src'), dstpath=job_json.get('dstPath'),
                truefile=job_json.get('trueFile'),
                split=job_json.get('split'), w=job_json.get('w'), h=job_json.get('h'))
            #re = myGraphicsMagick.myGraphicsMagick.convert_split(srcfile=job_json.get('src'),dstpath=job_json.get('dstPath'),truefile=job_json.get('trueFile'),split=job_json.get('split'),w=job_json.get('w'),h=job_json.get('h'))
        else:
            re = ImageConvert. ImageConvert.convert_split(srcfile=job_json.get('src'), dstpath=job_json.get('dstPath'),
                truefile=job_json.get('trueFile'),
                split=job_json.get('split'), w=job_json.get('w'), h=job_json.get('h'))

        return str(json.dumps(re))
    except Exception as e:
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"do_split failed:%s %s protoData:%s\n" % (e.args, e.message, proto.protocalStr ))
        sys.stderr.flush()
        return 'False'
    finally:
        if job_json:
            job_json = None


def worker_run():
    #TODO:需要在循环中检测该worker与job server 的连接状况，如异常，需要进行处理

    try:
        worker = CustomGearmanWorker(JOB_SERVER_LIST)
        worker.set_client_id(str(uuid.uuid1()))
        if worker:

            worker.register_task("convert", task_callback)
            worker.register_task("resize", do_resize)
            worker.register_task("rotate", do_rotate)
            worker.register_task("split", do_split)
            worker.register_task("convertSound",do_convertSound )
            worker.work()
        else:
            sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"worker_run notice\n")
            sys.stdout.flush()
            pass
    except Exception as e:
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"worker_run failed:%s %s \n" % (e.args, e.message ))


class GearmanWorkerDaemon(object):
    def __init__(self):
        self.name = 'gearman_worker_dameon'
        #TODO: working_directory 需要等候部署时待定
        self.working_directory = os.getcwd()
        self.stdin_path = os.devnull
        self.stdout_path = '/var/log/gearmanWorkerDaemon-access.log'
        self.stderr_path = '/var/log/gearmanWorkerDaemon-error.log'
        self.pidfile_path = '/var/run/' + self.name + '.pid'
        self.pidfile_timeout = 120
    def run(self):
        sys.stderr.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+"worker_run begin\n")
        workerList = list()
        #sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+'start gearman Worker begin: max_process %d'%(commFunc.confIniDict['default']['maxprocess']))
        maxProcess = int(commFunc.confIniDict['default']['maxprocess'])
        for tp in range(0, maxProcess ) :
            p = multiprocessing.Process(target=worker_run)
            workerList.append(p)
            p.name = 'gearman worker child process'
            p.daemon = True
            p.start()
        #sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+'start gearman Worker end!' )
        for p in workerList:
            p.join()

if __name__ == "__main__":
    daemon_instance = GearmanWorkerDaemon()
    myRunner = DaemonRunner(daemon_instance)
    sys.stdout.writelines(datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')+'do_action begin!\n' )
    myRunner.do_action()
