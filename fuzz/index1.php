<?php
$a = str_split('getFlag');
for($i = 0; $i < 256; $i++){
    $ch = '{'^ chr($i);
    if (in_array($ch, $a , true)) {
        echo "{ ^ chr(".$i.") = $ch<br>";
    }
}
echo "{{{{{{{"^chr(28).chr(30).chr(15).chr(61).chr(23).chr(26).chr(28);

?>
