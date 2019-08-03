#!/bin/bash

# 安装免费版
yum install -y wget
wget -O install.sh http://download.bt.cn/install/install.sh
bash install.sh

# 升级专业版
wget -O update.sh http://download.bt.cn/install/update_pro.sh
bash update.sh pro

# Patch
cp common.py /www/server/panel/class/common.py
echo > /www/server/panel/data/userInfo.json

# 重启并输出帐密
/etc/init.d/bt restart
bt default
