# -*- coding: utf-8 -*-
# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import random
import KBEMath
import Math
import Functions

class SEAction284( SEActionBase ):
	"""
	CST-6262 蟠龙秘境 随机一个奇晶
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.sparScriptID = section["param1"] # 奇晶的scriptID
		self.ballScriptID = section["param2"] # 光球的scriptID
		self.skillID = int(section["param3"]) # 技能ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		sparEntityList = spaceEntity.getEntityMailBoxRecord( self.sparScriptID )
		ballEntityList = spaceEntity.getEntityMailBoxRecord( self.ballScriptID )
		if not len( sparEntityList ):
			return
		sparEntity = random.choice( sparEntityList )
		sparEntity.setIsTrue( True )
		if len( ballEntityList ):
			ballEntityList[0].useSkillToEntity( self.skillID, sparEntity.id )

class SEAction291( SEActionBase ):
	"""
	CST-6262 蟠龙秘境 奇晶移动
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.sparScriptID = section["param1"] # 奇晶的scriptID
		self.maxMoveCount = int(section["param2"]) #奇晶的移动次数
		position = Functions.vector3TypeConvert(section["param3"])
		self.centerPos = Math.Vector3(KBEMath.Unreal2KBEnginePosition(tuple(position)))
		self.radius = float( section["param4"] ) # 半径

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		sparEntityList = spaceEntity.getEntityMailBoxRecord( self.sparScriptID )
		if not len( sparEntityList ):
			return
		sparEntityList[0].sparStartMove( self.maxMoveCount, self.centerPos, self.radius )

SEActionBase.setActionClass("SEAction284", SEAction284)
SEActionBase.setActionClass("SEAction291", SEAction291)

