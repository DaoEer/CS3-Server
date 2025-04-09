# -*- coding: utf-8 -*-

import KST
import Functions
import csdefine
import csstatus

class RoleEquipInterface:
	def __init__( self ):
		pass
		
	def BASE_remoteQueryTargetEquipInfo( self, targetName ):
		"""
		远程查询目标装备信息
		exposed method
		"""
		KST.g_baseAppEntity.lookupRoleBaseByName( targetName, self.remoteQuestyTargetEquipInfoCB )

	def remoteQuestyTargetEquipInfoCB( self,target ):
		"""
		远程查询目标装备回调
		"""
		if target is None:
			self.statusMessage( csstatus.TEAM_NOT_FIND_INVITER, "" )
			return
		target.cell.onQueryEquipInfo( self.cell )
		
