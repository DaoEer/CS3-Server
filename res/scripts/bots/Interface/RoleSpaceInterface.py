from Interface.RoleSpaceEffectInterface import RoleSpaceEffectInterface
# -*- coding: utf-8 -*-
class RoleSpaceInterface(
	RoleSpaceEffectInterface,
	):
	def __init__(self):
		RoleSpaceEffectInterface.__init__(self)
	def OnLoginSpaceNotify( self, p1, p2 ):
		pass
		
	def OnEnterSpaceNotify(self, str, int ):
		#进入地图
		self.outputMsg("OnEnterSpaceNotify: spaceScriptID %s"% self.spaceScriptID )
		self.clearStates()
		#self.behOver()
		
	def OnEnterAreaNotify(self):
		#同地图传送
		self.outputMsg("OnEnterAreaNotify: spaceScriptID %s"%self.spaceScriptID )
		self.clearStates()
		#self.behOver()
		
	def OnLeaveSpaceNotify(self):
		self.outputMsg("OnLeaveSpaceNotify: spaceScriptID %s"%self.spaceScriptID )
		
	def GotoSpacePlane(self, scriptID):
		#进入位面
		self.outputMsg("GotoSpacePlane: spaceScriptID %s"%scriptID )
		self.clearStates()
		#self.behOver()
		
	def LeaveSpacePlane(self, scriptID):
		self.outputMsg("LeaveSpacePlane: spaceScriptID %s"%scriptID )
	
	def OnGetSpaceEntityRecordPos( self, p1 ):
		pass
	def UpdateMazeDice( self ):
		pass
	def FlyToSubSpace( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def ShowMazeNum( self, p1 ):
		pass
	def StopFlyToSubSpace( self, p1 ):
		pass
	def ShowMazeDice( self, p1 ):
		pass
	def SeamLessLoadLevel( self ):
		pass
	def ChangeMovementMode( self, p1 ):
		pass
	def SetCanWalkOffLedges( self, p1 ):
		pass
	def CLIENT_RequestGotoLineNumberSpaceFailure( self ):
		pass
	def CLIENT_ArticleToReadNotify( self ):
		pass
	def CLIENT_StartVideoLoading( self ):
		pass
	def OnVideoLoading( self, p1, p2, p3 ):
		pass
	def AgainNotifySpaceData( self, p1 ):
		pass
	def OnNotifyPreloadSpace( self, p1, p2 ):
		pass
