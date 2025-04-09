# -*- coding: utf-8 -*-

import KST
import csdefine
import KBEngine
import KBEDebug
import CoreInterface.RoleLBCTaskInterface as RoleLBCTaskInterface
import CoreInterface.RoleQuestInterface as RoleQuestInterface
import ImpInterface.RoleLunHuiMiJinInterface as RoleLunHuiMiJinInterface
import CoreInterface.RoleSpaceContentInterface as RoleSpaceContentInterface
import ImpInterface.RoleGiftInterface as RoleGiftInterface
import ImpInterface.RoleWorkShopInterface as RoleWorkShopInterface

class RoleFixedUpdateInterface:
	def __init__( self ):
		pass
	
	def fixedTimeUpdate(self, fixedTimeType, token):
		KBEDebug.DEBUG_MSG("role[%d:%d] fixedTimeUpdate, %d, %s" %(self.playerDBID, self.id, fixedTimeType, token))
		self._onFixedTimeUpdate(fixedTimeType, token)
		
	def _onFixedTimeUpdate(self, fixedTimeType, token):
		"""
		""" 
		#0点更新
		if fixedTimeType == csdefine.FIXED_UPDATE_TOKEN_ZERO:
			RoleLBCTaskInterface.RoleLBCTaskInterface.onFixedTimeZero(self)
			RoleQuestInterface.RoleQuestInterface.onNewDayLogin( self )
			RoleLunHuiMiJinInterface.RoleLunHuiMiJinInterface.onNewDayLogin( self )
			RoleGiftInterface.RoleGiftInterface.onNewDayLogin( self )
			RoleWorkShopInterface.RoleWorkShopInterface.onNewDayLogin( self )
			self.onNewDayLogin()
		#5点更新
		elif fixedTimeType == csdefine.FIXED_UPDATE_TOKEN_FIVE:
			RoleSpaceContentInterface.RoleSpaceContentInterface.onFixedTimeUpdate(self, fixedTimeType, token)
	
