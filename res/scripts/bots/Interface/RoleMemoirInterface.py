# -*- coding: utf-8 -*-
class RoleMemoirInterface( object ):
	def __init__( self ):
		pass
	
	def AddMemoirStory( self, str1, str2 ):
		pass
	
	def ReceiveMemoirIDList( self, strList ):
		pass
	
	def PlayMemoirCG( self, memoirID, nextMemoirID ):
		pass
	def CLIENT_ReceiveMemoirIDList( self, p1 ):
		pass
	def CLIENT_AddMemoirStory( self, p1, p2 ):
		pass
	def CLIENT_PlayMemoirCG( self, p1, p2 ):
		pass
