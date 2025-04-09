# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import Functions
import KBEMath
import random

class SpaceCopySecondTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第二场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.enterInfos = []

	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		enterPosInfos = configData["SpaceData"].get("enterPosList","").split("|")
		enterDirInfos = configData["SpaceData"].get("enterDirList","").split("|")
		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEnginePosition( dir )
			enterDirList.append(dir)
		for i in range(0,len(enterPosList)):
			self.enterInfos.append( (enterPosList[i], enterDirList[i]) )

	def getEnterInfo( self, index ):
		"""
		获得进入信息
		"""
		return self.enterInfos[index]


