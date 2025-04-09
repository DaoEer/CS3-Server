# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import KBEDebug
import csdefine
import Define

class SpaceCopyJingShiDongKu( SpaceCopyRingTaskChild ):
	"""
	晶石洞窟副本
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )
		self.coordinates = []
		self.monsterScriptID =[]
		self.crystalCoordList = []
		self.crystalScriptIDList = []

	def initData( self, configData ):
		"""
		初始化数据
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		crystalHurtMonster = configData["SpaceData"].get( "crystalHurtMonster", "" )			# 水晶球击中怪物的伤害BUFFID
		if crystalHurtMonster:
			self.crystalHurtMonster = [int(i) for i in crystalHurtMonster.split("|")]
		self.spiritCrystalHarm = int(configData["SpaceData"].get( "spiritCrystalHarm", "" ))	# 灵晶击中玩家的伤害BUFFID
		coordinates = configData["SpaceData"].get("coordinates", "")
		if coordinates:
			self.coordinates = coordinates.split("|")											# 灵晶的坐标
		self.crystalScriptID = configData["SpaceData"].get( "crystalScriptID", "" )				# 抢夺掉落灵晶的怪物ID
		self.crystalCount = int(configData["SpaceData"].get( "crystalCount", "" ))				# 阶段目标总数
		monsterScriptID = configData["SpaceData"].get( "monsterScriptID", "" )
		if monsterScriptID:
			self.monsterScriptID = monsterScriptID.split("|")									# 根据灵晶颜色来刷新怪物的怪物ID列表
		self.upSkillID = int(configData["SpaceData"].get( "upSkillID", "" ))					# 给水晶怪物的技能加成
		self.distance = float(configData["SpaceData"].get("distance", ""))						# 距离玩家多远释放闪电
		crystalCoordList = configData["SpaceData"].get("crystalCoordList", "")					
		if crystalCoordList:
			self.crystalCoordList = crystalCoordList.split("|")									# 水晶球坐标
		crystalScriptIDList = configData["SpaceData"].get("crystalScriptIDList", "")
		if crystalScriptIDList:
			self.crystalScriptIDList = crystalScriptIDList.split("|")							# 水晶球的scriptID

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyRingTaskChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.crystalHurtMonster, self.spiritCrystalHarm, self.coordinates, self.crystalScriptID, self.crystalCount, \
			self.monsterScriptID, self.upSkillID, self.distance, self.crystalCoordList, self.crystalScriptIDList )
			
	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		playerRole.client.CLIENT_OnLeaveJSDFSpace()
		SpaceCopyRingTaskChild.onLeave( self, selfEntity, playerRole, packArgs )