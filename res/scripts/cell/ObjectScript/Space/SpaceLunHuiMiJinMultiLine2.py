# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceMultiLine import SpaceMultiLine
import Const
import KBEngine
import csdefine
import csstatus

class SpaceLunHuiMiJinMultiLine2( SpaceMultiLine ):
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		
	def checkEnterEnable( self, player, params ):
		"""
		virtual method
		检测进入条件
		"""
		result = SpaceMultiLine.checkEnterEnable(self, player, params)
		if result != csstatus.SPACE_ENTER_OR_LEAVE_OK:
			return result
		
		#如果当前地图没有开放
		#key = csdefine.CONTROL_SPACE_KEY + self.scriptID
		#openStatus = KBEngine.globalData.get(key, False)
		#if not openStatus:
		#	return csstatus.LHMJ_CAN_NOT_ENTER
			
		return csstatus.SPACE_ENTER_OR_LEAVE_OK
		

	
		
		
		