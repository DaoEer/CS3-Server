# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyStory import SpaceCopyStory
import KBEDebug
import Math

class SpaceCopyHeHuaFaZhen( SpaceCopyStory ):
	"""
	荷花阵法
	"""
	def __init__( self ):
		SpaceCopyStory.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopyStory.initData( self, configData )
		originPos = configData["SpaceData"].get( "originPos", "" )
		if originPos:
			originPos = originPos.split("|")
			self._originPos = tuple( [ float(i) for i in originPos ] )
		self._unitLength = float(configData["SpaceData"].get("unitLength",0.0))
		self._heYeID = configData["SpaceData"].get("heYeID","")
		self._whiteHeHuaID = configData["SpaceData"].get("whiteHeHuaID","")
		self._redHeHuaID = configData["SpaceData"].get("redHeHuaID","")
		self._redHeBaoID = configData["SpaceData"].get("redHeBaoID","")
		self._whiteHeBaoID = configData["SpaceData"].get("whiteHeBaoID","")
		self._whiteHeHuaMonsterID = configData["SpaceData"].get("whiteHeHuaMonsterID","")
		self._redHeHuaMonsterID = configData["SpaceData"].get("redHeHuaMonsterID")
		self._effectMonsterID = configData["SpaceData"].get("effectMonsterID")
		self._bossID = configData["SpaceData"].get("bossID","")
		self._redHeHuaSkillID = configData["SpaceData"].get("redHeHuaSkillID")
		self._whiteHeHuaSkillID = configData["SpaceData"].get("whiteHeHuaSkillID")
		self._mixHeHuaSkillID = configData["SpaceData"].get("mixHeHuaSkillID")
		


	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyStory.initEntity( self, selfEntity )
		selfEntity.initSpaceData( Math.Vector3(self._originPos), self._unitLength, self._heYeID, self._whiteHeHuaID, self._redHeHuaID, self._whiteHeBaoID, self._redHeBaoID, self._whiteHeHuaMonsterID, self._redHeHuaMonsterID, self._effectMonsterID, self._bossID, self._whiteHeHuaSkillID, self._redHeHuaSkillID, self._mixHeHuaSkillID)
