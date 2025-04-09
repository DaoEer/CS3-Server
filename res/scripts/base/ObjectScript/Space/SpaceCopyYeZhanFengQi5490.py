# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import Functions
import KBEMath
import random

class SpaceCopyYeZhanFengQi5490( SpaceCopy ):
	"""
	血斗凤栖镇 JIRA CST-5490
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.enterInfos = []

	def initData( self, configData ):
		"""
		virtual method
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
	
	def getEnterInfo( self ):
		"""
		获得进入信息
		"""
		info = None
		if self.enterInfos:
			info = random.choice(self.enterInfos)
			self.enterInfos.remove(info)
		return info