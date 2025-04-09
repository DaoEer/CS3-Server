# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BHZBTongWarTeamData( object ):
	"""
	帮会争霸帮会组队数据
	"""
	def __init__( self, teamNumber = 0, pointNumber = 0, pointState = 0, pointName = ""):
		"""
		"""
		self.teamNumber = teamNumber
		self.pointNumber = pointNumber
		self.pointState = pointState
		self.pointName = pointName

	def initData( self, dict ):
		"""
		"""
		self.teamNumber = dict["teamNumber"]
		self.pointNumber = dict["pointNumber"]
		self.pointState = dict["pointState"]
		self.pointName = dict["pointState"]

	def getDictFromObj( self, obj ):
		dict = {
			"teamNumber" 	: obj.teamNumber,
			"pointNumber"	: obj.pointNumber,
			"pointState"	: obj.pointState,
			"pointName"		: obj.pointName,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongWarTeamData )

class BHZBTongOccupyPointData( object ):
	"""
	帮会争霸帮会占领据点的数据
	"""
	def __init__( self, pointNumber = 0, pointState = 0, pointName = ""):
		"""
		"""
		self.pointNumber = pointNumber
		self.pointState = pointState
		self.pointName = pointName

	def initData( self, dict ):
		"""
		"""
		self.pointNumber = dict["pointNumber"]
		self.pointState = dict["pointState"]
		self.pointName = dict["pointState"]

	def getDictFromObj( self, obj ):
		dict = {
			"pointNumber" 	: obj.pointNumber,
			"pointState"	: obj.pointState,
			"pointName"		: obj.pointName,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongOccupyPointData )

class BHZBTongWarMsgData( object ):
	"""
	帮会争霸战场提示消息数据
	"""
	def __init__( self, statusID = 0, statusArgs = ""):
		"""
		"""
		self.statusID = statusID
		self.statusArgs = statusArgs

	def initData( self, dict ):
		"""
		"""
		self.statusID = dict["statusID"]
		self.statusArgs = dict["statusArgs"]

	def getDictFromObj( self, obj ):
		dict = {
			"statusID" 	: obj.statusID,
			"statusArgs"	: obj.statusArgs,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongWarMsgData )

