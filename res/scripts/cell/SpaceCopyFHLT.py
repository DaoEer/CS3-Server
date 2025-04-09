# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import math
import KBEngine
import csdefine
import csstatus
import Const
import time
import KBEMath
import Functions

class SpaceCopyFHLT( SpaceCopy ):
	"""
	烽火连天
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self._pointTimer = {}
		self._taosimIntegral = 0			# 仙道积分
		self._demonIntegral = 0				# 魔道积分
		self._taosimMaterialNum = 0			# 仙道资材分
		self._demonMaterialNum = 0			# 魔道资材分

	def onEnter( self, playerRole, packArgs ):
		""""""
		SpaceCopy.onEnter( self, playerRole, packArgs )
		self.memberDatas.add( playerRole, playerRole.id, playerRole.getName(), playerRole.camp )
		if playerRole.isInTeam():
			playerRole.leaveTeamFC( playerRole.id, playerRole.id )
		
	def onLeave( self,  playerRole, packArgs ):
		""""""
		SpaceCopy.onLeave( self, playerRole, packArgs )
		self.memberDatas.remove( playerRole.id )

	def activityEnd( self ):
		"""
		define method
		活动结束
		"""
		if self._taosimIntegral > self._demonIntegral:
			self.winGame( csdefine.CAMP_TAOSIM )
		else:
			self.winGame( csdefine.CAMP_DEMON )

	def onMemberKillPlayer( self, killer ):
		"""杀人添加积分"""
		if killer.camp == csdefine.CAMP_TAOSIM:
			self.addTaosimIntegral( 2 )
		else:
			self.addDemonIntegral( 2 )

	def addTaosimIntegral( self, integral ):
		"""
		添加/减少仙道积分
		"""
		self._taosimIntegral += integral
		for player in self._spaceRoles:
			player.client.OnIntegralChange( self._taosimIntegral, self._demonIntegral )
		if self._taosimIntegral >= Const.FHLT_INTEGRAL_WINNER:
			self.winGame( csdefine.CAMP_TAOSIM )
		
	def addDemonIntegral( self, integral ):
		"""
		添加/减少魔道积分
		"""
		self._demonIntegral += integral
		for player in self._spaceRoles:
			player.client.OnIntegralChange( self._taosimIntegral, self._demonIntegral )
		if self._demonIntegral >= Const.FHLT_INTEGRAL_WINNER:
			self.winGame( csdefine.CAMP_DEMON )

	def transferIntegral( self, camp, integralRatio ):
		"""
		转移积分
		"""
		integral = int( math.floor( self._taosimIntegral * integralRatio ) )
		if camp == csdefine.CAMP_TAOSIM:
			self.addTaosimIntegral( -integral )
			self.addDemonIntegral( integral )
		else:
			self.addTaosimIntegral( integral )
			self.addDemonIntegral( -integral )

	def addMaterialPoints( self, camp ):
		"""
		增加资材分
		"""
		if camp == csdefine.CAMP_TAOSIM:
			self._taosimMaterialNum += 1
		else:
			self._demonMaterialNum += 1

		if self._taosimMaterialNum - self.getScript()._materialPointNum >= 0:
			self.onCallVanMonster( csdefine.CAMP_TAOSIM )
		if self._demonMaterialNum - self.getScript()._materialPointNum >= 0:
			self.onCallVanMonster( csdefine.CAMP_DEMON )

	def onCallVanMonster( self, camp ):
		"""
		召唤先锋
		"""
		if camp == csdefine.CAMP_TAOSIM:
			for index, xianVanMonster in enumerate( self.getScript()._xianVanMonsterList ):
				if len( self.getEntityRecord( xianVanMonster )) == 0 and self._taosimMaterialNum - self.getScript()._materialPointNum >= 0:
					pos = KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( self.getScript()._xianVanPosList[index] ) )
					dir = KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( self.getScript()._xianVanDirList[index] ) )
					self.createEntityByScriptID( xianVanMonster, pos, dir, { "spawnPos": pos, "spawnDir": dir } )
					self._taosimMaterialNum -= self.getScript()._materialPointNum
		else:
			for index, moVanMonster in enumerate( self.getScript()._moVanMonsterList):
				if len( self.getEntityRecord( moVanMonster )) == 0 and self._demonMaterialNum - self.getScript()._materialPointNum >= 0:
					pos = KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( self.getScript()._moVanPosList[index] ) )
					dir = KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( self.getScript()._moVanDirList[index] ) )
					self.createEntityByScriptID( moVanMonster, pos, dir, { "spawnPos": pos, "spawnDir": dir } )
					self._demonMaterialNum -= self.getScript()._materialPointNum
		
	def occupyWarFlag( self, camp ):
		"""
		占领战旗
		"""
		if camp in self._pointTimer:
			self.popTimer( self._pointTimer[camp] )
		timer = self.addTimerRepeat( 1.0, "addIntegral", (camp,))
		self._pointTimer[camp] = timer

	def addIntegral( self, camp ):
		"""增加积分"""
		if camp == csdefine.CAMP_TAOSIM:
			self.addTaosimIntegral( 2 )
		elif camp == csdefine.CAMP_DEMON:
			self.addDemonIntegral( 2 )

	def winGame( self, camp ):
		"""获胜"""
		for memberData in self.memberDatas.values():
			if memberData["camp"] == camp:
				g_mailContentDataLoader.sendActivityReward( self.scriptID, 1, memberData["name"] )
			else:
				g_mailContentDataLoader.sendActivityReward( self.scriptID, 2, memberData["name"] )
		for timer in self._pointTimer.values():
			self.popTimer(timer)
		self._pointTimer.clear()
		for player in self._spaceRoles:
			player.client.OnWinGameFHLT( camp, self._taosimIntegral, self._demonIntegral )
		self.addTimerCallBack( 30, "closeSpace", () )