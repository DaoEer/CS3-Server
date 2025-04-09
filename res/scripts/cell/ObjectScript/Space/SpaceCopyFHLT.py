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

class SpaceCopyFHLT( SpaceCopy ):
	"""
	烽火连天
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._xianEnterPos = ( 0, 0, 0 )
		self._xianEnterDir = ( 0, 0, 0 )
		self._moEnterPos = ( 0, 0, 0)
		self._moEnterDir = ( 0, 0, 0 )
		self._materialPointNum = 0
		self._xianVanMonsterList = []
		self._moVanMonsterList = []
		self._xianVanPosList = []
		self._moVanPosList = []
		self._xianVanDirList = []
		self._moVanDirList = []
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
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
		self._materialPointNum = int( configData["SpaceData"].get( "materialPointNum", 0 ) )
		_xianVanMonsterList = configData["SpaceData"].get( "xianVanMonsterList", "" )
		if _xianVanMonsterList:
			self._xianVanMonsterList = _xianVanMonsterList.split("|")
		_moVanMonsterList = configData["SpaceData"].get( "moVanMonsterList", "" )
		if _moVanMonsterList:
			self._moVanMonsterList = _moVanMonsterList.split("|")
		_xianVanPosList = configData["SpaceData"].get( "xianVanPosList", "" )
		if _xianVanPosList:
			self._xianVanPosList = _xianVanPosList.split("|")
		_xianVanDirList = configData["SpaceData"].get( "xianVanDirList", "" )
		if _xianVanDirList:
			self._xianVanDirList = _xianVanDirList.split("|")
		_moVanPosList = configData["SpaceData"].get( "moVanPosList", "" )
		if _moVanPosList:
			self._moVanPosList = _moVanPosList.split("|")
		_moVanDirList = configData["SpaceData"].get( "moVanDirList", "" )
		if _moVanDirList:
			self._moVanDirList = _moVanDirList.split("|")

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "onLifeTimeArrive", () )
		#selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowFHLTLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()))

	def getEnterInfoByCamp( self, camp ):
		"""根据阵营获得进入副本的位置朝向"""
		if camp == csdefine.CAMP_TAOSIM:
			return self._xianEnterPos, self._xianEnterDir
		else:
			return self._moEnterPos, self._moEnterDir