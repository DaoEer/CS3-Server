# -*- coding: utf-8 -*-

# 副本事件行为
import random
import math
import time
import Math
import KBEMath
import KBEDebug
import KBEngine
import csdefine
import csstatus
import Const
import Functions
import csarithmetic
import KST
from csgeometry import Polygon
import csconst

import Reward.RewardBasicValueData as RewardBase
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from ConfigObject import PatrolRouteLoader
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
import ItemTypeEnum
HAS_PIECE_NONE = 0
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
from ConfigObject.Drop import DropItem
from ConfigObject.TongSpaceCopyRewardLoader import g_TongSpaceCopyRewardLoader

from MsgLogger import g_logger
import LogDefine

def createTeamDropBox(spaceEntity, position, direction, modelNumber, modelScale, itemInsts, ownerDBIDs, allocation, teamID, teamCaptainDBID):
	"""
	"""
	if spaceEntity is None:
		return
	
	freeAllocationItems = {}
	notAllocationItems = {}
	for itemInst in itemInsts:
		if itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN:
			notAllocationItems[itemInst.uid] = itemInst
		else:
			freeAllocationItems[itemInst.uid] = itemInst
	
	args = {
		"hasEffect"				: False,
		"teamID"				: teamID,
		"allocation"			: allocation,
		"ownerDBIDs"			: ownerDBIDs,
		"modelScale"			: modelScale,
		"modelNumber"			: modelNumber,
		"teamCaptainDBID"		: teamCaptainDBID,
		"freeAllocationItems"	: freeAllocationItems,
		"notAllocationItems"	: notAllocationItems,
	}
	dropbox = spaceEntity.createEntityNear("TeamDropBox", position, direction, args)

class SEAction1( SEActionBase ):
	"""
	设置副本当前阶段为某阶段
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.stageIndex = int( section["param1"] )	# 阶段索引值

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().setSpaceStage( spaceEntity, self.stageIndex )

class SEAction2( SEActionBase ):
	"""
	副本内所有玩家完成某任务目标
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = int( section["param1"] )
		self.taskID = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.questTaskIncreaseState( self.questID, self.taskID )

class SEAction3( SEActionBase ):
	"""
	副本通关
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isShowTimeCountDown = True
		if section["param1"]:
			self.isShowTimeCountDown = False

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().onSpaceSuccess( spaceEntity, self.isShowTimeCountDown )

class SEAction4( SEActionBase ):
	"""
	副本失败
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isShowTimeCountDown = True
		if section["param1"]:
			self.isShowTimeCountDown = False

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().onSpaceFailure( spaceEntity, self.isShowTimeCountDown )

class SEAction5( SEActionBase ):
	"""
	设置副本动态复活点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.positionStr  = section["param1"]
		self.directionStr = section["param2"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.setDynamicReviverInfo( self.positionStr, self.directionStr )

class SEAction6( SEActionBase ):
	"""
	指定位置召唤指定ID的entity，可支持多个位置对应召唤多个entities
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.spawnInfos = []	#[(scriptID,pos,dir,amount)]
	
	def init( self, section ):
		SEActionBase.init( self, section )
		__posList = []		#位置列表
		__dirList = []		#朝向列表
		__idAndNumList = []	#scriptID和数量列表 [[(scriptID,amount)]]
		
		# 读取
		posStrList = section["param1"].split("|")		#格式 "x1 y1 z1 | x2 y2 z2 |..."
		for posStr in posStrList:
			pos = Functions.vector3TypeConvert( posStr )
			__posList.append( KBEMath.Unreal2KBEnginePosition( pos ) )
		
		dirStrList = section["param2"].split("|")		#格式 "x1 y1 z1 | x2 y2 z2 |..."
		for dirStr in dirStrList:
			dir = Functions.vector3TypeConvert( dirStr )
			__dirList.append( KBEMath.Unreal2KBEngineDirection( dir ) )
		
		allEntityInfo = section["param3"].split("|")	#格式 "scriptID1:amount1; scriptID2:amount2 | scriptID3:amount3 |..."
		for onePosInfo in allEntityInfo:
			tempList = []
			for oneEntityInfo in onePosInfo.split(";"):
				tempInfo = oneEntityInfo.split(":")
				scriptID, amount = tempInfo[0], int( tempInfo[1] )
				tempList.append( ( scriptID, amount ) )
			__idAndNumList.append( tempList )
		
		# 验证
		if not __posList or not __dirList or not __idAndNumList:
			KBEDebug.ERROR_MSG( "Param lack!" )
			return
		if len( __posList ) != 1 and len( __dirList ) != 1 and len( __posList ) != len( __dirList ):
			KBEDebug.ERROR_MSG( "Pos num and dir num not match! ", section["param1"] )	#输出一个参数以便查找配置
			return
		if len( __posList ) != 1 and len( __idAndNumList ) != 1 and len( __posList ) != len( __idAndNumList ):
			KBEDebug.ERROR_MSG( "Pos num and scriptID num not match! ", section["param1"] )
			return
		
		# 组装位置和朝向
		posAndDirList = []
		if len( __posList ) == 1 and len( __dirList ) == 1:
			posAndDirList.append( ( __posList[0], __dirList[0] ) )
		elif len( __dirList ) == 1:
			for pos in __posList:
				posAndDirList.append( ( pos, __dirList[0] ) )
		elif len( __posList ) == 1:
			for dir in __dirList:
				posAndDirList.append( ( __posList[0], dir ) )
		else:
			for index, pos in enumerate( __posList ):
				posAndDirList.append( ( pos, __dirList[index] ) )
		
		# 扩充位置和朝向列表 或者 扩充scriptID和数量列表
		num = max( len( __idAndNumList ), len( posAndDirList ) )
		if len( __idAndNumList ) != num:
			__idAndNumList = __idAndNumList * num
		if len( posAndDirList ) != num:
			posAndDirList = posAndDirList * num
		
		# 组装位置、朝向、scriptID、数量
		for index, tempList in enumerate( __idAndNumList ):
			posAndDir = posAndDirList[ index ]
			for info in tempList:
				self.spawnInfos.append( ( info[0], posAndDir[0], posAndDir[1], info[1] ) )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for info in self.spawnInfos:
			for i in range( info[3] ):
				entity = spaceEntity.createEntityByScriptID( info[0], info[1], info[2], { "spawnPos": info[1], "spawnDir": info[2] } )

class SEAction7( SEActionBase ):
	"""
	scriptID为某值的entity播放镜头（AOI范围内的玩家有效）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID  = section["param1"]
		self.sceneID  = section["param2"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for id in spaceEntity.getEntityRecord( self.scriptID ):
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			for roleEntity in spaceEntity._spaceRoles:
				if roleEntity.position.distTo( entity.position ) <= roleEntity.getViewRadius():
					roleEntity.client.StartPlayStory( self.sceneID, 1 )

class SEAction8( SEActionBase ):
	"""
	scriptID为某值的entity播放动作,填多个则连续播放多个动作
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID  = section["param1"]
		self.actionIDs  = section["param2"].split("|")
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for id in spaceEntity.getEntityRecord( self.scriptID ):
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.allClients.CLIENT_SpaceEventPlayAction( self.actionIDs )

