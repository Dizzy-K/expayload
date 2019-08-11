<?php
$key = "product=card&pid=1";
$string = "QEJXUxNTQwlVABcGF0QMVAwFFmBwZzV1ZGd%2FJVhQQAIXWAMCBEZeBwAAUVJTAgoNA0BTBgdWBhZ8UgJVYkdTEywmDAxDdFRQVWVLUhR5c2tpAg4vVQFYVFQHBAVZUV5VBVEGAFdQBRIhVVVRfF9fXghkXllTXFRRCAdRAAUDBQUecwNUUnhZBgwMZV0IVW5rU1t1U1MNVVIOWFFRA1UEAwcEUQZaBUB1eWJpJiogcHcub2RmfA0XUwNUUldbEkoPVFkHVUMbX0BdRQdEXltYTxUKQQ";//加密的pd_encode字符串，需要修改
$string = base64_decode(urldecode($string));
for($i=0; $i<strlen($string); $i++)
{
        $code  .= $string[$i] ^ $key[$i];
}
echo "md5(\$key):" .$code;
?>
