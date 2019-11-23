<?php
    $fh = fopen("log.txt", "a");
    date_default_timezone_set('Asia/Shanghai');     # 东8区
    $ip = $_SERVER["REMOTE_ADDR"];                  # 访客IP
    $filename = $_SERVER['PHP_SELF'];               # 文件名
    $parameter = $_SERVER["QUERY_STRING"];          # GET参数内容
    $time = date('H:i:s',time());             # 时间
    $i = 0;
    foreach ($_POST as $key => $value) {
        if ($i === 0) {
            $logadd = '时间： '.$time."\r\n";
            # $logadd .= '访问： '.'http://'.$ip.$filename.'?'.$parameter."\r\n";
            $logadd .= '访问： '.$filename.'?'.$parameter."\r\n";
            $logadd .= '内容： '.$key.'='.$value;
            $i++;
        } else {
            $logadd .= "&".$key.'='.$value;
        }
    }
    fwrite($fh, $logadd."\r\n\r\n");
    fclose($fh);
?>
