#!/bin/sh

sleeptime=${1}
sleep ${sleeptime}
nowdate=`date +%Y_%m_%d_%H_%M_%S`
echo "${nowdate}"
echo "reboot now"
reboot
