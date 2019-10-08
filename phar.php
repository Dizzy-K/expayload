<?php
    class TestObject {

    }
    $phar = new Phar('phar.phar');
    $phar -> startBuffering();
    $phar -> setStub('GIF89a'.'<?php __HALT_COMPILER();?>');   //设置stub，增加gif文件头
    $phar ->addFromString('test.txt','test');  //添加要压缩的文件
    $object = new TestObject();
    $object -> data = 'nu11hex';
    $phar -> setMetadata($object);  //将自定义meta-data存入manifest
    $phar -> stopBuffering();
?>
