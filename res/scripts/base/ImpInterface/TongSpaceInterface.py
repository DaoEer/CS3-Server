# -*- coding: utf-8 -*-


class TongSpaceInterface( object ):
	def __init__( self ):
		object.__init__( self )
	
	def reqCreateTongSpace( self ):
		pass
	
	def reqTongSpaceData( self ):
		pass
	
	def reqEnterTongSpace( self ):
		pass
		
	def getMaxMember( self ):
		"""获取帮会人数上限"""
		return 10