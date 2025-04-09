# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
import csstatus

class ThirdTongStarcraftMember:
	"""
	帮会争霸 成员数据
	"""
	def __init__( self ):
		self.roleDBID = 0
		self.roleMB = None
		self.tongDBID = 0
		self.roleID = 0
		self.roleName = ""
		self.kill = 0
		self.beKill = 0
		self.assists = 0
		self.occupy = 0
		self.killNum = 0
	
	def initData( self, roleDBID, roleMB, tongDBID, roleName,roleID):
		self.roleDBID = roleDBID
		self.roleMB = roleMB
		self.tongDBID = tongDBID
		self.roleName = roleName
		self.roleID = roleID

	def addMemberKill( self ):
		"""
		"""
		self.kill += 1
		self.killNum += 1

	def addMemberBeKill( self ):
		"""
		"""
		self.beKill += 1
		self.killNum = 0

	def addMemberAssists( self ):
		"""
		"""
		self.assists += 1

	def addMemberOccupy( self ):
		"""
		"""
		self.occupy += 1

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict["roleDBID"] = obj.roleDBID
		tempDict["roleMB"] = obj.roleMB
		tempDict["tongDBID"] = obj.tongDBID
		tempDict["roleID"] = obj.roleID
		tempDict["roleName"] = obj.roleName
		tempDict["kill"] = obj.kill
		tempDict["beKill"] = obj.beKill
		tempDict["assists"] = obj.assists
		tempDict["occupy"] = obj.occupy
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = ThirdTongStarcraftMember()
		obj.roleDBID = dict["roleDBID"]
		obj.roleMB = dict["roleMB"]
		obj.tongDBID = dict["tongDBID"]
		obj.roleID = dict["roleID"]
		obj.roleName = dict["roleName"]
		obj.kill = dict["kill"]
		obj.beKill = dict["beKill"]
		obj.assists = dict["assists"]
		obj.occupy = dict["occupy"]
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, ThirdTongStarcraftMember )

class ThirdTongStarcraftTongData:
	"""
	帮会争霸 帮会数据
	"""
	def __init__( self ):
		self.tongDBID = 0
		self.members = {}
		self.tongName = ""
		self.integral = 0
		self.side = csdefine.TONG_BELONG_NONE_SIDE
	
	def init( self, tongDBID, tongName, side = csdefine.TONG_BELONG_NONE_SIDE ):
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.side = side

	def initData( self, dict ):
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		self.integral = dict["integral"]
		for m in dict["members"]:
			self.members[ m.roleDBID ] = m

	def addMember( self, dbid, roleMB, tongDBID ):
		"""
		"""
		if dbid in self.members:
			member = self.members[dbid]
			member.roleMB = roleMB
			member.roleID = roleMB.id
			return
		member = ThirdTongStarcraftMember()
		member.initData(dbid, roleMB,tongDBID, roleMB.getName(), roleMB.id )
		self.members[member.roleDBID] = member

	def removeMember( self, dbid ):
		"""
		"""
		if dbid in self.members:
			del self.members[dbid]

	def addThirdIntegral( self, value ):
		"""
		增加第三场积分
		"""
		self.integral += value

	def addMemberKill( self, playerDBID ):
		"""
		增加成员击杀数据
		"""
		if playerDBID in self.members:
			self.members[playerDBID].addMemberKill()
			return True
		return False

	def addMemberBeKill( self, playerDBID ):
		"""
		增加成员被击杀数据
		"""
		if playerDBID in self.members:
			self.members[playerDBID].addMemberBeKill()
			return True
		return False

	def addMemberAssists( self, playerDBID ):
		"""
		增加成员助攻数
		"""
		if playerDBID in self.members:
			self.members[playerDBID].addMemberAssists()
			return True
		return False

	def addMemberOccupy( self, playerDBID ):
		"""
		增加成员占领水晶数
		"""
		if playerDBID in self.members:
			self.members[playerDBID].addMemberOccupy()
			return True
		return False

	def getMember( self, dbid ):
		"""
		获得成员
		"""
		return self.members.get(dbid,None)

	def getMembers( self ):
		"""
		获得所有成员
		"""
		return list(self.members.values())

	def getDictFromObj( self, obj ):
		dict = {}
		dict[ "tongDBID" ] = obj.tongDBID
		dict[ "members" ] = list(obj.members.values())
		dict["tongName"] = obj.tongName
		dict["integral"] = obj.integral
		return dict
	
	def createObjFromDict( self, dict ):
		obj = ThirdTongStarcraftTongData()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, ThirdTongStarcraftTongData )

