<?php
$client = new GearmanClient();
$client->addServers('172.16.2.19:4730,172.16.2.20:4730');
#$client->addServers('127.0.0.1:4730');

if (count($argv) != 4 )
{
    echo "php ./php/testSoundConvert.php /data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda.spx /data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/aaa1.mp3 speexToMp3\n\n";
    exit;
}

$src = $argv[1];
$dst = $argv[2];
$type = isset( $argv[3] )?$argv[3]:'speexToMp3';

$func   = 'convertSound';
$param  = array(
        'src'   => $src,
        'dst'   => $dst,

        'appName' =>'mobileSoundConvert',
        'ver' => 1,
        'cmdSN' =>'1234567890',
        'type'  => $type
);
$id     = md5(serialize($param));
//print_r( json_encode($param) );
print_r( $client->doHigh($func, json_encode($param), $id) );

//myGraphicsMagick.myGraphicsMagick.convert_resize_gravity(srcfile="/data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda.jpg",dstfile="/data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda_256x172_1.jpg", w=256,h=172,need_return=False)

//(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
//                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
?>