class BHZBTongWarDetailData( object ):
	"""
	帮会争霸战况详情数据
	"""
	def __init__( self, tongDBID = 0,integral = 0,rank = 0,occupyPointAmount = 0):
		"""
		"""
		self.tongDBID = tongDBID
		self.integral = integral
		self.rank = rank
		self.occupyPointAmount = occupyPointAmount
		self.teamDatas = {}
		self.occupyPointDatas = {}
		self.warMsgDatas = []
		self.occupyPointNumberOrders = []

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.integral = dict["integral"]
		self.rank = dict["rank"]
		self.occupyPointAmount = dict["occupyPointAmount"]
		for teamData in dict["teamDatas"]:
			self.teamDatas[teamData.teamNumber] = teamData
		for occupyPointData in dict["occupyPointDatas"]:
			self.occupyPointDatas[occupyPointData.pointNumber] = occupyPointData
		self.warMsgDatas = dict["warMsgDatas"]

	def updateBHZBWarDetailIntegralData( self, integral, rank ):
		"""
		更新帮会争霸详情积分和排名数据
		"""
		self.integral = integral
		self.rank = rank

	def updateBHZBWarDetailOccupyNumber( self, occupyPointAmount ):
		"""
		更新帮会争霸详情占领的据点数据
		"""
		self.occupyPointAmount = occupyPointAmount

	def updateBHZBWarDetailTeamData( self, teamNumber, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情队伍数据
		"""
		if teamNumber in self.teamDatas:
			self.teamDatas[teamNumber].pointNumber = pointNumber
			self.teamDatas[teamNumber].pointState = pointState
		else:
			teamData = BHZBTongWarTeamData( teamNumber, pointNumber, pointState, pointName )
			self.teamDatas[teamData.teamNumber] = teamData

	def removeBHZBWarDetailTeamData( self, teamNumber ):
		"""
		移除帮会争霸详情队伍数据
		"""
		if teamNumber in self.teamDatas:
			del self.teamDatas[teamNumber]

	def updateBHZBWarDetailOccupyPointData( self, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情据点占领数据
		"""
		if pointNumber in self.occupyPointDatas:
			self.occupyPointDatas[pointNumber].pointState = pointState
		else:
			occupyData = BHZBTongOccupyPointData( pointNumber, pointState, pointName )
			self.occupyPointDatas[occupyData.pointNumber] = occupyData

		if pointNumber not in self.occupyPointNumberOrders:
			self.occupyPointNumberOrders.append(pointNumber)

	def removeBHZBWarrDetailOccupyPoint( self, pointNumber ):
		"""
		移除帮会争霸详情占领据点
		"""
		if pointNumber in self.occupyPointDatas:
			del self.occupyPointDatas[pointNumber]
		if pointNumber in self.occupyPointNumberOrders:
			self.occupyPointNumberOrders.remove(pointNumber)

	def addBHZBWarMsgData( self, statusID, statusArgs ):
		"""
		增加帮会争霸详情提示消息数据
		"""
		msgData = BHZBTongWarMsgData( statusID, statusArgs )
		self.warMsgDatas.append( msgData )

	def getBHZBWarDetailTeamData( self, teamNumber ):
		"""
		获得帮会争霸详情队伍数据
		"""
		if teamNumber not in self.teamDatas:
			return 0,0
		return self.teamDatas[teamNumber].pointNumber,self.teamDatas[teamNumber].pointState 

	def getBHZBWarDetailOccupyPointData( self, pointNumber ):
		"""
		获得帮会争霸详情据点占领数据
		"""
		if pointNumber not in self.occupyPointDatas:
			return 0,0

		return self.occupyPointDatas[pointNumber].pointNumber, self.occupyPointDatas[pointNumber].pointState

	def getOccupyPointNumberOrders( self ):
		"""
		"""
		return self.occupyPointNumberOrders

	def getDictFromObj( self, obj ):
		occupyPointDatas = []
		if len(obj.getOccupyPointNumberOrders()) > 0:
			for pointNumber in obj.getOccupyPointNumberOrders():
				if pointNumber not in obj.occupyPointDatas:
					continue
				occupyPointDatas.append( obj.occupyPointDatas[pointNumber] )
		else:
			occupyPointDatas = list(obj.occupyPointDatas.values())
		dict = {
			"tongDBID" 	: obj.tongDBID,
			"integral"	: obj.integral,
			"rank" : obj.rank,
			"occupyPointAmount" : obj.occupyPointAmount,
			"teamDatas":list(obj.teamDatas.values()),
			"occupyPointDatas":occupyPointDatas,
			"warMsgDatas":obj.warMsgDatas,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongWarDetailData )

class BHZBTongWarDetaileMgr( dict ):
	"""
	帮会争霸战况详情管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addBHZBWarDetailData( self, tongDBID ):
		"""
		增加帮会争霸详情数据
		"""
		if tongDBID not in self:
			self[tongDBID] = BHZBTongWarDetailData( tongDBID )

	def updateBHZBWarDetailIntegralData( self, tongDBID, integral, rank ):
		"""
		更新帮会争霸详情积分和排名数据
		"""
		if tongDBID in self:
			self[tongDBID].updateBHZBWarDetailIntegralData( integral, rank )

	def updateBHZBWarDetailOccupyNumber( self, tongDBID, occupyPointAmount ):
		"""
		更新帮会争霸详情占领的据点数据
		"""
		if tongDBID in self:
			self[tongDBID].updateBHZBWarDetailOccupyNumber( occupyPointAmount )

	def updateBHZBWarDetailTeamData( self, tongDBID, teamNumber, pointNumber, pointState, pointName  ):
		"""
		更新帮会争霸详情队伍数据
		"""
		if tongDBID not in self:
			return
		self[tongDBID].updateBHZBWarDetailTeamData( teamNumber, pointNumber, pointState, pointName )

	def removeBHZBWarDetailTeamData( self, tongDBID, teamNumber ):
		"""
		移除帮会争霸详情队伍数据
		"""
		if tongDBID not in self:
			return
		self[tongDBID].removeBHZBWarDetailTeamData( teamNumber )

	def updateBHZBWarDetailOccupyPointData( self, tongDBID, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情据点占领数据
		"""
		if tongDBID not in self:
			return
		self[tongDBID].updateBHZBWarDetailOccupyPointData( pointNumber, pointState, pointName )

	def removeBHZBWarrDetailOccupyPoint( self, tongDBID, pointNumber ):
		"""
		移除帮会争霸详情占领据点
		"""
		if tongDBID not in self:
			return
		self[tongDBID].removeBHZBWarrDetailOccupyPoint( pointNumber )

	def addBHZBWarMsgData( self, tongDBID, statusID, statusArgs ):
		"""
		增加帮会争霸详情提示消息数据
		"""
		if tongDBID not in self:
			return

		self[tongDBID].addBHZBWarMsgData( statusID, statusArgs)

	def getBHZBWarDetailOccupyPointData( self, tongDBID, pointNumber ):
		"""
		获得帮会争霸详情据点占领数据
		"""
		if tongDBID not in self:
			return 0,0

		return self[tongDBID].getBHZBWarDetailOccupyPointData( pointNumber )

	def getBHZBWarDetailTeamData( self, tongDBID, teamNumber ):
		"""
		获得帮会争霸详情队伍数据
		"""
		if tongDBID not in self:
			return 0,0

		return self[tongDBID].getBHZBWarDetailTeamData( teamNumber )


	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict["datas"].append( mObj )
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBTongWarDetaileMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongWarDetaileMgr )

g_BHZBTongWarDetaileMgr = BHZBTongWarDetaileMgr()
g_BHZBTongWarDetailData = BHZBTongWarDetailData()
g_BHZBTongWarMsgData = BHZBTongWarMsgData()
g_BHZBTongOccupyPointData = BHZBTongOccupyPointData()
g_BHZBTongWarTeamData = BHZBTongWarTeamData()