class SEAction9( SEActionBase ):
	"""
	销毁某些scriptID的entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for scriptID in self.scriptIDs:
			idList = list( spaceEntity.getEntityRecord( scriptID ) )
			for id in idList:
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entity.delayDestroy( 0.2 )

class SEAction10( SEActionBase ):
	"""
	给某些scriptID的怪物发送AI指令
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
		self.commandID = section["param2"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for scriptID in self.scriptIDs:
			for id in spaceEntity.getEntityRecord( scriptID ):
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entity.monsterAIOnCommand( spaceEntity.id, spaceEntity.scriptID, self.commandID )

class SEAction11( SEActionBase ):
	"""
	多个scriptID中随机几个发送AI指令
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
		self.randomNum = int( section["param2"] )
		self.commandID = section["param3"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		IDs = random.sample( self.scriptIDs, self.randomNum )
		for scriptID in IDs:
			for id in spaceEntity.getEntityRecord( scriptID ):
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entity.monsterAIOnCommand( spaceEntity.id, spaceEntity.scriptID, self.commandID )

class SEAction12( SEActionBase ):
	"""
	添加Timer
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.timerKey  = section["param1"]
		self.time = float( section["param2"] )
		self.isLoop = int( section["param3"] )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().spaceEvent_addTimer( spaceEntity, self.timerKey, self.time, self.isLoop )

class SEAction13( SEActionBase ):
	"""
	取消Timer
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.timerKey  = section["param1"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().spaceEvent_cancelTimer( spaceEntity, self.timerKey )

class SEAction14( SEActionBase ):
	"""
	销毁存活的某批次某scriptID的entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.group  = int( section["param1"] )
		self.scriptIDs = section["param2"].split( "|" )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		allRecord = spaceEntity.getAllEntityRecord()
		for scriptID in list(allRecord):
			if self.scriptIDs[0] != "" and scriptID not in self.scriptIDs:	#不填scriptID则销毁该批次所有entity
				continue
			idList = allRecord[scriptID]
			for id in list(idList):
				entity = KBEngine.entities.get( id )
				if not entity or entity.group != self.group:
					continue
				entity.destroySelf()

class SEAction15( SEActionBase ):
	"""
	触发者（必须是玩家）完成某任务目标
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = int( section["param1"] )
		self.taskID = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		trigger.questTaskIncreaseState( self.questID, self.taskID )

class SEAction16( SEActionBase ):
	"""
	系统对触发者释放一个技能
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.skillID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			trigger.useSkillToEntity( self.skillID, trigger.id )

class SEAction17( SEActionBase ):
	"""
	系统对副本内所有玩家释放一个技能
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.skillID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.useSkillToEntity( self.skillID, e.id )

class SEAction18( SEActionBase ):
	"""
	触发者（必须是玩家）播放界面提示并播放声音
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.soundID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			trigger.roleSpaceCopyPlaySound(self.soundID)

class SEAction19( SEActionBase ):
	"""
	副本内所有玩家播放界面提示并播放声音
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.soundID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.roleSpaceCopyPlaySound(self.soundID)

class SEAction20( SEActionBase ):
	"""
	传送所有玩家出位面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.leaveSpacePlane( self.scriptID )

class SEAction21( SEActionBase ):
	"""
	传送触发者（必须是玩家）到指定地图
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.spaceScriptID = section["param1"]
		
		pos = Functions.vector3TypeConvert( section["param2"] )
		dir = Functions.vector3TypeConvert( section["param3"] )
		self.position  = KBEMath.Unreal2KBEnginePosition( pos )
		self.direction = KBEMath.Unreal2KBEngineDirection( dir )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			trigger.gotoSpace( self.spaceScriptID, self.position, self.direction )

class SEAction22( SEActionBase ):
	"""
	传送副本内所有玩家到指定地图
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.spaceScriptID = section["param1"]
		
		pos = Functions.vector3TypeConvert( section["param2"] )
		dir = Functions.vector3TypeConvert( section["param3"] )
		self.position  = KBEMath.Unreal2KBEnginePosition( pos )
		self.direction = KBEMath.Unreal2KBEngineDirection( dir )

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.gotoSpace( self.spaceScriptID, self.position, self.direction )

class SEAction23( SEActionBase ):
	"""
	删除触发者（必须是玩家）某ID的物品（绑定和非绑定都移除）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDs = [ int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		
		for itemID in self.itemIDs:
			itemList = trigger.getItemInstsByID( itemID )
			for itemInst in itemList:
				trigger.removeItemByAmount( itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )

class SEAction24( SEActionBase ):
	"""
	删除副本内所有玩家某ID的物品（绑定和非绑定都移除）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDs = [ int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			for itemID in self.itemIDs:
				itemList = e.getItemInstsByID( itemID )
				for itemInst in itemList:
					e.removeItemByAmount( itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )

class SEAction25( SEActionBase ):
	"""
	移除触发者身上的Buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffIDs = [ int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			for buffID in self.buffIDs:
				if len(trigger.findBuffsByBuffID(buffID)):
					trigger.removeBuffByID( buffID )

class SEAction26( SEActionBase ):
	"""
	移除副本内所有玩家身上的Buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffIDs = [ int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			for buffID in self.buffIDs:
				e.removeBuffByID( buffID )

class SEAction27( SEActionBase ):
	"""
	刷新一批怪（刷了光效怪则先刷光效怪）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.group = int( section["param1"] )
		self.effectID = section["param2"]
		self.delaySpawnTime = 0
		if section["param3"]:
			self.delaySpawnTime = int( section["param3"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.spawnGroupEntity( self.group, self.effectID, self.delaySpawnTime )

class SEAction28( SEActionBase ):
	"""
	刷新一批怪物中的某一些怪物（刷了光效怪则先刷光效怪）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.group = int( section["param1"] )
		self.effectID = section["param2"]
		self.delaySpawnTime = 0
		if section["param3"]:
			self.delaySpawnTime = int( section["param3"] )
		
		self.idAndAmountDict = {}
		for tempStr in section["param4"].split( "|" ):
			id, amount = tempStr.split( ":" )
			self.idAndAmountDict[ id ] = int( amount )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.spawnGroupSomeEntity( self.group, self.effectID, self.delaySpawnTime, self.idAndAmountDict )

class SEAction29( SEActionBase ):
	"""
	重置触发者某任务目标
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = int( section["param1"] )
		self.taskIDs = [ int(i) for i in section["param2"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			for id in self.taskIDs:
				trigger.questTaskResetState( self.questID, id )

class SEAction30( SEActionBase ):
	"""
	重置副本内所有玩家某任务目标
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = int( section["param1"] )
		self.taskIDs = [ int(i) for i in section["param2"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			for id in self.taskIDs:
				e.questTaskResetState( self.questID, id )

class SEAction31( SEActionBase ):
	"""
	增加某计数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.countKey = section["param1"]
		self.addValue = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().spaceEvent_addCount( spaceEntity, self.countKey, self.addValue )

class SEAction32( SEActionBase ):
	"""
	给副本中的所有玩家发送消息 (宝箱钥匙)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.msg = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.statusMessage( csstatus.SPACE_EVENT_ADD_ITEM, eventParams["extraValue"], self.msg)

class SEAction33( SEActionBase ):
	"""
	系统对目标玩家施放（多个）Buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffIDs = [ int(i) for i in section["param1"].split("|") ]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			for buffID in self.buffIDs:
				trigger.addBuff( trigger, buffID )

class SEAction34( SEActionBase ):
	"""
	系统对副本内所有玩家施放（多个）buff
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.buffIDs = [ int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			for buffID in self.buffIDs:
				e.addBuff( e, buffID )

class SEAction42( SEActionBase ):
	"""
	触发者（必须是玩家）获得某ID的物品
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDList = section["param1"].split("|")
		self.amountList = []
		if section["param2"]:
			self.amountList = [int(i) for i in section["param2"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		for itemID in self.itemIDList:
			amount = 1
			index = self.itemIDList.index( itemID )
			if len( self.amountList ) > index:
				amount = self.amountList[index]
			trigger.addItemByID( int(itemID),amount,csdefine.ITEM_ADD_BY_SPACE_ACTION )

class SEAction43( SEActionBase ):
	"""
	副本内所有玩家身上增加某ID的物品
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDList = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			for itemID in self.itemIDList:
				player.addItemByID( int(itemID),1,csdefine.ITEM_ADD_BY_SPACE_ACTION )

class SEAction44( SEActionBase ):
	"""
	替换 场景效果
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.effectIDs = []
		if section["param1"]:
			self.effectIDs = [ int(i) for i in section["param1"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.replaceSpaceEffects( self.effectIDs )
		
class SEAction45( SEActionBase ):
	"""
	将某个timer的延长时间
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.timerKey = section["param1"]
		self.delayTime = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		self.time = spaceEntity.spaceEventTimers[ self.timerKey ][2] - int(Functions.convertTime(Functions.getTime() - spaceEntity.spaceEventTimers[ self.timerKey ][3])) +self.delayTime
		spaceEntity.getScript().spaceEvent_cancelTimer( spaceEntity, self.timerKey )
		spaceEntity.getScript().spaceEvent_addTimer( spaceEntity, self.timerKey, float(self.time), 0 )

class SEAction46( SEActionBase ):
	"""
	倒计时显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._time = int( section["param1"].strip() )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.ShowCountDown( self._time )
		
class SEAction47( SEActionBase ):
	"""
	开始副本计时
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().startSpaceLife( spaceEntity )
		
class SEAction48( SEActionBase ):
	"""
	副本计时 增加\减少
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._time = int( section["param1"].strip() )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().changeSpaceLife( spaceEntity, self._time )
		
class SEAction49( SEActionBase ):
	"""
	在三角形内随机刷某怪物
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		posA = Functions.vector3TypeConvert( section["param1"] )
		posB = Functions.vector3TypeConvert( section["param2"] )
		posC = Functions.vector3TypeConvert( section["param3"] )
		self._tPointA = Math.Vector3( KBEMath.Unreal2KBEnginePosition( posA ) )
		self._tPointB = Math.Vector3( KBEMath.Unreal2KBEnginePosition( posB ) )
		self._tPointC = Math.Vector3( KBEMath.Unreal2KBEnginePosition( posC ) )
		
		self._num = 1
		self._scriptID = ""
		tempList = section["param4"].split("|")
		self._scriptID = tempList[0]
		if len(tempList) >= 2:
			self._num = tempList[1] and int( tempList[1] ) or 1
		
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for i in range(self._num):
			s = random.random()
			t = random.random()
			a = 1 - math.sqrt(t)
			b = (1-s) * math.sqrt(t)
			c = s * math.sqrt(t)
			pos = self._tPointA * a + self._tPointB * b + self._tPointC * c
			yaw = random.uniform(-math.pi,math.pi)
			param={}
			param["position"] = pos
			param["direction"] = Math.Vector3(0,0,yaw)
			
			spaceEntity.spawnPointCreateEntityByScriptID( self._scriptID , param )

class SEAction50( SEActionBase ):
	"""
	对多边形区域内的玩家放技能
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.skillID = 0
		self.ceilHeight = 0.0
		self.floorHeight = 0.0
		self.polygon = None
	
	def init( self, section ):
		SEActionBase.init( self, section )
		self.skillID = int( section["param1"] )
		
		tempList = section["param2"].split("|")
		self.ceilHeight = float(tempList[0])/100	#配的客户端z值，转成服务器端y值
		self.floorHeight = float(tempList[1])/100	#配的客户端z值，转成服务器端y值
		if self.floorHeight >= self.ceilHeight:
			KBEDebug.ERROR_MSG( "FloorHeight is large than ceilHeight!", section["param2"] )
		
		kbePoints = []
		posList = section["param3"].split("|")
		for posStr in posList:
			clientX = int( posStr.split()[0] )
			clientY = int( posStr.split()[1] )
			kbePoints.append( ( clientY/100, clientX/100 ) )
		self.polygon = Polygon( kbePoints )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			vector2Pos = ( e.position.x, e.position.z )
			if self.polygon.isPointIn( vector2Pos ):
				if self.floorHeight < e.position.y <= self.ceilHeight:
					e.useSkillToEntity( self.skillID, e.id )

class SEAction51( SEActionBase ):
	"""
	在以触发者为圆心的指定距离的位置刷怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.radius = float( section["param1"] )
		self.idAndAmountDict = {}
		for tempStr in section["param2"].split( "|" ):
			id, amount = tempStr.split( ":" )
			self.idAndAmountDict[ id ] = int( amount )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		space = KST.g_objFactory.getSpaceObject( spaceEntity.scriptID )
		navmeshPath = space._navmeshPath
		trigger = KBEngine.entities.get( triggerID )
		poszlist = []
		for scriptID in self.idAndAmountDict:
			i = 0
			pool = 0
			while ( i < self.idAndAmountDict[scriptID] ):
				desPos = csarithmetic.getPositionByLink(trigger.position, self.radius)

				posList = KBEngine.navigatePathPoints( navmeshPath, trigger.position, desPos, self.radius, 0, 0xffff )
				if pool > 5:
					KBEDebug.ERROR_MSG("Has been find navigatePathPoints %s times"%pool)
					return						#当多次找不到位置时，则退出	
				if not posList:
					pool +=1
					continue

				pos = posList.pop()
				flag = 0
				for k in poszlist:			  		#避免出现怪物重叠
					if abs(pos.z - k) < 0.4:	  	#不允许的距离
						flag = 1
						break
				if flag:
					continue
				poszlist.append(pos.z)

				yaw = trigger.position - pos
				dir = Math.Vector3(0,0,math.atan2(yaw.x,yaw.z))
				spaceEntity.createEntityByScriptID(scriptID, pos, dir, {"spawnPos":pos, "spawnDir": dir})
				i += 1

class SEAction52( SEActionBase ):
	"""
	触发显示副本倒计时
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			for e in spaceEntity._spaceRoles:
				spaceEntity.getScript().showSpaceLifeTime(spaceEntity,e)

class SEAction53( SEActionBase ):
	"""
	触发显示物品耐久度
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		itemList = trigger.getItemInstsByID(eventParams["itemID"] )
		if len(itemList) == 1:
			trigger.client.ShowEquipHardiness( str(itemList[0].uid ))

class SEAction54( SEActionBase ):
	"""
	以某个点上的某个高度为圆心在一定范围内创建Entity并移动到底下随机取某一个点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.radius = float(section["param1"]) #半径范围
		self.height = float(section["param2"]) # 高度
		originPos = section["param3"].split("|")
		self.originPos = Math.Vector3( [ float(i) for i in originPos ] )

	def do( self, spaceEntity, triggerID, eventParams ):
		x = random.uniform( self.originPos.x,self.originPos.x + self.radius  )
		y = self.originPos.y+self.height
		z = random.uniform( self.originPos.z,self.originPos.z + self.radius  )
		createPos = Math.Vector3(x,y,z)
		dstPos = Math.Vector3(x,self.originPos.y,z)
		direction = Math.Vector3(0,0,csarithmetic.getYawByVector3(createPos - dstPos))
		spaceEntity.createEntityByScriptID( eventParams["scriptID"],createPos,direction,  {"spawnPos":createPos, "spawnDir": direction} )

class SEAction55( SEActionBase ):
	"""
	以某个位置上的某个高度为圆心在一定范围内创建多个Entity并移动到底下随机取某一个点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.radius = float(section["param1"]) #半径范围
		self.height = float(section["param2"]) # 高度
		originPos = section["param3"].split("|")
		self.originPos = Math.Vector3( [ float(i) for i in originPos ] )
		self.scriptID = section["param4"].split("|")[0]
		self.amount = int(section["param4"].split("|")[1])

	def do( self, spaceEntity, triggerID, eventParams ):
		entityList = []
		time = 0.0
		while self.amount > 0:
			x = random.uniform( self.originPos.x,self.originPos.x + self.radius  )
			y = self.originPos.y+self.height
			z = random.uniform( self.originPos.z,self.originPos.z + self.radius  )
			createPos = Math.Vector3(x,y,z)
			dstPos = Math.Vector3(x,self.originPos.y,z)
			direction = Math.Vector3(0,0,csarithmetic.getYawByVector3(createPos - dstPos))
			spaceEntity.addTimerCallBack(time,"createEntityByScriptID",( self.scriptID,createPos,direction,  {"spawnPos":createPos, "spawnDir": direction} ))
			if time > 1.0:
				time -= 0.1
			elif time >= 0.0:
				time += 0.1
			else:
				time = 0.0
			self.amount -= 1
		
class SEAction56( SEActionBase ):
	"""
	触发者为可移动的Entity,移动到某个与它高度不一致的位置
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.height = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID,None)
		if not entity:
			return
		dstPos = Math.Vector3( entity.position.x,self.height,entity.position.z )
		entity.moveToPosition( dstPos,True,True )
		
class SEAction62( SEActionBase ):
	"""
	副本所有玩家禁止移动
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.actCounterInc( csdefine.ACTION_FORBID_MOVE )
		
class SEAction63( SEActionBase ):
	"""
	副本所有玩家取消禁止移动
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.actCounterDec( csdefine.ACTION_FORBID_MOVE )

class SEAction67( SEActionBase ):
	"""
	将玩家传送回进入副本前的位置
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID,None)
		if not trigger:
			return
		if trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			trigger.gotoExitSpacePos()
		elif trigger.getEntityFlag() == csdefine.ENTITY_FLAG_SPACE:
			for e in spaceEntity._spaceRoles:
				e.gotoExitSpacePos()
		


class SEAction69( SEActionBase ):
	"""
	妖魔化身初始化：随机选出妖魔
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.npcScriptID = section["param1"].split("|")
		self.peopleScriptIDs = section["param2"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		demonModel = {}						# 妖魔化的模型ID
		demonMsg = []						# 妖魔外形提示
		randomModel = []					# 人群的模型ID
		
		def getRandomModel( nest ):
			nest += 1
			temp = {}
			msg = []
			
			for modelName, modelPart in Const.DEMON_PART_MODEL.items():				#先随机出性别（因为 可能会出现男模型随机出裙子）
				part = random.choice( modelPart.keys() )
				temp.update({modelName:part})
				msg.append( modelPart[part] )
				
			for modelName, modelPart in Const.SEX_TO_MODEL[part].items():	#根据性别，随机模型
				part = random.choice( modelPart.keys() )
				temp.update({modelName:part})
				msg.append( modelPart[part] )
			if nest >= 1000:
				return temp, msg
			if not temp in randomModel and temp != demonModel:
				return temp, msg
			else:
				return getRandomModel( nest )
			
		demonModel, demonMsg = getRandomModel(0)
		peoplePoint = []		# 人群
		if spaceEntity.scriptID in g_spawnPointFactory.spawnInfo:
			for point in g_spawnPointFactory.spawnInfo[spaceEntity.scriptID].values():
				pointScriptID = point.getEntityScriptID()
				if pointScriptID in self.npcScriptID:
					npc = point.spawnCreateEntity( spaceEntity )
					npc.setTemp("TalkMsg", demonMsg.pop() )
				if pointScriptID in self.peopleScriptIDs:
					peoplePoint.append( point )
					
		random.shuffle( peoplePoint )
		index = 0
		for modelName, model in demonModel.items():
			spaceEntity.setTemp( "demon_" + modelName, model )
		for point in peoplePoint:
			if index == 0:
				index += 1
				if demonModel["modelNumber"] == "SK_NPCM2000_Mon":
					demonModel["gender"] = csdefine.MALE
				else:
					demonModel["gender"] = csdefine.FEMALE
				point.spawnCreateEntity( spaceEntity, demonModel )
			else:
				model, msg = getRandomModel(0)
				if model["modelNumber"] == "SK_NPCM2000_Mon":
					model["gender"] = csdefine.MALE
				else:
					model["gender"] = csdefine.FEMALE
				point.spawnCreateEntity( spaceEntity, model )

class SEAction76( SEActionBase ):
	"""
	客户端显示分数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.client.ShowFishScore(eventParams["newValue"])

class SEAction77( SEActionBase ):
	"""
	显示通往阵灵路线
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._lengthAndWidth = [int(i) for i in section["param1"].split("|")][:2]			#长和宽
		self.routeListNum = [int(i) for i in section["param1"].split("|")][2]				# 路线长度
		self._scriptIDList = section["param2"].split("|") 								#阵灵ScriptID|发光怪ScriptID|陷阱ScriptID
		posList = section["param3"].split("|")
		firstPos = [float(i) for i in posList[0].split(" ")]						#第一个点的坐标
		firstPos = KBEMath.Unreal2KBEnginePosition(firstPos)
		self._firstPos = Math.Vector3(firstPos[0],firstPos[1],firstPos[2])
		rightPos = [float(i) for i in posList[1].split(" ")]						#右边最后点坐标
		rightPos = KBEMath.Unreal2KBEnginePosition(rightPos)
		self._rightPos = Math.Vector3(rightPos[0],rightPos[1],rightPos[2])
		upPos = [float(i) for i in posList[2].split(" ")]							#上边最后点坐标
		upPos = KBEMath.Unreal2KBEnginePosition(upPos)
		self._upPos = Math.Vector3(upPos[0],upPos[1],upPos[2])
		direction = section["param4"].split("|")[0]									#格子方向的朝向|conditionKey|阵灵动作时间
		direction = [float(i) for i in direction.split(" ")]
		self._direction = KBEMath.Unreal2KBEngineDirection(direction)
		self._conditionKey = section["param4"].split("|")[1]
		self._actionTime = 0.0
		if len(section["param4"].split("|")) > 2:
			self._actionTime = float(section["param4"].split("|")[2])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		allPosList = []
		routeList = []
		for x in range(0,self._lengthAndWidth[0]):
			for y in range(0,self._lengthAndWidth[1]):
				allPosList.append((x,y))
		allPosList.remove((0,0))
		recordPos = []
		removeRecordPos = []
		def getNextPos( srcPos ):
			tempList = []
			tempRouteList = []
			tempRouteList = list(recordPos)
			tempRouteList.remove(srcPos)
			for pos in allPosList:
				if (pos[0] == srcPos[0] or pos[1] == srcPos[1]) and (abs(pos[0] + pos[1] - srcPos[0] - srcPos[1]) == 1): #每次走一格
					tempList.append(pos)
			if len(tempList) > 0:
				needRemovePos = []
				for tempPos in tempList:
					for tempRoutePos in tempRouteList:
						if (tempRoutePos[0] == tempPos[0] and abs(tempRoutePos[1] - tempPos[1]) == 1) or (tempRoutePos[1] == tempPos[1] and abs(tempRoutePos[0] - tempPos[0]) == 1):
							needRemovePos.append(tempPos)
				for removePos in needRemovePos:
					if removePos in tempList:
						tempList.remove(removePos)
				for pos in removeRecordPos:
					if pos in tempList:
						tempList.remove(pos)
				if len(tempList) > 0:
					return random.choice(tempList)
			return None
		recordPos.append((0,0))
		realPos = None
		okPos = False
		loopNum = 2000
		while okPos != True:
			num = 1
			pos = getNextPos( recordPos[len(recordPos) - 1] )
			if pos != None:
				if removeRecordPos.count(pos) > 0:
					if pos not in allPosList:
						allPosList.append(pos)
					return
				allPosList.remove(pos)
				recordPos.append(pos)
			else:
				if len(recordPos) > 1:
					allPosList.append(recordPos[len(recordPos) - 1])
					removeRecordPos.append(recordPos[len(recordPos) - 1])
					recordPos.remove(recordPos[len(recordPos) - 1])
					dealPos = []
					for pos in removeRecordPos:
						if abs(pos[0] + pos[1] - recordPos[len(recordPos) - 1][0] - recordPos[len(recordPos) - 1][1] ) > 1:
							dealPos.append(pos)
					for pos in dealPos:
						removeRecordPos.remove(pos)

			if len(recordPos) == self.routeListNum:
				okPos = True
			num += 1
			if num > loopNum:
				break
		routeList.extend(recordPos)
		rightVector = self._rightPos - self._firstPos	#指向右方的向量
		rightNoamlVector = Math.Vector3(rightVector.x / (self._lengthAndWidth[0] - 1),0,rightVector.z / (self._lengthAndWidth[0] - 1)) #指向右方的单位向量
		upVector = self._upPos - self._firstPos	#指向上方的向量
		upNoamlVector = Math.Vector3(upVector.x / (self._lengthAndWidth[1] - 1),0,upVector.z / (self._lengthAndWidth[1] - 1)) #指向上方的单位向量
		if len(routeList) == self.routeListNum:
			createPos = self._firstPos + rightNoamlVector * routeList[self.routeListNum - 1][0] + upNoamlVector * routeList[self.routeListNum-1][1]
			spaceEntity.addTimerCallBack(13.0,"createEntityByScriptID",(self._scriptIDList[0],createPos,self._direction,{"spawnPos":createPos}))#创建阵灵
			time = 0.0
			for pos in routeList:
				spawnPos = self._firstPos + rightNoamlVector * pos[0] + upNoamlVector * pos[1]
				spaceEntity.addTimerCallBack(time,"createEntityByScriptID",(self._scriptIDList[1],spawnPos,self._direction,{"spawnPos":spawnPos}))#创建光效怪物
				time += 1.0
			for pos in allPosList:
				spawnPos = self._firstPos + rightNoamlVector * pos[0] + upNoamlVector * pos[1]
				tempDict = {}
				tempDict["PointPos"] = (pos[0],pos[1])
				spaceEntity.addTimerCallBack(14.0,"createEntityByScriptID",(self._scriptIDList[2],spawnPos,self._direction,{"spawnPos":spawnPos,"tempMapping":tempDict}))#创建陷阱
			spaceEntity.addTimerCallBackForScript((13.0+self._actionTime),"onConditionChange",("",spaceEntity.id,self._conditionKey,""))
		else:
			KBEDebug.ERROR_MSG("SEAction77 config is error")

class SEAction78( SEActionBase ):
	"""
	触发刷通往阵灵路线
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._conditionKey = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setTemp("GetBall",self._conditionKey)
		spaceEntity.getScript().onConditionChange( spaceEntity, "GETBALL", spaceEntity.id, self._conditionKey, "") #重新刷通往阵灵路线

class SEAction79( SEActionBase ):
	"""
	晶石怪物死亡，按照伤害百分比得到积分(金精)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID,None)
		if not entity:
			return
		countDamage = 0
		for damage in entity.damageList.values():
			countDamage += damage
		integral = entity.queryTemp("MonsterReward")
		for entityID,value in entity.damageList.items():
			e = KBEngine.entities.get(entityID,None)
			if not e:
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				spaceEntity.addPlayerIntegral(e,round(value/countDamage * integral))

class SEAction82(SEActionBase):
	"""
	倒计时加时 “+n（秒）”
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._time = int( section["param1"].strip() )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.ShowExtraTime( self._time )
			
class SEAction83(SEActionBase):
	"""
	环任务记录某个副本统计数量
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.entryIndex = int( section["param1"].strip() ) - 1
		self.questID = section["param2"].strip()
		self.msgInfo = section["param3"].strip()

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		num = spaceEntity.getSpaceStatisticsNum( self.entryIndex )
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( num )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				roleCell.client.ShowLoopRewardTip( self.msgInfo + str(num), exp, money, 0, 0 )
			
class SEAction84(SEActionBase):
	"""
	环任务记录副本剩余时间
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = section["param1"].strip()
		self.msgInfo = section["param2"].strip()

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		import time
		useTime = int( time.time() - spaceEntity.lifeStartTime ) + spaceEntity.dynamicTime
		limtTime = spaceEntity.lifeTime - useTime
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( limtTime )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				min = int( useTime / 60 )
				sec = useTime % 60
				time = ""
				if min:
					time += str( min ) + "分"
				if sec:
					time += str( sec ) + "秒"
				roleCell.client.ShowLoopRewardTip( self.msgInfo + time, exp, money, 0, 0 )
			
class SEAction85( SEActionBase ):
	"""
	在指定几个位置随机刷几个对应Entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._posList = []
		self._scriptIDList = section["param2"].split("|")
		posList = section["param1"].split("|")
		self._refreshAmount = int(section["param3"])
		for pos in posList:
			tempPos = ( float(pos.split(" ")[0]),float(pos.split(" ")[1]),float(pos.split(" ")[2]) )
			tempPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition(tempPos) )
			self._posList.append(tempPos)

	def do( self, spaceEntity, triggerID, eventParams ):
		if len(self._posList) < self._refreshAmount:
			KBEDebug.ERROR_MSG("SEAction85 config is error")
			return
		scriptIDList = random.sample( self._scriptIDList,  self._refreshAmount ) #随机取列表减1的值
		random.shuffle(self._posList) #打乱列表顺序
		for scriptID in scriptIDList:
			index = scriptIDList.index(scriptID)
			spawnPos = Math.Vector3(self._posList[index])
			spaceEntity.createEntityByScriptID( scriptID, spawnPos, Math.Vector3(0,0,0),{"spawnPos":spawnPos} )

class SEAction86( SEActionBase ):
	"""
	琴风古亭：在某范围内随机取值，并使相应的scripID的entity对自己释放技能，并记录释放技能的scriptID顺序
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptIDList = section["param1"].split("|")        	 #scriptID(字怪);scriptID(对应怪物)|scriptID(字怪);scriptID(对应怪物)
		self._range = [int(i) for i in section["param2"].split("|")] #范围[min，max]
		self._skillID = int(section["param3"]) 	#技能ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		length = random.sample(range(self._range[0],self._range[1]),1)
		random.shuffle( self._scriptIDList )
		if length[0] > len(self._scriptIDList):
			KBEDebug.ERROR_MSG("SEAction86 config is error")
			return
		recordScriptIDList = []
		for i in range(0,length[0]):
			idList = spaceEntity.getEntityRecord( self._scriptIDList[i].split(";")[0] )
			recordScriptIDList.append(self._scriptIDList[i].split(";")[1])
			for id in idList:
				entity = KBEngine.entities.get( id,None )
				if entity:
					entity.addTimerCallBack(i,"useSkillToEntity",(self._skillID,entity.id))
		
		spaceEntity.setTemp("recordScriptIDList",recordScriptIDList)

class SEAction87( SEActionBase ):
	"""
	琴风古亭：触发者(怪物) 按照记录sctipID顺序，击杀对应怪物，如果击杀顺序不对，给副本发送击杀失败，否则给副本发送击杀成功
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._successKey = section["param1"]	#成功key
		self._failureKey = section["param2"]    #失败Key

	def do( self, spaceEntity, triggerID, eventParams ):
		recordScriptIDList = spaceEntity.queryTemp("recordScriptIDList")
		if not spaceEntity or recordScriptIDList == None:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		if dieEntity == None:
			return
		if len(recordScriptIDList) > 0 and dieEntity.scriptID not in recordScriptIDList:
			spaceEntity.removeTemp("recordScriptIDList")
			spaceEntity.getScript().onConditionChange(spaceEntity,"",spaceEntity.id,self._failureKey,"")
		else:
			recordScriptIDList.remove(dieEntity.scriptID)
			if len(recordScriptIDList) == 0:
				spaceEntity.removeTemp("recordScriptIDList")
				spaceEntity.getScript().onConditionChange(spaceEntity,"",spaceEntity.id,self._successKey,"")
			else:
				spaceEntity.setTemp("recordScriptIDList",recordScriptIDList)

class SEAction88( SEActionBase ):
	"""
	灵岛危机刷滚石
	一批滚石，滚石随机取刷新位置；每个位置对应几条巡逻路线，滚石随机取其中一条路线；每个滚石选择不同的路线
	要求：巡逻路线数量必须大于等于一批滚石的数量
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.idAndAmount = {}	#滚石ID和数量：{id:amount}
		self.posList = []		#位置列表：[pos1, pos2]
		self.patrolLists = []	#巡逻路线列表：[1,2,3....]
	
	def init( self, section ):
		SEActionBase.init( self, section )
		
		tempList = section["param1"].split("|")		#格式 "scriptID1:amount1| scriptID2:amount2 |..."
		for tempStr in tempList:
			tempList1 = tempStr.split(":")
			self.idAndAmount[ tempList1[0] ] = int( tempList1[1] )
		
		tempList = section["param2"].split("|")		#格式 "x1 y1 z1 | x2 y2 z2 |..."
		for tempStr in tempList:
			pos = Functions.vector3TypeConvert( tempStr )
			self.posList.append( KBEMath.Unreal2KBEnginePosition( pos ) )
		
		self.patrolLists = [int(i) for i in section["param3"].split("|")] #格式 "1| 2 | 3..."
	
	def do( self, spaceEntity, triggerID, eventParams ):
		tempPatrolLists = list( self.patrolLists )
		tempPosList = list( self.posList )
		for id, amount in self.idAndAmount.items():
			for i in range(amount):
				posIndexList = range( len(tempPosList) )
				posIndex = random.choice( posIndexList )
				
				__pos = tempPosList[ posIndex ]
				tempPosList.pop(posIndex)
				__patrolList = tempPatrolLists.pop(posIndex)
				entity = spaceEntity.createEntityByScriptID( id, __pos, Math.Vector3(0,0,0), { "spawnPos": __pos, "patrolList":__patrolList } )

class SEAction89( SEActionBase ):
	"""
	强制设置当前阶段目标完成
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.stageIndex = int( section["param1"] )	# 阶段索引值
		if section["param2"]:
			self.taskIndex = int( section["param2"] )	# 阶段目标索引值

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if spaceEntity.spaceStage.stageIndex != self.stageIndex:
			KBEDebug.ERROR_MSG( "Space(stageIndex = %i) is not in stageIndex(%i)"%(spaceEntity.spaceStage.stageIndex,self.stageIndex) )
			return
		spaceEntity.getScript().spaceStage_forceCompleteStageTask( spaceEntity, self.taskIndex )

class SEAction90( SEActionBase ):
	"""
	CST-2149 化元盾吸收灵箭
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.effectIDList = section["param1"].split("|") #光效ID1;光效ID2(灵箭)|光效ID3;光效ID4(焚箭)|光效ID5;光效ID6(陨石)... 其中光效ID1和光效ID2为同类型光效
		self.keyList = section["param2"].split("|")	#接收灵箭计数的Key|化元盾耐久度Key|碰到地面火灵scriptID
		self.countAddList = [int(i) for i in section["param3"].split("|")] #吸收灵箭增加数量|吸收焚箭增加数量|吸收陨石增加数量
		radioDataList = section["param4"].split("|") #吸收焚箭减少耐久度值;造成伤害|吸收陨石减少耐久度值;造成伤害
		self.reduceShieldRadioList = []
		self.damageRadioList = []
		for radioData in radioDataList:
			radioList = radioData.split(";")
			self.reduceShieldRadioList.append(float(radioList[0]))
			if len(radioList) > 1:
				self.damageRadioList.append(float(radioList[1]))
			else:
				self.damageRadioList.append(0)

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		swordType = eventParams["extraValue"].split("|")[0]			#灵箭类型
		collisionType = int(eventParams["extraValue"].split("|")[1])  #碰撞类型
		position = (float(eventParams["extraValue"].split("|")[2]),float(eventParams["extraValue"].split("|")[3]),float(eventParams["extraValue"].split("|")[4]))
		position = KBEMath.Unreal2KBEnginePosition(position)
		reduceShieldRadio = 0.0
		addCount = 0
		if swordType in self.effectIDList[0].split(";") and collisionType == csdefine.COLLISION_TYPE_SHIELD:
			addCount = self.countAddList[0]
		elif swordType in self.effectIDList[1].split(";"):
			if collisionType == csdefine.COLLISION_TYPE_SHIELD:
				addCount = self.countAddList[1]
				reduceShieldRadio = self.reduceShieldRadioList[0]
			elif collisionType == csdefine.COLLISION_TYPE_PLAYER:
				for player in spaceEntity._spaceRoles:
					player.setHP(player.HP - math.ceil(player.HP_Max * self.damageRadioList[0]))
		elif swordType in self.effectIDList[2].split(";"):
			if collisionType == csdefine.COLLISION_TYPE_SHIELD:
				addCount = self.countAddList[2]
				reduceShieldRadio = self.reduceShieldRadioList[1]
			elif collisionType == csdefine.COLLISION_TYPE_UNDERGROUND:
				spaceEntity.createEntityByScriptID( self.keyList[2], Math.Vector3(position),Math.Vector3(0,0,0), { "spawnPos": Math.Vector3(position)})
			elif collisionType == csdefine.COLLISION_TYPE_PLAYER:
				for player in spaceEntity._spaceRoles:
					player.setHP(player.HP - math.ceil(player.HP_Max * self.damageRadioList[1]))
		if self.keyList[0] in spaceEntity.spaceEventCountInt:
			count = spaceEntity.spaceEventCountInt[self.keyList[0]] + addCount
			if count >= 0:
				spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.keyList[0] ,addCount )
			else:
				spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.keyList[0] , -spaceEntity.spaceEventCountInt[self.keyList[0]] )
		if self.keyList[0] not in spaceEntity.spaceEventCountInt:
			if addCount >= 0:
				spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.keyList[0] ,addCount )
			else:
				spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.keyList[0] ,0 )

		reduceShield = spaceEntity.spaceEventCountInt[self.keyList[1]] - int(reduceShieldRadio * spaceEntity.queryTemp("ShieldMaxValue"))
		if reduceShield >= 0:
			spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.keyList[1], -int(reduceShieldRadio * spaceEntity.queryTemp("ShieldMaxValue")) )
		else:
			spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.keyList[1], -spaceEntity.spaceEventCountInt[self.keyList[1]] )

