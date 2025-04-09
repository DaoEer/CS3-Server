# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
class RoleTeamInterface:
	def __init__(self):
		self.teamID = 0
		self.captainID = 0
		self.teamMembers = {}
		
	def addTeamMember( self, dbid, entityID, name, profession, isOnLine, level ):
		#记录队伍成员数据
		self.teamMembers[dbid] = {"dbid" : dbid, "entityID" : entityID}
		
	def TeamInviteByTeammate( self, targetID, targetName, camp, profession, level, inviteName, inviteID ):
		#某人向我（队长）请求邀请某人组队
		self.eventObj.fireEvent("Event_CTeamAISys_onInviteTeammate", targetID, targetName, inviteID)
		
	def OnTeamInviteBy( self, p1, p2, p3, p4, p5 ):
		self.eventObj.fireEvent("Event_CTeamAISys_onTeamInvite", p1)
		
	def teamInfoNotifyOnJoin( self, captainID, teamEntityid, p3, p4, p5, p6, p7 ):
		self.teamID = teamEntityid
		self.captainID = captainID
		self.eventObj.fireEvent("Event_CTeamAISys_onJoinTeam")
		
	def leaveTeamNotify( self, entityID, disemploy ):
		#要离队的是自己
		if entityID == self.id:
			self.teamID = 0
			self.captainID = 0
			self.teamMembers = {}
			self.eventObj.fireEvent("Event_CTeamAISys_onLeaveTeam")
		else:
			for k,v in self.teamMembers.items():
				if v["entityID"] == entityID:
					self.teamMembers.pop(k)
					break
		
	def disbandTeamNotify( self ):
		self.teamID = 0
		self.captainID = 0
		self.teamMembers = {}
		self.eventObj.fireEvent("Event_CTeamAISys_onLeaveTeam")
		
	def changeCaptainNotify( self, entityID ):
		self.captainID = entityID
		
	def logoutNotify( self, p1 ):
		pass
	def onRejoinTeam( self, p1, p2 ):
		pass
	def teammateInfoNotify( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def OnReceiveJoinTeamRequest( self, p1, p2, p3, p4, p5 ):
		pass
	def onSendTeamMSG( self, p1 ):
		pass
	def modifyAllocation( self, p1 ):
		pass
	def modifyQuality( self, p1 ):
		pass
	def OnTeamMemberAddBuff( self, p1, p2, p3, p4, p5 ):
		pass
	def OnTeamMemberRemoveBuff( self, p1, p2 ):
		pass
	def OnTeamMemberResetBuffTime( self, p1, p2, p3 ):
		pass
	def AddTeamSignCB( self, p1, p2 ):
		pass
	def StartTeamFollow( self, p1 ):
		pass
	def StopTeamFollow( self ):
		pass
	def FollowNewCaptain( self, p1 ):
		pass
	def StartNormalFollow( self, p1 ):
		pass
	def StopNormalFollow( self ):
		pass
	def RoleTeamSpellBoxFollow( self, p1, p2 ):
		pass
	def onMemberShareBigMapCustomMarker( self, p1, p2, p3, p4 ):
		pass
	def RemoveTeamSigner( self, p1 ):
		pass
	def CLIENT_OnRemoveInvitedArr( self, p1 ):
		pass
	def CLIENT_OnRemoveRequestArr( self, p1 ):
		pass
	def CLIENT_OnUpdateMemeberPos( self, p1 ):
		pass
	def CLIENT_notifyClientFastTeamSignUp( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_notifyClientFastTeamCancelSignUp( self ):
		pass
	def CLIENT_teamByApply( self ):
		pass
	def CLIENT_onTeamAssembled( self, p1, p2 ):
		pass
	def CLIENT_OnStartTeamSearch( self ):
		pass
	def CLIENT_OnFastTeamCancelMatch( self ):
		pass
	def CLIENT_OpenFastTeamWin( self, p1, p2, p3 ):
		pass
	def CLIENT_OnSetTeamSearchTime( self, p1 ):
		pass
	def FastTeamOnMatchSuccess( self ):
		pass
