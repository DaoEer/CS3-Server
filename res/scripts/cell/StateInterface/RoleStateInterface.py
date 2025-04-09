#-*- coding: utf-8 -*-


from StateInterface.StateInterface import StateInterface


import csdefine
import KBEngine
import KBEDebug


STATE_CHANGE_CALL_METHODS_MAPPING = { 
	csdefine.ENTITY_STATE_FREE : ( "onEnterFree", "onLeaveFree" ),
	csdefine.ENTITY_STATE_FIGHT : ( "onEnterFight", "onLeaveFight" ),
	csdefine.ENTITY_STATE_DEAD : ( "onEnterDead", "onLeaveDead" ),
	csdefine.ENTITY_STATE_PEAD : ( "onEnterPead", "onLeavePead"),
	csdefine.ENTITY_STATE_WARN : ( "onEnterWarn", "onLeaveWarn"),
	csdefine.ENTITY_STATE_STALL:( "onEnterStall","onLeaveStall" ),
}


STATE_TO_ACTION_FLAGS = {
			csdefine.ENTITY_STATE_PEAD				: [csdefine.ACTION_FORBID_USE_ITEM , csdefine.ACTION_FORBID_WIELD , csdefine.ACTION_FORBID_ATTACK 
				, csdefine.ACTION_FORBID_SPELL , csdefine.ACTION_FORBID_TALK , csdefine.ACTION_FORBID_BE_ATTACK , csdefine.ACTION_FORBID_TRIGGER_PASSIVE 
				, csdefine.ACTION_FORBID_BE_HIT_BACK , csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_JUMP , csdefine.ACTION_FORBID_EMERGENCY_EXIT
				, csdefine.ACTION_FORBID_BE_CONTROL],
			
			csdefine.ENTITY_STATE_FREE				: [],
			csdefine.ENTITY_STATE_WARN				: [],
			csdefine.ENTITY_STATE_FIGHT				: [],
			csdefine.ENTITY_STATE_STALL				: [csdefine.ACTION_FORBID_MOVE, csdefine.ACTION_FORBID_USE_ITEM , csdefine.ACTION_FORBID_SPELL 
				, csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_BE_CONTROL, csdefine.ACTION_FORBID_WIELD
				, csdefine.ACTION_FORBID_ATTACK, csdefine.ACTION_FORBID_BE_HIT_BACK, csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_EMERGENCY_EXIT
				, csdefine.ACTION_FORBID_TALK, csdefine.ACTION_FORBID_BE_DEPRESS, csdefine.ACTION_FORBID_INSANE],
			
			csdefine.ENTITY_STATE_DEAD				: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_WIELD 
				, csdefine.ACTION_FORBID_ATTACK , csdefine.ACTION_FORBID_SPELL , csdefine.ACTION_FORBID_JUMP , csdefine.ACTION_FORBID_TALK 
				, csdefine.ACTION_FORBID_CONJURE_PET , csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_EMERGENCY_EXIT
				, csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_BE_CONTROL,csdefine.ACTION_FORBID_TRIGGER_PASSIVE, csdefine.ACTION_FORBID_BE_DEPRESS
				, csdefine.ACTION_FORBID_INSANE],
	}

class RoleStateInterface(StateInterface):
	def __init__(self):
		self.state = csdefine.ENTITY_STATE_FREE
		self.stateMethodMap = STATE_CHANGE_CALL_METHODS_MAPPING
		self.stateActionFlags = STATE_TO_ACTION_FLAGS
		StateInterface.__init__(self)

	def onEnterFree(self):
		"""
		"""
		pass

	def onLeaveFree(self):
		"""
		"""
		pass

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		pass

	def onLeaveDead(self):
		"""
		"""
		pass

	def onEnterFight(self):
		"""
		"""
		pass

	def onLeaveFight(self):
		"""
		"""
		pass

	def onEnterPead(self):
		"""
		"""
		self.ChangeRoleJumpState(self.id, csdefine.JUMP_SHOW_STATE_STAND, True)

	def onLeavePead(self):
		"""
		"""
		pass

	def onEnterWarn(self):
		"""
		"""
		pass

	def onLeaveWarn(self):
		"""
		"""
		pass

	def onEnterStall(self):
		"""
		"""
		pass

	def onLeaveStall(self):
		"""
		"""
		pass

	def ChangeRoleJumpState(self, srcEntityID, jumpShowState, isServerCall):
		"""
		<Exposed method>
		申请改变玩家状态
		"""
		#CST-11882 当玩家传送之后客户端继续调用此接口修改了跳跃状态会引起bug,因此加入一个处理：
		#当玩家在未决状态的时候，不接受客户端的请求。
		if not isServerCall and (self.isInPending or self.getState()==csdefine.ENTITY_STATE_PEAD or self.getState()==csdefine.ENTITY_STATE_DEAD):
			return

		if not self.validateClientCall( srcEntityID ):
			return
		if self.jumpShowState == jumpShowState:
			return
		oldState = self.jumpShowState
		newState = jumpShowState
		self.OnChangeRoleJumpState(oldState, newState)
		self.allClients.OnRepJumpState(newState)
		self.jumpShowState = newState
		
	def ChangeClimbLadderState( self, srcEntityID, climbLadderState ):
		"""
		<Exposed method>
		改变玩家爬梯子状态
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.climbLadderState == climbLadderState:
			return
		self.climbLadderState = climbLadderState

	def UpdateClimbLadderActionStepPos( self, srcEntityID, ladderPosOffset ):
		"""
		<Exposed method>
		改变玩家爬梯子偏移
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.ladderPosOffset = ladderPosOffset
