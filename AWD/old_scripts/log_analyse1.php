<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>日志分析</title>
    <meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, width=device-width">
    <style>body{background-color:#fff;font-family:"Roboto",helvetica,arial,sans-serif;font-size:16px;font-weight:400;text-rendering:optimizeLegibility}div.table-title{display:block;margin:auto;max-width:600px;padding:5px;text-align:center;width:100%}.table-title h3{color:#000;font-size:30px;font-weight:400;font-style:normal;font-family:"Roboto",helvetica,arial,sans-serif;text-shadow:-1px -1px 1px rgba(0,0,0,0.1);text-transform:uppercase}.table-fill{background:white;border-radius:3px;border-collapse:collapse;height:320px;margin:auto;padding:5px;width:calc(98%);box-shadow:0 5px 10px rgba(0,0,0,0.1);animation:float 5s infinite}th{color:#D5DDE5;background:#1b1e24;border-bottom:4px solid #9ea7af;border-right:1px solid #343a45;font-size:23px;font-weight:100;padding:24px;text-align:left;text-shadow:0 1px 1px rgba(0,0,0,0.1);vertical-align:middle}th:first-child{border-top-left-radius:3px}th:last-child{border-top-right-radius:3px;border-right:none}tr{border-top:1px solid #C1C3D1;border-bottom-:1px solid #C1C3D1;color:#666B85;font-size:16px;font-weight:normal;text-shadow:0 1px 1px rgba(255,255,255,0.1)}tr:first-child{border-top:none}tr:last-child{border-bottom:none}tr:nth-child(odd) td{background:#EBEBEB}tr:last-child td:first-child{border-bottom-left-radius:3px}tr:last-child td:last-child{border-bottom-right-radius:3px}td{background:#FFFFFF;padding:20px;text-align:left;vertical-align:middle;font-weight:300;font-size:18px;text-shadow:-1px -1px 1px rgba(0,0,0,0.1);border-right:1px solid #C1C3D1;overflow:hidden;overflow-x:auto}td.cookie,td.header{max-width:300px}td:last-child{border-right:0}th.text-left{text-align:left}th.text-center{text-align:center}th.text-right{text-align:right}td.text-left{text-align:left}td.text-center{text-align:center}td.text-right{text-align:right}</style>
</head>
<?php
    error_reporting(0);

    $a=file_get_contents("/tmp/log.txt");
    $var=split("#####",$a);

    //var_dump($var[0]);

?>
<body>
    <div class="table-title">
        <h3>日志分析</h3>
    </div>
    <table class="table-fill">
        <thead>
            <tr>
                <th class="text-center">Time</th>
                <th class="text-center">Script_path</th>
                <th class="text-center">Get</th>
                <th class="text-center">Post</th>
                <th class="text-center">Cookie</th>
                <th class="text-center">File</th>
                <th class="text-center">Header</th>
            </tr>
        </thead>
        <tbody class="table-hover">
                <?php
                for($i=count($var)-1;$i>=0;$i--){
                    $var[$i]=urldecode($var[$i]);
                    $tmp=@split('-\+\*\*\+-',$var[$i]);
                    //var_dump($tmp);
                    date_default_timezone_set('PRC');
                    $date=date("Y-m-d G:i:s", $tmp[0]);
                    //echo "$tmp[1]";
                    $param=unserialize($tmp[1]);
                    //var_dump($param);
                    $filepath=$tmp[2];

                ?>
                    <tr>
                        <td class="text-left"><?php echo $date;?></td>
                        <td class="text-left"><?php echo $filepath;?></td>
                        <td class="text-left"><?php foreach($param['Get'] as $k=>$v){echo "&".htmlspecialchars($k)."= ".urlencode(htmlspecialchars($v));};?></td>
                        <td class="text-left"><?php foreach($param['Post'] as $k=>$v){echo "&".htmlspecialchars($k)."= ".urlencode(htmlspecialchars($v));};?></td>
                        <td class="text-left cookie"><?php foreach($param['Cookie'] as $k=>$v){echo htmlspecialchars($k)."= ".htmlspecialchars($v)."<br />";};?></td>
                        <td class="text-left"><?php foreach(reset($param['File']) as $k=>$v){echo htmlspecialchars($k).": ".htmlspecialchars($v)."<br />";};?></td>
                        <td class="text-left header"><?php foreach($param['Header'] as $k=>$v){echo htmlspecialchars($k).": ".htmlspecialchars($v)."<br />";};?></td>
                    </tr>
                <?php
                }
                ?>
        </tbody>
    </table>
</body>
</html>
