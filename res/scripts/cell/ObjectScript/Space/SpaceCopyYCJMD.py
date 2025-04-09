# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import Functions
import KBEMath
import Math
import random
import KBEDebug

class SpaceCopyYCJMD( SpaceCopy ):
	"""
	CST-8726 勇闯夺命岛
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.reviveInfos = []		# 复活点
		self.birthInfos = []		# 出生点

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		
		enterPosInfos = configData["SpaceData"].get("revivePosList","").split("|")
		enterDirInfos = configData["SpaceData"].get("reviveDirList","").split("|")

		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEngineDirection( tuple(dir) )
			enterDirList.append(dir)
		for i in range(0,len(enterPosList)):
			self.reviveInfos.append( (Math.Vector3(enterPosList[i]), Math.Vector3(enterDirList[i])) )

		birthPosInfos = configData["SpaceData"].get("birthPosList","").split("|")
		birthDirInfos = configData["SpaceData"].get("birthDirList","").split("|")

		birthPosList = []
		birthDirList = []
		for enterPosInfo in birthPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			birthPosList.append(pos)

		for enterDirInfo in birthDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEngineDirection( tuple(dir) )
			birthDirList.append(dir)
		for i in range(0,len(birthPosList)):
			self.birthInfos.append( (Math.Vector3(birthPosList[i]), Math.Vector3(birthDirList[i])) )

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.onEnterCampCopyYCJMD()
	
	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

	def getReviveInfos( self, position ):
		"""
		就近取复活点
		"""
		srcDists = []
		tempDists = []
		for reviveInfo in self.reviveInfos:
			dist = position.flatDistTo(reviveInfo[0])
			srcDists.append(dist)
			tempDists.append(dist)

		srcDists.sort()
		index = tempDists.index(srcDists[0])
		return self.reviveInfos[index]

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		selfEntity.setBirthInfos( self.birthInfos )
		SpaceCopy.initEntity( self, selfEntity )	
