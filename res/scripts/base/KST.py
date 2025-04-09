# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *
import Const
import csstatus
import csdefine
import Settings

from ObjectScript.ObjectScriptFactory import g_objFactory
from ConfigObject.ConfigLoader import g_configLoader

g_teleportTimes = 0		#统计地图切换次数

g_isBootstrap = False 	#是否是第一个启动的baseapp
g_baseAppEntity = None
g_serverInfosMgr = None

temp_cellApps = {}
temp_baseAppEntitys = []
def onBaseAppReady(isBootstrap):
	"""
	KBEngine method.
	baseapp已经准备好了
	@param isBootstrap: 是否为第一个启动的baseapp
	@type isBootstrap: BOOL
	"""
	INFO_MSG('onBaseAppReady: isBootstrap=%s, appID=%s, bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' %  (isBootstrap, os.getenv("KBE_COMPONENTID"), os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")) )
	global g_baseAppEntity
	global g_serverInfosMgr
	global temp_baseAppEntitys
	global g_isBootstrap
	
	g_isBootstrap = isBootstrap
	g_baseAppEntity = KBEngine.createEntityLocally( "BaseAppEntity", {} )
	for b in temp_baseAppEntitys:
		g_baseAppEntity.registerBaseAppEntity( b )
	temp_baseAppEntitys = []
	
	if isBootstrap:#如果是第一个启动的baseapp
		g_baseAppEntity.setIsFirst()
		
		g_serverInfosMgr = KBEngine.createEntityLocally( "ServerInfosMgr", {} )
		g_serverInfosMgr.init()
		
		# 生成活动赠送和充值数据记录表
		query = """CREATE TABLE IF NOT EXISTS `custom_ChargePresentUnite` (
				`id`				BIGINT(20)   UNSIGNED NOT NULL AUTO_INCREMENT,
				`sm_transactionID`  VARCHAR(255),
				`sm_account`		VARCHAR(255),
				`sm_giftPackage`	TEXT,
				`sm_expiredTime`	TEXT,
				`sm_silverCoins`	INTEGER UNSIGNED NOT NULL DEFAULT 0,
				`sm_goldCoins`		INTEGER UNSIGNED NOT NULL DEFAULT 0,
				`sm_chargeType`		TINYINT UNSIGNED,
				`sm_type`			TINYINT UNSIGNED NOT NULL,
				PRIMARY KEY  ( `id` ),
				KEY `account_index` ( `sm_account` )
				) ENGINE=InnoDB;"""
		KBEngine.executeRawDatabaseCommand( query, createTableCB )
		
		query = """CREATE TABLE IF NOT EXISTS `custom_PointCardsTable` (
				`id`				BIGINT(20)   UNSIGNED NOT NULL AUTO_INCREMENT,
				`sm_isSelling`		BIGINT(20),
				`sm_buyerName`		text not null,
				`sm_buyerAccount`	text not null,
				`sm_price`		 	BIGINT(20),
				`sm_cardNo`			text not null,
				`sm_passWord` 		text not null,
				`sm_orderID`		text not null,
				`sm_sellTime` 		text not null,
				`sm_serverName`	 	text not null,
				`sm_salesName`	 	text not null,
				`sm_salesIP`		BIGINT(20),
				`sm_parValue`	 	BIGINT(20),
				`sm_salesAccount` 	text not null,
				PRIMARY KEY  ( `id` )
				) ENGINE=InnoDB;"""
		KBEngine.executeRawDatabaseCommand( query, createTableCB )
		
def createTableCB( result, rows, insertid, errstr ):
	"""
	生成数据库表格回调函数
	param tableName:	生成的表格名字
	type tableName:		STRING
	"""
	if errstr:
		# 生成表格错误的处理
		ERROR_MSG( "Create table fault! %s" % errstr  )
		return

def onReadyForLogin(isBootstrap):
	"""
	KBEngine method.
	如果返回值大于等于1.0则初始化全部完成, 否则返回准备的进度值0.0~1.0。
	在此可以确保脚本层全部初始化完成之后才开放登录。
	@param isBootstrap: 是否为第一个启动的baseapp
	@type isBootstrap: BOOL
	"""
	if isBootstrap:
		global g_serverInfosMgr
		progress = g_serverInfosMgr.getStartProcessPCT()
		if progress >= 1.0: g_serverInfosMgr.onServerReady()
		return progress
	return 1.0

def onBaseAppShutDown(state):
	"""
	KBEngine method.
	这个baseapp被关闭前的回调函数
	@param state: 0 : 在断开所有客户端之前
				  1 : 在将所有entity写入数据库之前
				  2 : 所有entity被写入数据库之后
	@type state: int
	"""
	global g_isBootstrap
	if g_isBootstrap:
		if not state:
			global g_serverInfosMgr
			g_serverInfosMgr.onServerShutDown()
	INFO_MSG('onBaseAppShutDown: state=%i' % state)
		
def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	@param isReload: 是否是被重写加载脚本后触发的
	@type isReload: bool
	"""
	INFO_MSG('onInit::isReload:%s' % isReload)


def onFini():
	"""
	KBEngine method.
	引擎正式关闭
	"""
	INFO_MSG('onFini()')
	
def onCellAppDeath(addr):
	"""
	KBEngine method.
	某个cellapp死亡
	"""
	WARNING_MSG('onCellAppDeath: %s' % (str(addr)))
	
def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData有改变
	"""
	DEBUG_MSG('onGlobalData: %s' % key)
	if key.find( csdefine.GLOBALDATAPREFIX_CELLAPP ) != -1:
		cid = int(key[8:])
		global temp_cellApps
		if cid not in temp_cellApps:
			temp = value.split('|')
			temp_cellApps[cid] = {"pid":int(temp[0]), "groupID":int(temp[1])}
		
		#通知spaceManager初始化(spaceManager只存在于第一个baseapp中)
		global g_isBootstrap
		spaceMgr = KBEngine.globalData.get("SpaceManager", None)
		if g_isBootstrap and spaceMgr:
			spaceMgr.initDomains()
		
	#输出内存泄漏相关数据
	if Settings.test_flag:
		cid = os.getenv("KBE_COMPONENTID")
		if key == csdefine.GLOBAL_CHANNEL_KEY_MEMORY_LEAK and value:
			if hasattr(value, "client") and value.client:
				value.client.statusMessage( csstatus.GM_CHECK_INFO, "Base[{}]内存泄漏{}".format(cid, len(KBEngine.entities.garbages)) )
		elif key == csdefine.GLOBAL_CHANNEL_KEY_FIND_ROLE:
			if value[1] in KBEngine.entities:
				value[0].client.statusMessage( csstatus.GM_CHECK_INFO, "role[{}]在base[{}]".format(value[1], cid) )
		elif key == csdefine.GLOBAL_CHANNEL_KEY_HOT_CONST:
			HotUpdateConst()
	
	if key == csdefine.GLOBAL_CHANNEL_KEY_OUTPUT_PROCESS_INFOS:
		OutputProcessInfos()
	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData有删除
	"""
	DEBUG_MSG('onDelGlobalData: %s' % key)
	

def onBaseAppData( key, value ):
	if key == Const.GLOBAL_BASEDATA_REGISTER_BASEAPP:
		if g_baseAppEntity:
			g_baseAppEntity.registerBaseAppEntity( value )
		else:
			temp_baseAppEntitys.append( value )

def onBaseAppDataDel( key, value ):
	pass

def onLoseChargeCB(ordersID, dbid, success, datas):
	"""
	KBEngine method.
	有一个不明订单被处理， 可能是超时导致记录被billing
	清除， 而又收到第三方充值的处理回调
	"""
	DEBUG_MSG('onLoseChargeCB: ordersID=%s, dbid=%i, success=%i, datas=%s' % \
							(ordersID, dbid, success, datas))

def OutputProcessInfos():
	spaceNumber = 0
	roleNumber = 0
	for e in KBEngine.entities.values():
		if hasattr(e, "isEntityFlag") and e.isEntityFlag(csdefine.ENTITY_FLAG_SPACE):
			spaceNumber += 1
	
	if not g_baseAppEntity:
		return
	
	OUTPUT_PROCESS_INFOS( "entity detail: entity:{}".format( len( KBEngine.entities) )+ "  " + "role:{}".format( len( g_baseAppEntity._localAllPlayers ) ) + "  " + "spaceNumber:{}".format(spaceNumber) )
	
	#spaceManager只存在于第一个baseapp中
	global g_isBootstrap
	spaceMgr = KBEngine.globalData.get("SpaceManager", None)
	if g_isBootstrap and spaceMgr:
		spaceMgr.OutputProcessInfos()
		
def HotUpdateConst():
	import HotUpdate
	import HotConst
	HotUpdate.reloadByModule( HotConst )
	
def calculateTeleportTimes():
	"""
	"""
	global g_teleportTimes
	if Settings.test_flag:
		g_teleportTimes += 1
	
def resetTeleportTimes():
	global g_teleportTimes
	g_teleportTimes = 0