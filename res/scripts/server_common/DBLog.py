# -*- coding: utf-8 -*-
import sys
import KBEngine
import time

import Settings

def DB_LOG_MSG( type, msg, *args ):
	"""
	输出日志数据到数据库中。
	@param 			msg  : 输出的信息
	@type			msg  : STRING
	@param 			args : 可变参数，用于格式化msg
	@type 			args : 可变参数列表
	@return				 : None
	注:这里只需要打印即可被日志模块logger截获，并写入到日志数据库中
	"""
	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if args:
		message = msg % args
	else:
		message = msg
	print( "mysql$%s$%s$%s" % (type, t, message) )




def DB_LOG_log_icon_start( gyyx_lf, client_model, mac, imei, ifa, ifv ):
	"""
	玩家登录（选择指定区服，进入区服时）/登出区服时记录的日志。
	test: python cluster_controller.py sendlog 7055 DEBUG "mysql$enter_dist_log$2015-12-24 10:05:00$gyyx_lf_0001$123$account_id_001$1$10"
	
	@param      gyyx_lf: 生命指纹
	@param client_model: 设备型号
	@param          mac: MAC地址
	@param         imei: 移动设备识别码
	@param          ifa: iOS广告标识符
	@param          ifv: iOS厂商标识符
	"""
	DB_LOG_MSG( "log_icon_start", "%s$%s$%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, client_model, mac, imei, ifa, ifv ) )

def DB_LOG_log_account_login( gyyx_lf, account_id, login_type, online_sec ):
	"""
	玩家登录（选择指定区服，进入区服时）/登出区服时记录的日志。
	test: python cluster_controller.py sendlog 7055 DEBUG "mysql$enter_dist_log$2015-12-24 10:05:00$gyyx_lf_0001$123$account_id_001$1$10"
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param login_type: 类型（1:登录, 0:登出）
	@param online_sec: 在线时长
	"""
	DB_LOG_MSG( "log_account_login", "%s$%s$%s$%s" % ( gyyx_lf, account_id, login_type, online_sec ) )





def DB_LOG_enter_dist_log( gyyx_lf, account_id, login_type, online_sec ):
	"""
	玩家登录（选择指定区服，进入区服时）/登出区服时记录的日志。
	test: python cluster_controller.py sendlog 7055 DEBUG "mysql$enter_dist_log$2015-12-24 10:05:00$gyyx_lf_0001$123$account_id_001$1$10"
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param login_type: 类型（1:登录, 0:登出）
	@param online_sec: 在线时长
	"""
	DB_LOG_MSG( "enter_dist_log", "%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id, login_type, online_sec ) )

def DB_LOG_enter_scene_log( gyyx_lf, account_id, login_type, online_sec, role_id, role_lv ):
	"""
	玩家登录（选择指定角色，进入游戏时）/登出主场景时记录的日志。
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param login_type: 类型（1:登录, 0:登出）
	@param online_sec: 在线时长
	@param    role_id: 角色ID
	@param    role_lv: 角色等级
	"""
	DB_LOG_MSG( "enter_scene_log", "%s$%s$%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id, login_type, online_sec, role_id, role_lv ) )

def DB_LOG_online_log( gyyx_lf, account_id ):
	"""
	记录当前在线的玩家账号，需每五分钟内记录一次，可由服务器统一记录，亦可针对每个玩家单独记录。
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	"""
	DB_LOG_MSG( "online_log", "%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id ) )

def DB_LOG_level_log( gyyx_lf, account_id, role_id, role_lv ):
	"""
	玩家角色升级时记录的日志
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param    role_id: 角色ID
	@param    role_lv: 角色等级
	"""
	DB_LOG_MSG( "level_log", "%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id, role_id, role_lv ) )

def DB_LOG_credit_log( gyyx_lf, account_id, role_id, role_lv, money, order_no ):
	"""
	玩家充值成功时记录的日志
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param    role_id: 角色ID
	@param    role_lv: 角色等级
	@param      money: 充值金额（人民币）
	@param   order_no: 订单号
	"""
	DB_LOG_MSG( "credit_log", "%s$%s$%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id, role_id, role_lv, money, order_no ) )

def DB_LOG_cost_log( gyyx_lf, account_id, role_id, role_lv, cost_type, cost_name, money ):
	"""
	玩家在游戏中进行消费时记录的日志。
	该表中可能出现的“消费类型（cost_type列值）”及“消费名称（cost_name列值）”，
	需要您填写至《联运日志表枚举值清单》。
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param    role_id: 角色ID
	@param    role_lv: 角色等级
	@param  cost_type: 消费类型（中文，例如：金币、元宝）
	@param  cost_name: 消费名称（中文，例如：购买武器）
	@param      money: 消费金额
	"""
	DB_LOG_MSG( "cost_log", "%s$%s$%s$%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id, role_id, role_lv, cost_type, cost_name, money ) )

def DB_LOG_play_log( gyyx_lf, account_id, role_id, role_lv, t_type, t_name, op_type, use_time ):
	"""
	玩家在游戏中开始/结束某种玩法时记录的日志。
	该表中可能出现的“玩法类型（t_type列值）”及“玩法名称（t_name列值）”，
	需要您填写至《联运日志表枚举值清单》。
	
	@param    gyyx_lf: 生命指纹
	@param account_id: 账号ID
	@param    role_id: 角色ID
	@param    role_lv: 角色等级
	@param     t_type: 玩法类型（中文，例如：任务、副本）
	@param     t_name: 玩法名称（中文，例如：新手任务）
	@param    op_type: 状态（1:进入, 2:成功, 3:失败）
	@param   use_time: 完成耗时（秒）
	"""
	DB_LOG_MSG( "play_log", "%s$%s$%s$%s$%s$%s$%s$%s$%s" % ( gyyx_lf, Settings.DIST_ID, account_id, role_id, role_lv, t_type, t_name, op_type, use_time ) )

