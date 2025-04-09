# -*- coding: utf-8 -*-

import imp

import KBEngine
import KBEDebug

import csdefine
from ConfigObject.SpellBoxAdvancedState import SpellBoxAdvancedActions
from ConfigObject.SpellBoxAdvancedState import SpellBoxAdvancedConditions
from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase.SpellBoxAdvancedGroupState import SpellBoxAdvancedGroupState

#加载配置
import SpellBoxAdvancedState

class SpellBoxAdvancedStateMgr:
	"""
	"""
	def __init__( self ):
		"""
		"""
		self.dct = {}
	
	def getSpellBoxAdvancedGroupState( self, entity ):
		"""
		"""
		scriptID = entity.getScriptID()
		if scriptID not in self.dct:
			self.loadSpellBoxAdvancedState( scriptID )
		
		return self.dct[ scriptID ]
		
	def loadSpellBoxAdvancedState( self, scriptID ):
		"""
		加I配置
		"""
		#配置
		config = SpellBoxAdvancedState.getConfig( scriptID )
		
		#脚本
		if config:
			obj = SpellBoxAdvancedGroupState( scriptID )
			self.dct[ scriptID ] = obj
			self.dct[ scriptID ].initData( config )
		else:
			self.dct[ scriptID ] = None
	
	def reloadSpellBoxAdvancedState( self, scriptID ):
		"""
		重新加载配置
		"""
		self.reloadActions()
		self.reloadConditions()
		
		#配置
		try:
			config = SpellBoxAdvancedState.reloadConfig( scriptID )
		except Exception as e:
			KBEDebug.ERROR_MSG("SpellBoxAdvancedState.reloadConfig( %s ) failed!  error:%s" %(scriptID, e))
			return False
		
		#脚本
		if config:
			obj = SpellBoxAdvancedGroupState( scriptID )
			self.dct[ scriptID ] = obj
			self.dct[ scriptID ].initData( config )
			return True
		else:
			self.dct[ scriptID ] = None
			
		return False

	def reloadConditions( self ):
		"""
		热更新条件脚本
		"""
		imp.reload(SpellBoxAdvancedConditions)
		
	def reloadActions( self ):
		"""
		热更新行为脚本
		"""
		imp.reload(SpellBoxAdvancedActions)
		

g_spellBoxAdvancedStateMgr = SpellBoxAdvancedStateMgr()
