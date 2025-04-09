#!/bin/bash

files=( /home/kbe/CS3-Server/res/server/kbengine.xml /home/kbe/CS3-Server/res/config/ServerSettingConfig.json)
hosts=( 172.16.6.225 172.16.6.226 172.16.6.223 172.16.6.198 172.16.6.197)

for host in ${hosts[@]}
do
	for file in ${files[@]}
		do
			echo $host $file
			scp $file kbe@$host:$file
		done
done

echo "copy success"