class SEAction91( SEActionBase ):
	"""
	CST-2149 化元盾耐久度值显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.OnShieldChanged( eventParams["newValue"], spaceEntity.queryTemp("ShieldMaxValue") )

class SEAction92( SEActionBase ):
	"""
	CST-2149 隐藏化元盾
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.OnRemoveShield()

class SEAction93( SEActionBase ):
	"""
	副本计数改变给副本统计发送通知 (通知ID为计数key值)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().spaceStatistics_onConditionChange( spaceEntity,"",spaceEntity.id,eventParams["countKey"], str(eventParams["addValue"]) )

class SEAction94( SEActionBase ):
	"""
	副本计数改变给副本阶段发送通知 (通知ID为计数key值)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().spaceStage_onConditionChange( spaceEntity,"",spaceEntity.id,eventParams["countKey"], str(eventParams["addValue"]) )

class SEAction95( SEActionBase ):
	"""
	CST-3236 九天灵狱 随机激活某些scriptID，激活的scriptID替换对应的ModelNumber，并给副本发送激活完毕的通知
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")	# scriptID|scriptID....
		self.modelNumberList = section["param2"].split("|")
		self.conditionKey = section["param3"] #激活完毕后通知ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if len(spaceEntity._spaceRoles) < 1:
			return
		tempScriptIDList = list(self.scriptIDList)
		random.shuffle(tempScriptIDList) #打乱顺序
		recordScriptIDList = []
		time = 0.0
		for i in range(0,len(tempScriptIDList)):
			idList = spaceEntity.getEntityRecord(tempScriptIDList[i])
			recordScriptIDList.append(tempScriptIDList[i])
			time += 1.0
			for id in idList:
				entity = KBEngine.entities.get( id,None )
				if entity:
					index = self.scriptIDList.index(tempScriptIDList[i])
					entity.addTimerCallBack(time,"setExtraModelNumber",(self.modelNumberList[index],))
		spaceEntity.setTemp( "recordScriptIDList",recordScriptIDList )
		spaceEntity.getScript().onConditionChange(spaceEntity,"",spaceEntity.id,self.conditionKey,"")

class SEAction96( SEActionBase ):
	"""
	CST-2149 触发者是玩家:隐藏化元盾
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get(triggerID,None)
		if player == None:
			return
		player.client.OnRemoveShield()

class SEAction97( SEActionBase ):
	"""
	环任务总时间倒计时显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.loopQuestTime = int(section["param1"])
		self.showTime = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().spaceEvent_addTimer( spaceEntity, "LoopQuestLife", self.loopQuestTime, 0 )
		spaceEntity.addTimerCallBackForScript( float(self.loopQuestTime - self.showTime),"showTimeCountDown",(csstatus.SPACE_LOOPQUEST_TASK_END,self.showTime) )
		spaceEntity.lifeTime = self.loopQuestTime	# 副本时长
		spaceEntity.lifeStartTime = time.time()		# 副本计时开始时间
		for e in spaceEntity._spaceRoles:
			e.client.ShowSpaceLife( str(self.loopQuestTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), 0,str( Functions.getTime() ) )

class SEAction98( SEActionBase ):
	"""
	任务倒计时提示 {任务{0}秒后结束}
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.holdTime = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.statusMessage( csstatus.SPACE_LOOPQUEST_TASK_END, self.holdTime)

class SEAction99( SEActionBase ):
	"""
	添加Space临时值记录
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.tempKey = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		value = spaceEntity.queryTemp( "cehua_" + self.tempKey, 0 )					# 防止程序与策划设置的temp 相冲突
		spaceEntity.setTemp( "cehua_" + self.tempKey, value + 1 )
		
class SEAction100( SEActionBase ):
	"""
	刷新点中，随机刷怪（且游戏中有此怪不在刷）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptIDList = section["param1"].split("|")
		self._maxNum = int(section["param2"] )						# 最大随机数
		
	def do( self, spaceEntity, triggerID, eventParams ):
		for scriptID in self._scriptIDList:
			if spaceEntity.getEntityRecord( scriptID ):return		# 如果有 刷出，则不再刷
		
		num = min( len( self._scriptIDList ), max( self._maxNum, 1) )
		randNum = random.randint( 1, num )
		spawnList = random.sample( self._scriptIDList, num )
		
		for scriptID in spawnList:
			spaceEntity.spawnPointCreateEntityByScriptID(scriptID )

class SEAction101( SEActionBase ):
	"""
	强制设置当前阶段目标完成数量清0
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.stageIndex = int( section["param1"] )	# 阶段索引值
		self.taskIndex = int( section["param2"] )	# 阶段目标索引值

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if spaceEntity.spaceStage.stageIndex != self.stageIndex:
			KBEDebug.ERROR_MSG( "Space(stageIndex = %i) is not in stageIndex(%i)"%(spaceEntity.spaceStage.stageIndex,self.stageIndex) )
			return
		spaceEntity.getScript().spaceStage_forceSetCurrentStageTaskClear( spaceEntity, self.taskIndex )


class SEAction102( SEActionBase ):
	"""
	随机传送玩家到某个指定的坐标
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		posList =  section["param1"].split("|")
		self.posList = []
		for pos in posList:
			pos = Functions.vector3TypeConvert( pos )
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			self.posList.append(pos)
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		index = random.randint( 0, len(self.posList)-1 )
		for player in spaceEntity._spaceRoles:
			player.parent = None
			player.allClients.TeleportToDstPosition(KBEMath.KBEngine2UnrealPosition(self.posList[index]))
			player.position = self.posList[index]

class SEAction103( SEActionBase ):
	"""
	CST-3740 设置玩家能量条(触发者为玩家)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.maxEnergyValue = int(section["param1"]) #最大能量值

	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get(triggerID,None)
		if not player:
			return
			
		#CST-4225 玩家进入副本后，能量充满
		#player.setTemp("MaxEnergyValue",self.maxEnergyValue)
		#player.setTemp("CurEnergyValue",self.maxEnergyValue)
		player.updateEnergyBar( self.maxEnergyValue, self.maxEnergyValue )

class SEAction104( SEActionBase ):
	"""
	随机取条巡逻路线，在路线的随机点刷Entitiy
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.patrolLists = [int(i) for i in section["param1"].split("|")] #格式 "1| 2 | 3..."
		self.scriptID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		route = random.sample( self.patrolLists, 1 )[0]
		routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( spaceEntity.scriptID, route )
		patrolRoutePointNumber = len(routeInfo)
		routePointList = range(1,patrolRoutePointNumber + 1)
		index = random.choice(routePointList)
		spawnPos = routeInfo.get(index)["position"]
		entity = spaceEntity.createEntityByScriptID(self.scriptID,Math.Vector3(spawnPos),Math.Vector3(0,0,0), { "spawnPos": Math.Vector3(spawnPos), "patrolList":route })

class SEAction108( SEActionBase ):
	"""
	荷花法阵 显示Boss的圆形血条界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isOpen = bool(int(section["param1"]))	#开关: 0关闭 1打开
		self.scriptID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		if not self.isOpen:
			for e in spaceEntity._spaceRoles:
				e.client.ShowCircleHPPercentBar( 0, 0 )	

		entityIDList = spaceEntity.getEntityRecord(self.scriptID)
		if not len(entityIDList):
			return
		entityID = entityIDList[0]
		entity = KBEngine.entities.get(entityID,None)

		if not entity:
			return
		percent = int(math.floor(entity.HP/entity.HP_Max*100))
		for e in spaceEntity._spaceRoles:
			e.client.ShowCircleHPPercentBar( self.isOpen, percent )

class SEAction109( SEActionBase ):
	"""
	初始化荷花
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.initBoard()

class SEAction110( SEActionBase ):
	"""
	重刷荷花
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.refreshHeHua()

class SEAction111( SEActionBase ):
	"""
	在多个空画卷中随机出五个法阵，并将结果发给对应的画卷（CST-3790）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.matrixList = section["param1"].split("|")	#法阵标志列表
		self.pictureScrollList =section["param2"].split("|")	#画卷ScriptID列表

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		pictureScrollList = random.sample(self.pictureScrollList, 5)
		matrixList = list(self.matrixList)
		random.shuffle(matrixList)	#打乱顺序
		for scriptID in pictureScrollList:
			idList = list(spaceEntity.getEntityRecord(scriptID))
			if not idList or len(idList) > 1: #不同的画卷scriptID不同
				KBEDebug.ERROR_MSG("SEAction111 config is error, scriptID[%s] is None or more one" % scriptID)
				return
			entity = KBEngine.entities.get(idList[0], None)
			entity.monsterAIOnCommand(spaceEntity.id, spaceEntity.scriptID, matrixList.pop(0))
	
class SEAction112( SEActionBase ):
	"""
	在多个空画卷随机选出一个，并将指定消息发送给它（CST-3790）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.pictureScrollList = section["param1"].split("|")	#画卷ScriptID列表
		self.cmd =section["param2"]	#通知ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		pictureScrollList = list(self.pictureScrollList)
		for scriptID in self.pictureScrollList:
			idList = list(spaceEntity.getEntityRecord(scriptID))
			if not idList or len(idList) > 1: #不同的画卷scriptID不同
				KBEDebug.ERROR_MSG("SEAction112 config is error, scriptID[%s] is None or more one" % scriptID)
				return
			entity = KBEngine.entities.get(idList[0], None)
			if entity.queryTemp("attributeType", None):
				if scriptID in pictureScrollList:
					pictureScrollList.remove(scriptID)
					
		if len(pictureScrollList) <= 0:
			return
			
		scriptID = pictureScrollList[random.randint(0, len(pictureScrollList) - 1)]
		idList = list(spaceEntity.getEntityRecord(scriptID))
		if not idList or len(idList) > 1: #不同的画卷scriptID不同
			KBEDebug.ERROR_MSG("SEAction112 config is error, scriptID[%s] is None or more one" % scriptID)
			return
		entity = KBEngine.entities.get(idList[0], None)
		if entity and not entity.queryTemp("attributeType", None):
			entity.monsterAIOnCommand(spaceEntity.id, spaceEntity.scriptID, self.cmd)

class SEAction113(SEActionBase):
	"""
	逐风之路特殊的奖励方式
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = section["param1"].strip()
		self.msgInfo = section["param2"].strip()
		self.entryIndex = section["param3"].split("|")
		self.rewardID = section["param4"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		import time
		useTime = int( time.time() - spaceEntity.lifeStartTime ) + spaceEntity.dynamicTime
		limtTime = spaceEntity.lifeTime - useTime
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( limtTime )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				min = int( useTime / 60 )
				sec = useTime % 60
				time = ""
				if min:
					time += str( min ) + "分"
				if sec:
					time += str( sec ) + "秒"

				moneyAmount = 0
				expAmount = 0
				entity = KBEngine.entities.get(triggerID, None)
				moneyDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID[0], {"player":entity} )
				for moneyData in moneyDatas:
					moneyData["amount"] = moneyData["amount"] * spaceEntity.getSpaceStatisticsNum( int(self.entryIndex[0]) -1 )
					RewardMgr.g_rewardMgr.doReward( moneyData, entity.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_ZFZL )
					moneyAmount = int(moneyData["amount"])

				expDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID[1], {"player":entity} )
				for expData in expDatas:
					expData["amount"] = expData["amount"] * spaceEntity.getSpaceStatisticsNum( int(self.entryIndex[1]) -1 )
					RewardMgr.g_rewardMgr.doReward( expData, entity.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_ZFZL )
					expAmount = int(expData["amount"])
				
				roleCell.client.ShowLoopRewardTip( self.msgInfo + time, exp, money, moneyAmount, expAmount )	

class SEAction115( SEActionBase ):
	"""
	灵魂狩猎 更新积分统计
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isOpen = int(section["param1"])     #0：关闭界面 1：打开 更新界面

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		spaceEntity.getScript().LHSL_SetScoreUI(spaceEntity, trigger, self.isOpen)


class SEAction116(SEActionBase):
	"""
	幻莲天池里的莲叶开始移动 -- CST-3803
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.scriptIDList= []
		self._delayTime = 0.0
		self._order = False

	def init( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self.scriptIDList = section["param1"].split("|")
		
		if section["param2"]:
			self._delayTime = float(section["param2"])
		
		if section["param3"]:
			self._order = bool(int(section["param3"]))

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get( triggerID )
		def startMove(entitylist):
			oederList = []
			oederList = sorted( entitylist, key = lambda x:trigger.position.distTo( x.position ), reverse = self._order )
			delayTime = 0.0
			for _entity in oederList:
				_entity.addTimerCallBack(delayTime, "lotusMoveStart",())
				delayTime += self._delayTime

		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord( scriptID )
			entitylist = []
			for id in idList:
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entitylist.append(entity)
			startMove(entitylist)
		
class SEAction118( SEActionBase ):
	"""
	在多个位置随机刷出多个entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = []
		self.positionList = []
		self.directionList = []	#位置和朝向的顺序要一致
		for scriptIDInfo in section["param1"].split("|"):
			scriptID, amount = scriptIDInfo.split(":")
			self.scriptIDList.extend([scriptID] * int(amount))
		for position in section["param2"].split("|"):
			pos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(position))
			self.positionList.append(pos)
		for direction in section["param3"].split("|"):
			dir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(direction))
			self.directionList.append(dir)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if len(self.scriptIDList) != len(self.positionList) or len(self.scriptIDList) != len(self.directionList):
			KBEDebug.ERROR_MSG("SEAction118 config error")
			return
		scriptIDList = list(self.scriptIDList)
		random.shuffle(scriptIDList)
		for i in range(len(scriptIDList)):
			scriptID = scriptIDList[i]
			position = self.positionList[i]
			direction = self.directionList[i]
			spaceEntity.createEntityByScriptID(scriptID, Math.Vector3(position),Math.Vector3(direction), { "spawnPos": Math.Vector3(position), "spawnDir":  Math.Vector3(direction)})

class SEAction119( SEActionBase ):
	"""
	触发者必须是玩家 增加副本额外物品栏
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.maxNum = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get( triggerID, None )
		if player and player.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			player.setUnLockSpaceCopyGridNum( self.maxNum )
			spaceCopyItemList = player.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY)
			uidList = []
			for itemInst in spaceCopyItemList:
				uidList.append(str(itemInst.uid))
			player.client.CreateExtraItemBar( self.maxNum, uidList )

