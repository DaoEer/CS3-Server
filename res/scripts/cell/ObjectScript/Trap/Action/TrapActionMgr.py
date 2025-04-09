# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
import KBEDebug
from ObjectScript.Trap.Action.TrapNormalAction import *
from ObjectScript.Trap.Action.TrapInitAction import *
from ObjectScript.Trap.Action.TrapCycleAction import *
from ObjectScript.Trap.Action.TrapHoldAction import *
from Singleton import Singleton

class TrapActionMgr( Singleton ):
	"""
	陷阱触发效果
	"""
	def __init__( self ):
		"""
		"""
		self.initActionMap = {
			csdefine.TRAP_INIT_ACTION_ADD_BUFF:TrapInitActionAddBuff,											# 初始化行为
		}
		self.normalActionMap = {											# 进入/离开 行为
			csdefine.TRAP_NORMAL_ACTION_ENTER_PLANE		:	TrapNormalActionEnterPlane,
			csdefine.TRAP_NORMAL_ACTION_LEAVE_PLANE		:	TrapNormalActionLeavePlane,
			csdefine.TRAP_NORMAL_ACTION_SPELL_TARGET	:	TrapNormalActionSpell,
			csdefine.TRAP_NORMAL_ACTION_HITBACK			:	TrapNormalActionHitBack,
			csdefine.TRAP_NORMAL_ACTION_DEAD_SELF		:	TrapNormalActionDeadSelf,
			csdefine.TRAP_NORMAL_ACTION_START_WALK		:	TrapNormalActionStartWalk,
			csdefine.TRAP_NORMAL_ACTION_CREATEENTITY	:	TrapNormalActionCreateEntity,
			csdefine.TRAP_NORMAL_ACTION_SPACE_DOOR_TELEPORT	: TrapNormalSpaceDoorTeleport,
			csdefine.TRAP_NORMAL_ACTION_CHANGE_SPACE_LIFE	: TrapNormalChangeSpaceLife,
			csdefine.TRAP_NORMAL_ACTION_PLAY_ACTION		:	TrapNormalPlayAction,
			csdefine.TRAP_NORMAL_ACTION_GET_REWARD		:	TrapNormalGetReward,
			csdefine.TRAP_NORMAL_ACTION_SET_DIRECTION	:	TrapNormalSetDirection,
			csdefine.TRAP_NORMAL_ACTION_SET_TEMP		:	TrapNormalSetTemp,
			csdefine.TRAP_NORMAL_ACTION_CONDITIONCHANGE :	TrapNormalConditionChange,
			csdefine.TRAP_NORMAL_ACTION_CREATE_HEHUA    :	TrapNormalCreateHeHua,
			csdefine.TRAP_NORMAL_ACTION_GET_ITEM	    :	TrapNormalGetItem,
			csdefine.TRAP_NORMAL_ACTION_HQLZ_CREATE_ENTITY :TrapNormalHQLZCreateEntity,
			csdefine.TRAP_NORMAL_ACTION_TELEPORT_NEAREST_ENTITY:TrapNormalTeleportNearestEntity,
			csdefine.TRAP_NORMAL_ACTION_TELEPORT_RANDOM_POSITION:TrapNormalTeleportRandomPosition,
			csdefine.TRAP_NORMAL_ACTION_SPELL_SELF 		: 	TrapNormalActionSpellSelf,
			csdefine.TRAP_NORMAL_ACTION_REMOVE_BUFF 	:  	TrapNormalRemoveBuff,
			csdefine.TRAP_NORMAL_ACTION_T_SPELL_SELF 	:  	TrapNormalActionTriggerSpellSelf,
		}
		self.cycleActionMap = {												# 循环行为
			csdefine.TRAP_CYCLE_ACTION_USE_SKILL		:	TrapCycleActionUseSkill,
			csdefine.TRAP_CYCLE_ACTION_CREATE_ENTITY	:	TrapCycleActionCreateEntity,
			csdefine.TRAP_CYCLE_ACTION_CHECKAROUND		:	TrapCycleActionSparHunTingCheck,
			csdefine.TRAP_CYCLE_ACTION_CHECKHASPLAYER	:	TrapCycleActionCheckHasPlayer,
			csdefine.TRAP_CYCLE_ACTION_BATTLEFLAG_CHECK : 	TrapCycleActionBattleFlagCheck,
			csdefine.TRAP_CYCLE_ACTION_BARRACKS_REVIVE_CHECK 	: 	TrapCycleActionBarracksReviveCheck,
		}
		self.holdActionMap = {												# 持有行为
			csdefine.TRAP_HOLD_ACTION_UNCONTROL			:	TrapHoldActionUncontrollable,
			csdefine.TRAP_HOLD_ACTION_INVINCIBLE		:	TrapHoldActionInvincible,
			csdefine.TRAP_HOLD_ACTION_SUCK				:	TrapHoldActionSuck,
			csdefine.TRAP_HOLD_ACTION_BUFF				:	TrapHoldActionBuff,
		}
		
	def getInitType( self, type ):
		"""根据类型初始化"""
		return self.initActionMap.get( type, None )
		
	def init( self, selfEntity, type, value ):
		"""
		陷阱初始化
		@param selfEntity : 陷阱本身对象
		@type  selfEntity : entity
		@param type : 陷阱初始化关键字
		@type type : Int
		@param value : 陷阱行为数据
		@type value : List
		"""
		initFunc = self.getInitType( type )
		if initFunc:
			initFunc.init( selfEntity, value )

	def getActionType( self, type ):
		"""
		根据类型给予效果
		"""
		return self.normalActionMap.get( type, None )

	def action( self, selfEntity, avatar, type, value ):
		"""
		触发陷阱
		@param selfEntity: 陷阱本身对象
		@type  selfEntity: ENTITY
		@param avatar: 触发对象
		@type  avatar: ENTITY
		@param type: 陷阱行为关键字
		@type  type: INT
		@param value: 陷阱行为数据
		@type  value: LIST
		"""
		actionFunc = self.getActionType( type )
		if actionFunc == None:
			return

		actionFunc.do( selfEntity, avatar, value )
		
	def getCycleType( self, type ):
		"""根据类型执行周期行为"""
		return self.cycleActionMap.get( type, None )
		
	def cycleBegin( self, selfEntity, index, value ):
		"""
		陷阱开启周期性行为
		@param selfEntity : 陷阱本身对象
		@type  selfEntity : entity
		@param index : 索引
		@type index : Int
		@param value : 陷阱行为数据
		@type value : List
		"""
		cycleFunc = self.getCycleType( value["scriptKey"] )
		if cycleFunc:
			cycleFunc.cycleBegin( selfEntity, index, value )
		else:
			KBEDebug.ERROR_MSG( "Trap(scriptID:%s) can not find cycle action(scriptKey:%s)!!"%(selfEntity.scriptID, value["scriptKey"]))
			
	def cycleEnd( self, selfEntity, index, value ):
		"""
		陷阱结束周期性行为
		"""
		cycleFunc = self.getCycleType( value["scriptKey"] )
		if cycleFunc:
			cycleFunc.cycleEnd( selfEntity, index, value )
		else:
			KBEDebug.ERROR_MSG( "Trap(scriptID:%s) can not find cycle action(scriptKey:%s)!!"%(selfEntity.scriptID, value["scriptKey"]))
			
	def cycleDo( self, selfEntity, type, value ):
		"""
		陷阱执行周期性行为
		"""
		cycleFunc = self.getCycleType( type )
		if cycleFunc:
			cycleFunc.cycleDo( selfEntity, value )
			
	def getHoldType( self, type ):
		"""根据类型获取持续行为"""
		return self.holdActionMap.get( type, None )
		
	def holdBegin( self, selfEntity, targetEntity, type, value ):
		"""
		持续性行为
		@param selfEntity : 陷阱本身对象
		@type  selfEntity : entity
		@param targetEntity : 进入陷阱实体
		@param targetEntity : entity
		@type type : Int
		@param value : 陷阱行为数据
		@type value : List
		"""
		holdFunc = self.getHoldType( type )
		if holdFunc:
			holdFunc.onBegin( selfEntity, targetEntity, value )
			
	def holdEnd( self, selfEntity, targetEntity, type, value ):
		"""
		陷阱结束持续性行为
		"""
		holdFunc = self.getHoldType( type )
		if holdFunc:
			holdFunc.onEnd( selfEntity, targetEntity, value )


g_trapActionMgr = TrapActionMgr()