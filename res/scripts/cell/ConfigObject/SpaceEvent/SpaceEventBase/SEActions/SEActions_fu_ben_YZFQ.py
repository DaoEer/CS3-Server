# -*- coding: utf-8 -*-

# 副本事件行为
import random
import Math
import KBEMath
import KBEDebug
import KBEngine
import Functions
import csarithmetic
import csdefine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import time
import math

class SEAction211( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	设置安全区域
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		originCenterPos = Functions.vector3TypeConvert( section["param1"] )
		self.originCenterPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( originCenterPos ) )
		self.originRadius = float(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setOriginCenterPos( self.originCenterPos )
		spaceEntity.setOriginRadius( self.originRadius )

class SEAction212( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
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
		originCenterPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getOriginCenterPos()))
		originRadius = spaceEntity.getOriginRadius()
		player.client.ClIENT_ShowYeZhanFengQiOriginArea( originCenterPos, originRadius )

class SEAction213( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	设置安全区域终点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.endRadius = float( section["param1"] )
		self.minRadius = float( section["param2"] )
		self.maxRadius = float( section["param3"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		radius = random.uniform( self.minRadius,self.maxRadius )
		endCenterPos = csarithmetic.getPositionByLink( spaceEntity.getOriginCenterPos(), radius )
		spaceEntity.setEndCenterPos( endCenterPos )
		spaceEntity.setEndRadius( self.endRadius )

class SEAction214( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	副本内所有玩家显示缩小安全区域终点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		endCenterPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getEndCenterPos()))
		endRadius = spaceEntity.getEndRadius()
		for player in spaceEntity._spaceRoles:
			player.client.ClIENT_ShowYeZhanFengQiEndArea( endCenterPos, endRadius)

class SEAction215( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	开始缩小安全区域
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.totalUseTime = float( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.StartReduceYeZhanFengQiArea( self.totalUseTime )
		for player in spaceEntity._spaceRoles:
			player.client.ClIENT_StartReduceYeZhanFengQiArea( self.totalUseTime )

class SEAction216( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	检查玩家是否在安全区域里
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffID = int( section["param1"] ) # 毒物Buff

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.checkPlayerIsInSaveArea( self.buffID )

class SEAction227( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	玩家被击杀
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
		dieEntityIntegral = spaceEntity.getMemberIntegral( dieEntity )
		if dieEntityIntegral == None:
			KBEDebug.ERROR_MSG("SpaceCopyYeZhanFengQi has no this player(ID = %i) integral"%triggerID)
			return
		pos = csarithmetic.getPositionByLink( dieEntity.position,2.0 )
		posList = KBEngine.collideVertical( dieEntity.spaceID, dieEntity.layer, pos , 100,-100 )
		dstPos = None
		if posList:
			dstPos = posList[0]
		if dstPos != None:
			boxEntity = spaceEntity.createEntityByScriptID( self.boxScriptID, dstPos,dieEntity.direction,{} )
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
		memberInfo = spaceEntity.getMemberInfoByID( dieEntity.id )
		spaceEntity.yeZhanFengQiDropBox( memberInfo,dieEntity.position )
		spaceEntity.reducePlayerIntegral( dieEntity, totalIntegral )
		if killEntity and killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			# rank = spaceEntity.getYeZhanFengQiMemberRankByMemNum()
			# if rank:
			# 	spaceEntity.addTimerCallBack(4.0,"showYeZhanFengQiMemberRank",( dieEntity, rank,spaceEntity.getMemberKill(killEntity) ))
			# memberInfo = spaceEntity.getMemberInfoByID( dieEntity.id )
			# if memberInfo:
			# 	spaceEntity.yeZhanFengQiDropBox( memberInfo,dieEntity.position )
			# spaceEntity.reduceYeZhanFengQiMember(dieEntity)
			return
		spaceEntity.addPlayerIntegral( killEntity,integral )
		spaceEntity.addYeZhanFengQiMemberKillNum(killEntity,dieEntity)

class SEAction232( SEActionBase ):
	"""
	CST-5490 个人竞技 至尊争霸-血斗凤栖镇
	触发者是玩家：显示缩小安全区域终点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		player = KBEngine.entities.get(triggerID,None)
		if not player:
			return
		endCenterPos = KBEMath.KBEngine2UnrealPosition(tuple(spaceEntity.getEndCenterPos()))
		endRadius = spaceEntity.getEndRadius()
		player.client.ClIENT_ShowYeZhanFengQiEndArea( endCenterPos, endRadius)
		if spaceEntity.startReduceTime > 0.0:
			remainTime = spaceEntity.totalUseTime - (time.time() - spaceEntity.startReduceTime )
			player.client.ClIENT_StartReduceYeZhanFengQiArea( remainTime )

SEActionBase.setActionClass( "SEAction211",SEAction211 )
SEActionBase.setActionClass( "SEAction212",SEAction212 )
SEActionBase.setActionClass( "SEAction213",SEAction213 )
SEActionBase.setActionClass( "SEAction214",SEAction214 )
SEActionBase.setActionClass( "SEAction215",SEAction215 )
SEActionBase.setActionClass( "SEAction216",SEAction216 )
SEActionBase.setActionClass( "SEAction227",SEAction227 )
SEActionBase.setActionClass( "SEAction232",SEAction232 )
