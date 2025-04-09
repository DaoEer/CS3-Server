# -*- coding: utf-8 -*-

import Math
import random
import csdefine
import Const
import Functions
import KBEMath
import SpaceContainer
import QuestEventDefine
from ObjectScript.ObjectScriptBase.GameScript import GameScript
from ConfigObject.BunchChildStrategy.StrategyLoader import g_bunchChildStrategyLoader
from KBEDebug import *


class SpaceChild( object ):
	def __init__( self, bunchObj, index ):
		self.bunchObj = bunchObj
		self.index = index
		self.spaceScriptIDs = []
		self.doorsPos = []
		self.doorsDir = []
		self.isBig = 1		#是否是大副本，默认是大副本
		self.createDoorDelay = 5
		self.createDoorNotifyInfo = []
	
	def initData( self, info ):
		for posStr in info["doorsPos"].split( "|" ):
			pos = Functions.vector3TypeConvert( posStr )
			self.doorsPos.append( KBEMath.Unreal2KBEnginePosition( pos ) )
		
		for dirStr in info["doorsDir"].split( "|" ):
			dir = Functions.vector3TypeConvert( dirStr )
			self.doorsDir.append( KBEMath.Unreal2KBEngineDirection( dir ) )
		
		if "isBig" in info:
			self.isBig = info["isBig"]
		
		if "createDoorDelay" in info:
			self.createDoorDelay = info["createDoorDelay"]
		
		for listStr, soundID in info["createDoorNotifyInfo"].items():
			tempDict = { "spaceList": listStr.split("|"), "soundID": soundID }
			self.createDoorNotifyInfo.append( tempDict )

		self.spaceScriptIDs = info.get("spaceList",[])

	def getCreateDoorDelay( self ):
		return self.createDoorDelay
	
	def isBigSpace( self ):
		return self.isBig == 1

	def getFirstSpaceScriptID( self ):
		return self.spaceScriptIDs[0]

	def isChildSpaceComplete( self, spaceScriptID ):
		index = self.spaceScriptIDs.index( spaceScriptID )
		return index == (len( self.spaceScriptIDs ) - 1)

	def getNextSpace( self, spaceScriptID ):
		index = self.spaceScriptIDs.index( spaceScriptID )
		return self.spaceScriptIDs[index+1]
	
	def createDoor( self, spaceObj, spaceEntity ):
		"""
		刷门
		"""
		_completeList = list( spaceEntity.createArgs[ "completeList" ] )
		_completeList.append( spaceEntity.bunchChildSpaceIndex )
		_allList = list( self.bunchObj.childSpaces.keys() )
		_remainList = list( set( _completeList ) ^ set( _allList ) )
		for i in range( len( _remainList ) + 1 ):
			spaceEntity.createEntityByScriptID( Const.BUNCH_SPACE_TELEPORT_BOX_ID, tuple(Math.Vector3(self.doorsPos[i])), self.doorsDir[i], {} )#createSpellBox
		self.sendCreateDoorNotify( spaceEntity, _completeList )
		self.setNextSpace( spaceObj, spaceEntity )
	
	def setNextSpace( self, spaceObj, spaceEntity ):
		"""
		设置下一个子副本
		"""
		nextSpace = ""
		
		# 单人副本 + 有任务 -> 必进空门（CST-2438）
		if spaceEntity.belongType == csdefine.SPACE_BELONG_PERSON:
			if len( spaceEntity._spaceRoles ):
				role = spaceEntity._spaceRoles[0]
				if self.bunchObj.bunchType == csdefine.SPACE_BUNCH_TYPE_POTENTAIL and role.questEventMgr.hasEvent( QuestEventDefine.EVENT_ENTER_POTENTIAL_COPY ):
					nextSpace = Const.BUNCH_RECORD_SPACE_STR
				elif self.bunchObj.bunchType == csdefine.SPACE_BUNCH_TYPE_CHUANCHENG and role.questEventMgr.hasEvent( QuestEventDefine.EVENT_ENTER_CHUAN_CHENG_COPY ):
					nextSpace = Const.BUNCH_RECORD_SPACE_STR
		
		# 按配置的策略随机
		if nextSpace == "":
			nextSpace = g_bunchChildStrategyLoader.getNextSpace( self.bunchObj, spaceEntity )
		
		if nextSpace == "":
			nextSpace = Const.BUNCH_RECORD_SPACE_STR
		spaceObj.spaceBunch_setNextSpace( spaceEntity, nextSpace )
	
	def sendCreateDoorNotify( self, spaceEntity, completeList ):
		"""
		刷门提示
		@param completeList:已完成子副本（包括当前副本）
		"""
		for info in self.createDoorNotifyInfo:
			if set( info["spaceList"] ) == set( completeList ):
				for e in spaceEntity._spaceRoles:
					e.showMessagePlaySound( info["soundID"] )
				break

