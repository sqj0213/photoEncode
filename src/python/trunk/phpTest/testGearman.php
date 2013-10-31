<?php
$client = new GearmanClient();
#$client->addServers('172.16.2.19:4730,172.16.2.20:4730');
$client->addServers('127.0.0.1:4730');


if ( isset( $argv['1'] )  && isset( $argv['2'] ) && isset( $argv['3'] ) )
{
	$src    = $argv['1'];
	$size   = $argv['2'];
	$mode   = $argv['3'];
}
elseif ( isset( $argv['1'] ) )
{
    echo "/gearman_worker/testPIC/srcPic/meitu/changgaodouda.jpg 256x172 1\n\n";
	$src    = "/gearman_worker/testPIC/srcPic/meitu/changgaodouda.jpg";
	$size   = "256x172";
	$mode   = 1;
}
elseif ( isset( $_GET['src'] ) )
{
	$src    = $_GET['src'];
	$size   = $_GET['size'] ? $_GET['size'] : '100x100';
	$mode   = $_GET['mode'] ? $_GET['mode'] : 0;
}
else
{
    echo "php ./php/testGearman.php /data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda.jpg /data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda_256x172_1.jpg 256x174 1";
    exit;
}

$sizeArr        = explode('x', $size);
$dst            = str_replace('.jpeg', "_{$size}_{$mode}.jpeg", $src);
$dst            = str_replace('.jpg', "_{$size}_{$mode}.jpg", $src);

$func   = 'resize';
$param  = array(
#        'src'   => '/data2/shm/itmp/'.$src,
#        'dst'   => '/data2/shm/itmp/'.$dst,
        'src'   => ''.$src,
        'dst'   => ''.$dst,
        'w'     => $sizeArr[0],
        'h'     => $sizeArr[1],
	'appName' =>'space_photo',
	'ver' => 1,
	'cmdSN' =>'1234567890',
        'type'  => $mode
);
$id     = md5(serialize($param));
//print_r( json_encode($param) );
$client->doHigh($func, json_encode($param), $id);

//myGraphicsMagick.myGraphicsMagick.convert_resize_gravity(srcfile="/data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda.jpg",dstfile="/data2/shm/itmp/gearman_worker/testPIC/srcPic/meitu/changgaodouda_256x172_1.jpg", w=256,h=172,need_return=False)

//(srcfile=job_json.get('src'), dstfile=job_json.get('dst'),
//                    w=job_json.get('w'), h=job_json.get('h'), need_return=False)
?>
