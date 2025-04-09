# -*- coding: utf-8 -*-
#
import csdefine
import csconst
import csstatus
import KBEngine
from KBEDebug import *
import ConfigObject.Skill.SkillBase.Skill as Skill
import Const
import math
import Math

DISTANCE_OWNER_MAX		= 30	#距离主人最大的距离 
AI_TICK_REPEAT				= 0.5	#AI循环时间
AI_START_TIME_VALUE 		= 0.1	#AI开始时间

FIND_ENEMY_RANGE 					= 12.0	#检查范围
DISTANCE_OWNER_ATTACK_MAX		= 20.0	#可以攻击距离主人最远距离的怪物
DISTANCE_TELEPORT					= 30	#距离主人大于这个距离认为是传送 
DISTANCE_TELEPORT_FREE				= 6		#距离主人大于这个距离认为是传送 自由
DISTANCE_HIGH						= 5		#距离主人大于这个高度传送

FOLLOW_OWNER_RANGE = 1.5

ATTACK_TYPE_DEFENSE		    =	1	#防御
ATTACK_TYPE_INITIATIVE		=	2	#主动
ATTACK_TYPE_PASSIVITY		=	3	#被动

PET_COMMAND_STAY			=	1	#停留
PET_COMMAND_FOLLOW		    =	2	#跟随
ATTACK_STATE_LIST = [ ATTACK_TYPE_DEFENSE, ATTACK_TYPE_INITIATIVE, ATTACK_TYPE_PASSIVITY ]

class PetAIStateBase( object ):
	_CLASS = {}
	def __init__( self ):
		pass
		
	@classmethod
	def setClassObject( SELF, state, objectClass ):
		SELF._CLASS[ state ] = objectClass
	
	@classmethod
	def getClassObject( SELF, state ):
		return SELF._CLASS[ state ]
	
	def onTick( self, entity ):
		pass
	
	def onEnter( self, entity ):
		"""
		进入模式
		"""
		pass
		
	def onLeave( self, entity ):
		"""
		离开模式
		"""
		pass
	
	def onOwnerAddEnemy( self, entity, enemyID ):
		"""
		主人加敌人列表
		"""
		pass
	
	def selectAttackTarget( self, entity ):
		pass
	
class PetAIStateDefend( PetAIStateBase ):
	"""
	防御
	"""
	def onTick( self, entity ):
		if entity.AIIsCanAttackTargetID( entity.AIOwnerSetTargetID ):
			entity.AIAttackTargetID = entity.AIOwnerSetTargetID
		else:
			entity.AIOwnerSetTargetID = 0
			
		ownerEntity = entity.getOwnerEntity()
		
		if  ownerEntity != None and ( entity.AIAttackTargetID != 0 or ownerEntity.getState() == csdefine.ENTITY_STATE_FIGHT ):
			entity.AIAttack()
		
		if  ownerEntity == None or entity.AIAttackTargetID == 0:
			entity.AIFollow()
	
	def selectAttackTarget( self, entity ):
		"""
		查找攻击目标
		"""
		owner = entity.getOwnerEntity()
		if owner:
			enemyID = owner.findEnemyByMaxDamage() #选择主人仇恨最大的敌人
			if enemyID == 0:
				enemyID = entity.findEnemyByMaxDamage() #选择自己仇恨最大的敌人
			
			if enemyID == 0:
				enemyID = owner.findFirstEnemyByTime()
				
			if enemyID and entity.AIIsCanAttackTargetID( enemyID ): #如果可以选择
				entity.AIAttackTargetID = enemyID

class PetAIStateInitiative( PetAIStateBase ):
	"""
	主动
	"""
	def onTick( self, entity ):
		if entity.AIIsCanAttackTargetID( entity.AIOwnerSetTargetID ):
			entity.AIAttackTargetID = entity.AIOwnerSetTargetID
		else:
			entity.AIOwnerSetTargetID = 0
			
		entity.AIAttack()
		if entity.AIAttackTargetID == 0:
			entity.AIFollow()
	
	def selectAttackTarget( self, entity ):
		"""
		选择攻击目标
		"""
		owner = entity.getOwnerEntity()
		if owner:
			enemyID = owner.findEnemyByMaxDamage() #选择主人仇恨最大的敌人
			if enemyID == 0:
				enemyID = entity.findEnemyByMaxDamage() #选择自己仇恨最大的敌人
				
			if enemyID == 0:
				enemyID = owner.findFirstEnemyByTime()
			
			if enemyID and entity.AIIsCanAttackTargetID( enemyID ): #如果可以选择
				entity.AIAttackTargetID = enemyID
			else:
				entity.AIFindRangeEnemy()

