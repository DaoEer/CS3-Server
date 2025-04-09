# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyRingTask import SpaceCopyRingTask
import Math
import KBEngine
import csdefine
import Functions
import KBEMath
import FightRuleMgr

class SpaceCopyJingShiDongKu( SpaceCopyRingTask ):
	"""
	晶石洞窟副本
	"""
	def __init__( self ) :
		SpaceCopyRingTask.__init__( self )
		self.addCount = 1
		self.randomList = [1,2,3]
		self.oneCoordDataList = []
		self.secondCoordDataList = []
		self.threeCoordDataList = []

	def initSpaceData( self, crystalHurtMonster, spiritCrystalHarm, coordinates, crystalScriptID, crystalCount, monsterScriptID, upSkillID, distance, \
		crystalCoordList, crystalScriptIDList ):
		"""
		初始化数据
		"""	
		self.crystalHurtMonster = crystalHurtMonster	# 水晶球击中怪物的伤害BUFFID
		self.spiritCrystalHarm = spiritCrystalHarm		# 灵晶击中玩家的伤害BUFFID
		self.coordinates = coordinates 					# 灵晶的坐标
		self.crystalScriptID = crystalScriptID 			# 抢夺掉落灵晶的怪物ID
		self.crystalCount = crystalCount 				# 阶段目标总数
		self.monsterScriptID = monsterScriptID 			# 根据灵晶颜色来刷新怪物的怪物ID列表
		self.upSkillID = upSkillID						# 给水晶怪物的技能加成
		self.distance = distance						# 距离玩家多远释放闪电
		self.crystalCoordList = crystalCoordList		# 水晶球坐标
		self.crystalScriptIDList = crystalScriptIDList	# 水晶球的scriptID

		self.crystalCount1 = random.randint( int(self.crystalCount / 2), self.crystalCount - 6 )
		self.crystalCount2 = random.randint( int((self.crystalCount - self.crystalCount1) / 2 ), self.crystalCount - self.crystalCount1 - 1 )
		self.crystalCount3 = self.crystalCount - self.crystalCount1 - self.crystalCount2

		self.count1 = int( self.crystalCount1 / self.crystalCount * 20 )
		self.count2 = int( self.crystalCount2 / self.crystalCount * 20 )
		self.count3 = int( self.crystalCount3 / self.crystalCount * 20 )

	def onTeleportCompleted( self, playerRole ):
		SpaceCopyRingTask.onTeleportCompleted( self, playerRole )
		playerRole.entityEventSubscribe(csdefine.ENTITY_EVENT_HP_CHANGE, self.id, "triggerSpaceEvent_roleChangeHP" )

	def initData( self, coordinates ):
		"""
		数据更新
		"""
		#每次数据更新之前先清空
		self.spiritCrystalPoint = {}
		self.coordXList = []
		self.coordYList = []
		self.coordZList = []
		self.colorNumList = []
		tempCoordinates = list( coordinates )
		coordList1 = random.sample( tempCoordinates, self.count1 )
		for coord in coordList1:
			if coord in tempCoordinates:
				tempCoordinates.remove(coord)
		coordList2 = random.sample( tempCoordinates, self.count2 )
		for coord in coordList2:
			if coord in tempCoordinates:
				tempCoordinates.remove(coord)
		coordList3 = random.sample( tempCoordinates, self.count3 )

		i = 0
		for coord in coordinates:
			posStr = Functions.vector3TypeConvert( coord )
			self.spiritCrystalPoint[posStr] = i
			self.coordXList.append( int(posStr[2] * 100) )
			self.coordYList.append( int(posStr[0] * 100) )
			self.coordZList.append( int(posStr[1] * 100) )
			if coord in coordList1:
				self.colorNumList.append(1)
			elif coord in coordList2:
				self.colorNumList.append(2)
			else:
				self.colorNumList.append(3)
			i+=1

	def onRefreshSpiritCrystal( self ):
		"""
		初始化刷新灵晶
		"""
		tempCoordinates = list( self.coordinates )
		temp = [tempCoordinates[i:i+20] for i in range(0,len(tempCoordinates),20)]
		self.oneCoordDataList = temp[0]
		self.secondCoordDataList = temp[1]
		self.threeCoordDataList = temp[2]
		self.onRefreshOneSpiritCrystal()

	def onRefreshCrystalBall( self ):
		"""
		随机刷新水晶球
		"""
		crystalCoordList = random.sample( self.crystalCoordList, 20 )
		for posStr in crystalCoordList:
			pos = Functions.vector3TypeConvert( posStr )
			crystalID = random.choice( self.crystalScriptIDList )
			self.createSpellBox( str(crystalID), pos, Math.Vector3(0, 0, 0), {} )

	def onDestroyCrystalBall( self ):
		"""
		销毁场上所有水晶球
		"""
		for crystalID in self.crystalScriptIDList:
			entitylist = self.getEntityMailBoxRecord( str(crystalID) )
			if len(entitylist) == 0: continue
			for entity in list(entitylist):
				if entity:
					entity.destroySelf()

	def onRefreshOneSpiritCrystal( self ):
		"""
		刷第一波
		"""
		if len( self.oneCoordDataList ) <= 0 :
			self.onRefreshSecondSpiritCrystal()
			return
		self.initData( self.oneCoordDataList )
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_refreshSpiritCrystal( self.coordXList, self.coordYList, self.coordZList, self.colorNumList )
		self.onDestroyCrystalBall()
		self.onRefreshCrystalBall()
		self.addTimerCallBack( 30.0, "onRefreshSecondSpiritCrystal", () )

	def onRefreshSecondSpiritCrystal( self ):
		"""
		刷第二波
		"""
		if len(self.secondCoordDataList) <= 0:
			self.onRefreshThreeSpiritCrystal()
			return
		self.initData( self.secondCoordDataList )
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_refreshSpiritCrystal( self.coordXList, self.coordYList, self.coordZList, self.colorNumList )
		self.onDestroyCrystalBall()
		self.onRefreshCrystalBall()
		self.addTimerCallBack( 28.0, "onRefreshThreeSpiritCrystal", () )

	def onRefreshThreeSpiritCrystal( self ):
		"""
		刷第三波
		"""
		if len(self.threeCoordDataList) <= 0:
			self.onRefreshOneSpiritCrystal()
			return
		self.initData( self.threeCoordDataList )
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_refreshSpiritCrystal( self.coordXList, self.coordYList, self.coordZList, self.colorNumList )
		self.onDestroyCrystalBall()
		self.onRefreshCrystalBall()
		self.addTimerCallBack( 26.0, "onRefreshOneSpiritCrystal", () )

	def onRemoveSpiritCrystalNum( self, spiritCrystalNum ):
		"""
		移除掉落的灵晶
		"""
		for coord, num in self.spiritCrystalPoint.items():
			if num == spiritCrystalNum:
				self.spiritCrystalPoint.pop(coord)
				if coord in self.oneCoordDataList:
					self.oneCoordDataList.remove(coord)
				if coord in self.secondCoordDataList:
					self.secondCoordDataList.remove(coord)
				if coord in self.threeCoordDataList:
					self.threeCoordDataList.remove(coord)
				return

	def onSpiritCrystalHitPlayer( self, entityID ):
		"""
		灵晶击中玩家
		"""
		player = KBEngine.entities.get( entityID, None )
		if player:
			player.addBuff( player, self.spiritCrystalHarm )

	def onCrystalHitMonster( self ):
		"""
		水晶球击中怪物
		"""
		entitylist = self.getEntityRecord( self.crystalScriptID )
		if len(entitylist) == 0: return
		entity = KBEngine.entities.get( entitylist[0] )
		if entity:
			for buffID in self.crystalHurtMonster:
				entity.addBuff( entity, buffID )

	def onPlayerTouchCrystal( self, colorNum ):
		"""
		玩家碰撞到灵晶
		"""
		if colorNum == 1:
			self.redCounts += 1
		elif colorNum == 2:
			self.yellowCounts += 1
		else:
			self.blueCounts += 1
		if self.redCounts >= self.crystalCount1 or self.yellowCounts >= self.crystalCount2 or self.blueCounts >= self.crystalCount3:
			self.getScript().onConditionChange( self, "", self.id, "AGOAL", "" )
		if self.redCounts >= self.crystalCount1 and self.yellowCounts >= self.crystalCount2 and self.blueCounts >= self.crystalCount3:
			self.getScript().onConditionChange( self, "", self.id, "COMPLETE", "" )
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_NotifyAccordToCount( self.addCount )
				player.client.CLIENT_NotifyPlayerAddCount( colorNum, self.addCount, True )		

	# def moveToSpiritCrystalPos( self, position ):
	# 	"""
	# 	移动
	# 	"""
	# 	entitylist = self.getEntityRecord( self.crystalScriptID )
	# 	if len(entitylist) == 0: return
	# 	entity = KBEngine.entities.get( entitylist[0] )
	# 	if entity:
	# 		if entity.touchCount < 5:
	# 			entity.startMovePos(KBEMath.Unreal2KBEnginePosition(position))
				
	# def moveToSpiritCrystalSkyPos( self ):
	# 	"""
	# 	移动
	# 	"""
	# 	entitylist = self.getEntityRecord( self.crystalScriptID )
	# 	if len(entitylist) == 0: return
	# 	entity = KBEngine.entities.get( entitylist[0] )
	# 	if entity:
	# 		entity.stopMovingForType( csdefine.MOVE_TYPE_MOVE_POINT )
			
	def onMonsterTouchCrystal( self, colorNum ):
		"""
		怪物碰撞到灵晶
		"""
		entitylist = self.getEntityRecord( self.crystalScriptID )
		if len(entitylist) == 0: return
		entity = KBEngine.entities.get( entitylist[0] )
		if entity:
			if entity.touchCount >= 5:
				return
			entity.touchCount += 1
			if colorNum == 1:
				self.getScript().onConditionChange( self, "", self.id, "MonsterRed", "" )
				entity.redCount +=1
			elif colorNum == 2:
				self.getScript().onConditionChange( self, "", self.id, "MonsterYellow", "" )
				entity.yellowCount += 1
			else:
				self.getScript().onConditionChange( self, "", self.id, "MonsterBlue", "" )
				entity.blueCount += 1
			for player in self._spaceRoles:
				if player.getClient():
					player.client.CLIENT_NotifyMonsterToCount(entity.id, entity.touchCount)
					player.client.CLIENT_NotifyMonsterAddCount( colorNum, self.addCount, True )
			if entity.touchCount > 4:
				if entity.redCount == entity.yellowCount or entity.redCount == entity.blueCount or entity.yellowCount == entity.blueCount:
					eventID = random.choice( self.randomList )
					self.onTriggerEvent( eventID )
				else:
					if entity.redCount > entity.yellowCount:
						maxNum = entity.redCount
						eventID = 1
					else:
						maxNum = entity.yellowCount
						eventID = 2
					if maxNum < entity.blueCount:
						eventID = 3
					self.onTriggerEvent( eventID )

	def onTriggerEvent( self, eventID ):
		"""
		根据事件ID触发不同效果
		"""
		entitylist = self.getEntityRecord( self.crystalScriptID )
		if len(entitylist) == 0: return
		entity = KBEngine.entities.get( entitylist[0] )
		if not entity: return
		
		if eventID == 1:
			entity.useSkillToEntity( self.upSkillID, entity.id )
			self.getScript().onConditionChange( self, "", self.id, "Red", "" )
		elif eventID == 2 and self._spaceRoles[0].getClient():
			self._spaceRoles[0].client.CLIENT_NotifyCrystalPlayLight( self.distance )
			self.getScript().onConditionChange( self, "", self.id, "Yellow", "" )
		elif eventID == 3:
			self.getScript().onConditionChange( self, "", self.id, "Bule", "" )
		entity.chaseEntity( self._spaceRoles[0], 1.0 )
		FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, self._spaceRoles[0])

	def onLocationBrushStrange( self, colorNum, position ):
		"""
		在指定位置刷怪
		"""
		if len(self.monsterScriptID) < 3:
			return
		if colorNum == 1:
			monsterScriptID = self.monsterScriptID[0]
		elif colorNum == 2:
			monsterScriptID = self.monsterScriptID[1]
		else:
			monsterScriptID = self.monsterScriptID[2]
		self.createEntityByScriptID( monsterScriptID, KBEMath.Unreal2KBEnginePosition(position), Math.Vector3(0,0,0), {} )