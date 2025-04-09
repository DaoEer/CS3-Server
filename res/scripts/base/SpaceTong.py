# -*- coding: utf-8 -*-

from CoreObject.SpaceObject import SpaceObject

class SpaceTong( SpaceObject ):
	def __init__( self ):
		self.tongDBID = self.cellData["tongDBID"]
		SpaceObject.__init__( self )
		
	def tongOnDismiss( self ):
		"""
		define method
		帮会解散
		"""
		self.cell.tongOnDismiss()
		