class PetAIStatePassivity( PetAIStateBase ):
	"""
	被动
	"""
	def onTick( self, entity ):
		if entity.AIIsCanAttackTargetID( entity.AIOwnerSetTargetID ):
			entity.AIAttackTargetID = entity.AIOwnerSetTargetID
		else:
			entity.AIOwnerSetTargetID = 0
		
		if entity.AIAttackTargetID == 0:
			entity.AIFollow()
		else:
			entity.AIAttack()
	
	def selectAttackTarget( self, entity ):
		"""
		选择攻击目标
		"""
		pass


PetAIStateBase.setClassObject( ATTACK_TYPE_DEFENSE,  PetAIStateDefend() )
PetAIStateBase.setClassObject( ATTACK_TYPE_INITIATIVE,  PetAIStateInitiative() )
PetAIStateBase.setClassObject( ATTACK_TYPE_PASSIVITY,  PetAIStatePassivity() )

class PetAICmdBase( object ):
	_CLASS = {}
	def __init__( self ):
		self.cmdType = 0
		
	@classmethod
	def setClassObject( SELF, cmd, objectClass ):
		SELF._CLASS[ cmd ] = objectClass
	
	@classmethod
	def getClassObject( SELF, cmd ):
		return SELF._CLASS[ cmd ]
	
	def onTick( self, entity ):
		pass
	
	def onEnter( self, entity ):
		"""
		进入模式
		"""
		pass
		
	def onLeave( self, entity ):
		"""
		离开模式
		"""
		pass

class PetAICmdFollow( PetAICmdBase ):
	def __init__( self ):
		PetAICmdBase.__init__( self )
		self.cmdType = PET_COMMAND_FOLLOW
	
	def onTick( self, entity ):
		owner = entity.getOwnerEntity()
		dist = FOLLOW_OWNER_RANGE / math.sin(math.pi/180*45) + 0.2
		if entity.position.distTo( owner.position ) <= dist:
			entity.AIStopCommand( self.cmdType )
		else:
			entity.AIFollow()
		
	def onEnter( self, entity ):
		"""
		进入模式
		"""
		entity.AIFollow()
		
	def onLeave( self, entity ):
		"""
		离开模式
		"""
		pass
		

class PetAICmdStay( PetAICmdBase ):
	def __init__( self ):
		PetAICmdBase.__init__( self )
		self.cmdType = PET_COMMAND_STAY
	
	def onTick( self, entity ):
		entity.AIGetStateObject().onTick( entity )
		owner = entity.getOwnerEntity()
		if entity.AIAttackTargetID or owner == None or entity.position.distTo( owner.position ) > DISTANCE_OWNER_MAX:
			entity.AIStopCommand( self.cmdType )
	
	def onEnter( self, entity ):
		"""
		进入模式
		"""
		pass
		
	def onLeave( self, entity ):
		"""
		离开模式
		"""
		pass

PetAICmdBase.setClassObject( PET_COMMAND_FOLLOW,  PetAICmdFollow() )
PetAICmdBase.setClassObject( PET_COMMAND_STAY,  PetAICmdStay() )

