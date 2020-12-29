#!/bin/bash

NOW=`date '+%s'`
YYYYMMDD=`TZ=JST-9 date --date=@${NOW} '+%Y%m%d'`
YYYYMMDD_HHMMSS=`TZ=JST-9 date --date=@${NOW} '+%Y%m%d-%H%M%S'`

mkdir -p ${IMAGE_SEQUENCE_DIRECTORY}/${YYYYMMDD}
/usr/bin/raspistill --timestamp --quality 90 --awb sun --timeout 1000 --output ${IMAGE_SEQUENCE_DIRECTORY}/${YYYYMMDD}/${YYYYMMDD_HHMMSS}.jpg