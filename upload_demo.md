``` js
<script type="text/javascript">
    function selectFile(fnUpload) {
        var filename = fnUpload.value;
        var mime = filename.toLowerCase().substr(filename.lastIndexOf("."));
        if(mime!=".jpg") {
            alert("请选择jpg格式的照片上传");
            fnUpload.outerHTML = fnUpload.outerHTML;
        }
    }
</script>
// 改JS/Burp抓包绕过
```

``` php
$info = pathinfo($_FILE]"file"]["name"]);
$ext = $info['extension'];
if (strtolower($ext) == "php") {
    exit("不允许的后缀名");
}
// php5、phtml， shell.php.aaa

if (($_FILE["file"]["type"] != "image/gif") && ($_FILES["file"]["type"] != "image/jpeg") && ($_FILES["FILE"]["type"] != "image/pjpeg")){
    echo("不允许的文件格式")
    exit($_FILES["file"]["type"]);
}
// Content-Type: image/jpeg

if(!getimagesize($_FILES["file"]["tmp_name"])){
    exit("不允许的文件");
}
// 添加文件头

# PHP < 5.3.4 && magic_quotes_gpc: OFF
$ext_arr = array('zip','rar','gif','jpg','png','bmp');
$file_ext = substr($_FILES['file']['name'],strrpos($_FILES['file']['name'],".")+1);
if(in_array($file_ext,$ext_arr)){
    $tempFile = $_FILE['file']['tmp_name'];
    $targetPath = $_REQUEST['jieduan'].rand(10,99).date("YmdHis").".".$file_ext;
    if(move_uploaded_file($tempFile,$targetPath)){
        echo '上传成功'.'<br>';
        echo '路径：'.$targetPath;
    }
}
//shell.php%00.xxx
```