class VehiclePetAIInterface( object ):
	"""
	幻兽接口
	"""
	def __init__(self):
		object.__init__( self )
		if Const.VEHICLEPET_IS_SERVER_OR_CLIENT:
			return
		self.AIAttackTargetID = 0 		#当前攻击目标
		self.AIOwnerSetTargetID = 0	#主人设置的目标
		self.AITickCBID = 0
		self.AIAttackUseSkill = 0
		self.petSpellIndex = -1
		self.addTimerCallBack( AI_START_TIME_VALUE, "AITickStart", () )
		self.AIChangeAttackState( ATTACK_TYPE_DEFENSE  )
		
		#TODO(QRN):先临时这样解决一下CST-3932，建议后期重新理一下相应的流程
		#1、状态机有进入的机制，但是切换的时候，并没有先离开（leave）前一个状态，才进入（enter）新的状态
		#2、有些地方是通过直接改变相关属性的来做的
		#3、服务器在接收客户端发送的数据后，需要自己做一下验证，不能直接认为客户端发送的数据就一定是正确的。
		if self.AIPetCommand == PET_COMMAND_FOLLOW or self.AIPetCommand == PET_COMMAND_STAY:
			self.AIStopCommand( self.AIPetCommand )
		self.AIPetCommand = 0
		
	def AIGetStateObject( self ):
		return  PetAIStateBase.getClassObject( self.AICurrentState )
	
	def AIGetCmdObject( self ):
		return  PetAICmdBase.getClassObject( self.AIPetCommand )

	def onOwnerAddEnemy( self, enemyID ):
		self.AIGetStateObject().onOwnerAddEnemy( self,  enemyID )
	
	def AIChangeAttackState( self, newState ):
		"""
		切换模式
		"""
		self.AICurrentState = newState
		if self.baseOwner:
			self.baseOwner.client.petOnSetAttackState(  self.AICurrentState )
	
	def AITickStart( self ):
		self.AITickStop()
		self.AITickCBID = self.addTimerRepeat( AI_TICK_REPEAT, "AITickCB", () )
	
	def AITickStop( self ):
		if self.AITickCBID:
			self.popTimer( self.AITickCBID )
			self.AITickCBID = 0
	
	def AITickCB( self ):
		"""
		AI循环
		"""
		if self.AIPetCommand:
			self.AIGetCmdObject().onTick( self )
		else:
			self.AIGetStateObject().onTick( self )

	def AIAttack( self ):
		"""
		攻击
		"""
		if self.isCastingSkill():
			return
			
		self.AISetAttackTarget()
		if self.AIAttackTargetID != 0:
			skillID = self.AISelectAttackSkillID()
			result = self.useSkillToEntity( skillID, self.AIAttackTargetID )
			if result == csstatus.SKILL_GO_ON:
				self.AIAttackUseSkill = 0
				self.stopMoving( csdefine.MOVE_TYPE_CHASE )
			elif result == csstatus.SKILL_TOO_FAR:
				targetEntity = KBEngine.entities[ self.AIAttackTargetID ]
				self.chaseEntity( targetEntity , 0.5 )
	
	def _AISelectNextSkillID( self ):
		if len( self.attrSkillBox ) == 0:
			return 0
			
		self.petSpellIndex += 1
		if len( self.attrSkillBox ) < ( self.petSpellIndex +1 ):
			self.petSpellIndex = 0
		
		return self.attrSkillBox[ self.petSpellIndex ]
	
	def AISelectAttackSkillID( self ):
		resultSkillID = 0
		if self.AIAttackUseSkill != 0:
			resultSkillID = self.AIAttackUseSkill
		else:
			loopNumber = len( self.attrSkillBox )
			for i in range( loopNumber ):
				selectNextSkillID = self._AISelectNextSkillID()
				selectSkill = self.getSkill( selectNextSkillID )
				if selectSkill != None and not selectSkill.isCasterCooldown( self ):
					resultSkillID = selectNextSkillID
					break
			if resultSkillID == 0:
				resultSkillID = 180000001
				
		return resultSkillID
	
	def AISetAttackTarget( self ):
		if not self.AIIsCanAttackTargetID( self.AIAttackTargetID ) :
			self.AIAttackTargetID = 0
			self.AIGetStateObject().selectAttackTarget( self )

	def AIFindRangeEnemy( self ):
		owner = self.getOwnerEntity()
		if owner:
			pos  = owner.position
			if self.AIPetCommand == PET_COMMAND_STAY:
				pos = self.position
			for e in self.entitiesInRangeExt( FIND_ENEMY_RANGE, None, pos ):
				if self.AIIsCanAttackTargetID( e.id ):	#当前处理可被攻击状态
					self.AIAttackTargetID = e.id
					break
	
		
	def AIIsCanAttackTargetID( self, targetID ):
		"""
		判断当前目标是否可攻击
		"""
		result = True
		if targetID == 0:
			result = False
		else:
			targetEntity = KBEngine.entities.get( targetID )
			if targetEntity == None:
				result = False
			else:
				if not targetEntity.isCombatEntity():
					result = False
				else:
					if targetEntity.getState() in csconst.NOT_FIGHT_STATES:
						result = False
					else:
						owner = self.getOwnerEntity()
						if not owner:
							result = False
						else:
							if owner.position.distTo( targetEntity.position ) > DISTANCE_OWNER_ATTACK_MAX:
								result = False
							
		if result == True and  self.queryRelation( targetEntity  ) != csdefine.COMBAT_RELATION_ENEMY:
			result = False
			
		return result
	
	def AIFollow( self ):
		"""
		跟随
		"""
		self.AIAttackTargetID = 0 #设置攻击 
		owner = self.getOwnerEntity()
		if self.AIPetCommand == PET_COMMAND_STAY:
			return
		if owner:
			if self.getState() == csdefine.ENTITY_STATE_FIGHT and self.position.distTo( owner.position ) > DISTANCE_TELEPORT :
				self.position = self.AIGetFollowPosition()
			elif self.getState() == csdefine.ENTITY_STATE_FREE and self.position.distTo( owner.position ) > DISTANCE_TELEPORT_FREE:
				self.position = self.AIGetFollowPosition()
			elif abs(( self.position.y - owner.position.y )) > DISTANCE_HIGH:
				self.position = self.AIGetFollowPosition()
			else:
				self.gotoPosition( self.AIGetFollowPosition() )
		else:
			self.reqTeleportToOwner()
	
	def AIGetFollowPosition( self ):
		owner = self.getOwnerEntity()
		newYaw = owner.getYaw() + math.pi/180*(45)
		dest = Math.Vector3( FOLLOW_OWNER_RANGE * math.sin( newYaw ), 0, FOLLOW_OWNER_RANGE * math.cos( newYaw ) )
		return Math.Vector3( owner.position + dest )

	#--------------------------------owner do---------------------------------------------
	def AIOwnerChangeState( self,  state ):
		"""
		define method
		切换战斗模式
		"""
		#if not self.isOwner( exposed ):
		#	return 
		
		self.AIAttackTargetID = 0
		self.AIOwnerSetTargetID = 0
		self.stopMovingForType( csdefine.NORMAL_MOVE )
		self.AIChangeAttackState( state )
	
	def AIStopCommand( self, cmd ):
		self.AIGetCmdObject().onLeave( self )
		self.AIPetCommand = 0
		owner = self.getOwnerEntity()
		if owner:
			owner.AICommandEndNotice()
	
	def AIOwnerUseCommand( self,  cmd ):
		"""
		define method
		切换命令模式
		"""
		self.AIPetCommand = cmd
		self.AIGetCmdObject().onEnter( self )
		
	def AIOwnerAttack( self, skillID, targetID ):
		"""
		define method
		主人发送攻击命令
		"""
		#if not self.isOwner( exposed ):
		#	return 
		self.AIAttackUseSkill = skillID
		if self.AIIsCanAttackTargetID( targetID ):
			self.AIOwnerSetTargetID = targetID
		targetEntity = KBEngine.entities.get( targetID )
		if (targetEntity != None and not targetEntity.isCombatEntity()) or targetID == self.id or targetID == 0:
			self.statusMessage( csstatus.PET_NO_TARGET_FOR_ATTACK, "" )
		owner = self.getOwnerEntity()
		if targetEntity != None and owner.position.distTo( targetEntity.position ) > DISTANCE_OWNER_ATTACK_MAX and targetEntity.isCombatEntity():
			self.statusMessage( csstatus.PET_TARGET_IS_TOO_FAR_NOT_ATTACK, "" )

	def RequestAttackTarget( self, skillID, targetID ):
		"""
		客户端请求AI攻击
		"""
		if self.isCastingSkill():
			return
		
		self.AIAttackUseSkill = skillID
		if targetID != 0:
			currentSkillID = self.AISelectAttackSkillID()
			result = self.useSkillToEntity( currentSkillID, targetID )