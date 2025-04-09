# -*- coding: utf-8 -*-

import KBEDebug
import csdefine

class TongStarcraftMember:
	"""
	帮会争霸 成员数据
	"""
	def __init__( self ):
		self.dbid = 0
		self.mailbox = None
		self.tongDBID = 0
		self.groupID = -1
		self.stageIndex = -1 #这个是表示玩家使用哪个阶段index (第一场争霸需要用到)
		self.integral = 0
		self.isCanFight = True
	
	def initData( self, dbid, mailbox, tongDBID, groupID, stageIndex ):
		self.dbid = dbid
		self.mailbox = mailbox
		self.tongDBID = tongDBID
		self.groupID = groupID
		self.stageIndex = stageIndex

	def addIntegral( self, value ):
		"""
		增加积分
		"""
		self.integral += value
		
	def reduceIntegral( self, value ):
		"""
		减少积分
		"""
		self.integral = max( 0, self.integral - value )

	def setIsCanFight( self, isCanFight ):
		"""
		设置是否可以战斗
		"""
		self.isCanFight = isCanFight

	def getIsCanFight( self ):
		"""
		"""
		return self.isCanFight

	def getIntegral( self ):
		"""
		获得积分
		"""
		return self.integral

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict["dbid"] = obj.dbid
		tempDict["mailbox"] = obj.mailbox
		tempDict["tongDBID"] = obj.tongDBID
		tempDict["groupID"] = obj.groupID
		tempDict["stageIndex"] = obj.stageIndex
		tempDict["integral"] = obj.integral
		tempDict["isCanFight"] = obj.isCanFight
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = TongStarcraftMember()
		obj.dbid = dict["dbid"]
		obj.mailbox = dict["mailbox"]
		obj.tongDBID = dict["tongDBID"]
		obj.groupID = dict["groupID"]
		obj.stageIndex = dict["stageIndex"]
		obj.integral = dict["integral"]
		obj.isCanFight = dict["isCanFight"]
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TongStarcraftMember )

class TongStarcraftTongData:
	"""
	帮会争霸 帮会数据
	"""
	def __init__( self ):
		self.tongDBID = 0
		self.members = {}
		self.tongName = ""
		self.passTime = 0.0
		self.integral = 0
		self.side = csdefine.TONG_BELONG_NONE_SIDE
	
	def init( self, tongDBID, tongName, side = csdefine.TONG_BELONG_NONE_SIDE ):
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.side = side

	def initData( self, dict ):
		self.tongDBID = dict["tongDBID"]
		self.passTime = dict["passTime"]
		self.tongName = dict["tongName"]
		self.integral = dict["integral"]
		for m in dict["members"]:
			self.members[ m.dbid ] = m

	def addMember( self, dbid, mailbox, tongDBID, groupID, stageIndex ):
		"""
		"""
		if dbid in self.members:
			member = self.members[dbid]
			member.mailbox = mailbox
			return
		member = TongStarcraftMember()
		member.initData(dbid, mailbox,tongDBID, groupID, stageIndex)
		self.members[member.dbid] = member

	def removeMember( self, dbid ):
		"""
		"""
		if dbid in self.members:
			del self.members[dbid]

	def addIntegral( self, dbid,value ):
		"""
		增加积分
		"""
		self.integral += value
		self.members[dbid].addIntegral( value )

	def reduceIntegral( self, dbid, value ):
		"""
		减少积分
		"""
		self.integral = max( 0, self.integral - value )
		self.members[dbid].reduceIntegral( value )

	def addThirdIntegral( self, value ):
		"""
		增加第三场积分
		"""
		self.integral += value

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

	def getMemberByEntityID( self, entityID ):
		"""
		"""
		for member in self.members.values():
			if member.mailbox and member.mailbox.id == entityID:
				return member
		return None

	def getMembersByStageIndex( self, stageIndex ):
		memberList = []
		for member in self.members.values():
			if member.stageIndex == stageIndex and member.mailbox:
				memberList.append(member)
		return memberList

	def getRoleUseSpaceStage( self, playerDBID ):
		if playerDBID in self.members:
			return self.members[playerDBID].stageIndex
		return -1

	def getDictFromObj( self, obj ):
		dict = {}
		dict[ "tongDBID" ] = obj.tongDBID
		dict[ "members" ] = list(obj.members.values())
		dict["passTime"] = obj.passTime
		dict["tongName"] = obj.tongName
		dict["integral"] = obj.integral
		return dict
	
	def createObjFromDict( self, dict ):
		obj = TongStarcraftTongData()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TongStarcraftTongData )

