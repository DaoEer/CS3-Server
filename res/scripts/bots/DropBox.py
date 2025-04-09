# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import NPCBaseObject
class DropBox(
	KBEngine.Entity,
	NPCBaseObject,
	):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		NPCBaseObject.__init__(self)
		
	def FPickup_GetItemInfoList(self, infoStream):
		pass
		
	def FPickup_GetItemNum(self, account):
		pass
		
	def FPickup_GetRollItemList( self, rollItemUIDs ):
		pass
		
	def ClearItemInfoList(self):
		pass
		
	def receiverRollRemainTime( self, rollRemainTime ):
		pass
		
	def receiverRollResult(self, uid, a, b):
		pass
		
	def pickUpToMember( self, uid, ownershipIDs ):
		pass
		
	def isCanPickUp(self, canPickup):
		pass
	def updateDropBoxModelVisible( self ):
		pass
	def OnIsDisplayInMiniMap( self ):
		pass
