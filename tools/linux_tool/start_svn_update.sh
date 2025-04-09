#!/bin/sh

cd /home/kbe/CS3-Server
svn update

hosts=(172.16.6.225 172.16.6.226 172.16.6.223 172.16.6.198 172.16.6.197)
for host in ${hosts[@]}
do
	#echo $host
	ssh kbe@$host "cd /home/kbe/CS3-Server && svn update && echo $host done!"
	sleep 5
done
echo done!
exit 0
