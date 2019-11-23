<?php
    error_reporting(1);
    define('LOG_FILENAME','/tmp/log.txt');
    function waf()
    {  
        $size=filesize("/tmp/log.txt");
        if($size>1024*1024){
            $a=file_get_contents("/tmp/log.txt");
            file_put_contents("/tmp/log".time().".txt",$a);
            unlink("/tmp/log.txt");
        }
        //it's useful when using nginx
        if (!function_exists('getallheaders')) {
            function getallheaders() {
                foreach ($_SERVER as $name => $value) {
                    if (substr($name, 0, 5) == 'HTTP_')
                        $headers[str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))))] = $value;
                }
                return $headers;

            }
        }
        $get = $_GET;
        $post = $_POST;
        $cookie = $_COOKIE;
        $header = getallheaders();
        $files = $_FILES;
        $ip = $_SERVER["REMOTE_ADDR"];
        $method = $_SERVER['REQUEST_METHOD'];
        $filepath = $_SERVER["SCRIPT_NAME"];
        $append = "<?php exit();?>".PHP_EOL;
        //print $filepath;
        //rewirte shell which uploaded by others, you can do more
        foreach ($_FILES as $key => $value) {
            $content = file_get_contents($_FILES[$key]['tmp_name']);
            file_put_contents($_FILES[$key]['tmp_name'],$append.$content);
        }

        unset($header['Accept']);//fix a bug
        $input = array("Get"=>$get, "Post"=>$post, "Cookie"=>$cookie, "File"=>$files, "Header"=>$header);
        //deal with
        $pattern = "select|insert|update|left|right|delete|and|or|\'|\/\*|\*|\.\.\/|\.\/|union|into|load_file|outfile|dumpfile|sub|hex";
        $pattern .= "|file_put_contents|fwrite|curl|system|eval|assert";
        $pattern .="|passthru|exec|system|chroot|scandir|chgrp|chown|shell_exec|proc_open|proc_get_status|popen|ini_alter|ini_restore";
        $pattern .="|`|dl|openlog|syslog|readlink|symlink|popepassthru|stream_socket_server|assert|pcntl_exec";
        $pattern .="|flag";
        #$pattern .="|tee|;|less|nano|grep|file|sed|awk|touch|usr|bin|vi|pwd|cat|head|tail|more|tac|rm|ls|tail|IFS|ls|echo|ps|ifconfig|mkdir|cp|chmod|wget|curl|`|printf";
        $vpattern = explode("|",$pattern);
        $bool = false;
        foreach ($input as $k => $v) {
            foreach($vpattern as $value){
                foreach ($v as $kk => $vv) {
                    if (preg_match( "/$value/i", $vv )){
                        $bool = true;
                        #echo "loging!";
                        logging($input,$filepath);
                        while (preg_match( "/$value/i", $vv )) {
                            $vv = preg_replace("/$pattern/i", '', $vv);
                            $v[$kk]=$vv;
                        }
                    }
                }
            }
            $input[$k] = $v; 
        }
        return $input;
    }

    function logging($var,$filepath){
        //var_dump($var);
        file_put_contents(LOG_FILENAME, urlencode(time()."-+**+-".print_r(serialize($var), true)."-+**+-".$filepath)."#####", FILE_APPEND);
    }
    $input = waf();
    $_GET = $input['Get'];
    $_POST = $input['Post'];
    $_COOKIE = $input['Cookie'];
?>
