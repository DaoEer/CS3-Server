# -*- coding: utf-8 -*-
import csdefine

#用于事件的拓展
from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase import SpellBoxAdvancedEventBase

class SpellBoxAdvancedEventInteractive( SpellBoxAdvancedEventBase.SpellBoxAdvancedEventBase ):
	"""
	交互事件
	"""
	def __init__( self, eventType ):
		SpellBoxAdvancedEventBase.AIEventBase.__init__( self, eventType )

	
SpellBoxAdvancedEventBase.SpellBoxAdvancedEventBase.setEventClass( csdefine.SPELLBOXADVANCED_EVENT_INTERACTIVE, SpellBoxAdvancedEventInteractive )
