# -*- coding: utf-8 -*-
class MonsterOwnerInterface():
	def __init__(self):
		self.owners = []
		
	def CLIENT_OnSetBootyOwner( self, p1 ):
		# id 可能是DBID，也可能是teamID
		self.owners = eval( p1 )
