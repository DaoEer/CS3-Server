# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEMath
import Functions
import csdefine

class SpaceCopyBHZBPointWarPVP( SpaceCopy ):
	"""
	帮会争霸 据点争夺战 PVP
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.enterProtectInfo = ()	# 进入防守方的位置
		self.enterAttackInfo = ()	# 进入进攻方位置数据
	
	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		if configData["SpaceData"].get("enterPos",""):
			enterPosInfos = configData["SpaceData"].get("enterPos","").split("|")
			enterDirInfos = configData["SpaceData"].get("enterDir","").split("|")
			enterPosList = []
			enterDirList = []
			for enterPosInfo in enterPosInfos:
				pos = Functions.vector3TypeConvert(enterPosInfo)
				pos = KBEMath.Unreal2KBEnginePosition( pos )
				enterPosList.append(pos)

			for enterDirInfo in enterDirInfos:
				dir = Functions.vector3TypeConvert(enterDirInfo)
				dir = KBEMath.Unreal2KBEngineDirection( dir )
				enterDirList.append(dir)
			self.enterAttackInfo = (enterPosList[0],enterDirList[0] )
			if len(enterPosList) > 1 and len( enterDirList ) > 1:
				self.enterProtectInfo = (enterPosList[1],enterDirList[1] )

	def getProtectEnterInfo( self ):
		"""
		获得防守方的进入信息
		"""
		return self.enterProtectInfo

	def getAttackEnterInfo( self ):
		"""
		获得进攻方的进入信息
		"""
		return self.enterAttackInfo
