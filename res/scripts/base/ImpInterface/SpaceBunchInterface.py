# -*- coding: utf-8 -*-

class SpaceBunchInterface:
	"""
	副本串功能接口
	"""
	def __init__( self ):
		self.bunchSpaceScriptID = ""
	
	def initData( self, configData ):
		self.bunchSpaceScriptID = configData.get( "bunchSpaceScriptID", "" )
	
	def isBunchChildSpace( self ):
		"""
		此副本是不是副本串中的子副本
		"""
		return self.bunchSpaceScriptID != ""