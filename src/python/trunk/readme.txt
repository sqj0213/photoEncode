效果:
    graphicsMagick的处理速度比convert命令行处理速度快2.5-4倍左右
    测试用例里由于convert处理封面切图时会死循环，应该是convert命令版本的问题，所以没有进行验证测试
    lib处理后的图片大小普遍比convert处理后的图片大小小40%左右(流量带宽会减少大约40%)
    gif图片的处理只能处理一帧

    运行时间测试结果:(二进制转换是普通转换的近5.5倍)
        old convert end! runTIme:6.56295609474
        lib convert end! runTIme:1.30523514748

    图片大小处理结果:
        root@sunshare-Compaq-510:~/桌面/gearman_worker# du -sk ./testPIC/libConvert
        684	./testPIC/libConvert
        root@sunshare-Compaq-510:~/桌面/gearman_worker# du -sk ./testPIC/binConvert
        1172	./testPIC/binConvert

    线上600m图片共3331张图片的处理数据:
        处理时间的数据:
            old convert end! runTIme:7646.09836388
            lib convert end! runTIme:1494.64559507

        图片处理空间数据:

            sunshare@sunshare-Compaq-510:~/桌面/gearman_worker$ du -sh ./testPIC/binConvert
                2.8G	./testPIC/binConvert
            sunshare@sunshare-Compaq-510:~/桌面/gearman_worker$ du -sh ./testPIC/libConvert
                1.2G	./testPIC/libConvert

        cmdData:{"src":"\/data2\/www\/itmp\/fengmian\/20130106\/1820\/50e94fd42dacf.jpg","dstPath":"\/data2\/www\/imggx\/i\/fengmian\/20130106\/1820","trueFile":"\/data2\/www\/imggx\/i\/fengmian\/20130106\/1820\/50e94fd42dacf.jpg","w":100,"h":100,"split":"5x4"}

        gif图片的二进制处理与lib处理结果
            35张图片的处理结果
                old convert end! runTIme:2129.611444
                lib convert end! runTIme:241.36677599
            占用空间数据
                root@sunshare-Compaq-510:/home/sunshare/桌面/gearman_worker# du -sh ./testPIC/binConvert
                212M	./testPIC/binConvert
                root@sunshare-Compaq-510:/home/sunshare/桌面/gearman_worker# du -sh ./testPIC/libConvert
                195M	./testPIC/libConvert


线上gif图片的运营数据:
     39 "type":0}
     37 "type":"1"
      6 "type":"1"}
    136 "type":"2"}
     23 "type":"3"}
      7 "type":"5"}
    145 "type":6}
      1 "type":7}
     20 "type":8}
     15 "type":9}




测试办法：
    #python不走gearmanworker测试办法
    python testCase/testCase.py
    #python走gearmanworker测试办法
    php ./phpTest/testGearman.php

上线办法:
    需要预先安装:pgmagick
    easy_install pgmagick
    会依赖boost.python包


已知问题：
    长形gif处理为对132x260_6的gif图片的处理有bug，线上对于6的gif转换要做群举测试
    产品对于高宽比失调的图片如:2600x9 10x260等图片要不允许用户上传并保存


包路径：
	http://172.16.1.200/websvn/viewvc.cgi/systemdev/gearman_convert_worker/packages/rpm/
gearman_worker程序路径:
	http://172.16.1.200/websvn/viewvc.cgi/systemdev/gearman_convert_worker/python/
音频处理部署过程：
	1.安装依赖:
		yum install sox lame libspeex-dev -y
	2.安装音频可执行程序
		rpm -ivh simpleSpeexDecode
	3.部署gearman_worker,并重启gearman_worker
	4.测试办法:到gearman_worker的程序路径运行：php ./phpTest/testSound.php测试结果


php部署过程：参见邮件