class TongStarcraftInfos( dict ):
	"""
	帮会争霸 帮会数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addMember( self, tongDBID, tongName,dbid, mailbox, isUpdate = 0, groupID = -1, stageIndex = -1,):
		"""
		"""
		if tongDBID in self.keys():
			tongInfo = self[tongDBID]
		else:
			tongInfo = TongStarcraftTongData()
			tongInfo.init( tongDBID,tongName )
			self[tongDBID] = tongInfo
		tongInfo.addMember( dbid,mailbox,tongDBID, groupID, stageIndex )
		if isUpdate:
			self.receiveAllMembersIntegral( mailbox ) #接收所有成员积分
			self.receiveAllTongIntegral( mailbox ) #接受所有帮会的积分
			self.updateMemberIntegralToAllClient(tongDBID,dbid) # 自己的积分更新到所有人的客户端
			self.updateTongIntegralToAllClient( tongDBID ) # 自己帮会的积分更新到所有人的客户端

	def addThirdTongStarcraftMember( self, tongDBID, tongName,dbid, side,mailbox, otherTongDBID = 0,otherTongName = 0,otherSide = 0 ):
		"""
		增加第三场的成员
		"""
		if tongDBID in self.keys():
			tongInfo = self[tongDBID]
		else:
			tongInfo = TongStarcraftTongData()
			tongInfo.init( tongDBID,tongName,side )
			self[tongDBID] = tongInfo
		if otherTongDBID != 0:
			if otherTongDBID not in self.keys():
				otherTongInfo = TongStarcraftTongData()
				otherTongInfo.init( otherTongDBID, otherTongName, otherSide )
				self[otherTongDBID] = otherTongInfo
		tongInfo.addMember( dbid,mailbox,tongDBID, -1, -1 )
		self.receiveAllThirdTongStarcraftIntegral( mailbox )
		self.updateThirdTongStarcraftIntegralToAllClient( tongDBID )



	def addIntegral( self, tongDBID, dbid, value ):
		"""
		增加积分
		"""
		if tongDBID not in self.keys():
			return
		self[tongDBID].addIntegral( dbid, value )
		self.updateMemberIntegralToAllClient( tongDBID,dbid )	# 自己的积分更新到所有人的客户端
		self.updateTongIntegralToAllClient( tongDBID )	# 自己帮会的积分更新到所有人的客户端

	def reduceIntegral( self, tongDBID, dbid, value ):
		"""
		减少积分
		"""
		if tongDBID not in self.keys():
			return
		self[tongDBID].reduceIntegral( dbid,value )
		self.updateMemberIntegralToAllClient( tongDBID,dbid )	# 自己的积分更新到所有人的客户端
		self.updateTongIntegralToAllClient( tongDBID )	# 自己帮会的积分更新到所有人的客户端

	def updateMemberIntegralToAllClient( self, tongDBID,dbid ):
		"""
		自己的积分更新到所有人的客户端
		"""
		member = self.getMember( tongDBID, dbid )
		if not member:
			return

		for mem in self.getMembers():
			if mem.mailbox and mem.mailbox.getClient():
				mem.mailbox.client.CLIENT_UpdateMemberIntegral( member.mailbox.id, member.integral )

	def updateTongIntegralToAllClient( self, tongDBID ):
		"""
		自己帮会的积分更新到所有人的客户端
		"""
		if tongDBID not in self.keys():
			return
		tong = self[tongDBID]
		for mem in self.getMembers():
			if mem.mailbox and mem.mailbox.getClient():
				mem.mailbox.client.CLIENT_UpdateTongIntegral( tong.tongName,tong.integral )

	def receiveAllMembersIntegral( self, player ):
		"""
		接受所有人的积分
		"""
		for mem in self.getMembers():
			if player.getClient():
				player.client.CLIENT_UpdateMemberIntegral( mem.mailbox.id,mem.integral )

	def receiveAllTongIntegral( self, player ):
		"""
		接受所有人的帮会积分
		"""
		for tong in self.values():
			if player.getClient():
				player.client.CLIENT_UpdateTongIntegral( tong.tongName, tong.integral )

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
			if mem.mailbox and mem.mailbox.getClient():
				mem.mailbox.client.CLIENT_UpdateThirdTongStarcraftIntegral( tong.side,tong.integral )

	def receiveAllThirdTongStarcraftIntegral( self, player ):
		"""
		接受是所有人的帮会积分
		"""
		for tong in self.values():
			if player.getClient():
				player.client.CLIENT_ReceiveAllThirdTongStarcraftIntegral( tong.side,tong.tongName,tong.integral )

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

	def getMembersByStageIndex( self, tongDBID, stageIndex ):
		if tongDBID in self.keys():
			return self[tongDBID].getMembersByStageIndex(stageIndex)
		return []

	def getRoleUseSpaceStage( self, tongDBID, playerDBID ):
		if tongDBID in self.keys():
			return self[tongDBID].getRoleUseSpaceStage( playerDBID )

		return -1

	def getFirstTong( self ):
		return sorted( self.values(), key = lambda s:s.integral, reverse = True )[0]

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = TongStarcraftInfos()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TongStarcraftInfos )

g_tongStarcraftInfos = TongStarcraftInfos()
g_tongStarcraftTongData = TongStarcraftTongData()
g_tongStarcraftMember = TongStarcraftMember()