# -*- coding: utf-8 -*-
import KBEngine
class RoleRelationInterface:
	
	def __init__(self):
		pass
		
	def relation_initRelationCatalog(self, params):
		pass
		
	def relation_finishSendCatalog(self):
		pass
		
	def relation_sendRelationData(self, UID, playerName, remarkName, myRelationStatus, profession, level, callResult):
		pass
		
	def relation_onNoticePlayerLogin(self, params):
		pass
		
	def relation_onNoticePlayerLogout(self, params):
		pass
		
	def relation_addFriendRelation(self, params):
		pass
	
	def relation_addFriendRelationData(self, u1, u2, i1, i2):
		pass
		
	def relation_removeFriend(self, params):
		pass
		
	def relation_addFoeRelation(self, params):
		pass
		
	def relation_removeFoe(self, params):
		pass
		
	def relation_addBlacklistRelation(self, params):
		pass
		
	def relation_removeBlackList(self, params):
		pass
		
	def relation_addRecentContacts(self,params):
		pass
		
	def relation_addRecentContactsDatas(self,uid,playerName,param1,relationStatus,profession, level, camp, param2):
		pass
		
	def relation_removeRecentContacts(self, param):
		pass
		
	def relation_receiverGroup(self, groupID, groupName, endTime, createrName):
		pass
		
	def relation_receiverGroupInfo(self, groupID, playerName, profession, level, isMB):
		pass
		
	def relation_onNoticePlayerOnLine(self, uid, name, level):
		pass
		
	def relation_onPlayerOffLine(self, uid, name):
		pass
		
	def relation_beInvitedToGroup(self, playerName, groupName):
		pass
		
	def relation_onPlayerRemoveGroup(self, uid, groupName):
		pass
		
	def relation_onDelectGroup(self, uid):
		pass
	
	def relation_changeGroupLeater( self, uniStr1, uniStr2 ):
		ass
	
	def relation_addEndTime( self, uniStr, timeStr ):
		pass
	
	def relation_addGroupBlackList( self, uniStr1, uniStr2 ):
		pass
	
	def relation_delGroupBlackList( self, uniStr1, uniStr2 ):
		pass
	
	def relation_recommendGroup( self, uniStr1 ):
		pass
	
	def OpenGroupPassWordWidget( self, uniStr1, uniStr2 ):
		pass
	
	def relation_updateGroupInfo( self, uniStr1, uniStr2, int, uniStr3 ):
		pass
	def OnSetRelationNotice( self, p1 ):
		pass
	def relation_requestPlayerInfo( self, p1, p2, p3, p4 ):
		pass
	def relation_delRelationCatalog( self, p1 ):
		pass
	def relation_addRelationCatalog( self, p1, p2 ):
		pass
	def OnInitRelationDataCompleted( self ):
		pass
	def coverInvitedToFriend( self, p1 ):
		pass
	def relation_moveToOtherCatalog( self, p1, p2, p3 ):
		pass
	def BeInvitedtoFriend( self, p1, p2 ):
		pass
	def ReceiveInviteToFriend( self, p1, p2 ):
		pass
