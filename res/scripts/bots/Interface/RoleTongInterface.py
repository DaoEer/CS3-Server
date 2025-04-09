# -*- coding: utf-8 -*-
import json
import KBEDebug
import KBEngine
class RoleTongInterface:
	def __init__(self):
		self.tongLeader = 0
		self.isTongInit = False
		self.tongs = {}
		self.tongMember = {}
		
	def OnTongInitNotity(self):
		self.isTongInit = True
	
	def UpdateTongDatas(self, tongDatas):
		self.isTongInit = True
		info = eval(tongDatas)["ROOT"]
		self.tongLeader = int(info["TongLeader"])
		self.eventObj.fireEvent("Event_CTongAISys_onTongJoin")
		
	def UpdateTongMember(self, tongMemberDatas):
		if self.tongDBID <= 0:
			return
		
		tongMemberDatas = json.loads(tongMemberDatas)
		member = tongMemberDatas["ROOT"]
		self.tongMember[member["DBID"]] = member
	
	def OnReceiveAllTong(self, tongInfos):
		self.tongs = {}
		infos = eval( tongInfos )["ROOT"]
		for info in infos:
			self.tongs[info["TongDBID"]] = info
		self.eventObj.fireEvent("Event_CTongAISys_onReceTongInfos")
		
	def isInSelfTong(self, entityID):
		for dbid, member in self.tongMember.items():
			if member["id"] == entityID:
				return True
		return False
		
	def OnLeaderChange( self, p1 ):
		self.tongLeader = p1
		
	def OnOtherReqJoinTong( self, roleDBID, roleName, level, profession ):
		self.eventObj.fireEvent("Event_CTongAISys_onReqJoinTong", roleDBID)
		
	def OnRequireJoinTong(self, roleDBID, roleName, level, profession ):
		pass
		
	def OnCancelJoinTong( self, roleDBID ):
		pass
		
	def OnSetTitleName( self, titleID, titleName ):
		pass
	
	def OnSetTongTitle( self, targetEntityDBID, titleID ):
		pass
	
	def OnSetGrade(self, int1,int2):
		pass
		
	def OnDonateMoney(self, dbid, name, int1, int2):
		pass
		
	def OnJoinTong( self ):
		pass
		
	def OnLeaveTong(self):
		self.tongDBID = 0
		self.tongLeader = 0
		self.tongMember = {}
		self.eventObj.fireEvent("Event_CTongAISys_onLeaveTong")
		
	def OnKickTongMember(self, dbid1, dbid2):
		if dbid2 == self.playerDBID:
			self.OnLeaveTong()
		else:
			self.tongMember.pop(dbid1, None)
		
	def OnQuitTong(self, dbid):
		if dbid == self.playerDBID:
			self.OnLeaveTong()
		else:
			self.tongMember.pop(dbid, None)
		
	def OnUpgrowTong(self, level):
		pass
		
	def OnUpgrowBuild(self, int1, int2):
		pass
		
	def OnTongMoneyChange(self, int1):
		pass
		
	def OnResearchTongSkill(self, skillID):
		pass
		
	def OnPauseSkill(self, skillID):
		pass
		
	def OnTongSkillProgressChange(self, int1):
		pass
		
	def OnFinishResearchSkill(self, int1):
		pass
		
	def OnTongSign( self ):
		pass
	def OnRequireTongStoreEvent( self, p1 ):
		pass
	def OnSetGradeFailed( self ):
		pass
	def OnRequestJoinList( self, p1, p2, p3, p4 ):
		pass
	def OnSetGag( self, p1, p2 ):
		pass
	def OpenTongStore( self, p1, p2 ):
		pass
	def OnSetTitleNameFailed( self ):
		pass
	def OnRequireTongEvent( self, p1 ):
		pass
	def onDawnArrive( self ):
		pass
	def OnSetRecruitAffiche( self, p1 ):
		pass
	def OnActivityChange( self, p1 ):
		pass
	def OnGetSalaryFail( self ):
		pass
	def OnGrowChange( self, p1 ):
		pass
	def onDonateMoney( self, p1 ):
		pass
	def OnRefuseJoinTong( self, p1, p2 ):
		pass
	def onTongMemberExpChange( self, p1, p2 ):
		pass
	def OnMemberOffline( self, p1, p2, p3, p4 ):
		pass
	def OnSetAffiche( self, p1 ):
		pass
	def OnMemberOnline( self, p1, p2 ):
		pass
	def OnContributionChange( self, p1, p2 ):
		pass
	def OnOtherCancelJoinTong( self, p1 ):
		pass
	def OnInitTongApplyList( self, p1 ):
		pass
	def OnApplyJoinTongFailed( self, p1 ):
		pass
	def OnApplyJoinTongSuccess( self, p1 ):
		pass
	def OnConferenceHallLevelChange( self, p1 ):
		pass
	def UpdateTongMemberInfo( self, p1, p2, p3 ):
		pass
	def OpenTongNagualUI( self ):
		pass
	def OnChangeNagualCB( self, p1 ):
		pass
	def UpdateNagualType( self, p1 ):
		pass
	def OnPauseTongSkill( self, p1 ):
		pass
	def OnFinishLearnSkill( self, p1 ):
		pass
	def CLIENT_UpdateTongMember( self, p1 ):
		pass
	def CLIENT_OnReceiveAllTong( self, p1 ):
		pass
	def CLIENT_OnRequireTongStoreEvent( self, p1 ):
		pass
	def CLIENT_OnRequireTongEvent( self, p1 ):
		pass
	def BeInviteJoinTong( self, p1, p2, p3 ):
		pass
	def ReceiveInviteJoinTong( self, p1, p2, p3, p4 ):
		pass
	def OnSureSignUpBHZBMember( self, p1 ):
		pass
	def OnRemoveApplyJoinTongMember( self, p1 ):
		pass
	def OnPlunderMemberChange( self, p1 ):
		pass
	def OpenPlunderTongListWnd( self ):
		pass
	def SetbhzbSignUpMembersIsActive(self, p1, p2, p3):
		pass
	def onSetTongAllocation(self, p1):
		pass
	def onSetTongBHLDAllocation(self, p1):
		pass
	
	def ClearAllTongSignMemberData( self ):
		pass

	def OnTongBlocklistChange( self, p1 ):
		pass