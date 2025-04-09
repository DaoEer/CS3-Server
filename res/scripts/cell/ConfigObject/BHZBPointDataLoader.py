# -*- coding: utf-8 -*-

import KBEDebug
from Singleton import Singleton
import KBEngine
import csdefine
import csconst
import json

def utf16ToJsonCfg( path ):
	allPath = csconst.CONFIG_PATCH + path
	fileObject = open( allPath, encoding="utf16" )
	jsFileObj = json.loads( fileObject.read() )
	fileObject.close()
	return jsFileObj

class PointItem:
	def __init__( self, index, pointName, pointType, pveSpaceScriptID, pvpSpaceScriptID, readyTime, maxJoinPlayerNum, restTime ):
		self.index = index
		self.pointName = pointName
		self.pointType = pointType
		self.pveSpaceScriptID = pveSpaceScriptID
		self.pvpSpaceScriptID = pvpSpaceScriptID
		self.readyTime = readyTime
		self.maxJoinPlayerNum = maxJoinPlayerNum
		self.restTime = restTime

	def getPointName( self ):
		"""
		据点名称
		"""
		return self.pointName

	def getPointType( self ):
		"""
		据点类型
		"""
		return self.pointType

	def getPointIndex( self ):
		"""
		据点编号
		"""
		return self.index

	def getPointEnterPVESpaceScriptID( self ):
		"""
		据点pveSpaceScriptID
		"""
		return self.pveSpaceScriptID

	def getPointEnterPVPSpaceScriptID( self ):
		"""
		据点pvpSpaceScriptID
		"""
		return self.pvpSpaceScriptID

	def getReadyTime( self ):
		"""
		获得据点准备时间
		"""
		return self.readyTime

	def getMaxJoinPlayerNum( self ):
		"""
		获得据点最大参加人数
		"""
		return self.maxJoinPlayerNum

	def getRestTime( self ):
		"""
		获得据点休整时间
		"""
		return self.restTime

class BHZBPointDataLoader( Singleton ):
	"""
	帮会争霸据点数据读取类
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self.BHZBPointDatas = {}

	def init( self ):
		"""
		读取配置
		"""
		self.BHZBPointDatas.clear()
		pointDatas = utf16ToJsonCfg( "BHZBPointCfg.json" )
		for pointData in pointDatas:
			pointType =  getattr( csdefine, pointData["PointType"], csdefine.NPCEXTPOINT_TYPE_LOWER_LEVEL )
			self.BHZBPointDatas[pointData["Index"]] = PointItem( pointData["Index"], pointData["PointName"],pointType,pointData["PVESpaceScriptID"],pointData["PVPSpaceScriptID"],float(pointData["ReadyTime"]),pointData["MaxJoinPlayerNum"],float(pointData["RestTime"]) )

	def getBHZBPointItemByPointIndex( self, index ):
		"""
		获得帮会争霸某个据点
		"""
		if index in self.BHZBPointDatas:
			return self.BHZBPointDatas[index]

		return None

	def getAllBHZBPointIndexs( self ):
		"""
		获得所有据点编号
		"""
		return list( self.BHZBPointDatas.keys() )

	def getAllBHZBPVEAndPVPSpace( self ):
		"""
		获得帮会争霸所有PVE和PVP spaceScriptID
		"""
		tempList = []
		for pointCfgItem in self.BHZBPointDatas.values():
			if pointCfgItem.getPointEnterPVESpaceScriptID() not in tempList:
				tempList.append( pointCfgItem.getPointEnterPVESpaceScriptID() )
			if pointCfgItem.getPointEnterPVPSpaceScriptID() not in tempList:
				tempList.append( pointCfgItem.getPointEnterPVPSpaceScriptID() )

		return tempList

g_BHZBPointDataLoader = BHZBPointDataLoader()