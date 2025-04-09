# -*- coding: utf-8 -*-

# 副本事件行为
import random
import Math
import KBEMath
import KBEDebug
import KBEngine
import Functions
import csarithmetic
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction189( SEActionBase ):
	"""
	迷幻丛书:开始答题
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.sendRandomQuestion()

class SEAction225( SEActionBase ):
	"""
	迷幻丛书：刷新题目entity
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.onStartFreshEntity()


SEActionBase.setActionClass("SEAction189", SEAction189)
SEActionBase.setActionClass( "SEAction225",SEAction225 )