class BunchSpaceBase( GameScript ):
	"""
	副本串script对象
	它不是一个真正的副本script，只是起到一个读取数据的作用
	"""
	def __init__( self ):
		GameScript.__init__( self )
		self._belongType = []
		self.bunchType = 0
		self.childSpaces = {}
		self.strategyID = ""
		self.failureOutNotify = ""
		self.bunchSpaceName = ""
		self.rewardRates = []	#奖励倍率
	
	def initData( self, configData ):
		GameScript.initData( self, configData )
		self._belongType = [ int(i) for i in configData[ "belongType" ].split("|") ]
		self.bunchType = getattr( csdefine, configData[ "bunchType" ] )
		for index, info in configData[ "ChildSpace" ].items():
			child = SpaceChild( self, index )
			child.initData( info )
			self.childSpaces[ index ] = child
		
		self.strategyID = configData["strategyID"]
		
		if "failureOutNotify" in configData:
			self.failureOutNotify = configData[ "failureOutNotify" ]

		if "rewardRates" in configData:
			self.rewardRates = [ float(i) for i in configData["rewardRates"].split("|") ]

	def getBunchSpaceName( self ):
		"""
		"""
		return self.bunchSpaceName

	def getReWardRateByIndex( self, index ):
		"""
		"""
		if index >= len( self.rewardRates ):
			return 1.0
		return self.rewardRates[index]
	
	def getAllChildScriptID( self ):
		result = []
		for child in self.childSpaces.values():
			result.extend(child.spaceScriptIDs)
		return result

	def getAllChildIndex( self ):
		return list( self.childSpaces.keys() )
	
	def getPackDomainData( self, playerEntity, args ):
		if "packBelongType" in args:		#打包了副本归属类型
			belongType = args.pop( "packBelongType" )
		else:								#没打包就取配置的第一个值
			belongType = self._belongType[ 0 ]
		return SpaceContainer.getPickContainerData( belongType, self.scriptID, playerEntity, args )
	
	def getChildCreateDoorDelay( self, childIndex ):
		"""
		获取子副本延迟刷门时间
		"""
		return self.childSpaces[ childIndex ].getCreateDoorDelay()
	
	def createDoor( self, spaceObj, spaceEntity ):
		"""
		刷连接门：这里是一个吟唱物件
		"""
		self.childSpaces[ spaceEntity.bunchChildSpaceIndex ].createDoor( spaceObj, spaceEntity )
	
	def showFailureOutNotify( self, playerEntity ):
		"""
		提示“未通关所有子副本”
		"""
		playerEntity.showMessagePlaySound( self.failureOutNotify )
	
	def isBigChildSpace( self, index ):
		"""
		某子副本是大副本？
		"""
		return self.childSpaces[index].isBigSpace()
	
	def getAllBigChildSpace( self ):
		"""
		获取所有大副本
		"""
		result = []
		for index, childSpace in self.childSpaces.items():
			if childSpace.isBigSpace():
				result.append( index )
		return result
	
	def getAllSmallChildSpace( self ):
		"""
		获取所有小副本
		"""
		result = []
		for index, childSpace in self.childSpaces.items():
			if not childSpace.isBigSpace():
				result.append( index )
		return result

	def getChildSpaceScriptIDByIndex( self, index ):
		"""
		获得子副本的spaceScriptID
		"""
		return self.childSpaces[index].getFirstSpaceScriptID()

	def isChildSpaceComplete( self, index, spaceScriptID ):
		"""
		子副本是否完成
		"""
		return self.childSpaces[index].isChildSpaceComplete(spaceScriptID)

	def getChildIndexBySpaceScriptID( self, spaceScriptID ):
		"""
		获得子副本的index
		"""
		for index, childSpace in self.childSpaces.items():
			if spaceScriptID in childSpace.spaceScriptIDs:
				return index
		return None

	def getChildNextSpace( self, index, spaceScriptID ):
		"""
		获得子副本下个Space
		"""
		return self.childSpaces[index].getNextSpace( spaceScriptID )
