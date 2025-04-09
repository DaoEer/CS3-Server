# -*- coding: utf-8 -*-
from SrvDef import LogDct, MoveTestTypeDct

#读取服务器配置
from LoadModule import openFile
g_serverSettingConfig = openFile('res/config/ServerSettingConfig.json')


logger_except_file = {
	"level"    : 0,
	#"format"   : '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	"format"   : '%(asctime)s %(levelname)s %(message)s',
	"datefmt"  : '%Y-%m-%d %H:%M:%S',
	"filename" : 'logs/logger_thread_except.log',
	#"filemode" : 'a'
}

# 光宇华夏登录服务器地址
sdk_server_addr = "http://api.mobile.gyyx.cn"
# 光宇华夏登录请求接口
sdk_login_path = "/gateway/user/login/?"
# server_key
sdk_encrypt_key = ""
# client_id
sdk_client_id = ""

#------------ 服务器配置 Server -------------------------------------
'''服务器ID'''
# "Local"	本地服务器
# "Trunk"	测试服务器
# "Operate"	运营服务器
serverCfg = g_serverSettingConfig["Server"]
SERVER_NAME = serverCfg["CurServerName"]
#区服ID
ServerID = serverCfg[SERVER_NAME]['serverID']

'''服务器日志数据库配置'''
# 创世3游戏日志数据库
DB_GAME_LOG_CSOL = serverCfg[SERVER_NAME]['CSGameLogDB']

'''登录排队'''
#普通登录通道最大登录人数
NormalLoginRole = int(serverCfg[SERVER_NAME]['NormalLoginRole'])
#绿色登录通道最大登录人数
GreenLoginRole = int(serverCfg[SERVER_NAME]['GreenLoginRole'])

'''登录排队web服务器相关配置'''
LoginInfoServer = serverCfg[SERVER_NAME]['LoginInfoServer']
# 组服务器
cs_server_name = serverCfg[SERVER_NAME]["name"]
# web服务器通信签名
cs_secret_key = LoginInfoServer['secret']
# web服务器地址
cs_login_ip = LoginInfoServer['ip']
cs_login_addr = "http://%s/loginInfo/" %cs_login_ip

'''验证扫码登录服务器相关配置'''
QCodeLoginServer = serverCfg[SERVER_NAME]['QCodeLoginServer']
# 服务器通信签名
cs_qcode_login_secret_key = QCodeLoginServer['secret']
# 服务器地址
cs_qcode_login_ip = QCodeLoginServer['ip']
cs_qcode_login_addr = "http://%s/qrcodeLogin/" %cs_qcode_login_ip

'''日志输出控制'''
#日志输出等级
#等级 查看SrvDef.py中LogLevel
log_level = LogDct[serverCfg[SERVER_NAME]['LogLevel']]

'''space配置'''
spaceCfg = serverCfg[SERVER_NAME]["SpaceCfg"]
#space中刷新点加载完毕后，spaceManager才算初始化完毕
#spaceManager初始化完毕才有可能开放玩家登录
space_init_completed_space_scriptID = spaceCfg["SpaceInitComplete"]
#至少起多少个cell之后才开始初始化spaceManager
space_wait_init_cell_amount = int(spaceCfg["SpaceWaitCellAmount"])
#SpaceManager初始化等待时长
space_wait_init_time = int(spaceCfg["SpaceWaitInitTime"])
#每个Tick初始化的领域数目
space_init_domain_per = int(spaceCfg["SpaceInitPer"])
#tick时长
space_wait_init_tick = int(spaceCfg["SpaceWaitInitTick"])

#防沉迷配置
antiwallow_Info = serverCfg[SERVER_NAME]["AntiwallowInfo"]
#防沉迷服务器(远端服务器)
antiWallowBridgeSVHost = antiwallow_Info["AWBSVHOST"]
#本地监听ip及端口
antiWallowBridgeCLHost = antiwallow_Info["AWBCLHOST"]

'''游戏付费时间'''
gameTimeCfg = serverCfg[SERVER_NAME]["GameTime"]
#是否开放游戏时间付费（开放后，未激活的账号无法创建）
open_game_time_activation = gameTimeCfg['OpenGameTimeActivation']
#系统默认给与玩家的游戏时间
default_game_time = gameTimeCfg['DefaultGameTime']
#开始消耗游戏付费时间等级
start_billing_level = gameTimeCfg['StartBillingLevel']
#到达付费等级后，玩家没有剩余时间，给玩家在游戏中的缓冲时间
slack_time = gameTimeCfg['SlackTime']

'''测试总开关'''
#只有这里设置为True，下面服务器测试配置选项才有效
test_flag = serverCfg[SERVER_NAME]['TestFlag']


#------------ 服务器测试相关 ServerTest (只有test_flag设置为True，测试配置才有效) ---------
ServerTest = g_serverSettingConfig['ServerTest']

'''测试配置'''
#是否等待系统初始化完毕才开放玩家登录
wait_system_init = ServerTest['WaitSystemInit']
#是否开放账号激活接口（开放后，未激活的账号无法创建）
open_account_activation = ServerTest['OpenAccountActivation']

'''移动测试配置'''
#移动方式测试配置 查看SrvDef.py中MoveTestType
move_test = MoveTestTypeDct[ServerTest['MonsterMoveTest']]

'''间隔时间配置'''
#服务器打印进程信息时间间隔（包括副本怪物数目，玩家数目……）
record_Process_Info_Time = float(ServerTest['RecordProcessInfoTime'])

'''服务器信息统计间隔时间（地图跳转次数、技能释放次数）'''
culate_Server_Info_Time = float(ServerTest['CulateServerInfoTime'])

'''跨服'''
cross_service_ip = serverCfg[SERVER_NAME]['CrossService']['ip']
cross_service_addr = "http://%s/CrossService" % cross_service_ip