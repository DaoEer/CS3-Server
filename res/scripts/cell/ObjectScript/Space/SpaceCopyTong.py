# -*- coding: utf-8 -*-


import KBEDebug
import Math
import KBEMath
import Functions
import csdefine
import Const
from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyTong( SpaceCopy ):
	"""
	帮会副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.spaceName = ""
		self.doorScriptID = []
		self.pos = []
		self.dir = []
		self.reqLevel = 0
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		if "SpaceName" in configData:
			self.spaceName = configData["SpaceName"]
			
		if "doorData" in configData["SpaceData"]:
			for doorData in configData["SpaceData"]["doorData"]:
				self.doorScriptID.append( doorData["scriptID"] )
				_pos = Functions.vector3TypeConvert( doorData["position"] )
				self.pos.append( KBEMath.Unreal2KBEnginePosition( _pos ) )
				_dir = Functions.vector3TypeConvert( doorData["direction"] )
				self.dir.append( KBEMath.Unreal2KBEngineDirection( _dir ) )
		
		if "reqLevel" in configData["SpaceData"]:
			self.reqLevel = configData["SpaceData"]["reqLevel"]
		
		import ObjectScript.Space as space
		space.registerTongSpaceCopy( self.scriptID, self.reqLevel )
		
	def getSpaceName( self ):
		return self.spaceName
		
	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.onEnterTongSpaceCopy()
		if playerRole.getActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY ) == 2:
			playerRole.addKMGXiuweiRate( Const.TONG_SPACE_COPY_XIUWEI_RATE )				# CST-13701，在这里处理比较安全！
		
	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		if playerRole.getActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY ) == 2:
			playerRole.removeKMGXiuweiRate( Const.TONG_SPACE_COPY_XIUWEI_RATE )				# CST-13701
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		"""
		SpaceCopy.onSpaceSuccess( self, selfEntity, isShowTimeCountDown )
		role = selfEntity._spaceRoles[0]
		for index, scriptID in enumerate( self.doorScriptID ):
			role.createEntityByScriptID( str(scriptID), self.pos[index], self.dir[index], {} )