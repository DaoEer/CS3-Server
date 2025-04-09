# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine
import csstatus

class SpaceCopySanYuanJingZhu( SpaceCopy ):
	"""
	三源镜柱副本
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self._monsterData = {}
		self._mirrorID = 0
		self._prismID = 0
		self._buffID = 0
		self._effectID = []
		self._score = 0
		self.timerID1 = 0 #停掉计时器
		self.timerID2 = 0 #停掉计时器

	def initSpaceData( self, monsterData ):
		""""""
		self._monsterData = monsterData

	def getData( self, data ):
		"""
		数据解析
		"""
		if data["effectID"]:
			self._effectID = data["effectID"].split("|")
		if data["buffID"]:
			self._buffID = data["buffID"]
		if data["angularVelocity"]:
			self.angularVelocity = data["angularVelocity"]

	def onStartRotatSource( self, selfEntity, scriptID ):
		"""
		开始转动图腾
		"""
		if scriptID in self._monsterData:
			for key, value in self._monsterData[scriptID].items():
				entity = self.getObtainEntity( scriptID )
				if type(value) == dict:
					self.getData( value )
					for mirrorID, prismID in value:
						if self._mirrorID != mirrorID:
							mirrorEntity = self.getObtainEntity( mirrorID )
							prismEntity = self.getObtainEntity( prismID )
							entity.allClients.CLIENT_SimulationCircle( self.angularVelocity, mirrorEntity.id )
							entity.addBuff( mirrorEntity, self._buffID )
							mirrorEntity.addBuff( prismEntity, self._buffID)
							self._mirrorID = mirrorID
							self._prismID = prismID
							break
						else:
							continue
				else:
					if self.totemKey == 3:
						self.totemKey = 0
					if self._prismID == scriptID:
						totemEntity = self.getObtainEntity( self._monsterData[scriptID][totemKey] )
						prismEntity = self.getObtainEntity( self.prismID )
						prismEntity.allClients.CLIENT_SimulationCircle( self.angularVelocity, totemEntity.id )
						prismEntity.addBuff( totemEntity, self._buffID )
						self.totemKey += 1
						self.onConsistentTotem( int(self._effectID[0]) )

	def getObtainEntity( self, scriptID ):
		"""
		获取entity
		"""
		idList = self.getEntityRecord( scriptID )
		if len(idList) <= 0:
			return
		entity = KBEngine.entities.get( idList[0], None )
		return entity

	def onConsistentTotem( self, effectID ):
		"""
		是否投射成功
		"""
		for key, value in self.totemDict:
			if value == effectID:
				self._score += 1
				self.spaceEvent_addCount( self, "SYZJ_score", self._score )
				self.getScript().onConditionChange( self, "", "", "SYJZ", "" )
				self.popTimer( self.timerID1 )
				self.popTimer( self.timerID2 )
				for player in self._spaceRoles:
					player.client.CLIENT_NotifyClientStopEffect( effectID )
			else:
				self.timerID1 = self.addTimerCallBack( 10, "onExplosionEnergy", (int(self._effectID[1])) )
				self.timerID2 = self.addTimerCallBack( 20, "onProjectionFailure", (int(self._effectID[1])) )

	def onProjectionFailure( self, effectID ):
		"""
		投射失败
		"""
		self.getScript().onConditionChange( self, "", "", "FAILURE", "" )
		for key, value in self.totemDict:
			theTrue = KBEngine.entities.get( key )
			for player in self._spaceRoles:
				player.client.CLIENT_NotifyClientStopEffect( value )
				theTrue.allClients.CLIENT_OnPlayParticles( theTrue.id, effectID,"", 1.0,Math.Vector3(0,0,0) )

	def onExplosionEnergy( self, effectID ):
		"""
		能量爆炸
		"""
		for key, value in self.totemDict:
			theTrue = KBEngine.entities.get( key )
			theTrue.allClients.CLIENT_OnPlayParticles( theTrue.id, effectID,"", 1.0,Math.Vector3(0,0,0) )


