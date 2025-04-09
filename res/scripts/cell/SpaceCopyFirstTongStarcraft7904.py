# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import Const

class SpaceCopyFirstTongStarcraft7904( SpaceCopy ):
	"""
	帮会争霸 第二场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.camp = self.createArgs["camp"]
		self.bossDamageDict = {}
		self.recordFirstHurtBossEntityID = []

	def addIntegral( self, role, value ):
		"""
		增加积分
		"""
		hasBuff = False
		#找到是否拥有某buffID 来增加积分
		for buffID in self.getScript().getDoubleAddIntegralBuffs():
			buffList = role.findBuffsByBuffID(buffID)
			if len(buffList) > 0:
				hasBuff = True
		if hasBuff:
			value = value * 2
		self.warInfos.addIntegral( role.tongDBID,role.playerDBID, value)

	def reduceIntegral( self, role, value ):
		"""
		减少积分
		"""
		member = self.warInfos.getMember( role.tongDBID, role.playerDBID )
		if not member:
			return
		playerCurIntegral = member.getIntegral(role)
		if playerCurIntegral == 0:
			# member.setIsCanFight( False )
			# role.addBuff(role,Const.TONG_STARCRAFT_WATCH_BUFF)
			return
		self.warInfos.reduceIntegral( role.tongDBID, role.playerDBID, value )

	def getMemberIntegral( self, role ):
		"""
		获得成员的积分
		"""
		return self.warInfos.getMemberIntegral( role.tongDBID, role.playerDBID )

	def addBossDamageData( self, bossEntityID, damageList ):
		"""
		增加Boss受到伤害的数据
		"""
		self.bossDamageDict[bossEntityID] = damageList

	def getBossDamageList( self, bossEntityID ):
		"""
		"""
		return self.bossDamageDict.get(bossEntityID,{})

	def addRecordFirstHurtBossEntityID( self, bossEntityID ):
		"""
		增加已经受到第一次伤害的Boss
		"""
		self.recordFirstHurtBossEntityID.append( bossEntityID )

	def isBossAlreadyFirstHurt( self, bossEntityID ):
		"""
		是否Boss收到第一次的伤害
		"""
		if bossEntityID in self.recordFirstHurtBossEntityID:
			return True
		return False
