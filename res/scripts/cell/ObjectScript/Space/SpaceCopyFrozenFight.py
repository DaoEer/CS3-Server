# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import csdefine
import Const
import csconst
import Functions
import csstatus
from ObjectScript.Space.SpaceCopy import SpaceCopy



class SpaceCopyFrozenFight( SpaceCopy ):
	"""
	冰雪之战
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._initCampPoint = 0
		self._xianEnterPos = (0,0,0)
		self._xianEnterDir = (0,0,0)
		self._moEnterPos = (0,0,0)
		self._moEnterDir = (0,0,0)
		self._revivePosInfo = {}
		self._towerInfo = []
		self._pointInfo = {}
		self.iceCrystalsItemID = 0
		self.iceCrystalsSpBoxID = ""

	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		self._initCampPoint = configData["SpaceData"].get("initCampPoint", 100)	
		posStr = configData["SpaceData"].get( "xianEnterPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._xianEnterPos = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "xianEnterDir", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._xianEnterDir = KBEMath.Unreal2KBEngineDirection( dir )
		posStr = configData["SpaceData"].get( "moEnterPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._moEnterPos = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "moEnterDir", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._moEnterDir = KBEMath.Unreal2KBEngineDirection( dir )

		
		revivePosInfo = configData["SpaceData"].get("revivePosInfo",{})
		for key,value in revivePosInfo.items():
			camp = value["camp"]
			pos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(value["pos"]))
			dir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(value["dir"]))
			param = {key:{"camp":camp, "pos":pos, "dir":dir}}
			self._revivePosInfo.update(param)
		self._towerInfo = configData["SpaceData"].get("towerInfo", [])
		self._pointInfo = configData["SpaceData"].get("pointInfo", {})
		self.iceCrystalsItemID = configData["SpaceData"].get("iceCrystalsItemID", 0)
		self.iceCrystalsSpBoxID = configData["SpaceData"].get("iceCrystalsSpBoxID", "")

	def initEntity(self, selfEntity):
		""""""
		SpaceCopy.initEntity(self, selfEntity)
		selfEntity.initSpaceData(self._initCampPoint, self._revivePosInfo, self._towerInfo, self._pointInfo)
		
				
	def getEnterInfoByCamp( self, camp ):
		"""根据阵营获得进入副本的位置朝向"""
		if camp == csdefine.CAMP_TAOSIM:
			return self._xianEnterPos, self._xianEnterDir
		else:
			return self._moEnterPos, self._moEnterDir


	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "onLifeTimeArrive", () )

		for e in selfEntity._spaceRoles:
		 	e.client.CLIENT_ShowFrozenFightLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()))

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		param = SpaceCopy.getPackDomainData( self, playerEntity, {} )
		param.update(args)
		return param