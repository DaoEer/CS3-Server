# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyRingTask import SpaceCopyRingTask
import KBEngine
import csdefine
import KBEMath
import Functions
import csconst

class SpaceCopyXuanTianBaoLu( SpaceCopyRingTask ):
	"""
	玄天宝录副本
	"""	
	def __init__( self ) :
		SpaceCopyRingTask.__init__( self )
		self.allEntityList = []
		self.allInSunEntityList = []	#当前在阳关中的entity

	def initSpaceData( self, stoneScriptID, stoneBurstNum, outBreakBuff, intervalTime, mirrorId, turnSpeed, petrifyBuff ):
		"""
		初始化数据
		"""	
		self.stoneScriptID = stoneScriptID		# 石像的scriptID
		self.stoneBurstNum = int(stoneBurstNum)	# 石像爆发的个数
		self.outBreakBuff = outBreakBuff		# 爆发妖气Buff
		self.intervalTime = float(intervalTime) # 间隔时间
		self.mirrorId = mirrorId				# 大日宝镜的SpellboxScriptID
		self.turnSpeed = turnSpeed				# 旋转速度
		self.petrifyBuff = petrifyBuff			# 石化Buff

	def onTeleportCompleted( self, playerRole ):
		SpaceCopyRingTask.onTeleportCompleted( self, playerRole )
		self.getStochasticStone()

	def getStochasticStone( self ):
		"""
		获取副本内所有的石像
		"""
		for _scriptID in self.stoneScriptID:
			entitylist = self.getEntityRecord( _scriptID )
			if len(entitylist) == 0: continue
			for entityID in entitylist:
				self.entitylist.append( entityID )

	def initStochasticStoneCritical( self, stoneNum, nextRiotTime ):
		"""
		随机若干个石像开始颤动并爆发出妖气
		"""
		if len(self.entitylist) < stoneNum:
			randomEntityList = list(self.entitylist)
		else:
			randomEntityList = random.sample( list(self.entitylist), stoneNum )
		self.outBreakEvilSpirits( randomEntityList )
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_NotifyNextRiotTime( str(nextRiotTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()) )

	def outBreakEvilSpirits( self, entitylist ):
		"""
		开始爆发妖气
		"""
		for stoneID in entitylist:
			entity = KBEngine.entities.get( stoneID )
			if not entity:
				continue
			entity.monsterAISendCommand( entity.id, "selection" )
			self.allEntityList.append( entity.id )
			self.entitylist.remove( entity.id )
		self.checkTimeID = self.addTimerRepeat( 0.5, "checkStoneSolidify", () )

	def checkStoneSolidify( self ):
		"""
		检查爆发石像是否被抑制
		"""
		if len(self.allEntityList) <= 0:
			for player in self._spaceRoles:
				if player.getClient():
					player.client.CLIENT_NotifyStopNextExplosionTime()
			if self.checkTimeID:
				self.popTimer( self.checkTimeID )
				self.checkTimeID = 0
		for stoneID in list(self.allEntityList):
			entity = KBEngine.entities.get( stoneID )
			if not entity:
				continue
			if len( entity.findBuffsByBuffID( int(self.petrifyBuff) ) ) <= 0:
				self.allEntityList.remove( entity.id )
				
	def onStoneInSunShone( self, entityID ):
		"""
		怪物石像在日光中
		"""
		if entityID not in self.allInSunEntityList:
			self.allInSunEntityList.append(entityID)
		self.checkStoneControl(entityID)

	def checkStoneControl( self, entityID ):
		"""
		检查石像是否被抑制
		"""
		entity = KBEngine.entities.get( entityID, None )
		if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			return
		
		if len( entity.findBuffsByBuffID( int(self.outBreakBuff) ) ) > 0:
			entity.monsterAISendCommand( entity.id, "StopBreak" )
			if entityID in self.allEntityList:
				self.allEntityList.remove( entityID )
		if entityID in self.entitylist:
			self.entitylist.remove( entityID )
			
	def onStoneOutSunShone( self, entityID ):
		"""
		怪物石像不在日光中
		"""
		if entityID in self.allInSunEntityList:
			self.allInSunEntityList.remove(entityID)
		self.checkSolidify(entityID)

	def checkSolidify( self, entityID ):
		"""
		"""
		entity = KBEngine.entities.get( entityID, None )
		if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			return
		
		#没有爆发妖气BUFF但是有石化BUFF
		if len( entity.findBuffsByBuffID( int(self.outBreakBuff) ) ) <= 0:
			if len( entity.findBuffsByBuffID( int(self.petrifyBuff) ) ) > 0:
				if entityID not in self.entitylist:
					if entityID not in self.allInSunEntityList:
						self.entitylist.append( entityID )
		
	def onStartTurnMirror( self ):
		"""
		玩家开始交互（转动大日宝镜或反射镜）
		"""
		entitylist = self.getEntityRecord( self.mirrorId )
		if len(entitylist) == 0: return
		entity = KBEngine.entities.get( entitylist[0], None )
		if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_SPELL:
			return
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_OnRotationAngleRange( KBEMath.KBEngine2UnrealPosition(entity.position), self.turnSpeed )
				
	def onStopStochasticStoneCritical( self ):
		"""
		停止爆发妖气，并且正在爆发妖气的也移除
		"""
		if self.randomTimeID:
			self.popTimer( self.randomTimeID )
			self.randomTimeID = 0
		if self.checkTimeID:
			self.popTimer( self.checkTimeID )
			self.checkTimeID = 0
		if len(self.allEntityList) < 0: return
		for stoneID in list(self.allEntityList):
			entity = KBEngine.entities.get( stoneID )
			if not entity:
				continue
			if len( entity.findBuffsByBuffID( int(self.outBreakBuff) ) ) > 0:
				entity.monsterAISendCommand( entity.id, "StopBreak" )
				self.allEntityList.remove( entity.id )
