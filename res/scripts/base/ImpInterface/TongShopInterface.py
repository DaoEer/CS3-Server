# -*- coding: utf-8 -*-

class TongShopInterface( object ):
	
	
	def addContribution( self, playerDBID, num ):
		"""
		define method
		添加帮贡
		"""
		if playerDBID in self.members:
			self.members[playerDBID].addContribution( self, num )
		
	def subContribution( self, playerDBID, num, order ):
		"""
		define method
		减少帮贡
		"""
		if playerDBID in self.members:
			self.members[playerDBID].sudContribution( self, num, True, order )