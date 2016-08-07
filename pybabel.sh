#!/bin/bash
for cmd; do
	if [ $cmd == about ]; then
		echo Nguyen Tien Trung Kien
	elif [ $cmd == extract ]; then
		pybabel extract -F babel.cfg -o messages.pot .
	elif [ $cmd == init ]; then
		pybabel init -i messages.pot -d translations -l vi
	elif [ $cmd == compile ]; then
		pybabel compile -d translations
	elif [ $cmd == update ]; then
		pybabel update -i messages.pot -d translations
	elif [ $cmd == poedit ]; then
		poedit translations/*/LC_MESSAGES/*.po
	else
		echo -e './pybabel.sh extract \t Create pot files'
		echo -e './pybabel.sh init \t Init po files'
		echo -e './pybabel.sh compile \t Create mo files'
		echo -e './pybabel.sh update \t Update po files'
		echo -e './pybabel.sh poedit \t Open po files with poedit'
		echo 'For example:'
		echo './pybabel.sh extract update poedit compile'
	fi
done
