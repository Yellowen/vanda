#! /bin/bash
param=""
if [ ! -z $1 ]
 then
param=$1
fi
mkdir -p cache
python manage.py runserver_plus $param  --adminmedia=./media/
