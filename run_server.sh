#! /bin/bash
param=""
if [ ! -z $1 ]
 then
param=$1
fi
python manage.py runserver $param  --adminmedia=./media/
