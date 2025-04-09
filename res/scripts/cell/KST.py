# -*- coding: utf-8 -*-
import os, json

import KBEngine
from KBEDebug import *


# 加载游戏对象script类
from ConfigObject.ConfigLoader import g_configLoader
from ObjectScript.ObjectScriptFactory import g_objFactory
from RoleActivityRecordMgr import g_activityRecordMgr

from ConfigObject.NavmeshLoader import g_navmeshLoader
import Const
import csstatus
import csdefine
import Settings

#当前cell中的space
g_curSpace = {}
#技能释放次数
g_useSkillTimes = 0
#地图创建次数
g_createSpaceTimes = 0
#地图销毁次数
g_destroySpceTimes = 0
#entity创建次数
g_createEntityTimes = 0
#entity销毁次数
g_destroyEntityTimes = 0

g_useSkillTimes_list = []
g_createEntityTimes_list = []
g_destroyEntityTimes_list = []

g_initFlag = False


def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	"""
	DEBUG_MSG('onInit::isReload:%s' % isReload)
	#KBEngine.cellAppData["openCheckPos"] = 1
	
	cid = os.getenv("KBE_COMPONENTID")
	key = csdefine.GLOBALDATAPREFIX_CELLAPP + cid
	KBEngine.globalData[ key ] = "{}|{}".format(os.getpid(), os.getenv("KBE_BOOTIDX_GROUP") )
	
	#设置本cellapp不参与负载均衡
	cids = g_objFactory.getAllNoBalanceCellAPPList()
	if int(cid) in cids: KBEngine.setAppFlags(KBEngine.APP_FLAGS_NOT_PARTCIPATING_LOAD_BALANCING )
	
	global g_useSkillTimes_list
	global g_createEntityTimes_list
	global g_destroyEntityTimes_list
	g_useSkillTimes_list = [0, 0]
	g_createEntityTimes_list = [0 for i in range(csdefine.ENTITY_FLAG_MAX)]
	g_destroyEntityTimes_list = [0 for i in range(csdefine.ENTITY_FLAG_MAX)]

def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData改变
	"""
	DEBUG_MSG('onGlobalData: %s' % key)
	
	#输出内存泄漏相关数据
	if Settings.test_flag:
		cid = os.getenv("KBE_COMPONENTID")
		if key == csdefine.GLOBAL_CHANNEL_KEY_MEMORY_LEAK and value:
			if hasattr(value, "client") and value.client:
				value.client.statusMessage( csstatus.GM_CHECK_INFO, "Cell[{}]内存泄漏{}".format(cid, len(KBEngine.entities.garbages)) )
		elif key == csdefine.GLOBAL_CHANNEL_KEY_RECORD_ENTITY_NUM and value:
			if hasattr(value, "client") and value.client:
				role = monster = space = 0
				for e in KBEngine.entities.values():
					if e.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
						role += 1
					elif e.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
						monster += 1
					elif e.isEntityFlag( csdefine.ENTITY_FLAG_SPACE ):
						space += 1
				value.client.statusMessage( csstatus.GM_SHOW_BASEAPP_ROLE, "Cell[{}]|role:[{}], monster:[{}], space:[{}]".format(cid, role, monster, space) )
		elif key == csdefine.GLOBAL_CHANNEL_KEY_FIND_ROLE:
			if value[1] in KBEngine.entities:
				value[0].client.statusMessage( csstatus.GM_CHECK_INFO, "role[{}]在cell[{}]".format(value[1], cid) )
		elif key == csdefine.GLOBAL_CHANNEL_KEY_HOT_CONST:
			HotUpdateConst()
		elif key == csdefine.GLOBAL_CHANNEL_KEY_CALCULATE_SERVER_INFO:
			DealServerInfo()
			
	if key == csdefine.GLOBAL_CHANNEL_KEY_OUTPUT_PROCESS_INFOS:
		OutputProcessInfos(value)

	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData删除
	"""
	DEBUG_MSG('onDelGlobalData: %s' % key)

def onCellAppData(key, value):
	"""
	KBEngine method.
	cellAppData改变
	"""
	DEBUG_MSG('onCellAppData: %s' % key)

def onCellAppDataDel(key):
	"""
	KBEngine method.
	cellAppData删除
	"""
	DEBUG_MSG('onCellAppDataDel: %s' % key)

def onSpaceData( spaceID, key, value ):
	"""
	KBEngine method.
	spaceData改变
	"""
	spaceBaseKey = Const.GET_SPACE_CELLAPP_KEY( spaceID )
	if spaceBaseKey in KBEngine.cellAppData:
		KBEngine.cellAppData[ spaceBaseKey ].cell.onSpaceDataChange( spaceID, key, value )

def onAllSpaceGeometryLoaded( spaceID, isBootstrap, mapping ):
	"""
	KBEngine method.
	space 某部分或所有chunk等数据加载完毕
	具体哪部分需要由cell负责的范围决定
	"""
	spaceBaseKey = Const.GET_SPACE_CELLAPP_KEY( spaceID )
	if spaceBaseKey in KBEngine.cellAppData:
		INFO_MSG("+++++++++++++++++++spaceEntityID =%i  spaceID=%i"%(KBEngine.cellAppData[ spaceBaseKey ].id, spaceID))
	g_navmeshLoader.loadNavmeshOver( spaceID )
	
def startLoadSpaceSpawnPoint( spaceScriptID ):
	"""
	space开始加载刷新点
	通知到这里
	"""
	pass
	
def loadOverSpaceSpawnPoint( spaceScriptID ):
	"""
	space刷新点加载完毕
	通知到这里
	"""
	#space中刷新点加载完毕后，spaceManager才算初始化完毕
	#spaceManager初始化完毕才有可能开放玩家登录
	if spaceScriptID in Settings.space_init_completed_space_scriptID:
		KBEngine.globalData[ "SpaceManager" ].onLoadOver( spaceScriptID )
		
def registerSpace(spaceID, scriptID, id, spaceKey):
	"""
	"""
	global g_curSpace
	g_curSpace[spaceID] = [scriptID, id, spaceKey]
	
	if Settings.test_flag:
		global g_createSpaceTimes
		g_createSpaceTimes += 1
	
def deregisterSpace(spaceID):
	global g_curSpace
	g_curSpace.pop(spaceID, None)
	
	if Settings.test_flag:
		global g_destroySpceTimes
		g_destroySpceTimes += 1
	
def OutputProcessInfos(token):
	temp = {}
	role = monster = 0
	global g_curSpace
	for e in KBEngine.entities.values():
		if e.spaceID not in g_curSpace:
			OUTPUT_PROCESS_INFOS("ENTITY[%d] NO FOUND SPACEID [%d]" %(e.id, e.spaceID))
			continue
		
		if e.spaceID not in temp:
			temp[e.spaceID] = [g_curSpace[e.spaceID][0], g_curSpace[e.spaceID][1], 0, 0, 0, 0, g_curSpace[e.spaceID][2]]
		
		if e.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
			role += 1
			temp[e.spaceID][2] += 1
			if e.getState() == csdefine.ENTITY_STATE_FIGHT:
				temp[e.spaceID][3] += 1
		elif e.isEntityFlag(csdefine.ENTITY_FLAG_MONSTER):
			monster += 1
			temp[e.spaceID][4] += 1
			if e.getState() == csdefine.ENTITY_STATE_FIGHT:
				temp[e.spaceID][5] += 1
		
	for lst in list(temp.values()):
		OUTPUT_PROCESS_INFOS("space:{}-{}-{}, [role:{} fight role:{}], [monster:{} fight monster:{}]".format(lst[0], lst[1], lst[6], lst[2], lst[3], lst[4], lst[5]))
	OUTPUT_PROCESS_INFOS( "token:{} entity detail: entity:{}".format( token, len( KBEngine.entities) )+ "  " + "role:{}".format(role) + "  " + "monster:{} \n".format(monster) )
	
import TracebackHook

def HotUpdateConst():
	import HotUpdate
	import HotConst
	HotUpdate.reloadByModule( HotConst )
	
def calculateUseSkillTimes(entityFlag):
	"""
	"""
	global g_useSkillTimes
	global g_useSkillTimes_list
	
	if Settings.test_flag:
		g_useSkillTimes += 1

		if entityFlag == csdefine.ENTITY_FLAG_ROLE:
			g_useSkillTimes_list[0] += 1
		else:
			g_useSkillTimes_list[1] += 1
		
def calculateCreateEntity(entityFlag):
	global g_createEntityTimes
	global g_createEntityTimes_list
	
	if Settings.test_flag:
		g_createEntityTimes+= 1
		
		if entityFlag < len(g_createEntityTimes_list):
			g_createEntityTimes_list[entityFlag] += 1
	
def calculateDestroyEntity(entityFlag):
	global g_destroyEntityTimes
	global g_destroyEntityTimes_list
	
	if Settings.test_flag:
		g_destroyEntityTimes += 1
		
		if entityFlag < len(g_destroyEntityTimes_list):
			g_destroyEntityTimes_list[entityFlag] += 1
	
def DealServerInfo():
	global g_initFlag
	global g_useSkillTimes
	global g_createSpaceTimes
	global g_destroySpceTimes
	global g_createEntityTimes
	global g_destroyEntityTimes
	global g_useSkillTimes_list
	global g_createEntityTimes_list
	global g_destroyEntityTimes_list
	
	if KBEngine.globalData.get("ServerInfosMgr", None) is None: return
	cid = os.getenv("KBE_COMPONENTID")
	KBEngine.globalData['ServerInfosMgr'].recvServerInfo(str(cid), str(g_useSkillTimes), str(g_createSpaceTimes), str(g_destroySpceTimes), str(g_createEntityTimes), str(g_destroyEntityTimes), g_useSkillTimes_list, g_createEntityTimes_list, g_destroyEntityTimes_list)
	
	#清零
	g_useSkillTimes = 0	
	g_createSpaceTimes = 0
	g_destroySpceTimes = 0
	g_createEntityTimes = 0
	g_destroyEntityTimes = 0
	
	g_useSkillTimes_list = [0, 0]
	g_createEntityTimes_list = [0 for i in range(csdefine.ENTITY_FLAG_MAX)]
	g_destroyEntityTimes_list = [0 for i in range(csdefine.ENTITY_FLAG_MAX)]