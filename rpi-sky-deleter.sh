#!/bin/bash

NOW=`date '+%s'`
YYYYMMDD=`TZ=JST-9 date --date=@${NOW} '+%Y%m%d'`

rm -r ${IMAGE_SEQUENCE_DIRECTORY}/${YYYYMMDD}