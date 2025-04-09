#-*- coding: utf-8 -*-


from StateInterface.StateInterface import StateInterface

import csdefine


STATE_CHANGE_CALL_METHODS_MAPPING = { 
	csdefine.ENTITY_STATE_FREE : ( "onEnterFree", "onLeaveFree" ),
	csdefine.ENTITY_STATE_FIGHT : ( "onEnterFight", "onLeaveFight" ),
	csdefine.ENTITY_STATE_DEAD : ( "onEnterDead", "onLeaveDead" ),
	csdefine.ENTITY_STATE_PEAD : ( "onEnterPead", "onLeavePead"),
	csdefine.ENTITY_STATE_WARN : ( "onEnterWarn", "onLeaveWarn"),
	csdefine.ENTITY_STATE_RESET : ( "onEnterReset", "onLeaveReset"),
	csdefine.ENTITY_STATE_SHOW : ( "onEnterShow", "onLeaveShow"),
	csdefine.ENTITY_STATE_STABLE:( "onEnterStable","onLeaveStable" ),
}

STATE_TO_ACTION_FLAGS = {
			csdefine.ENTITY_STATE_PEAD				: [csdefine.ACTION_FORBID_USE_ITEM, csdefine.ACTION_FORBID_WIELD, csdefine.ACTION_FORBID_ATTACK,
													csdefine.ACTION_FORBID_SPELL, csdefine.ACTION_FORBID_TALK, csdefine.ACTION_FORBID_BE_ATTACK,
													csdefine.ACTION_FORBID_TRIGGER_PASSIVE, csdefine.ACTION_FORBID_BE_HIT_BACK, csdefine.ACTION_FORBID_MOVE, 
													csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_EMERGENCY_EXIT, csdefine.ACTION_FORBID_BE_CONTROL],
			
			csdefine.ENTITY_STATE_FREE				: [],
			csdefine.ENTITY_STATE_WARN				: [],
			csdefine.ENTITY_STATE_FIGHT				: [],
			csdefine.ENTITY_STATE_SHOW				: [csdefine.ACTION_FORBID_BE_HIT_BACK, csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_BE_CONTROL],
			csdefine.ENTITY_STATE_DEAD				: [csdefine.ACTION_FORBID_MOVE, csdefine.ACTION_FORBID_WIELD, csdefine.ACTION_FORBID_ATTACK, csdefine.ACTION_FORBID_SPELL,
													csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_TALK,csdefine.ACTION_FORBID_CONJURE_PET, csdefine.ACTION_FORBID_TRANSLATE_DIRECTION, 
													csdefine.ACTION_FORBID_EMERGENCY_EXIT,csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_BE_CONTROL,
													csdefine.ACTION_FORBID_TRIGGER_PASSIVE, csdefine.ACTION_FORBID_BE_DEPRESS, csdefine.ACTION_FORBID_INSANE],
				
			csdefine.ENTITY_STATE_RESET				: [csdefine.ACTION_FORBID_ATTACK, csdefine.ACTION_FORBID_SPELL, csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_BE_CONTROL
													, csdefine.ACTION_FORBID_BE_DEPRESS, csdefine.ACTION_FORBID_INSANE],
			csdefine.ENTITY_STATE_STABLE: [],
	}


class MonsterStateInterface(StateInterface):
	def __init__(self):
		self.state = csdefine.ENTITY_STATE_PEAD
		self.stateMethodMap = STATE_CHANGE_CALL_METHODS_MAPPING
		self.stateActionFlags = STATE_TO_ACTION_FLAGS
		StateInterface.__init__(self)


	def onEnterFree( self ):
		"""
		virtual method
		进入自由状态
		"""
		pass
		
	def onLeaveFree( self ):
		"""
		virtual method
		离开自由状态
		"""
		pass
	
	def onEnterFight( self ):
		"""
		virtual method
		进入战斗
		"""
		pass
		
	def onLeaveFight( self ):
		"""
		virtual method
		离开战斗
		"""
		pass
	
	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		pass
		
	def onLeaveDead( self ):
		"""
		virtual method
		离开死亡状态
		"""
		pass
		
	def onEnterPead( self ):
		"""
		virtual method
		进入未决状态
		"""
		pass
		
	def onLeavePead( self ):
		"""
		virtual method
		离开未决状态
		"""
		pass
		
	def onEnterWarn( self ):
		"""
		virtual method
		进入警戒状态
		"""
		pass
		
	def onLeaveWarn( self ):
		"""
		virtual method
		离开警戒状态
		"""
		pass
		
	def onEnterReset( self ):
		"""
		virtual method
		进入重置状态
		"""
		pass
		
	def onLeaveReset( self ):
		"""
		virtual method
		离开重置状态
		"""
		pass

	def onEnterShow( self ):
		"""
		virtual method
		进入表演状态
		"""
		pass

	def onLeaveShow( self ):
		"""
		virtual method
		离开表演状态
		"""
		pass

	def onEnterStable( self ):
		"""
		virtual method
		进入稳定状态
		"""
		pass

	def onLeaveStable( self ):
		"""
		virtual method
		离开稳定状态
		"""
		pass
