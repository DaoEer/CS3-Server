cp_srv_cfg.sh:此脚本可将本地的服务器配置文件(kbengine.xml, ServerSettingConfig.json, SpaceCreateCellAllotConfig.py)
		复制到指定的机器上的指定位置（位置暂时是固定的）

set_sys_cfg.sh:此脚本主要是设置一次系统参数，这些参数影响服务器崩溃后崩溃文件的命名、大小等内容(相关内容可查看服务器部署文档1.4)

socket_optimization.sh:此脚本主要是socket参数调优

start_all_machine.sh：重命名组网服务器之前生成的logs并将其移动到../logs，重启machine

mv_and_start.sh:重命名当前服务器之前生成的logs并将其移动到../logs，重启machine

start_svn_update.sh：组网服务器svn批量更新