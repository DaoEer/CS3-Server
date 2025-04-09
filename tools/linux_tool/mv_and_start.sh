#!/bin/sh

logpath="/home/kbe/logs"
if [ ! -d "$logpath" ]; then
	mkdir "$logpath"
fi

if [ ! -x "$logpath" ]; then
	chmod 777 "$logpath" -R
fi

cd /home/kbe/CS3-Server/
mv nohup.out ./logs/

dir=$(date "+%Y-%m-%d#%H_%M_%T")
mv logs/ $dir
mv $dir ../logs/

chmod 755 kbe/bin/Hybrid_linux -R

export KBE_ROOT=$(dirname $(readlink -f "${BASH_SOURCE[0]}"))
export KBE_RES_PATH=$KBE_ROOT/res/:$KBE_ROOT/kbe/res/
export KBE_BIN_PATH=$KBE_ROOT/kbe/bin/Hybrid_linux/

killall machine
nohup $KBE_BIN_PATH/machine > nohup.out 2>&1 &

exit
