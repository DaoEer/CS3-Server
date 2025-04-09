#!/bin/sh

chmod 755 mv_and_start.sh
sh mv_and_start.sh

hosts=(172.16.6.225 172.16.6.226 172.16.6.223 172.16.6.198 172.16.6.197)
for host in ${hosts[@]}
do
	#echo $host
	ssh kbe@$host "cd /home/kbe/CS3-Server/tools/linux_tool/ && ./mv_and_start.sh && echo $host done!"
	sleep 5
done
echo done!
exit 0
