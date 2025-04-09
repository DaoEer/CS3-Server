# -*- coding: utf-8 -*-
import Math
import KST
import KBEngine
import KBEDebug
import KST_Config
from Monster import Monster
class MonsterFollowRole(Monster):
	"""
	"""
	def __init__(self):
		Monster.__init__(self)
		self.isSetControlledBy = False
		
		self.callbackID = 0
		self.controllerID = 0
		self.roleLastPos = None
		self.nextMovePos = None
		
	def onEnterWorld( self ):
		"""
		"""
		flag = False
		if not self.isSetControlledBy:
			lst = [(r[0].clientapp.id, r[0].id) for r in KST.roles.values()]
			for l in lst:
				if self.clientapp.id == l[0] and self.controlEntityID == l[1]:
					self.isSetControlledBy = True
					self.cell.CELL_onSetControlledBy()
					flag = True
					
					if not KST_Config.follow_auto_sync_server:
						player = self.clientapp.entities.get(self.controlEntityID)
						player.eventObj.fireEvent("Event_OnControlMonster", self.id)						
					break
		
		if not flag: return
		if not self.callbackID:
			self.callbackID = KBEngine.callback(0.5, self.onCallBack)
		
	def onLeaveWorld( self ):
		"""
		"""
		if self.callbackID:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
		
		if self.controllerID:
			self.cancelController(self.controllerID)
			self.controllerID = 0
		
	def onCallBack(self):
		"""
		"""
		self.callbackID = KBEngine.callback(0.5, self.onCallBack)
		
		role  = None
		for r in KST.roles.values():
			if r[0].id == self.controlEntityID:
				role = r[0]
				break
			
		if role is None: 
			return
		
		if self.roleLastPos is None: 
			self.roleLastPos = Math.Vector3(role.position.x, role.position.y, role.position.z)
		if self.nextMovePos is None: 
			self.nextMovePos = Math.Vector3(self.position.x, self.position.y, self.position.z)
		
		if (role.position - self.roleLastPos).length >= 1:
			self.nextMovePos += role.position - self.roleLastPos
			self.roleLastPos = Math.Vector3(role.position.x, role.position.y, role.position.z)
		
		if (self.nextMovePos - self.position).length >= 1:
			self.controllerID = self.moveToPoint(self.nextMovePos, self.moveSpeed, 0.0, 0, True, True)
			
	def onMoveOver( self, controllerID, userData ):
		"""
		"""
		self.controllerID = 0
	
	def onMoverFailure( self, controllerID, userData ):
		"""
		"""
		self.controllerID = 0
	
		if (self.nextMovePos - self.position).length >= 1:
			self.controllerID = self.moveToPoint(self.nextMovePos, self.moveSpeed, 0.0, 0, True, True)
	def CLIENT_syncPosAndDir( self, position, direction ):
		"""
		"""
		pass
