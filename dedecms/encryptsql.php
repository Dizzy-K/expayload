<?php
$GLOBALS['cfg_cookie_encode'] = 'CaQIm1790O';
function mchStrCode($string,$action='ENCODE')
{
    $key    = substr(md5($GLOBALS['cfg_cookie_encode']),8,18);
    $string    = $action == 'ENCODE' ? $string : base64_decode($string);
    $len    = strlen($key);
    $code    = '';
    for($i=0; $i<strlen($string); $i++)
    {
        $k        = $i % $len;
        $code  .= $string[$i] ^ $key[$k];
    }
    $code = $action == 'DECODE' ? $code : base64_encode($code);
    return $code;
}
