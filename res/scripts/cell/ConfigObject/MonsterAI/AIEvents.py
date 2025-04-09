# -*- coding: utf-8 -*-
import csdefine

#用于AI事件的拓展
from ConfigObject.MonsterAI.AIBase import AIEventBase

class AIEventEnemyChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventDamageChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventCureChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventFriendChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventAttackRemove( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventHPChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )
	
class AIEventMPChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventEnterAttackRange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )
		
class AIEventCommand( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

class AIEventStateChange(AIEventBase.AIEventBase ):
	def __init__(self,eventType):
		AIEventBase.AIEventBase.__init__( self, eventType)

class AIEventOutOfTerritory(AIEventBase.AIEventBase ):
	def __init__(self,eventType):
		AIEventBase.AIEventBase.__init__( self, eventType)

class AIEventTriggerProximity(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerDestorySelf(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerSkillSuccessful(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerSkillFailure(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)
		
class AIEventTriggerOnLeftMouseDoubleClick(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)
		
class AIEventTriggerGossipWith(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerLeaveBattle(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerOnWitnessed(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerGangqiChange(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerOnEnterFree(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerOnEnterFight(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerChangeMoveType(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerStopPlaySound(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventPlayerBeginPush(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventTriggerSpecialAttributesChange(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventPlayerEndPush(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventActionCompleted(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)
		
class AIEventMemberSoldierChange(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventBeKill(AIEventBase.AIEventBase):
	def __init__(self, eventType):
		AIEventBase.AIEventBase.__init__(self,eventType)

class AIEventHatredChange( AIEventBase.AIEventBase ):
	def __init__( self, eventType ):
		AIEventBase.AIEventBase.__init__( self, eventType )

AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ENEMY_CHANGED, AIEventEnemyChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_DAMAGE_CHANGED, AIEventDamageChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_CURE_CHANGED, AIEventCureChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_FRIEND_CHANGED, AIEventFriendChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ATTACKER_REMOVE, AIEventAttackRemove )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_HP_CHANGE, AIEventHPChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_MP_CHANGE, AIEventMPChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ENTER_ATTACK_RANGE, AIEventEnterAttackRange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_COMMAND, AIEventCommand )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE, AIEventStateChange )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_OUT_OF_TERRITORY, AIEventOutOfTerritory )
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_TRIGGER_PROXIMITY,AIEventTriggerProximity)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_DESTORY_SELF,AIEventTriggerDestorySelf)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_SKILL_SUCCESSFUL,AIEventTriggerSkillSuccessful)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_SKILL_FAILURE,AIEventTriggerSkillFailure)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_LEFT_MOUSE_DOUBLE_CLICK,AIEventTriggerOnLeftMouseDoubleClick)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_GOSSIP_WITH_MONSTER,AIEventTriggerGossipWith)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ACTIVE_LEAVE_BATTLE,AIEventTriggerLeaveBattle)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_WITNESSED,AIEventTriggerOnWitnessed)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_GANG_QI_CHANGE,AIEventTriggerGangqiChange)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_ENTER_FREE,AIEventTriggerOnEnterFree)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_ENTER_FIGHT,AIEventTriggerOnEnterFight)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_CHANGE_MOVE_TYPE,AIEventTriggerChangeMoveType)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_STOP_PLAY_SOUND,AIEventTriggerStopPlaySound)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE,AIEventTriggerSpecialAttributesChange)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_PLAYER_BEGIN_PUSH,AIEventPlayerBeginPush)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ON_PLAYER_END_PUSH,AIEventPlayerEndPush)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ACTION_COMPLETED,AIEventActionCompleted)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_ACTION_COMPLETED,AIEventActionCompleted)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_MEMBER_SOLDIER_CHANGE,AIEventMemberSoldierChange)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_BE_KILL,AIEventBeKill)
AIEventBase.AIEventBase.setEventClass( csdefine.ENTITY_EVENT_HATRED_CHANGED, AIEventHatredChange )