class SEAction120( SEActionBase ):
	"""
	触发者必须是玩家 清除副本额外物品栏
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get( triggerID, None )
		if player and player.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			player.setUnLockSpaceCopyGridNum( 0 )
			player.client.RemoveExtralItemBar()

class SEAction121( SEActionBase ):
	"""
	通知客户端开始炼丹  CST-4019
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return		
		for player in spaceEntity._spaceRoles:
			_remainTime = spaceEntity.lifeTime - int( time.time() - spaceEntity.lifeStartTime )
			player.client.AlchemyStart( _remainTime, spaceEntity.lifeTime )

class SEAction122( SEActionBase ):
	"""
	触发者必须是玩家 将副本的剩余时间发给客户端  CST-4019
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get( triggerID, None )
		if player and player.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			_remainTime = spaceEntity.lifeTime - int( time.time() - spaceEntity.lifeStartTime )
			player.client.CopyRemainTime( _remainTime )

class SEAction123( SEActionBase ):
	"""
	在环形区域刷出非移动陷阱  CST-4019
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.inradius = 0.0
		self.exradius = 0.0

	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]
		posO = Functions.vector3TypeConvert( section["param2"] )
		self._posO = KBEMath.Unreal2KBEnginePosition( posO )
		self.exradius = float(section["param3"])	
		if section["param4"]:
			self.inradius = float(section["param4"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		radian = random.uniform( self.inradius, self.exradius )
		theta = random.randint(0,360)
		srcPos= Math.Vector3( self._posO + Math.Vector3( math.sin(math.pi/180*theta)*radian, 0, math.cos(math.pi/180*theta)*radian ))
		dir = Math.Vector3(0,0,0)
		_entity = spaceEntity.createEntityByScriptID( self._scriptID , srcPos, dir,{"spawnPos":srcPos, "spawnDir": dir } )
		if not _entity:
			KBEDebug.DEBUG_MSG("----SEAction123----scriptID = %s is error "%self._scriptID)

class SEAction124( SEActionBase ):
	"""
	开启阻挡墙
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.number = section["param1"]		#阻挡墙编号

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.OpenAreaWall( self.number )

class SEAction125( SEActionBase ):
	"""
	关闭阻挡墙
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.number = section["param1"]		#阻挡墙编号

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.CloseAreaWall( self.number )

class SEAction126( SEActionBase ):
	"""
	随机取条巡逻路线(排除自己的巡逻路线)，在路线的随机点刷触发者 触发者为怪物
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.patrolLists = [int(i) for i in section["param1"].split("|")] #格式 "1| 2 | 3..."

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID,None)
		if not (spaceEntity and entity):
			return
		tempList = list( self.patrolLists )
		if entity.patrolList in tempList:
			tempList.remove(entity.patrolList)
		if len(tempList) < 1:
			KBEDebug.ERROR_MSG("SEAction126 config is error")
			return
		route = random.sample( tempList, 1 )[0]
		routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( spaceEntity.scriptID, route )
		patrolRoutePointNumber = len(routeInfo)
		routePointList = range(1,patrolRoutePointNumber + 1)
		index = random.choice(routePointList)
		spawnPos = routeInfo.get(index)["position"]
		entity = spaceEntity.createEntityByScriptID(entity.scriptID,Math.Vector3(spawnPos),Math.Vector3(0,0,0), { "spawnPos": Math.Vector3(spawnPos), "patrolList":route })


class SEAction127( SEActionBase ):
	"""
	给副本内所有玩家发送消息 查看客户端MessageConfig表
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.statusID = int(section["param1"]) #消息ID表
		self.param = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			role.statusMessage(self.statusID, self.param)

class SEAction128( SEActionBase ):
	"""
	CST-3781 触发者开始按键组合镜头QTE
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self._qteTypes = ""

	def init( self, section ):
		SEActionBase.init( self, section )
		self._qteTypes = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entity = KBEngine.entities.get(triggerID,None)
		if entity:
			entity.client.OnStartStoryQTE(self._qteTypes)

class SEAction129( SEActionBase ):
	"""
	荷花法阵 同色荷花消除后 刷怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = []
		if not len(section["param1"]):
			return
		datas= section["param1"].split("|")     #eg:"20000001:2|20000002:3"
		for data in datas:
			_data = data.split(":")
			scriptID = _data[0]
			num = int(_data[1])
			self.scriptIDList+=[scriptID]*num

	def do( self, spaceEntity, triggerID, eventParams ):

		if not len(self.scriptIDList):
			return

		if not spaceEntity:
			return
		spaceEntity.createMonsterByPosition(list(self.scriptIDList))

class SEAction130( SEActionBase ):
	"""
	使某些scriptID死亡
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for scriptID in self.scriptIDs:
			idList = list( spaceEntity.getEntityRecord( scriptID ) )
			for id in idList:
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entity.changeState(csdefine.ENTITY_STATE_DEAD)

class SEAction131( SEActionBase ):
	"""
	将某范围的随机整数发副本里的所有玩家  CST-4019
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._randomMin =  int(section["param1"])
		self._randomMax =  int(section["param2"])
		self._amount = int(section["param3"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		_randList = []
		randomList = spaceEntity.queryTemp("randomList",[])
		while len(_randList) < self._amount:
			_rand = random.randint(self._randomMin,self._randomMax)
			if _rand in randomList or _rand in _randList:
				continue
			_randList.append(_rand)
		spaceEntity.setTemp( "randomList", _randList )

		for player in spaceEntity._spaceRoles:		
			player.client.SendRandomList( _randList )

class SEAction132( SEActionBase ):
	"""
	开启副本策略点 (只有副本有策略点)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.indexList = [int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for index in self.indexList:
			spaceEntity.getScript().startStrategy( spaceEntity, index )

class SEAction133( SEActionBase ):
	"""
	结束副本策略点(只有副本有策略点)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.indexList = [int(i) for i in section["param1"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for index in self.indexList:
			spaceEntity.getScript().endStrategy( spaceEntity, index )


class SEAction134( SEActionBase ):
	"""
	CST-4141 触发者玩家触发显示 “夜袭凤栖镇”
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get( triggerID, None )
		if not player:
			return
		player.client.ShowEnterFengQiMsg()

class SEAction135( SEActionBase ):
	"""
	随机取刷新点 刷entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.spawnList = section["param1"].split("|")	#刷新点的Index "1;2;3|4;5;6"
		self.amountList = section["param2"].split("|")  #刷新数量 2|3

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if len(self.spawnList) != len(self.amountList):
			KBEDebug.ERROR_MSG("SEAction135 config is error")
			return
		for i in range(0,len(self.amountList)):
			indexListStr = self.spawnList[i]
			if int(self.amountList[i]) > len(indexListStr):
				KBEDebug.ERROR_MSG("SEAction135 config amountIndex(%i) is more than indexList(%i)"%(self.amountList[i],len(indexListStr)))
				return
			indexList = [int(i) for i in indexListStr.split(";")]
			random.shuffle(indexList)
			for i in range(0,int(self.amountList[i])):
				spaceEntity.onRequestSpawnEntity( indexList[i] )
				
class SEAction136( SEActionBase ):
	"""
	(QRN)
	CST-4225 程序功能需求（20级）——帮会日常【收集法宝碎片】功能改进
	清理玩家身上与副本相关数据
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		for roleCell in spaceEntity._spaceRoles:
			roleCell.clearWithExpendEnergyData()
		
class SEAction137 ( SEActionBase ):
	"""
	(QRN)
	CST-4225 程序功能需求（20级）——帮会日常【收集法宝碎片】功能改进
	给玩家设置部分跟副本相关的数据
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._expendEnergy = int(section["param1"])
		self._addSpeedBuffID = int(section["param2"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get( triggerID, None )
		if not player or player.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		
		player.setExpendEnergyData(self._expendEnergy, self._addSpeedBuffID)

class SEAction138 ( SEActionBase ):
	"""
	发送副本时间和副本名字到客户端
	"""
	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.client.SendGameCopyTime( spaceEntity.lifeTime, spaceEntity.scriptID )

class SEAction139( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	玩家被击杀 瓜分玩家积分，并增加击杀者(玩家)击杀数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.killerRatio = float(section["param1"]) # 击杀者获得积分的概率
		self.boxScriptID = section["param2"] #箱子的scriptID
		self.boxRatio = float( section["param3"] ) #箱子获得积分的概率
		self.reduceIntegral = int(section["param4"]) #玩家死亡最少的减少积分

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		dieEntityIntegral = spaceEntity.memberDatas.getIntegral(triggerID)
		if dieEntityIntegral == None:
			KBEDebug.ERROR_MSG("SpaceCopyYeZhanFengQi has no this player(ID = %i) integral"%triggerID)
			return
		boxEntity = spaceEntity.createEntityByScriptID( self.boxScriptID, dieEntity.position,dieEntity.direction,{} )
		if boxEntity:
			integral = math.ceil(self.boxRatio * dieEntityIntegral)
			boxEntity.setTemp("RewardIntegral",integral)
		integral = math.ceil(self.killerRatio * dieEntityIntegral)
		boxIntegral = math.ceil(self.boxRatio * dieEntityIntegral)
		totalIntegral = boxIntegral + integral
		if totalIntegral < self.reduceIntegral:
			totalIntegral = self.reduceIntegral
		if totalIntegral > dieEntityIntegral:
			totalIntegral = dieEntityIntegral
		spaceEntity.reducePlayerIntegral( dieEntity, totalIntegral )
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE or killEntity.id == dieEntity.id:
			return
		spaceEntity.addPlayerIntegral( killEntity,integral )
		spaceEntity.memberDatas.kill( triggerID, eventParams["killerID"] ) #增加玩家的击杀数

class SEAction140( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	怪物被玩家，获得积分
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.integral = int(section["param1"]) #积分值

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get(eventParams["killerID"],None)
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			KBEDebug.ERROR_MSG("SEAction139 killEntity is not player ")
			return
		spaceEntity.addPlayerIntegral( killEntity, self.integral )

class SEAction141( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	设置安全区域起点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		upLeftOriginPos = Functions.vector3TypeConvert( section["param1"] )
		upRightOriginPos = Functions.vector3TypeConvert( section["param2"] )
		downLeftOriginPos = Functions.vector3TypeConvert( section["param3"] )
		downRightOriginPos = Functions.vector3TypeConvert( section["param4"] )
		self.upLeftOriginPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( upLeftOriginPos ) )
		self.upRightOriginPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( upRightOriginPos ) )
		self.downLeftOriginPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( downLeftOriginPos ) )
		self.downRightOriginPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( downRightOriginPos ) )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setUpLeftOriginPos( self.upLeftOriginPos )
		spaceEntity.setUpRightOriginPos( self.upRightOriginPos )
		spaceEntity.setDownLeftOriginPos( self.downLeftOriginPos )
		spaceEntity.setDownRightOriginPos( self.downRightOriginPos )

class SEAction142( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	设置缩小安全区域终点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		upLeftEndPos = Functions.vector3TypeConvert( section["param1"] )
		upRightEndPos = Functions.vector3TypeConvert( section["param2"] )
		downLeftEndPos = Functions.vector3TypeConvert( section["param3"] )
		downRightEndPos = Functions.vector3TypeConvert( section["param4"] )
		self.upLeftEndPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( upLeftEndPos ) )
		self.upRightEndPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( upRightEndPos ) )
		self.downLeftEndPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( downLeftEndPos ) )
		self.downRightEndPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( downRightEndPos ) )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setUpLeftEndPos( self.upLeftEndPos )
		spaceEntity.setUpRightEndPos( self.upRightEndPos )
		spaceEntity.setDownLeftEndPos( self.downLeftEndPos )
		spaceEntity.setDownRightEndPos( self.downRightEndPos )

class SEAction143( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	触发者为玩家：显示安全区域起点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		player = KBEngine.entities.get(triggerID,None)
		if not player:
			return
		if player.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			KBEDebug.ERROR_MSG("SEAction143 trigger is not player (ID = %i)"%triggerID)
			return
		upleftOriginPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getUpLeftOriginPos()))
		upRightOriginPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getUpRightOriginPos()))
		downLeftOriginPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getDownLeftOriginPos()))
		downRightOriginPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getDownRightOriginPos()))
		player.client.CLIENT_ShowOriginArea( upleftOriginPos,upRightOriginPos,downLeftOriginPos,downRightOriginPos  )


class SEAction144( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	触发者为玩家：显示缩小安全区域终点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		player = KBEngine.entities.get(triggerID,None)
		if not player:
			return
		if player.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			KBEDebug.ERROR_MSG("SEAction142 trigger is not player (ID = %i)"%triggerID)
			return

		upLeftEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getUpLeftEndPos()))
		upRightEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getUpRightEndPos()))
		downLeftEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getDownLeftEndPos()))
		downRightEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getDownRightEndPos()))

		player.client.CLIENT_ShowEndArea( upLeftEndPos,upRightEndPos, downLeftEndPos,downRightEndPos )

class SEAction145( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	副本内所有玩家显示缩小安全区域终点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		upLeftEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getUpLeftEndPos()))
		upRightEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getUpRightEndPos()))
		downLeftEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getDownLeftEndPos()))
		downRightEndPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getDownRightEndPos()))
		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_ShowEndArea( upLeftEndPos,upRightEndPos, downLeftEndPos,downRightEndPos )

