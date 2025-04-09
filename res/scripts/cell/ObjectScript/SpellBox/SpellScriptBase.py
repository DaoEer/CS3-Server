# -*- coding: utf-8 -*-
from ObjectScript.ObjectScriptBase import GameScript
from ObjectScript.SpellBox import SpellBoxPropertyLoader

class SpellScriptBase( GameScript.GameScript,SpellBoxPropertyLoader.SpellBoxPropertyLoader ):
	def __init__( self ):
		GameScript.GameScript.__init__( self )
		SpellBoxPropertyLoader.SpellBoxPropertyLoader.__init__(self)

	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		GameScript.GameScript.initData( self, data )
		SpellBoxPropertyLoader.SpellBoxPropertyLoader.initData(self,data)
	
	def getEntityProperties( self, params ):
		return SpellBoxPropertyLoader.SpellBoxPropertyLoader.getEntityProperties( self, params )
	
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化entity
		"""
		pass