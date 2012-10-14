#! /bin/bash
param=""
runserver="runserver"
if [ ! -z $1 ]
 then
param=$1
fi
python -c 'import werkzeug'
if [ $? = 0 ]
 then
    runserver="runserver_plus"
fi
mkdir -p cache
python manage.py $runserver $param  --adminmedia=./media/
