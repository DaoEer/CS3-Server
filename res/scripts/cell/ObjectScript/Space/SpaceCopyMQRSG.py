# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import KBEDebug

class SpaceCopyMQRSG( SpaceCopyRingTaskChild ):
	"""
	冥气人参果副本
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )
		self.cikuCoordList = []
		self.cikuCoordList1 = []
		self.monsterScriptIDList = []
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		cikuCoordList = configData["SpaceData"].get("cikuCoordList", "")					
		if cikuCoordList:
			self.cikuCoordList = cikuCoordList.split("|")
		cikuCoordList1 = configData["SpaceData"].get("cikuCoordList1", "")
		if cikuCoordList1:
			self.cikuCoordList1 = cikuCoordList1.split("|")
		monsterScriptIDList = configData["SpaceData"].get( "monsterScriptIDList", "" )
		if monsterScriptIDList:
			self.monsterScriptIDList = monsterScriptIDList.split("|")

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyRingTaskChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.cikuCoordList, self.cikuCoordList1, self.monsterScriptIDList )

