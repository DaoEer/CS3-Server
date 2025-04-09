# -*- coding: utf-8 -*-
import csdefine
from ObjectScript.ObjectScriptBase.GameScript import GameScript
import Math
import KBEMath
import Functions
import KBEDebug

class SpaceBase( GameScript ):
	"""
	空间领域
	"""
	def __init__( self ):
		GameScript.__init__( self )
		self.scriptID = ""
		self._spaceType = 0
		self._belongType = []		#同一个副本可以有多种归属
		self._spaceName = ""
		self._exitScriptID = ""
		self._exitPosition = Math.Vector3(0.0, 0.0, 0.0)
		self._exitDirection = Math.Vector3(0.0, 0.0, 0.0)
	
	def initData( self, configData ):
		GameScript.initData( self, configData )
		self.scriptID = configData[ "scriptID" ]
		self._spaceType = getattr( csdefine, configData[ "spaceType" ] )
		self._belongType = [ int(i) for i in configData[ "belongType" ].split("|") ]
		self._spaceName = configData.get("SpaceName","")
		if "ExitSpace" in configData:
			self._exitScriptID = configData["ExitSpace"].get( "ScriptID", "")
			posStr = configData["ExitSpace"].get( "Position", "" )
			pos = Functions.vector3TypeConvert( posStr )
			if pos:
				self._exitPosition = KBEMath.Unreal2KBEnginePosition( pos )
			dirStr = configData["ExitSpace"].get( "Direction", "" )
			dir = Functions.vector3TypeConvert( dirStr )
			if dir:
				self._exitDirection = KBEMath.Unreal2KBEngineDirection( dir )

	def getSpaceBelongTypes( self ):
		"""
		获得副本归属
		"""
		return self._belongType

	def getEntityProperties( self, params ):
		entityDict = GameScript.getEntityProperties( self, params )
		return entityDict
		
	def teleportEntity( self, selfEntity, roleBase, position, direction, packArgs ):
		selfEntity.cell.teleportEntity( roleBase, position, direction, packArgs )
	
	def getSpaceName( self ):
		"""
		获得SpaceName
		"""
		return self._spaceName

	def getReviveToExitInfo( self, playerRole, pickArgs ):
		return ( self._exitScriptID, self._exitPosition, self._exitDirection )
