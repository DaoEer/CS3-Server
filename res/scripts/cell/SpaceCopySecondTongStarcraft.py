# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import Const

class SpaceCopySecondTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第二场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.camp = self.createArgs["camp"]

	def addIntegral( self, role, value ):
		"""
		增加积分
		"""
		hasBuff = False
		#找到是否拥有某buffID 来增加积分
		for buffID in Const.TONG_STARCRAFT_DOUBLE_INTEGRAL_BUFF:
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
			member.setIsCanFight( False )
			role.addBuff(role,Const.TONG_STARCRAFT_WATCH_BUFF)
			return
		self.warInfos.reduceIntegral( role.tongDBID, role.playerDBID, value )
