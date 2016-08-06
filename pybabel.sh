#!/bin/bash
if [ "$1" == about ]; then
	echo Nguyen Tien Trung Kien
elif [ "$1" == extract ]; then
	pybabel extract -F babel.cfg -o messages.pot .
elif [ "$1" == init ]; then
	pybabel init -i messages.pot -d translations -l vi
elif [ "$1" == compile ]; then
	pybabel compile -d translations
elif [ "$1" == update ]; then
	pybabel update -i messages.pot -d translations
else
	echo -e './pybabel.sh extract \t Create pot files'
	echo -e './pybabel.sh init \t Init po files'
	echo -e './pybabel.sh compile \t Create mo files'
	echo -e './pybabel.sh update \t Update po files'
fi