class ThirdTongStarcraftInfos( dict ):
	"""
	帮会争霸第三场 帮会数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addThirdTongStarcraftMember( self, tongDBID, tongName,dbid, side,mailbox, otherTongDBID = 0,otherTongName = 0,otherSide = 0 ):
		"""
		增加第三场的成员
		"""
		if tongDBID in self.keys():
			tongInfo = self[tongDBID]
		else:
			tongInfo = ThirdTongStarcraftTongData()
			tongInfo.init( tongDBID,tongName,side )
			self[tongDBID] = tongInfo
		if otherTongDBID != 0:
			if otherTongDBID not in self.keys():
				otherTongInfo = ThirdTongStarcraftTongData()
				otherTongInfo.init( otherTongDBID, otherTongName, otherSide )
				self[otherTongDBID] = otherTongInfo
		if tongInfo.getMember( dbid ) != None:
			srcMember = tongInfo.getMember( dbid )
			srcRoleID = srcMember.roleID
			tongInfo.addMember( dbid,mailbox,tongDBID )
			self.receiveAllThirdTongStarcraftIntegral( mailbox )
			self.receiveAllThirdTongStarcraftMemberData( mailbox )
			self.updateThirdTongStarcraftLoginMemToOtherClient( tongInfo.side,srcRoleID, mailbox.id )
		else:
			tongInfo.addMember( dbid,mailbox,tongDBID )
			self.receiveAllThirdTongStarcraftIntegral( mailbox )
			self.updateThirdTongStarcraftIntegralToAllClient( tongDBID )
			self.receiveAllThirdTongStarcraftMemberData( mailbox )
			self.updateThirdTongStarcraftMemToOtherClient( mailbox, tongDBID )

	def addThirdTongStarcraftIntegral( self, tongDBID, value ):
		"""
		增加帮会积分
		"""
		if tongDBID not in self.keys():
			return
		self[tongDBID].addThirdIntegral( value )
		self.updateThirdTongStarcraftIntegralToAllClient( tongDBID )

	def getThirdTongStarcraftIntegral( self, tongDBID ):
		"""
		获得某个帮会的积分
		"""
		if tongDBID not in self.keys():
			return
		tong = self[tongDBID]
		return tong.integral

	def updateThirdTongStarcraftIntegralToAllClient( self, tongDBID ):
		"""
		自己帮会的积分更新到所有人的客户端
		"""
		if tongDBID not in self.keys():
			return
		tong = self[tongDBID]
		for mem in self.getMembers():
			if mem.roleMB and mem.roleMB.getClient():
				mem.roleMB.client.CLIENT_UpdateThirdTongStarcraftIntegral( tong.side,tong.integral )

	def receiveAllThirdTongStarcraftIntegral( self, player ):
		"""
		接受是所有人的帮会积分
		"""
		for tong in self.values():
			if player.getClient():
				player.client.CLIENT_ReceiveAllThirdTongStarcraftIntegral( tong.side,tong.tongName,tong.integral )

	def receiveAllThirdTongStarcraftMemberData( self, player ):
		"""
		接受所有帮会成员的数据
		"""
		for tong in self.values():
			members = tong.getMembers()
			for member in members:
				if player.getClient():
					player.client.CLIENT_ReceiveAllThirdTongStarcraftMemberData( tong.side, member.roleID,member.roleName,member.kill,member.beKill,member.assists,member.occupy )

	def updateThirdTongStarcraftMemToOtherClient( self, player, tongDBID ):
		"""
		更新自己数据到其他客户端
		"""
		if tongDBID not in self.keys():
			return
		playerMem = self.getMember( tongDBID, player.playerDBID )
		if not playerMem:
			return
		for tong in self.values():
			members = tong.getMembers()
			for member in members:
				if member.roleMB and member.roleMB.getClient():
					member.roleMB.client.CLIENT_UpdateThirdTongStarcraftMemToOtherClient( self[tongDBID].side, playerMem.roleID,playerMem.roleName,playerMem.kill,playerMem.beKill,playerMem.assists,playerMem.occupy  )

	def updateThirdTongStarcraftLoginMemToOtherClient( self, side,srcRoleID, dstRoleID ):
		"""
		"""
		members = self.getMembers()
		for member in members:
			if member.roleMB and member.roleMB.getClient() and member.roleID != player.id:
				member.roleMB.client.CLIENT_UpdateThirdTongStarcraftLoginMemToOtherClient( side,srcRoleID , dstRoleID )

	def getMember( self, tongDBID, dbid ):
		"""
		获得成员
		"""
		if tongDBID not in self.keys():
			return None
		return self[tongDBID].getMember( dbid )

	def getMembers( self ):
		"""
		获得所有成员
		"""
		members = []
		for tong in self.values():
			members.extend(tong.getMembers())

		return members

	def getTongDBIDByEntityID( self, entityID ):
		"""
		通过entityID获得
		"""
		for tong in self.values():
			member = tong.getMemberByEntityID()
			if member:
				return member
		return None

	def getAllTongs( self ):
		return list(self.keys())

	def kill( self, killTongDBID, killRole,dieTongDBID,dieRole ):
		"""
		击杀
		"""
		if killTongDBID not in self.keys() or dieTongDBID not in self.keys():
			return
		killTong = self[killTongDBID]
		dieTong = self[dieTongDBID]
		killMember = self.getMember( killTongDBID, killRole.playerDBID )
		dieMember = self.getMember( dieTongDBID, dieRole.playerDBID )
		if not killMember or not dieMember:
			return
		self.checkKillGodPlayer( killTong, killMember, dieMember )
		if killTong.addMemberKill( killRole.playerDBID ):
			for mem in self.getMembers():
				if mem.roleMB and mem.roleMB.getClient():
					mem.roleMB.client.CLIENT_UpdateThirdTongStarcraftMemKill(killTong.side, killMember.roleID, killMember.kill )
		if dieTong.addMemberBeKill( dieRole.playerDBID ):
			for mem in self.getMembers():
				if mem.roleMB and mem.roleMB.getClient():
					mem.roleMB.client.CLIENT_UpdateThirdTongStarcraftMemBeKill( dieTong.side, dieMember.roleID, dieMember.beKill )
		self.checkIsFirstKill( killTong,killMember)
		self.checkKillNum( killTong,killMember,dieMember )

	def addTongMemberAssists( self, tongDBID, assistsRole ):
		"""
		增加帮会成员的助攻数
		"""
		if tongDBID not in self.keys():
			return
		tong = self[tongDBID]
		if not tong.addMemberAssists( assistsRole.playerDBID ):
			return
		member = self.getMember( tongDBID, assistsRole.playerDBID )
		for mem in self.getMembers():
			if mem.roleMB and mem.roleMB.getClient():
				mem.roleMB.client.CLIENT_UpdateThirdTongStarcraftMemAssists( tong.side, member.roleID, member.assists )

	def addTongMemberOccupy( self, tongDBID, occupyRole ):
		"""
		增加帮会成员的水晶占领数
		"""
		if tongDBID not in self.keys():
			return
		tong = self[tongDBID]
		if not tong.addMemberOccupy( occupyRole.playerDBID ):
			return
		member = self.getMember( tongDBID, occupyRole.playerDBID )
		for mem in self.getMembers():
			if mem.roleMB and mem.roleMB.getClient():
				mem.roleMB.client.CLIENT_UpdateThirdTongStarcraftMemOccupy( tong.side, member.roleID, member.occupy )

	def checkIsFirstKill( self, killTong,killMember ):
		"""
		是否为首杀
		"""
		isFirstKill = True
		if killMember.kill == 1:
			for mem in self.getMembers():
				if mem.roleID != killMember.roleID and mem.kill != 0:
					isFirstKill = False
		else:
			isFirstKill = False

		if isFirstKill:
			for mem in self.getMembers():
				if mem.roleMB.getClient():
					mem.roleMB.client.CLIENT_OnFirstKill( killMember.roleName )
					mem.roleMB.statusMessage( csstatus.THIRD_TONG_STARCRAFT_FIRST_KILL,killTong.tongName,killMember.roleName )

	def checkKillNum( self, killTong,killMember,dieMember ):
		"""
		检查连续击杀数
		"""
		statusID = 0
		if killMember.killNum >= 5:
			statusID = csstatus.THIRD_TONG_STARCRAFT_FIVE_KILL
		if killMember.killNum >= 8:
			statusID = csstatus.THIRD_TONG_STARCRAFT_EIGHT_KILL
		if killMember.killNum >= 12:
			statusID = csstatus.THIRD_TONG_STARCRAFT_GOD_LIKE
		if statusID:
			for mem in self.getMembers():
				if mem.roleMB.getClient():
					mem.roleMB.statusMessage( statusID, killTong.tongName,killMember.roleName )
					if statusID == csstatus.THIRD_TONG_STARCRAFT_GOD_LIKE:
						mem.roleMB.client.CLIENT_OnGodLike( killMember.roleName )

	def checkKillGodPlayer( self, killTong, killMember, dieMember ):
		"""
		检查是否击杀超神玩家
		"""
		if dieMember.killNum > 12:
			for mem in self.getMembers():
				if mem.roleMB.getClient():
					mem.roleMB.statusMessage( csstatus.THIRD_TONG_STARCRAFT_KILL_GOD_PLAYER, killTong.tongName,killMember.roleName,dieMember.roleName )
					mem.roleMB.client.CLIENT_OnEndLegendary( killMember.roleName )
		

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict

	def getFirstTong( self ):
		return sorted( self.values(), key = lambda s:s.integral, reverse = True )[0]
	
	def createObjFromDict( self, dict ):
		obj = ThirdTongStarcraftInfos()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, ThirdTongStarcraftInfos )

g_thirdTongStarcraftInfos = ThirdTongStarcraftInfos()
g_thirdTongStarcraftTongData = ThirdTongStarcraftTongData()
g_thirdTongStarcraftMember = ThirdTongStarcraftMember()