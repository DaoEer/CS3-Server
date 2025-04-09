#-*- coding: utf-8 -*-


from StateInterface.StateInterface import StateInterface


import csdefine


STATE_CHANGE_CALL_METHODS_MAPPING = { 
	csdefine.ENTITY_STATE_FREE : ( "onEnterFree", "onLeaveFree" ),
	csdefine.ENTITY_STATE_DEAD : ( "onEnterDead", "onLeaveDead" ),
}
GET_ENTER_STATE_CALL_METHOD = lambda entity, state:getattr( entity, STATE_CHANGE_CALL_METHODS_MAPPING.get( state )[0] )
GET_LEAVE_STATE_CALL_METHOD = lambda entity, state:getattr( entity, STATE_CHANGE_CALL_METHODS_MAPPING.get( state )[1] )


STATE_TO_ACTION_FLAGS = {
			csdefine.ENTITY_STATE_FREE				: [],
			csdefine.ENTITY_STATE_DEAD				: [csdefine.ACTION_FORBID_ATTACK , csdefine.ACTION_FORBID_SPELL , csdefine.ACTION_FORBID_TALK
				, csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_BE_CONTROL
				, csdefine.ACTION_FORBID_BE_DEPRESS],
	}


class TrapStateInterface(StateInterface):
	def __init__(self):
		self.stateMethodMap = STATE_CHANGE_CALL_METHODS_MAPPING
		self.stateActionFlags = STATE_TO_ACTION_FLAGS
		self.state = csdefine.ENTITY_STATE_FREE
		StateInterface.__init__(self)

	def onEnterFree(self):
		"""
		"""
		pass

	def onLeaveFree(self):
		"""
		"""
		pass

	def onEnterDead(self):
		"""
		"""
		pass
		
	def onLeaveDead(self):
		"""
		"""
		pass

