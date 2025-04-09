# -*- coding: utf-8 -*-

import csdefine
from ObjectScript.ObjectScriptBase.GameScript import GameScript

class SpaceChild( object ):
	def __init__( self, bunchObj, index ):
		self.bunchObj = bunchObj
		self.index = index
		self.spaceScriptIDs = []

	def initData( self, info ):
		self.spaceScriptIDs = info.get("spaceList",[])

	def getFirstSpaceScriptID( self ):
		return self.spaceScriptIDs[0]

class BunchSpaceBase( GameScript ):
	"""
	副本串script对象
	它不是一个真正的副本script，只是起到一个读取数据的作用
	"""
	def __init__( self ):
		GameScript.__init__( self )
		self.scriptID = ""
		self.bunchType = 0
		self._belongType = []
		self.childSpaces = {}
		self.bunchSpaceName = ""
	
	def initData( self, configData ):
		GameScript.initData( self, configData )
		self.scriptID = configData[ "scriptID" ]
		self.bunchSpaceName = configData["SpaceName"]
		self.bunchType = getattr( csdefine, configData[ "bunchType" ] )
		self._belongType = [ int(i) for i in configData[ "belongType" ].split("|") ]
		for index, info in configData[ "ChildSpace" ].items():
			child = SpaceChild( self, index )
			child.initData(info)
			self.childSpaces[ index ] = child

	def getBunchSpaceName( self ):
		"""
		获得副本串名字
		"""
		return self.bunchSpaceName
	
	def getAllChildScriptID( self ):
		"""
		"""
		result = []
		for child in self.childSpaces.values():
			result.extend(child.spaceScriptIDs)
		return result
	
	def getChildSpaceScriptIDByIndex( self, index ):
		"""
		获得子副本的spaceScriptID
		"""
		return self.childSpaces[index].getFirstSpaceScriptID()