class SEAction146( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	开始缩小安全区域
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.totalUseTime = float( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.CLIENT_StartReduceArea( self.totalUseTime )
		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_StartReduceArea( self.totalUseTime )

class SEAction147( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	检查玩家是否在安全区域里
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffID = int( section["param1"] ) # 毒物Buff

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.checkPlayerIsInSaveArea( self.buffID )

class SEAction148( SEActionBase ):
	"""
	主线任务倒计时显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questTime = int(section["param1"]) #任务总时间
		self.showTime = int(section["param2"])	#剩余多久显示提示(单位秒)

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if spaceEntity.queryTemp("questMsgID"):
			timeID = spaceEntity.queryTemp("questMsgID")
			spaceEntity.popTimer(timeID)
			spaceEntity.removeTemp("questMsgID")
		timeID = spaceEntity.addTimerCallBackForScript( (self.questTime - self.showTime),"showTimeCountDown",(csstatus.SPACE_QUEST_END_NOTIFY,self.showTime) )
		spaceEntity.setTemp("questMsgID",timeID)
		for e in spaceEntity._spaceRoles:
			e.client.ShowSpaceLife( str(self.questTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), 1,str( Functions.getTime() ) )

class SEAction149( SEActionBase ):
	"""
	隐藏任务倒计时界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if spaceEntity.queryTemp("questMsgID"):
			timeID = spaceEntity.queryTemp("questMsgID")
			spaceEntity.popTimer(timeID)
			spaceEntity.removeTemp("questMsgID")
		for e in spaceEntity._spaceRoles:
			e.client.HideSpaceLife()

class SEAction150(SEActionBase):
	"""
	撞击怪物开始播动作
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.scriptIDList= []

	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord( scriptID )
			for id in idList:
				entity = KBEngine.entities.get( id, None )
				if not entity:
					continue
				entity.playMoveAction()

class SEAction151(SEActionBase):
	"""
	CST-4021 幻阵迷宫奇遇副本藏宝库程序需求
	多种id的spellBOX同种信号的保底操作
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
		try:
			params = section["param1"].split("|")
			self.key = params[0]				#通知副本ID
			self.times = int(params[1])			#接收通知的最大次数
			self.securityTimes = int(params[2])	#保底次数
			self.spellBoxIDList = section["param2"].split("|")
			self.initSelf = True
		except:
			KBEDebug.ERROR_MSG("SEAction151:init error")
			self.initSelf = False
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not self.initSelf:
			return
		
		if not spaceEntity:
			return

		if spaceEntity.queryTemp(self.key):
			KBEDebug.ERROR_MSG("SEAction151:Space's temp dct has exist %s" %(self.key))
			return
	
		spaceEntity.setTemp(self.key, {"times" : self.times, "securityTimes" : self.securityTimes, "spellBoxIDList" : self.spellBoxIDList})

class SEAction153( SEActionBase ):
	"""
	灵魂之誓副本 打开/关闭 灵魂能量球UI
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isOpen = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			spaceEntity.isOpen =  self.isOpen
			spaceEntity.updateSoulPercent(player, self.isOpen)
		

class SEAction154( SEActionBase ):
	"""
	副本增加额外修为
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.xiuwei = int(section["param1"]) #额外增加修为

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.addXiuwei(self.xiuwei, csdefine.XIUWEI_ADD_REASON_SPACE_SENTLEMENT)
		

class SEAction155( SEActionBase ):
	"""
	副本所有玩家脚下刷个entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.createEntityByScriptID(self.scriptID, player.position, player.direction,{ "spawnPos":player.position ,"spawnDir":player.direction})
	
		
class SEAction156( SEActionBase ):
	"""
	指定位置 朝向  刷怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")
		self.positionList = section["param2"].split("|")
		self.directionList = section["param3"].split("|")
		self.number = [int(x) for x in section["param4"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		scriptIDList = list(self.scriptIDList)
		positionList = list(self.positionList)
		directionList = list(self.directionList)
		random.shuffle(scriptIDList)
		random.shuffle(positionList)
		random.shuffle(directionList)

		number = self.number[0]
		if len(self.number)>1:
			number = random.randint(self.number[0], self.number[1])
		for index in range(0,number):
			position = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(positionList[index]))	#位置
			direction = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(directionList[index]))	#朝向
			spaceEntity.createEntityByScriptID(scriptIDList[index], position, direction,{ "spawnPos":position ,"spawnDir":direction})

			
class SEAction157( SEActionBase ):
	"""
	阴阳棋阵 随机指定若干棋子位置 创建entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]
		self.number = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		pointList = [ point for point, value in  spaceEntity.pointHasPiece.items() if value != HAS_PIECE_NONE]
		if self.number >len(pointList):
			return
		points = random.sample(pointList, self.number)

		for point in points:
			position = spaceEntity.getBoardPosition(point[0], point[1])
			direction = (0.0,0.0,0.0)
			spaceEntity.createEntityByScriptID(self.scriptID, position, direction,{ "spawnPos":position ,"spawnDir":direction})



class SEAction164( SEActionBase ):
	"""
	幻莲天池 刷金鱼 CST-3803
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.spawnInfos = []	#[(ID,pos,sacle)]
	
	def init( self, section ):
		SEActionBase.init( self, section )
		_ID = []	
		_posList = []		
		_sacle = []		
				
		# 读取
		IDList = section["param1"].split("|")
		for ID in IDList:
			i = int(ID)
			_ID.append(i)

		posStrList = section["param2"].split("|")		#格式 "x1 y1 z1 | x2 y2 z2 |..."
		for posStr in posStrList:
			pos = Functions.vector3TypeConvert( posStr )
			_posList.append( pos )
		
		sacleStrList = section["param3"].split("|")
		for sacleStr in sacleStrList:
			sacle = float(sacleStr)
			_sacle.append( sacle )

		k = 0
		for i in _ID:
			self.spawnInfos.append((_ID[i],_posList[i],_sacle[i]))
			k+=1

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for infos in self.spawnInfos:
			for e in spaceEntity._spaceRoles:
				e.client.CreateFish( infos[0], infos[1][0], infos[1][1], infos[1][2], infos[2] )

class SEAction168( SEActionBase ):
	"""
	随机选择一个图腾随机发出特定光效
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.effectIDList = section["param1"].split("|")
		self.scriptIDs = section["param2"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		idList = []
		scriptID = random.choice( self.scriptIDs)
		idList = spaceEntity.getEntityRecord( scriptID )
		if len(idList) == 0: return
		spaceEntity.totemDict = {}
		theTrue = KBEngine.entities.get(random.choice( idList ))
		effectID = random.choice( self.effectIDList )
		theTrue.allClients.CLIENT_OnPlayParticles( theTrue.id, int(effectID),"", 1.0,Math.Vector3(0,0,0) )
		spaceEntity.totemDict[theTrue.id] = int(effectID)

class SEAction169( SEActionBase ):
	"""
	随机选择两个雷电柱随机选择旋转速度
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rotatSpeed = section["param1"].split("|")
		self._scriptID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		otherIDs = []
		entitylist = spaceEntity.getEntityRecord( self._scriptID )
		if len(entitylist) == 0: return
		IDs = random.sample( entitylist, 2 )
		for scriptID in entitylist:
			if scriptID not in IDs:
				otherIDs.append( scriptID )
		for id in IDs:
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.allClients.NotifyClinetRotat( entity.id, float(self.rotatSpeed[0]) )
		for id in otherIDs:
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.allClients.NotifyClinetRotat( entity.id, float(self.rotatSpeed[1]) )

class SEAction170( SEActionBase ):
	"""
	副本内所有玩家播放某镜头	
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.sceneID  = section["param1"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.client.StartPlayStory( self.sceneID, 1 )

class SEAction171 ( SEActionBase ):
	"""
	对触发副本收到通知事件的entity施法技能 CST-3803
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._skillID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(int(eventParams["extraValue"]),None)
		if entity:
			entity.useSkillToEntity( self._skillID, entity.id )

class SEAction172( SEActionBase ):
	"""
	刷某些批次的entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.groups = [ int(i) for i in section["param1"].split("|") ]
		self.refreshAmount = int( section["param2"] )
		self.scriptIDs = section["param3"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if len(self.groups) <= self.refreshAmount:
			KBEDebug.ERROR_MSG( "SEAction172 config is error " )
			return
		groups = list( self.groups )
		refreshAmount = self.refreshAmount
		entityIDList = []
		for scriptID in self.scriptIDs:
			entityIDList.extend( spaceEntity.getEntityRecord(scriptID ) )
		for entityID in entityIDList:
			entity = KBEngine.entities.get( entityID,None )
			if entity and entity.group in groups:
				groups.remove(entity.group)
				refreshAmount -= 1				

		if refreshAmount <= 0:
			return
		random.shuffle( groups )
		groupList = random.sample( groups, refreshAmount )
		for group in groupList:
			spaceEntity.spawnGroupEntity(group,"",0)

class SEAction173( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	设置动态复活点
	""" 		
	def init( self, section ):
		SEActionBase.init( self, section )
		posListStr = section["param1"].split("|")
		dirListStr = section["param2"].split("|")
		self.posList = []
		self.dirList = []
		for posStr in posListStr:
			pos = Functions.vector3TypeConvert( posStr )
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			self.posList.append(pos)
		for dirStr in dirListStr:
			dir = Functions.vector3TypeConvert(dirStr)
			dir = KBEMath.Unreal2KBEngineDirection( dir )
			self.dirList.append(dir)

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		reviverInfo = []
		for i in range( len(self.posList) ):
			reviverInfo.append( ( self.posList[i], self.dirList[i] ) )
		spaceEntity.getScript().setReviverInfo( reviverInfo )

class SEAction174( SEActionBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	设置副本可移动区域
	""" 		
	def init( self, section ):
		SEActionBase.init( self, section )
		self.flag = int(section["param1"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setAreaFlags(self.flag)

class SEAction175 ( SEActionBase ):
	"""
	对触发副本收到通知事件的entity添加BUFF
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._buffID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(int(eventParams["extraValue"]),None)
		if entity:
			entity.addBuff( entity, self._buffID)

class SEAction176( SEActionBase ):
	"""
	神乐雕像 拾取乐器
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.talkTargetScriptID = section["param1"]
		self.yueqiScriptID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.onPlayerGetYueQi( self.talkTargetScriptID, self.yueqiScriptID )

class SEAction177( SEActionBase ):
	"""
	改变石笋状态
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.ChangeTerrainByBOSS()

class SEAction178( SEActionBase ):
	"""
	cst-4056 冰雪之战 击杀玩家
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		spaceEntity.memberDatas.kill(dieEntity.id,killEntity.id)


class SEAction179( SEActionBase ):
	"""
	cst-4056 冰雪之战 大将被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		spaceEntity.killBoss(killEntity)

class SEAction180( SEActionBase ):
	"""
	根据不同的光效刷不同的怪物
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.monsterDataList = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for monsterData in self.monsterDataList:
			data = self.monsterDataList.split(":")
		for entityID, effectID in spaceEntity.totemDict:
			if int(effectID) == int(data[0]):
				entity = KBEngine.entities.get( entityID, None)
				entity.createEntityByScriptID(self._scriptID,entity.position,entity.direction,{"spawnPos":entity.position, "spawnDir": entity.direction})

class SEAction181( SEActionBase ):
	"""
	CST-3805 副本某些脚本类型的怪播放动作
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]
		self._actionID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityIDlist = spaceEntity.getEntityRecord(self._scriptID)
		for entityID in entityIDlist:
			entity = KBEngine.entities.get(entityID,None)
			if entity:
				entity.allClients.CLIENT_OnPlayAction(self._actionID,-1.0)

class SEAction182( SEActionBase ):
	"""
	CST-3805 某批次的怪上下移动
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]
		self._moveDistance = float(section["param2"])
		self._speed = float(section["param3"]) if section["param3"] else 0

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityIDlist = spaceEntity.getEntityRecord(self._scriptID)
		for entityID in entityIDlist:
			entity = KBEngine.entities.get(entityID,None)
			if not entity:
				continue
			dstPos = Math.Vector3(entity.position.x, entity.position.y+self._moveDistance, entity.position.z)
			speed = self._speed if self._speed else entity.getSpeed()
			entity.moveStart( csdefine.MOVE_TYPE_MOVE_POINT, speed, True, ( dstPos, 0.0, False, True ) )

class SEAction183( SEActionBase ):
	"""
	CST-3805 根据某scriptID的boss(位置)的范围随机筛选MovingPlatformLotus的entity并开始移动
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.offsetFront = 0.0												#向前偏移量
		self.offsetLeft  = 0.0												#向左偏移量
		self.offsetUp	 = 0.0												#向上偏移量

	def init( self, section ):
		SEActionBase.init( self, section )
		self._bossScriptID = section["param1"]
		self._scriptID = section["param2"]
		strList = section["param3"].split("|")
		self._radius = int(strList[0])
		self._amount = int(strList[1])
		offset = section["param4"].split("|")
		if offset[0]:
			self.offsetFront = float( offset[0] )
		if len(offset) >= 2 and offset[1]:
			self.offsetLeft = float( offset[1] )
		if len(offset) >= 3 and offset[2]:
			self.offsetUp = float( offset[2] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		bossEntityID = spaceEntity.getEntityRecord(self._bossScriptID)
		if len(bossEntityID) != 1:
			return
		bossEntity = KBEngine.entities.get(bossEntityID[0],None)
		if not bossEntity:
			return
		def calculateOffset( position, direction ):
			"""计算偏移量"""
			yaw = direction.z
			if self.offsetFront:
				position.x += self.offsetFront * math.sin( yaw )
				position.z += self.offsetFront * math.cos( yaw )
			if self.offsetLeft:
				position.x += self.offsetLeft * math.sin( yaw - math.pi/2 )
				position.z += self.offsetLeft * math.cos( yaw - math.pi/2 )
			if self.offsetUp:
				position.y += self.offsetUp
			return position
		pos = calculateOffset(bossEntity.position, bossEntity.direction)
		idList = spaceEntity.getEntityRecord( self._scriptID )
		entitylist = []
		for id in idList:
			i = KBEngine.entities.get( id )
			if not i:
				continue
			if pos.distTo(i.position)<self._radius:
				entitylist.append(i)
		randList = random.sample(entitylist, self._amount)
		for entity in randList:
			entity.lotusMoveStart()

class SEAction184( SEActionBase ):
	"""
	CST-3805 重置MovingPlatformLotus的entity的位置
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		idList = spaceEntity.getEntityRecord( self._scriptID )
		for id in idList:
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.resetPosition()

class SEAction185( SEActionBase ):
	"""
	CST-3805 镇煞宫副本交互处理
	"""
	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().onSpellGossipOver(spaceEntity, eventParams["extraValue"])

class SEAction186( SEActionBase ):
	"""
	CST-4446 帮会争霸第二场 击杀怪物获得积分
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.integral = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get(eventParams["killerID"],None)
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			KBEDebug.ERROR_MSG("SEAction180 killEntity is not player ")
			return
		spaceEntity.addIntegral( killEntity, self.integral )

class SEAction187( SEActionBase ):
	"""
	CST-4446 帮会争霸第二场 玩家被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self.boxScriptID = section["param1"].split("|")[0] #掉落的箱子
			self.reduceIntegralByTrap = float(section["param1"].split("|")[1]) #被陷阱击杀掉落的积分倍率
		self.reduceIntegralByRole = float(section["param2"]) #被玩家击杀减少的积分倍率

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get(eventParams["killerID"],None)
		if dieEntity == None or killEntity == None:
			return
		member = self.warInfos.getMember( dieEntity.tongDBID, dieEntity.playerDBID )
		if not member:
			return
		dieCurIntegral = member.getIntegral()
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_TRAP:
			reduceIntegral = min(dieCurIntegral, int(self.reduceIntegralByTrap * dieCurIntegral))
			spaceEntity.reduceIntegral( dieEntity, reduceIntegral )
			boxEntity = spaceEntity.createEntityByScriptID( self.boxScriptID, dieEntity.position,dieEntity.direction,{} )
			if boxEntity:
				boxEntity.setTemp("integral",reduceIntegral)
		elif killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			reduceIntegral = min(dieCurIntegral, int(self.reduceIntegralByRole * dieCurIntegral))
			spaceEntity.reduceIntegral( dieEntity, reduceIntegral )

class SEAction188( SEActionBase ):
	"""
	四象变幻副本、梦魇画卷副本 怪物血量变化
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._index = section["param1"]		#索引
		self._scriptID = section["param2"]	#怪物scriptID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		entityIDList = spaceEntity.getEntityRecord(self._scriptID)
		if not len(entityIDList):
			return
		entityID = entityIDList[0]
		entity = KBEngine.entities.get(entityID,None)
		if not entity:
			return
		percent = int(math.ceil(entity.HP/entity.HP_Max*100))
		for e in spaceEntity._spaceRoles:
			e.client.CLIENT_OnPremierHPChanged( int(self._index), percent )

class SEAction192( SEActionBase ):
	"""
	cst-4276 神乐雕像 刷灵球
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.delayTime = float( section["param1"] )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.createLingQiu( self.delayTime )
		
class SEAction194( SEActionBase ):
	"""
	天之幻境：随机位置刷怪（可接对应巡逻路线，如无可配0）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.positionList = []
		self.directionList = []
		self.patrolList= []
		self.bRepeat = True
		num = section["param1"].split("|")
		self.spawnNum = int(num[0])							# 刷新数量
		self.scriptIDs = num[1].split(";")					# 刷新scriptID
		if len(num) >= 3:									# 是否重复刷
			self.bRepeat = int(num[2])
		for position in section["param2"].split("|"):
			pos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(position))
			self.positionList.append(pos)
		for direction in section["param3"].split("|"):
			dir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(direction))
			self.directionList.append(dir)
		for patrol in section["param4"].split("|"):
			self.patrolList.append(int(patrol))
		maxNum = len(self.positionList)
		assert maxNum == len(self.directionList),"Num is not matching!"
		assert maxNum >= self.spawnNum,"Max num is smaller than spawnNum!"
		self.spawnPoints = []
		for i in range(maxNum):
			self.spawnPoints.append(i)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if self.bRepeat:
			spawnPoints = self.spawnPoints
		else:
			spawnPoints = list(self.spawnPoints)
			allEntityRecord = list( spaceEntity.getAllEntityRecord() )
			
			for index, scriptID in enumerate( self.scriptIDs):
				if scriptID in allEntityRecord and index in spawnPoints:
					spawnPoints.remove(index)
			
		num = min(len(spawnPoints), self.spawnNum)
		spawnPoints = random.sample( spawnPoints, num )
		for index in spawnPoints:
			scriptID = self.scriptIDs[index]
			pos = self.positionList[index]
			dit = self.directionList[index]
			patrol = 0
			if len(self.patrolList) >= index:
				patrol = self.patrolList[index]
			spaceEntity.createEntityByScriptID(scriptID, pos,dit, { "spawnPos": pos, "spawnDir": dit, "patrolList" : patrol})

class SEAction195( SEActionBase ):
	"""
	帮会争霸第三场 传送所有报名内场人员进入内场
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.teleportEnterField()

class SEAction196( SEActionBase ):
	"""
	帮会争霸第三场 内场战斗结束
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.integral = int(section["param1"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.fieldFightEnd( self.integral )


class SEAction197( SEActionBase ):
	"""
	冰雪之战 双方阵营持续掉分
	"""
	def init(self, section):
		SEActionBase.init(self, section)
		
	def do(self, spaceEntity, triggerID, eventParams):
		if spaceEntity:
			spaceEntity._decreasePowerPoint()

class SEAction198( SEActionBase ):
	"""
	临渊试炼 随机创建灵草
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.initRandomCreateSpellBox()

class SEAction199( SEActionBase ):
	"""
	给某些scriptID的spellbox发送指令
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
		self.commandID = section["param2"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for scriptID in self.scriptIDs:
			for id in spaceEntity.getEntityRecord( scriptID ):
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				for player in spaceEntity._spaceRoles:
					entity.spaceNotifyTempData[player.playerDBID] = self.commandID
					entity.requestRefreshCondition( entity, player )

class SEAction200( SEActionBase ):
	"""
	触发者（玩家）申请进入警戒
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self._time = 0.0

	def init( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self._time  = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			trigger.applyEnterWarn(csdefine.ROLE_WARN_REASON_SPACE, self._time)

class SEAction201( SEActionBase ):
	"""
	触发者（玩家）申请离开警戒
	"""
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			trigger.applyLeaveWarn(csdefine.ROLE_WARN_REASON_SPACE)

class SEAction202( SEActionBase ):
	"""
	冰雪之战 哨塔被抢夺闪烁提示
	"""
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		towerID = eventParams["receiverID"]
		attackID = eventParams["casterID"]
		spaceEntity.onTowerBeAttack(towerID, casterID)

class SEAction203( SEActionBase ):
	"""
	刷新场景物件条件
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			entityList = player.entitiesInView()
			for entity in entityList:
				if entity.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
					entity.requestRefreshCondition( entity, player )

class SEAction204( SEActionBase ):
	"""
	触发者（必须是玩家）设置PK模式
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		# 1:进入副本设置pk模式，并锁定模式
		# 2:离开副本解锁模式，并恢复之前的pk模式
		self._actionType = int( section["param1"] )
		if section["param2"]:
			self._pkModel = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		if self._actionType == 1 and self._pkModel:
			trigger.setTemp("pkModel", trigger.pkMode )
			trigger.setPkMode( self._pkModel )
			trigger.lockPkMode()
		elif self._actionType == 2:
			trigger.unLockPkMode()
			trigger.setPkMode( trigger.queryTemp("pkModel") )

class SEAction205( SEActionBase ):
	"""
	触发者必须是玩家,发送副本剩余时间和副本名字到客户端
	"""
	def do( self, spaceEntity, triggerID, eventParams ):
		for player in spaceEntity._spaceRoles:
			_remainTime = spaceEntity.lifeTime - int( time.time() - spaceEntity.lifeStartTime )
			player.client.CopyRemainTimeAndName( _remainTime, spaceEntity.scriptID )

class SEAction206( SEActionBase ):
	"""
	临渊试炼 生存周期到达之后随机刷新灵草
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entity = KBEngine.entities.get( triggerID )
		if not entity:
			return
		spaceEntity.randomRefrehMedicine( entity.position, entity.direction )

class SEAction207( SEActionBase ):
	"""
	添加不清空的场景效果
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.effectIDs = []
		if section["param1"]:
			self.effectIDs = [ int(i) for i in section["param1"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.addSpaceEffects( self.effectIDs )

class SEAction208( SEActionBase ):
	"""
	移除场景效果
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.effectIDs = []
		if section["param1"]:
			self.effectIDs = [ int(i) for i in section["param1"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.removeSpaceEffects( self.effectIDs )

class SEAction209( SEActionBase ):
	"""
	暂停副本声音
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isStop = int(section["param1"])
		self.VoiceTypeList = section["param2"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		CurPauseTypes = self.VoiceTypeList
		CurHideTypes = []
		bPause = False
		bIsHideVoiceType = False
		if not self.isStop:
			CurHideTypes = self.VoiceTypeList
			bPause = True

		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_SetPausedSpaceVoice(CurPauseTypes, CurHideTypes, bPause, bIsHideVoiceType )

class SEAction210( SEActionBase ):
	"""
	强制完成阶段目标: 阶段目标ID 次数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.stageIndex = int( section["param1"] )	# 阶段目标ID
		if section["param2"]:
			self.progress = int( section["param2"] )	# 次数

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().spaceStage_gmCompleteStageTask( spaceEntity, self.stageIndex, self.progress )


class SEAction218( SEActionBase ):
	"""
	神乐雕像 初始化雕像
	根据配置刷出雕像交互对象 并且给不需要交互的大雕像上挂件
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.initStatue()

class SEAction222( SEActionBase ):
	"""
	发送随机通知ID到副本
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._randomKey = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		randomKey = list(self._randomKey)
		random.shuffle( randomKey )
		spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, randomKey[0], "")

class SEAction223( SEActionBase ):
	"""
	发送不连续一样随机通知ID到副本
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._randomKey = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		randomKey = list(self._randomKey)
		if len(randomKey) > 1:
			if spaceEntity.queryTemp("randomKeyNotice") in randomKey:
				randomKey.remove(spaceEntity.queryTemp("randomKeyNotice"))
		random.shuffle( randomKey )
		spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, randomKey[0], "")
		spaceEntity.setTemp("randomKeyNotice", randomKey[0])

class SEAction224( SEActionBase ):
	"""
	在触发者(不是玩家)位置和朝向创建entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]
		self._direction = Functions.vector3TypeConvert( section["param2"] ) if section["param2"] else None

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID, None)
		if entity and spaceEntity:
			position = entity.position
			direction = entity.direction if self._direction == None else self._direction
			spaceEntity.createEntityByScriptID(self._scriptID ,position, direction,{"spawnPos":position, "spawnDir": direction})

class SEAction231( SEActionBase ):
	"""
	魔像水晶：随机位置刷怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.positionList = []
		self.directionList = []
		num = section["param1"].split("|")
		self.spawnNum = int(num[1])							# 刷新数量
		self.scriptIDs = num[0].split(";")					# 刷新scriptIDs
		
		for position in section["param2"].split("|"):
			if position:
				pos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(position))
				self.positionList.append(pos)
		for direction in section["param3"].split("|"):
			if direction:
				dir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(direction))
				self.directionList.append(dir)

		maxNum = len(self.positionList)
		self.spawnPoints = []
		for i in range(maxNum):
			self.spawnPoints.append(i)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		num = self.spawnNum * len(self.scriptIDs)
		
		spawnPoints = random.sample( self.spawnPoints, num )
		scriptIDs = []
		for id in self.scriptIDs:
			for i in range(self.spawnNum):
				scriptIDs.append(id)
		
		for index, point  in enumerate(spawnPoints):
			pos = self.positionList[point]
			dit = self.directionList[point]
			
			spaceEntity.createEntityByScriptID(scriptIDs[index], pos,dit, { "spawnPos": pos, "spawnDir": dit})

class SEAction233( SEActionBase ):
	"""
	显示五行画卷机关属性界面
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.isOpen = 0
		
	def init( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self.isOpen = bool(int(section["param1"]))	#开关: 0关闭 1打开
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.client.CLIENT_ShowWXHJAttrUI( self.isOpen  )

class SEAction236( SEActionBase ):
	"""
	某些scriptID自己给自己的添加buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
		self.buffIDs = [ int(i) for i in section["param2"].split("|") ]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for scriptID in self.scriptIDs:
			for entity in spaceEntity.getEntityMailBoxRecord( scriptID ):
				for buffID in self.buffIDs:
					entity.addBuff( entity, buffID )

class SEAction237( SEActionBase ):
	"""
	给某些scriptID的移除buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
		self.buffIDs = [ int(i) for i in section["param2"].split("|") ]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for scriptID in self.scriptIDs:
			for entity in spaceEntity.getEntityMailBoxRecord( scriptID ):
				for buffID in self.buffIDs:
					entity.removeBuffByID( buffID )

class SEAction241( SEActionBase ):
	"""
	副本追杀鱼怪
	给所有指定scriptID怪物发通知
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.cmd = section["param1"]
		self.monsterScriptID = section["param2"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityIDlist = []
		for scriptID in self.monsterScriptID:
			entityIDlist.extend(spaceEntity.getEntityRecord(scriptID))

		if not len(entityIDlist):
			return
		scriptID = random.choice(entityIDlist)
		monster = KBEngine.entities.get(scriptID, None)
		if monster:
			monster.monsterAIOnCommand( spaceEntity.id, "AI", self.cmd )

class SEAction254( SEActionBase ):
	"""
	副本里的所有玩家开始迷雾效果
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self._albedo = ""
		self._extinctionMulity = ""
		self._holeRadius = ""
		self._insideExtinction = ""
		self._outsideExtinction = ""
		self._enterTime = 0.0

	def init( self, section ):
		SEActionBase.init( self, section )
		self._albedo = section["param1"]
		List = section["param2"].split(";")
		self._extinctionMulity = List[0]
		self._holeRadius = List[1]
		self._insideExtinction = List[2]
		self._outsideExtinction = List[3]
		if section["param3"]:
			self._enterTime = float(section["param3"])
		self._scriptID = section["param4"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord( self._scriptID )
		if not len(entityList):
			return
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_StartFog(entityList[0].id, self._albedo, self._extinctionMulity, self._holeRadius,self._insideExtinction, self._outsideExtinction, self._enterTime)

class SEAction255( SEActionBase ):
	"""
	副本里的所有玩家结束迷雾效果
	"""
	def __init__( self ):
		SEActionBase.__init__( self )

	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_EndFog()

class SEAction271( SEActionBase ):
	"""
	根据玩家的职业添加对应的Buff  根据策划的配置习惯从战士，剑客，链刃，法师依次填写技能ID，用“|”隔开
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.professions = [csdefine.CLASS_FIGHTER, csdefine.CLASS_SWORDMAN, csdefine.CLASS_ARCHER, csdefine.CLASS_MAGE]						
		self.Dict = {}

	def init( self, section ):
		SEActionBase.init( self, section )
		BuffIDs = [int(BuffID) for BuffID in section["param1"].strip().split("|")]
		self.Dict = dict(zip(self.professions, BuffIDs ))

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID, None)
		if not spaceEntity or not entity:
			return
		entity.addBuff(entity,self.Dict[entity.profession])
		
class SEAction273( SEActionBase ):
	"""
	scriptID为某值的SpellBox,设置雾气属性
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID  = section["param1"]
		self.albedo  = section["param2"]
		strList = section["param3"].split("|")
		self.starHoldRadius = float(strList[0])
		self.endHoldRadius = float(strList[1])
		self.extinction = float(strList[2])
		self.time = float(strList[3])
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for id in spaceEntity.getEntityRecord( self.scriptID ):
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.allClients.CLIENT_OnHoldRadiusFog(self.albedo, self.starHoldRadius, self.endHoldRadius, self.extinction, self.time)

class SEAction274( SEActionBase ):
	"""
	强制改变玩家的方向为朝向某个坐标
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.direction = None

	def init( self, section ):
		SEActionBase.init( self, section )
		direction = Functions.vector3TypeConvert( section["param1"] )
		self.direction = KBEMath.Unreal2KBEngineDirection( direction )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.changeDirection(self.direction, csdefine.REASON_CHANGE_DIR_FORCE)

class SEAction280( SEActionBase ):
	"""
	触发者（必须是玩家）设置AOI
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._aoiRadius = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			trigger.setViewRadius( self._aoiRadius, Const.DEFAULT_AOI_EXTRA_RADIUS )

class SEAction281( SEActionBase ):
	"""
	副本内所有玩家设置AOI
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._aoiRadius = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.setViewRadius( self._aoiRadius, Const.DEFAULT_AOI_EXTRA_RADIUS )

class SEAction282( SEActionBase ):
	"""
	在多边形区域内随机位置刷怪
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.belowHeight = 0
		self.ceilHeight = 0
		self.spawnInfos = []
		self.kbePoints = []
		self.polygon = None
	
	def init( self, section ):
		SEActionBase.init( self, section )	
		tempList = section["param1"].split("|")
		self.floorHeight = float(tempList[0])/100   #地面高度
		if len(tempList) > 1:
			self.belowHeight = float(tempList[1])/100 	#配的客户端z值，转成服务器端y值
			self.ceilHeight = float(tempList[2])/100	#配的客户端z值，转成服务器端y值
				
		posList = section["param2"].split("|")
		for posStr in posList:
			clientX = float( posStr.split()[0] )
			clientY = float( posStr.split()[1] )
			self.kbePoints.append( ( clientY/100, clientX/100 ) )
		self.polygon = Polygon( self.kbePoints )
		spawnList = section["param3"].split("|")
		for infos in spawnList:
			info = infos.split(":")
			self.spawnInfos.append((info[0], int(info[1])))
		self.isCheck = int(section["param4"]) if section["param4"] else 0
	
	def do( self, spaceEntity, triggerID, eventParams ):
		def getPoint():
			times = 0
			while 1:
				pos = self.polygon.getRandomPoint()
				if pos:
					cubePos = Math.Vector3(pos[0], self.floorHeight, pos[1])
					if not self.isCheck:
						return cubePos
					PositionList = KBEngine.collideVertical(spaceEntity.spaceID, 0, cubePos, 10, -10 )
					if len(PositionList):
						return cubePos
					if times> 20:  	#允许循环最大次数
						List = list(self.kbePoints)
						random.shuffle( List )
						return Math.Vector3(List[0][0], self.floorHeight, List[0][1])
					times += 1
		for infos in self.spawnInfos:
			for i in range(infos[1]):
				height = random.uniform(self.belowHeight, self.ceilHeight)
				position = getPoint()
				pos = Math.Vector3(position.x, position.y + height, position.z)
				dir = (0.0, 0.0, 0.0)
				spaceEntity.createEntityByScriptID(infos[0], pos, dir, {"spawnPos":pos, "spawnDir": dir})

class SEAction290( SEActionBase ):
	"""
	某怪物对某怪物使用某技能 所有scriptID的怪物只能存在一个
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.srcScriptIDs = section["param1"].split("|")
		self.dstScriptIDs = section["param2"].split("|")
		self.skillIDs = [int(i) for i in section["param3"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for i in range(0,len(self.srcScriptIDs)):
			srcEntitys = spaceEntity.getEntityMailBoxRecord( self.srcScriptIDs[i] )
			dstEntitys = spaceEntity.getEntityMailBoxRecord( self.dstScriptIDs[i] )
			if len(srcEntitys) and len(dstEntitys):
				srcEntitys[0].useSkillToEntity( self.skillIDs[i],dstEntitys[0].id )

class SEAction301( SEActionBase ):
	"""
	大地图不同ID的怪物,显示不同的颜色
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.Dict = {}
		strList = section["param1"].split("|")
		for Str in strList:
			List = Str.split(":")
			self.Dict[List[0]] = int(List[1])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for key,value in self.Dict.items():
			List = spaceEntity.getEntityMailBoxRecord( key )
			for i in List:
				for role in spaceEntity._spaceRoles:
					role.client.ClIENT_DisplayLocationAndColor(KBEMath.KBEngine2UnrealPosition(i.position), value )

class SEAction311( SEActionBase ):
	"""
	清除副本内所有玩家额外物品栏 (务必还需配置120行为,以确保掉线后重登进其他地图能正确移除额外物品栏 )
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		for player in spaceEntity._spaceRoles:
			if player and player.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				player.setUnLockSpaceCopyGridNum( 0 )
				player.client.RemoveExtralItemBar()

class SEAction312( SEActionBase ):
	"""
	增加副本内所有玩家额外物品栏
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.maxNum = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		for player in spaceEntity._spaceRoles:
			if player and player.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				player.setUnLockSpaceCopyGridNum( self.maxNum )
				spaceCopyItemList = player.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY)
				uidList = []
				for itemInst in spaceCopyItemList:
					uidList.append(str(itemInst.uid))
				player.client.CreateExtraItemBar( self.maxNum, uidList )

class SEAction321(SEActionBase):
	"""
	环任务根据某个怪物血量给奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"].strip()
		self.questID = section["param2"].strip()
		self.msgInfo = section["param3"].strip()

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		num = 0
		entitys = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if len(entitys):
			num = int(entitys[0].HP)
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( num )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				roleCell.client.ShowLoopRewardTip( self.msgInfo + str(num), exp, money, 0, 0 )

class SEAction323( SEActionBase ):
	"""
	显示某怪物圆形血量界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.isOpen = bool(int(section["param1"]))	#开关 0：关闭 1打开
		self.scriptID = section["param2"]
		self.describe = section["param3"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		if not self.isOpen:
			for e in spaceEntity._spaceRoles:
				e.client.ShowMonsterCircleHPPercentBar( 0, 0, self.describe )	

		entityList = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if not len(entityList):
			return
		percent = int(math.floor(entityList[0].HP/entityList[0].HP_Max*100))
		for e in spaceEntity._spaceRoles:
			e.client.ShowMonsterCircleHPPercentBar( self.isOpen, percent, self.describe )

class SEAction324( SEActionBase ):
	"""
	CST-7929 废弃！！！
	触发对话选择界面（触发者必须是玩家）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.optionID = section["param1"] 	# 对话选择界面ID

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		optionKeys = g_optionTalkLoader.getOptionTalkDes( self.optionID )	# 获取对话选择界面的key和选项描述
		defaultOptions = g_optionTalkLoader.getDefaultOptions()		# 获取默认选项
		countDown = g_optionTalkLoader.getCountDown()		# 获取倒计时时间
		trigger.client.onShowDefaultOption( self.optionID, defaultOptions, float(countDown) )
		for optionKey, optionDes in optionKeys.items():
			trigger.client.onShowOptionTalkDes( self.optionID, optionKey, optionDes )

class SEAction325( SEActionBase ):
	"""
	环任务副本失败
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.countDown = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().onLoopQuestSpaceFailure( spaceEntity, self.countDown )

class SEAction326( SEActionBase ):
	"""
	给副本内所有玩家发送奖励 (走奖励流程)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rewardID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		useTime = int( time.time() - spaceEntity.lifeStartTime )
		for player in spaceEntity._spaceRoles:
			rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":player} )
			RewardMgr.g_rewardMgr.doRewards( rewardDatas, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_SPACE_EVENT )
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, player.accountDBID, player.playerDBID, player.getLevel(), 
				LogDefine.ACTIVE_REWARD_TYPE_REWARD_ID, self.rewardID, spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
class SEAction335( SEActionBase ):
	"""
	暂停副本计时
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().stopSpaceLife( spaceEntity )

class SEAction336( SEActionBase ):
	"""
	继续副本计时
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().gotoSpaceLife( spaceEntity )

class SEAction340( SEActionBase ):
	"""
	荷花法阵 强制玩家下荷花
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			role.forceDismountHeHua()

class SEAction341(SEActionBase):
	"""
	魔像水晶：清除玩家数据
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			trigger.removeTemp( "ClickMonsterIDs_MXSJ" )

class SEAction351(SEActionBase):
	"""
	触发者(玩家)播放镜头
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.sceneID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		if trigger.getClient():
			trigger.client.StartPlayStory( self.sceneID, 1 )

class SEAction352(SEActionBase):
	"""
	触发者(玩家)设置血量
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.percent = float(section["param1"])
		self.addValue = 0
		if section["param2"]:
			self.addValue = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		hp = int(trigger.HP_Max * self.percent + self.addValue)
		trigger.setHP(hp)

class SEAction353(SEActionBase):
	"""
	触发者(玩家)设置蓝量
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.percent = float(section["param1"])
		self.addValue = 0
		if section["param2"]:
			self.addValue = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		mp = int(trigger.MP_Max * self.percent + self.addValue)
		trigger.setMP(mp)

class SEAction359( SEActionBase ):
	"""
	多个scriptID中随机几个发送AI指令(如果该怪物不存在将不参与随机)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")
		self.randomNum = int( section["param2"] )
		self.commandID = section["param3"]
	
	def do( self, spaceEntity, triggerID, eventParams ):
		existEntityList = []
		for scriptID in self.scriptIDs:
			entityList = spaceEntity.getEntityRecord( scriptID )
			if len( entityList ) == 0:
				continue
			existEntityList.append( entityList )
		if len( existEntityList ) < self.randomNum:
			self.randomNum = len( existEntityList )
		entityIDs = random.sample( existEntityList, self.randomNum )
		for entityID in entityIDs:
			for id in entityID:
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entity.monsterAIOnCommand( spaceEntity.id, spaceEntity.scriptID, self.commandID )
				
class SEAction360( SEActionBase ):
	"""
	设置坐标同步频率/取消坐标同步（CST-9224 测试用）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
		self.sync = int(section["param1"])
		self.frequency = int( section["param2"] )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity: return
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
			
		pass
	

class SEAction361( SEActionBase ):
	"""
	充能道具物品
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.amount = int( section["param1"] ) #充能次数
		self.itemID = int( section["param2"] ) #物品ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			itemInstList = role.getItemInstsByID( self.itemID )
			for itemInst in itemInstList:
				itemInst.addUseNumber( self.amount, role )

class SEAction373( SEActionBase ):
	"""
	指定位置根据概率召唤指定ID的entity，可支持多个位置对应召唤多个entities
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.spawnInfos = []	#[(pos,dir,idAndNumList, probList)]
	
	def init( self, section ):
		SEActionBase.init( self, section )
		__posList = []		#位置列表
		__dirList = []		#朝向列表
		__idAndNumList = []	#scriptID和数量列表 [[(scriptID1,amount),(scriptID2,amount)]]
		__probList = []		#概率列表[[概率1，概率2...], ]其中概率相加等于1 
		# 读取
		posStrList = section["param1"].split("|")		#格式 "x1 y1 z1 | x2 y2 z2 |..."
		for posStr in posStrList:
			pos = Functions.vector3TypeConvert( posStr )
			__posList.append( KBEMath.Unreal2KBEnginePosition( pos ) )
		
		dirStrList = section["param2"].split("|")		#格式 "x1 y1 z1 | x2 y2 z2 |..."
		for dirStr in dirStrList:
			dir = Functions.vector3TypeConvert( dirStr )
			__dirList.append( KBEMath.Unreal2KBEngineDirection( dir ) )
		
		allEntityInfo = section["param3"].split("|")	 #格式 "scriptID1:amount1; scriptID2:amount2... | scriptID1:amount1; scriptID2:amount2... |..."
		for onePosInfo in allEntityInfo:
			tempList = []
			for oneEntityInfo in onePosInfo.split(";"):
				tempInfo = oneEntityInfo.split(":")
				scriptID, amount = tempInfo[0], int( tempInfo[1] )
				tempList.append( ( scriptID, amount ) )
			__idAndNumList.append( tempList )

		if section["param4"]:
			param4List = section["param4"].split("|")	# 概率列表[[概率1，概率2...], ]其中概率相加等于1 
			for probs in param4List:
				tempList = []
				for prob in probs.split(":"):
					tempList.append(float(prob))
				__probList.append(tempList)


		# 验证
		if not __posList or not __dirList or not __idAndNumList:
			KBEDebug.ERROR_MSG( "Param lack!" )
			return
		if len( __posList ) != 1 and len( __dirList ) != 1 and len( __posList ) != len( __dirList ):
			KBEDebug.ERROR_MSG( "Pos num and dir num not match! ", section["param1"] )	#输出一个参数以便查找配置
			return
		if len( __posList ) != 1 and len( __idAndNumList ) != 1 and len( __posList ) != len( __idAndNumList ):
			KBEDebug.ERROR_MSG( "Pos num and scriptID num not match! ", section["param1"] )
			return
		if len( __probList ) != 1 and len( __idAndNumList ) != 1 and len(__idAndNumList) != len( __probList ):
			KBEDebug.ERROR_MSG( "prob num and scriptID num not match! ")
			return

		
		# 组装位置和朝向
		posAndDirList = []
		if len( __posList ) == 1 and len( __dirList ) == 1:
			posAndDirList.append( ( __posList[0], __dirList[0] ) )
		elif len( __dirList ) == 1:
			for pos in __posList:
				posAndDirList.append( ( pos, __dirList[0] ) )
		elif len( __posList ) == 1:
			for dir in __dirList:
				posAndDirList.append( ( __posList[0], dir ) )
		else:
			for index, pos in enumerate( __posList ):
				posAndDirList.append( ( pos, __dirList[index] ) )
		
		# 扩充位置和朝向列表 或者 扩充scriptID和数量列表
		num = max( len( __idAndNumList ), len( posAndDirList ) )
		if len( __idAndNumList ) != num:
			__idAndNumList = __idAndNumList * num
		if len( posAndDirList ) != num:
			posAndDirList = posAndDirList * num
		
		# 组装位置、朝向、scriptID、数量
		for index, tempList in enumerate( __idAndNumList ):
			posAndDir = posAndDirList[ index ]
			self.spawnInfos.append((posAndDir[0], posAndDir[1], tempList, __probList[index] ) )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		for info in self.spawnInfos:
			scriptID = 0
			amount = 0
			randomProb = random.random()
			prob = 0.0
			for index, i in enumerate(info[3]):
				prob += i
				if randomProb <= prob:
					scriptID = info[2][index][0]
					amount = info[2][index][1]
					break
			for x in range(amount):
				entity = spaceEntity.createEntityByScriptID( scriptID, info[0], info[1], { "spawnPos": info[0], "spawnDir": info[1] } )

class SEAction377( SEActionBase ):
	"""
	副本内所有玩家放弃某任务
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			e.abandonQuest( self.questID)

class SEAction384( SEActionBase ):
	"""
	通知客户端玩家是否是第一次进入该副本
	"""
	def init( self, section ):
		SEActionBase.init(self, section)

	def do(self, spaceEntity, triggerID, eventParams):
		entity = KBEngine.entities.get(triggerID)
		DBID = entity.playerDBID
		enterPlayerList = spaceEntity.queryTemp("enterPlayerList", [])
		if DBID not in enterPlayerList:
			enterPlayerList.append(DBID)
			spaceEntity.setTemp("enterPlayerList", enterPlayerList)
			entity.client.SetIsFirstEnterCopy(True)
		else:
			entity.client.SetIsFirstEnterCopy(False)

class SEAction406( SEActionBase ):
	"""
	随机销毁副本某scriptID的怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]  #scriptID
		self._amount = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		idList = list( spaceEntity.getEntityRecord( self._scriptID ) )
		random.shuffle(idList)
		destroyIDList = idList[:self._amount]
		for id in destroyIDList:
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.destroySelf()

class SEAction409( SEActionBase ):
	"""
	练兵场PVP 击杀玩家
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.jade = int(section["param1"]) #获得魂玉
		self.exploits = int(section["param2"]) #获得军功

	def do( self, spaceEntity, triggerID, eventParams ):
		
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return

		spaceEntity.onPlayerBeKilled(dieEntity, killEntity, self.jade, self.exploits)


class SEAction410( SEActionBase ):
	"""
	练兵场PVP 击杀士兵
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.jade = int(section["param1"]) #获得魂玉

	def do( self, spaceEntity, triggerID, eventParams ):
		
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return

		spaceEntity.onSoldierBeKilled(dieEntity, killEntity, self.jade)


class SEAction411( SEActionBase ):
	"""
	练兵场 摧毁水晶
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		dieEntity = KBEngine.entities.get(triggerID,None)
		if dieEntity == None:
			return

		spaceEntity.onBaseTowerBeDestroyed(dieEntity)


class SEAction412( SEActionBase ):
	"""
	练兵场PVE 将领死亡
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		dieEntity = KBEngine.entities.get(triggerID,None)
		if dieEntity == None:
			return

		spaceEntity.onCmderDead(dieEntity)
	
	
class SEAction419( SEActionBase ):
	"""
	CST-11329 根据副本玩家的队长等级（若是单人则根据该玩家等级）发送邮件
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.mailIDList = section["param1"].split("|")
		
		self.levelsegment = []
		segmentList = section["param2"].split("|")
		for segment in segmentList:
			temp = segment.split("-")
			self.levelsegment.append([int(temp[0]), int(temp[1])])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		useTime = int( time.time() - spaceEntity.lifeStartTime )	
		if len(self.levelsegment) != len(self.mailIDList):
			KBEDebug.ERROR_MSG("config error, %s, %s" %(self.levelsegment, self.mailIDList))
			return
		
		for role in spaceEntity._spaceRoles:
			level = role.level
			if role.isInTeam():
				e = KBEngine.entities.get(role.captainID)
				if e: level = e.level
			
			mailID = self.getMailByLevel(level)
			if mailID is None:continue
			g_mailContentDataLoader.sendSpaceReward(mailID, role.getName())
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, role.accountDBID, role.playerDBID, role.getLevel(), 
				LogDefine.ACTIVE_REWARD_TYPE_MAIL, mailID, spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
			
	def getMailByLevel(self, level):
		for index, levelsegment in enumerate(self.levelsegment):
			if level >= levelsegment[0] and level <= levelsegment[1]:
				return self.mailIDList[index]
		return None	
	
class SEAction421( SEActionBase ):
	"""
	CST-11376 帮会副本奖励结算 界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.countDownTime = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		useTime = int( time.time() - spaceEntity.lifeStartTime )
		countdown = (10 * 60 - useTime) if (10 * 60 - useTime) > 0 else 1
		
		config = g_TongSpaceCopyRewardLoader.getCfgByScriptIDAndValue(spaceEntity.scriptID, countdown)
		if config is None:
			KBEDebug.ERROR_MSG("NOT FOUND CONFIG %s - %s" %(spaceEntity.scriptID, useTime))
			return
			
		for roleCell in spaceEntity._spaceRoles:
			if len(config["buffList"]):
				for buff in config["buffList"]:
					roleCell.addBuff(roleCell, buff)
			
			itemStr = ""
			items = []
			rewardDatas = RewardMgr.g_rewardMgr.getReward(config["rewardID"], {"player" : roleCell, "spaceLevel": spaceEntity.spaceLevel, })
			rewardItemDatas = self.calcRewardDatas( rewardDatas )
			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				if roleCell.addItem(itemInst, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT) != csstatus.ITEM_GO_ON:
					items.append( itemInst )
				
				if itemStr : itemStr += "|"
				itemStr += "{}:{}".format(itemInst.id, itemInst.getAmount())
				
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
				LogDefine.ACTIVE_REWARD_TYPE_ITEM, itemInst.id, spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				
			#没有加成功的物品通过邮件发送
			if len(items):
				role.sendRemainItemWithMail(items, csdefine.REMAIN_ITEM_SPACE_COPY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
			
			rate = 1
			if roleCell.getActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY ) == 2:
				rate = Const.TONG_SPACE_COPY_TOTAL_RATE
			
			if config["barracksExp"]:
				barracksExp = int(config["barracksExp"] * rate)
				roleCell.addBarracksExp( barracksExp )
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
				LogDefine.ACTIVE_REWARD_TYPE_BARRACKS_EXP, str(barracksExp), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
			
			if roleCell.tongMB:
				if config["contribute"]:
					contribute = int(config["contribute"] * rate)
					roleCell.tongMB.addContribution(roleCell.playerDBID, contribute)
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_CONTRIBUTE, str(contribute), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				
				if config["money"]:
					money = int(config["money"] * rate)
					roleCell.tongMB.addTongMoney( money, csdefine.TONG_MONEY_ADD_REASON_NORMAL )
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_TONG_MONEY, str(money), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)

				#完成帮会副本，获取对应奖励
				roleCell.tongMB.onTongSpaceComplete(roleCell.playerDBID)
				
				roleCell.client.ShowTongSpaceSettlementWin( self.countDownTime, useTime, barracksExp, contribute, money, config["buff"], itemStr, config["score"], config["grade"] )
				
	def calcRewardDatas(self, rewardDatas):
		"""
		"""
		rewardItemDatas = []
		for data in rewardDatas:
			type = data["type"]
			amount = data["amount"]
			goodsid = data["goodsid"]
			# 物品奖励
			if type == csdefine.REWARD_TYPE_ITEM:
				rewardItemDatas.append( data )
		return rewardItemDatas
			

class SEAction427( SEActionBase ):
	"""
	CST-11472 生成副本奖励宝箱
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.position = Math.Vector3(0,0,0)
		self.direction = Math.Vector3( 0,0,0 )
		self.modelNumber = ""
		self.modelScale = 1.0
		if section["param1"]:
			infos = section["param1"].split("|")
			pos = Functions.vector3TypeConvert( infos[0] )
			dir = Functions.vector3TypeConvert( infos[1] )
			self.position = KBEMath.Unreal2KBEnginePosition( pos )
			self.direction = KBEMath.Unreal2KBEngineDirection( dir )
		if section["param2"]:
			self.modelNumber = section["param2"].split("|")[0]
			self.modelScale = float( section["param2"].split("|")[1] )
		self.rewardID =  section["param3"] 

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		rewardItemDatas = []
		def calcRewardDatas(rewardDatas):
			for data in rewardDatas:
				type = data["type"]
				amount = data["amount"]
				goodsid = data["goodsid"]
				# 物品奖励
				if type == csdefine.REWARD_TYPE_ITEM:
					rewardItemDatas.append( data )

		rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID,{"spaceLevel":spaceEntity.spaceLevel})
		calcRewardDatas( rewardDatas )
		allocationItems = {} #已分配物品列表{"DBID": [item1, item2,...], ... }
		notAllocationItems = []	#未分配物品列表
		ascriptionID = 0
		ownershipIDs = []
		teamCaptainDBID = 0
		if len(spaceEntity._spaceRoles) > 0:
			entity = KBEngine.entities.get(spaceEntity._spaceRoles[0].id,None)
			if entity:
				if not entity.isInTeam(): #个人，默认全部已分配给玩家
					allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						if entity.playerDBID not in allocationItems:
							allocationItems[ entity.playerDBID ] = []
						allocationItems[ entity.playerDBID ].append( itemInst )
					ascriptionID = entity.playerDBID
					ownershipIDs.append( entity.playerDBID )
				elif entity.isInTeam(): #组队
					allocation = entity.getOwnerAllocation()
					quality = entity.getOwnerQuality()

					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						notAllocationItems.append( itemInst )
					ascriptionID = entity.teamMailbox.id
					captain = KBEngine.entities.get( entity.captainID, None )
					if captain:
						teamCaptainDBID = captain.playerDBID
					ownershipIDs.extend(entity.getAllTeamMemberDBIDs())
					
					#除了自由拾取，其他的都创建成队伍箱子
					if allocation != csdefine.TEAM_PICKUP_TYPE_FREEDOM:
						createTeamDropBox(spaceEntity, self.position, self.direction, self.modelNumber, self.modelScale, notAllocationItems, ownershipIDs, allocation, ascriptionID, teamCaptainDBID)
						return
		else:
			allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				notAllocationItems.append( itemInst )
		dropBoxEntiy = spaceEntity.createEntityNear( "DropBox", self.position, self.direction, {"modelNumber":self.modelNumber,"modelScale":self.modelScale,"ownershipIDs":ownershipIDs, "allocationItems": allocationItems, "notAllocationItems": notAllocationItems, "allocation": allocation,"ascriptionID": ascriptionID, "teamCaptainDBID": teamCaptainDBID } )

class SEAction428( SEActionBase ):
	"""
	CST-11533 在触发者脚底生成奖励宝箱
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.modelScale = 1.0
		self.modelNumber = section["param1"]
		if section["param2"]:
			self.modelScale = float(section["param2"])
		self.rewardID = section["param3"]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		if not spaceEntity:
			return

		rewardItemDatas = []
		def calcRewardDatas(rewardDatas):
			for data in rewardDatas:
				type = data["type"]
				amount = data["amount"]
				goodsid = data["goodsid"]
				# 物品奖励
				if type == csdefine.REWARD_TYPE_ITEM:
					rewardItemDatas.append( data )

		rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID,{"spaceLevel":spaceEntity.spaceLevel})
		calcRewardDatas( rewardDatas )
		allocationItems = {} #已分配物品列表{"DBID": [item1, item2,...], ... }
		notAllocationItems = []	#未分配物品列表
		ascriptionID = 0
		ownershipIDs = []
		teamCaptainDBID = 0
		if len(spaceEntity._spaceRoles) > 0:
			entity = KBEngine.entities.get(spaceEntity._spaceRoles[0].id,None)
			if entity:
				if not entity.isInTeam(): #个人，默认全部已分配给玩家
					allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						if entity.playerDBID not in allocationItems:
							allocationItems[ entity.playerDBID ] = []
						allocationItems[ entity.playerDBID ].append( itemInst )
					ascriptionID = entity.playerDBID
					ownershipIDs.append( entity.playerDBID )
				elif entity.isInTeam(): #组队
					allocation = entity.getOwnerAllocation()
					quality = entity.getOwnerQuality()

					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						notAllocationItems.append( itemInst )
					ascriptionID = entity.teamMailbox.id
					captain = KBEngine.entities.get( entity.captainID, None )
					if captain:
						teamCaptainDBID = captain.playerDBID
					ownershipIDs.extend(entity.getAllTeamMemberDBIDs())
					
					#除了自由拾取，其他的都创建成队伍箱子
					if allocation != csdefine.TEAM_PICKUP_TYPE_FREEDOM:
						createTeamDropBox(spaceEntity, trigger.position, trigger.direction, self.modelNumber, self.modelScale, notAllocationItems, ownershipIDs, allocation, ascriptionID, teamCaptainDBID)
						return
		else:
			allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				notAllocationItems.append( itemInst )
		dropBoxEntiy = spaceEntity.createEntityNear( "DropBox", trigger.position, trigger.direction, {"modelNumber":self.modelNumber,"modelScale":self.modelScale,"ownershipIDs":ownershipIDs, "allocationItems": allocationItems, "notAllocationItems": notAllocationItems, "allocation": allocation,"ascriptionID": ascriptionID, "teamCaptainDBID": teamCaptainDBID } )

class SEAction430( SEActionBase ):
	"""
	击杀士兵，增加计数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		spaceEntity.memberDatas.killSD(dieEntity.id,killEntity.id)


class SEAction431( SEActionBase ):
	"""
	CST-10782 
	新增一个副本计数，随机一个初值
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.countKey = section["param1"]
		self.randomStr = [int(x) for x in section["param2"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		num = random.randint(self.randomStr[0], self.randomStr[1])
		spaceEntity.getScript().spaceEvent_addCount( spaceEntity, self.countKey, num)


class SEAction432( SEActionBase ):
	"""
	CST-10782 
	给触发者怪物发送AI指令
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.commandID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entity = KBEngine.entities.get(triggerID, None)
		entity.monsterAIOnCommand( spaceEntity.id, spaceEntity.scriptID, self.commandID )

class SEAction438( SEActionBase ):
	"""
	洞府 第一阶段结果
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.stage = 1						# 1:第一阶段,2:第二阶段
		self.isChallenge = 1				# (0：掠夺战，1：争夺战)
		self.isSuccess = False				# 结果(0：攻方失败，1：为攻方成功)
		if section["param1"]:
			self.stage = int( section["param1"])
		if section["param2"]:
			self.isChallenge = int( section["param2"] )
		if section["param3"]:
			self.isSuccess = int( section["param3"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if self.stage == 1:
			spaceEntity.getScript().onFirstStageResult( spaceEntity, self.isChallenge, self.isSuccess )
		else:
			spaceEntity.onActiveResult( self.isChallenge, self.isSuccess )


class SEAction439( SEActionBase ):
	"""
	练兵场播放宣战消息提示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		lbcItem = spaceEntity.createArgs.get("lbcItem")

		for role in spaceEntity._spaceRoles:
			role.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_DECLAR_WAR, lbcItem.declarerName, lbcItem.occupierName, lbcItem.lbcName)
			
class SEAction440( SEActionBase ):
	"""
	掉落惊喜宝箱(该宝箱每个玩家只能开启一次，获得专属奖励。)
	CST--11293
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.modelNumber = section["param1"]
		self.modelScale = 1.0
		if section["param2"]:
			self.modelScale = float(section["param2"])
		self.rewardID = section["param3"]

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		
		if not spaceEntity:
			return
		
		allocationItems = {} #已分配物品列表{"DBID": [item1, item2,...], ... }
		notAllocationItems = []	#未分配物品列表
		ascriptionID = 0
		ownershipIDs = []
		teamCaptainDBID = 0
		if len(spaceEntity._spaceRoles) > 0:
			allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人自由拾取模式
			for role in spaceEntity._spaceRoles:
				if role and not role.isDestroyed:
					ownershipIDs.append(role.playerDBID)
					
					rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID,{"spaceLevel":spaceEntity.spaceLevel,"dieEntity":trigger, "player" : role})
					rewardItemDatas = self.calcRewardDatas( spaceEntity, trigger, rewardDatas )
					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						if itemInst is None: continue
						if role.playerDBID not in allocationItems:
							allocationItems[ role.playerDBID ] = []
						allocationItems[ role.playerDBID ].append( itemInst )
			
			dropBoxEntiy = spaceEntity.createEntityNear( "DropBox", trigger.position, trigger.direction, {"modelNumber":self.modelNumber,"modelScale":self.modelScale,"ownershipIDs":ownershipIDs, "allocationItems": allocationItems, "notAllocationItems": notAllocationItems, "allocation": allocation,"ascriptionID": ascriptionID, "teamCaptainDBID": teamCaptainDBID } )
	
	def calcRewardDatas(self, spaceEntity, trigger, rewardDatas):
		"""
		"""
		rewardItemDatas = []
		for data in rewardDatas:
			type = data["type"]
			amount = data["amount"]
			goodsid = data["goodsid"]
			# 物品奖励
			if type == csdefine.REWARD_TYPE_ITEM:
				rewardItemDatas.append( data )
		return rewardItemDatas
			
class SEAction441( SEActionBase ):
	"""
	设置下一副本等级
	CST-11293
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.level = int(section["param1"]) if section["param1"] else 0
	
	def do( self, spaceEntity, triggerID, eventParams ):	
		if not spaceEntity or len(spaceEntity._spaceRoles) <= 0:
			return
		
		role = spaceEntity._spaceRoles[0]
		spaceEntity.setTemp("NextBunchSpaceLevel", role.level + self.level)
		if  role.isInTeam():
			captain = KBEngine.entities.get(role.captainID)
			if captain:
				spaceEntity.setTemp("NextBunchSpaceLevel", captain.level + self.level)

class SEAction442( SEActionBase ):
	"""
	击杀将领，增加计数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		spaceEntity.memberDatas.killGeneral(dieEntity.id,killEntity.id)
		
class SEAction443( SEActionBase ):
	"""
	根据建筑等级刷新护卫
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buildType = int( section["param1"] )
		self.scriptIDs = [ i for i in section["param2"].split("|") ]
		self.position = KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( section["param3"] ) )
		self.direction = KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( section["param4"]  ) )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if self.buildType in spaceEntity.buildLevel:			# 还没初始化好数据
			level = spaceEntity.buildLevel[self.buildType]
			param = {}
			param["spawnPos"] = self.position
			param["spawnDir"] = self.direction
			spaceEntity.createEntityByScriptID( self.scriptIDs[level-1], self.position, self.direction, param )

class SEAction444( SEActionBase ):
	"""
	在以 所有玩家/攻方/守方 为圆心的指定距离的位置刷怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.playerType = int( section["param1"])				# 0:所有玩家、1：攻方玩家、2：守方玩家
		self.radius = float( section["param2"] )
		self.idAndAmountDict = {}
		for tempStr in section["param3"].split( "|" ):
			id, amount = tempStr.split( ":" )
			self.idAndAmountDict[ id ] = int( amount )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		space = KST.g_objFactory.getSpaceObject( spaceEntity.scriptID )
		navmeshPath = space._navmeshPath
		
		for trigger in spaceEntity._spaceRoles:
			if self.playerType == 1 and trigger.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
				continue
			if self.playerType == 2 and trigger.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				continue
				
			poszlist = []
			for scriptID in self.idAndAmountDict:
				i = 0
				pool = 0
				while ( i < self.idAndAmountDict[scriptID] ):
					desPos = csarithmetic.getPositionByLink(trigger.position, self.radius)

					posList = KBEngine.navigatePathPoints( navmeshPath, trigger.position, desPos, self.radius, 0, 0xffff )
					if pool > 5:
						KBEDebug.ERROR_MSG("Has been find navigatePathPoints %s times"%pool)
						return						#当多次找不到位置时，则退出	
					if not posList:
						pool +=1
						continue

					pos = posList.pop()
					flag = 0
					for k in poszlist:			  		#避免出现怪物重叠
						if abs(pos.z - k) < 0.4:	  	#不允许的距离
							flag = 1
							break
					if flag:
						continue
					poszlist.append(pos.z)

					yaw = trigger.position - pos
					dir = Math.Vector3(0,0,math.atan2(yaw.x,yaw.z))
					spaceEntity.createEntityByScriptID(scriptID, pos, dir, {"spawnPos":pos, "spawnDir": dir})
					i += 1

class SEAction445( SEActionBase ):
	"""
	CST-12069 一定概率触发玉玦蕴灵（废弃）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.probability = float( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			v = random.random()
			if v <= self.probability and role.getClient():
				role.client.StartYunLing()

class SEAction449( SEActionBase ):
	"""
	对触发者（玩家）生成光墙
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get( triggerID )
		if trigger.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			for monster in spaceEntity.getEntityMailBoxRecord( self.scriptID ):
				clientEntity = trigger.clientEntity( monster.id )
				if clientEntity:
					monster.wallCountDownTime = 0
					clientEntity.CLIENT_CreateFightArea()

class SEAction451( SEActionBase ):
	"""
	给副本内攻/守方玩家发送消息 查看客户端MessageConfig表
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.statusID = int(section["param1"]) #消息ID表
		self.param = section["param2"]
		self.belongSide = int( section["param3"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			if role.isBelongSide( self.belongSide ):
				role.statusMessage(self.statusID, self.param)

class SEAction452( SEActionBase ):
	"""
	副本内所攻\守方玩家播放界面提示并播放声音
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.soundID = section["param1"]
		self.belongSide = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			if e.isBelongSide( self.belongSide ):
				e.roleSpaceCopyPlaySound(self.soundID)

class SEAction453( SEActionBase ):
	"""
	洞府活动阶段+1
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].addDFActiveStage( spaceEntity.belongDBID )

class SEAction454( SEActionBase ):
	"""
	生成归属于击杀者的奖励箱子
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.modelNumber = section["param1"]
		self.modelScale = float(section["param2"])
		self.rewardID =  section["param3"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		killEntity = KBEngine.entities.get( eventParams["killerID"], None )
		if not killEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		if not dieEntity:
			return
		rewardItemDatas = []
		def calcRewardDatas(rewardDatas):
			for data in rewardDatas:
				type = data["type"]
				amount = data["amount"]
				goodsid = data["goodsid"]
				# 物品奖励
				if type == csdefine.REWARD_TYPE_ITEM:
					rewardItemDatas.append( data )

		rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID,{"spaceLevel":spaceEntity.spaceLevel})
		calcRewardDatas( rewardDatas )
		allocationItems = {} #已分配物品列表{"DBID": [item1, item2,...], ... }
		notAllocationItems = []	#未分配物品列表
		ascriptionID = 0
		ownershipIDs = []
		teamCaptainDBID = 0
		if not killEntity.isInTeam(): #个人，默认全部已分配给玩家
			allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				if killEntity.playerDBID not in allocationItems:
					allocationItems[ killEntity.playerDBID ] = []
				allocationItems[ killEntity.playerDBID ].append( itemInst )
			ascriptionID = killEntity.playerDBID
			ownershipIDs.append( killEntity.playerDBID )
		elif killEntity.isInTeam(): #组队
			allocation = killEntity.getOwnerAllocation()
			quality = killEntity.getOwnerQuality()

			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				notAllocationItems.append( itemInst )
			ascriptionID = killEntity.teamMailbox.id
			captain = KBEngine.entities.get( killEntity.captainID, None )
			if captain:
				teamCaptainDBID = captain.playerDBID
			ownershipIDs.extend(killEntity.getAllTeamMemberDBIDs())
			
			#除了自由拾取，其他的都创建成队伍箱子
			if allocation != csdefine.TEAM_PICKUP_TYPE_FREEDOM:
				createTeamDropBox(spaceEntity, dieEntity.position, dieEntity.direction, self.modelNumber, self.modelScale, notAllocationItems, ownershipIDs, allocation, ascriptionID, teamCaptainDBID)
				return
		else:
			allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				notAllocationItems.append( itemInst )
		
		dropBoxEntiy = spaceEntity.createEntityNear( "DropBox", dieEntity.position, dieEntity.direction, {"modelNumber":self.modelNumber,"modelScale":self.modelScale,"ownershipIDs":ownershipIDs, "allocationItems": allocationItems, "notAllocationItems": notAllocationItems, "allocation": allocation,"ascriptionID": ascriptionID, "teamCaptainDBID": teamCaptainDBID } )
		
class SEAction456( SEActionBase ):
	"""
	副本设置临时标记
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.key = section["param1"]
		self.value = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity: return
		spaceEntity.setTemp("SPACE_{}".format(self.flag), self.value)
		
class SEAction457( SEActionBase ):
	"""
	副本移除临时标记
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.key = section["param1"]
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity: return
		spaceEntity.removeTemp("SPACE_{}".format(self.key))
		
class SEAction460( SEActionBase ):
	"""
	给触发者发送消息（MessageCfg配置表的消息）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.statusID = int(section["param1"])	 #消息ID
		self.param = section["param2"] #消息ID表中的动态参数

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			trigger.statusMessage(self.statusID, self.param)

class SEAction462( SEActionBase ):
	"""
	显示临时装备栏
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			tempEquipList = trigger.getItemListByKBType(ItemTypeEnum.BAG_TEMP_EQUIP)
			data = {}
			for itemInst in tempEquipList:
				data.update({itemInst.order:itemInst.id})
			trigger.client.CreateTempEquipBar(data)

class SEAction463( SEActionBase ):
	"""
	关闭临时装备栏
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			trigger.client.RemoveTempEquipBar()
			tempEquipList = trigger.getItemListByKBType(ItemTypeEnum.BAG_TEMP_EQUIP)
			for itemInst in tempEquipList:
				itemInst.unWield(trigger)
				trigger.removeItemByAmount( itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )
			#恢复技能栏可用
			trigger.client.SetIsEnabledQuickBar(True)

class SEAction465( SEActionBase ):
	"""
	大荒战场 玩家大风筝飞行
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			spaceEntity.roleStartYCJMDFly(trigger)

class SEAction469( SEActionBase ):
	"""
	设置副本掉落数量 用于 RewardForNumber 
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rate = float( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.setTemp("spaceRewardRate",self.rate)
		
class SEAction470( SEActionBase ):
	"""
	帮会副本给奖励（CST-13701）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rewardID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":player} )
			if player.getActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY ) == 2:
				for data in rewardDatas:
					data["amount"] = int( data["amount"] * Const.TONG_SPACE_COPY_TOTAL_RATE )
			RewardMgr.g_rewardMgr.doRewards( rewardDatas, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_SPACE_EVENT )
		
SEActionBase.setActionClass("SEAction1", SEAction1)
SEActionBase.setActionClass("SEAction2", SEAction2)
SEActionBase.setActionClass("SEAction3", SEAction3)
SEActionBase.setActionClass("SEAction4", SEAction4)
SEActionBase.setActionClass("SEAction5", SEAction5)
SEActionBase.setActionClass("SEAction6", SEAction6)
SEActionBase.setActionClass("SEAction7", SEAction7)
SEActionBase.setActionClass("SEAction8", SEAction8)
SEActionBase.setActionClass("SEAction9", SEAction9)
SEActionBase.setActionClass("SEAction10", SEAction10)
SEActionBase.setActionClass("SEAction11", SEAction11)
SEActionBase.setActionClass("SEAction12", SEAction12)
SEActionBase.setActionClass("SEAction13", SEAction13)
SEActionBase.setActionClass("SEAction14", SEAction14)
SEActionBase.setActionClass("SEAction15", SEAction15)
SEActionBase.setActionClass("SEAction16", SEAction16)
SEActionBase.setActionClass("SEAction17", SEAction17)
SEActionBase.setActionClass("SEAction18", SEAction18)
SEActionBase.setActionClass("SEAction19", SEAction19)
SEActionBase.setActionClass("SEAction20", SEAction20)
SEActionBase.setActionClass("SEAction21", SEAction21)
SEActionBase.setActionClass("SEAction22", SEAction22)
SEActionBase.setActionClass("SEAction23", SEAction23)
SEActionBase.setActionClass("SEAction24", SEAction24)
SEActionBase.setActionClass("SEAction25", SEAction25)
SEActionBase.setActionClass("SEAction26", SEAction26)
SEActionBase.setActionClass("SEAction27", SEAction27)
SEActionBase.setActionClass("SEAction28", SEAction28)
SEActionBase.setActionClass("SEAction29", SEAction29)
SEActionBase.setActionClass("SEAction30", SEAction30)
SEActionBase.setActionClass("SEAction31", SEAction31)
SEActionBase.setActionClass("SEAction32", SEAction32)
SEActionBase.setActionClass("SEAction33", SEAction33)
SEActionBase.setActionClass("SEAction34", SEAction34)
SEActionBase.setActionClass("SEAction42", SEAction42)
SEActionBase.setActionClass("SEAction43", SEAction43)
SEActionBase.setActionClass("SEAction44", SEAction44)
SEActionBase.setActionClass("SEAction45", SEAction45)
SEActionBase.setActionClass("SEAction46", SEAction46)
SEActionBase.setActionClass("SEAction47", SEAction47)
SEActionBase.setActionClass("SEAction48", SEAction48)
SEActionBase.setActionClass("SEAction49", SEAction49)
SEActionBase.setActionClass("SEAction50", SEAction50)
SEActionBase.setActionClass("SEAction51", SEAction51)
SEActionBase.setActionClass("SEAction52", SEAction52)
SEActionBase.setActionClass("SEAction53", SEAction53)
SEActionBase.setActionClass("SEAction54", SEAction54)
SEActionBase.setActionClass("SEAction55", SEAction55)
SEActionBase.setActionClass("SEAction56", SEAction56)
SEActionBase.setActionClass("SEAction62", SEAction62)
SEActionBase.setActionClass("SEAction63", SEAction63)
SEActionBase.setActionClass("SEAction67", SEAction67)
SEActionBase.setActionClass("SEAction69", SEAction69)
SEActionBase.setActionClass("SEAction76", SEAction76)
SEActionBase.setActionClass("SEAction77", SEAction77)
SEActionBase.setActionClass("SEAction78", SEAction78)
SEActionBase.setActionClass("SEAction79", SEAction79)
SEActionBase.setActionClass("SEAction82", SEAction82)
SEActionBase.setActionClass("SEAction83", SEAction83)
SEActionBase.setActionClass("SEAction84", SEAction84)
SEActionBase.setActionClass("SEAction85", SEAction85)
SEActionBase.setActionClass("SEAction86", SEAction86)
SEActionBase.setActionClass("SEAction87", SEAction87)
SEActionBase.setActionClass("SEAction88", SEAction88)
SEActionBase.setActionClass("SEAction89", SEAction89)
SEActionBase.setActionClass("SEAction90", SEAction90)
SEActionBase.setActionClass("SEAction91", SEAction91)
SEActionBase.setActionClass("SEAction92", SEAction92)
SEActionBase.setActionClass("SEAction93", SEAction93)
SEActionBase.setActionClass("SEAction94", SEAction94)
SEActionBase.setActionClass("SEAction95", SEAction95)
SEActionBase.setActionClass("SEAction96", SEAction96)
SEActionBase.setActionClass("SEAction97", SEAction97)
SEActionBase.setActionClass("SEAction98", SEAction98)
SEActionBase.setActionClass("SEAction99", SEAction99)
SEActionBase.setActionClass("SEAction100", SEAction100)
SEActionBase.setActionClass("SEAction101", SEAction101)
SEActionBase.setActionClass("SEAction102", SEAction102)
SEActionBase.setActionClass("SEAction103", SEAction103)
SEActionBase.setActionClass("SEAction104", SEAction104)
SEActionBase.setActionClass("SEAction108", SEAction108)
SEActionBase.setActionClass("SEAction109", SEAction109)
SEActionBase.setActionClass("SEAction110", SEAction110)
SEActionBase.setActionClass("SEAction111", SEAction111)
SEActionBase.setActionClass("SEAction112", SEAction112)
SEActionBase.setActionClass("SEAction113", SEAction113)
SEActionBase.setActionClass("SEAction115", SEAction115)
SEActionBase.setActionClass("SEAction116", SEAction116)
SEActionBase.setActionClass("SEAction118", SEAction118)
SEActionBase.setActionClass("SEAction119", SEAction119)
SEActionBase.setActionClass("SEAction120", SEAction120)
SEActionBase.setActionClass("SEAction121", SEAction121)
SEActionBase.setActionClass("SEAction122", SEAction122)
SEActionBase.setActionClass("SEAction123", SEAction123)
SEActionBase.setActionClass("SEAction124", SEAction124)
SEActionBase.setActionClass("SEAction125", SEAction125)
SEActionBase.setActionClass("SEAction126", SEAction126)
SEActionBase.setActionClass("SEAction127", SEAction127)
SEActionBase.setActionClass("SEAction128", SEAction128)
SEActionBase.setActionClass("SEAction129", SEAction129)
SEActionBase.setActionClass("SEAction130", SEAction130)
SEActionBase.setActionClass("SEAction131", SEAction131)
SEActionBase.setActionClass("SEAction132", SEAction132)
SEActionBase.setActionClass("SEAction133", SEAction133)
SEActionBase.setActionClass("SEAction134", SEAction134)
SEActionBase.setActionClass("SEAction135", SEAction135)
SEActionBase.setActionClass("SEAction136", SEAction136)
SEActionBase.setActionClass("SEAction137", SEAction137)
SEActionBase.setActionClass("SEAction138", SEAction138)
SEActionBase.setActionClass("SEAction139", SEAction139)
SEActionBase.setActionClass("SEAction140", SEAction140)
SEActionBase.setActionClass("SEAction141", SEAction141)
SEActionBase.setActionClass("SEAction142", SEAction142)
SEActionBase.setActionClass("SEAction143", SEAction143)
SEActionBase.setActionClass("SEAction144", SEAction144)
SEActionBase.setActionClass("SEAction145", SEAction145)
SEActionBase.setActionClass("SEAction146", SEAction146)
SEActionBase.setActionClass("SEAction147", SEAction147)
SEActionBase.setActionClass("SEAction148", SEAction148)
SEActionBase.setActionClass("SEAction149", SEAction149)
SEActionBase.setActionClass("SEAction150", SEAction150)
SEActionBase.setActionClass("SEAction151", SEAction151)
SEActionBase.setActionClass("SEAction153", SEAction153)
SEActionBase.setActionClass("SEAction154", SEAction154)
SEActionBase.setActionClass("SEAction155", SEAction155)
SEActionBase.setActionClass("SEAction156", SEAction156)
SEActionBase.setActionClass("SEAction157", SEAction157)
SEActionBase.setActionClass("SEAction164", SEAction164)
SEActionBase.setActionClass("SEAction168", SEAction168)
SEActionBase.setActionClass("SEAction169", SEAction169)
SEActionBase.setActionClass("SEAction170", SEAction170)
SEActionBase.setActionClass("SEAction171", SEAction171)
SEActionBase.setActionClass("SEAction172", SEAction172)
SEActionBase.setActionClass("SEAction173", SEAction173)
SEActionBase.setActionClass("SEAction174", SEAction174)
SEActionBase.setActionClass("SEAction175", SEAction175)
SEActionBase.setActionClass("SEAction176", SEAction176)
SEActionBase.setActionClass("SEAction177", SEAction177)
SEActionBase.setActionClass("SEAction178", SEAction178)
SEActionBase.setActionClass("SEAction179", SEAction179)
SEActionBase.setActionClass("SEAction180", SEAction180)
SEActionBase.setActionClass("SEAction181", SEAction181)
SEActionBase.setActionClass("SEAction182", SEAction182)
SEActionBase.setActionClass("SEAction183", SEAction183)
SEActionBase.setActionClass("SEAction184", SEAction184)
SEActionBase.setActionClass("SEAction185", SEAction185)
SEActionBase.setActionClass("SEAction186", SEAction186)
SEActionBase.setActionClass("SEAction187", SEAction187)
SEActionBase.setActionClass("SEAction188", SEAction188)
SEActionBase.setActionClass("SEAction192", SEAction192)
SEActionBase.setActionClass("SEAction194", SEAction194)
SEActionBase.setActionClass("SEAction195", SEAction195)
SEActionBase.setActionClass("SEAction196", SEAction196)
SEActionBase.setActionClass("SEAction197", SEAction197)
SEActionBase.setActionClass("SEAction198", SEAction198)
SEActionBase.setActionClass("SEAction199", SEAction199)
SEActionBase.setActionClass("SEAction200", SEAction200)
SEActionBase.setActionClass("SEAction201", SEAction201)
SEActionBase.setActionClass("SEAction202", SEAction202)
SEActionBase.setActionClass("SEAction203", SEAction203)
SEActionBase.setActionClass("SEAction204", SEAction204)
SEActionBase.setActionClass("SEAction205", SEAction205)
SEActionBase.setActionClass("SEAction206", SEAction206)
SEActionBase.setActionClass("SEAction207", SEAction207)
SEActionBase.setActionClass("SEAction208", SEAction208)
SEActionBase.setActionClass("SEAction209", SEAction209)
SEActionBase.setActionClass("SEAction210", SEAction210)
SEActionBase.setActionClass("SEAction218", SEAction218)
SEActionBase.setActionClass("SEAction222", SEAction222)
SEActionBase.setActionClass("SEAction223", SEAction223)
SEActionBase.setActionClass("SEAction224", SEAction224)
SEActionBase.setActionClass("SEAction231", SEAction231)
SEActionBase.setActionClass("SEAction233", SEAction233)
SEActionBase.setActionClass("SEAction236", SEAction236)
SEActionBase.setActionClass("SEAction237", SEAction237)
SEActionBase.setActionClass("SEAction241", SEAction241)
SEActionBase.setActionClass("SEAction254", SEAction254)
SEActionBase.setActionClass("SEAction255", SEAction255)
SEActionBase.setActionClass("SEAction271", SEAction271)
SEActionBase.setActionClass("SEAction273", SEAction273)
SEActionBase.setActionClass("SEAction274", SEAction274)
SEActionBase.setActionClass("SEAction280", SEAction280)
SEActionBase.setActionClass("SEAction281", SEAction281)
SEActionBase.setActionClass("SEAction282", SEAction282)
SEActionBase.setActionClass("SEAction290", SEAction290)
SEActionBase.setActionClass("SEAction301", SEAction301)
SEActionBase.setActionClass("SEAction311", SEAction311)
SEActionBase.setActionClass("SEAction312", SEAction312)
SEActionBase.setActionClass("SEAction321", SEAction321)
SEActionBase.setActionClass("SEAction323", SEAction323)
SEActionBase.setActionClass("SEAction324", SEAction324)
SEActionBase.setActionClass("SEAction325", SEAction325)
SEActionBase.setActionClass("SEAction326", SEAction326)
SEActionBase.setActionClass("SEAction335", SEAction335)
SEActionBase.setActionClass("SEAction336", SEAction336)
SEActionBase.setActionClass("SEAction340", SEAction340)
SEActionBase.setActionClass("SEAction341", SEAction341)
SEActionBase.setActionClass("SEAction351", SEAction351)
SEActionBase.setActionClass("SEAction352", SEAction352)
SEActionBase.setActionClass("SEAction353", SEAction353)
SEActionBase.setActionClass("SEAction359", SEAction359)
SEActionBase.setActionClass("SEAction360", SEAction360)
SEActionBase.setActionClass("SEAction361", SEAction361)
SEActionBase.setActionClass("SEAction373", SEAction373)
SEActionBase.setActionClass("SEAction377", SEAction377)
SEActionBase.setActionClass("SEAction384", SEAction384)
SEActionBase.setActionClass("SEAction406", SEAction406)
SEActionBase.setActionClass("SEAction409", SEAction409)
SEActionBase.setActionClass("SEAction410", SEAction410)
SEActionBase.setActionClass("SEAction411", SEAction411)
SEActionBase.setActionClass("SEAction412", SEAction412)
SEActionBase.setActionClass("SEAction419", SEAction419)
SEActionBase.setActionClass("SEAction421", SEAction421)
SEActionBase.setActionClass("SEAction427", SEAction427)
SEActionBase.setActionClass("SEAction428", SEAction428)
SEActionBase.setActionClass("SEAction430", SEAction430)
SEActionBase.setActionClass("SEAction431", SEAction431)
SEActionBase.setActionClass("SEAction432", SEAction432)
SEActionBase.setActionClass("SEAction438", SEAction438)
SEActionBase.setActionClass("SEAction439", SEAction439)
SEActionBase.setActionClass("SEAction440", SEAction440)
SEActionBase.setActionClass("SEAction441", SEAction441)
SEActionBase.setActionClass("SEAction442", SEAction442)
SEActionBase.setActionClass("SEAction443", SEAction443)
SEActionBase.setActionClass("SEAction444", SEAction444)
SEActionBase.setActionClass("SEAction445", SEAction445)
SEActionBase.setActionClass("SEAction449", SEAction449)
SEActionBase.setActionClass("SEAction451", SEAction451)
SEActionBase.setActionClass("SEAction452", SEAction452)
SEActionBase.setActionClass("SEAction453", SEAction453)
SEActionBase.setActionClass("SEAction454", SEAction454)
SEActionBase.setActionClass("SEAction456", SEAction456)
SEActionBase.setActionClass("SEAction457", SEAction457)
SEActionBase.setActionClass("SEAction460", SEAction460)
SEActionBase.setActionClass("SEAction462", SEAction462)
SEActionBase.setActionClass("SEAction463", SEAction463)
SEActionBase.setActionClass("SEAction465", SEAction465)
SEActionBase.setActionClass("SEAction469", SEAction469)
SEActionBase.setActionClass("SEAction470", SEAction470)
