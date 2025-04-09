# -*- coding- : utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import csconst
import csstatus
import ConfigObject.Skill.SkillLoader as SkillLoader

class BehaviourInterface:
	def __init__( self ):
		pass

	def behIsOptimize(self, bedType, behDescribe):
		"""
		是否采用优化的方案，目前暂时没有确定是判断逻辑
		:return: bool
		"""
		return False

	def behStop( self ):
		"""
		停止所有行为
		"""
		for behObj in self.behaviours.values():
			behObj.reset( self )
	
	def behControlReset( self, behaviourType ):
		"""
		重置行为管理器
		"""
		if behaviourType == 0: #重置所有
			for behObj in self.behaviours.values():
				behObj.reset( self )
		else:
			self.behaviours[ behaviourType ].reset( self )
		
	def behOver( self, behaviourType):
		"""
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) behaviour( behaviourType:%d ) Over!"\
		%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, behaviourType ))

		self.behaviours[ behaviourType ].doOver( self )

		if len( self.behaviours[ behaviourType ] ):
			self.addTimerCallBack( 0.2, "behDoNext", ( behaviourType,))

	def behDoNext( self, behaviourType ):
		if len( self.behaviours[ behaviourType ] ):
			self.behaviours[ behaviourType ].doNext( self )
	
	def behAdd( self, behaviourType, args, priorityLevel = csdefine.BEHAVIOUR_COMMON  ):
		"""
		增加单个行为
		"""
		result = self.behaviours[ behaviourType ].add( self, args,priorityLevel )
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) add behaviourr result( behaviourType:%d, args:%s, result:%s)!"\
		%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, behaviourType, str( args ), result ))

	def behAdds( self, behaviourType, args, priorityLevel = csdefine.BEHAVIOUR_COMMON  ):
		"""
		增加一组行为
		"""
		result = self.behaviours[ behaviourType ].addList( self, args,priorityLevel )
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) add behaviourr list result( behaviourType:%d, args:%s, result:%s)!"\
		%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, behaviourType, str( args ), result ))

	#-------------------------------------
	# 施法行为
	#-------------------------------------
	def behDoSpell(self, skillID, spellTargetID, isGroupSkill=False ):
		"""
		执行施法行为
		:param skillID:
		:param spellTargetID:
		:param isOptimize: 是否使用优化方案
		:return:
		"""
		# 是否使用优化方案
		isOptimize = self.behIsOptimize( csdefine.BEHAVIOUR_TYPE_SPELL, skillID  )

		# 没有视野
		if self.isWitnessed == False:
			self.__ServerSpell(skillID, spellTargetID, isGroupSkill)
		elif isOptimize == False or self.checkSkillIsExit(skillID): #不采取优化方案
			self.__ServerSpell(skillID, spellTargetID, isGroupSkill)
		elif not self.__tryClientSpell( skillID, spellTargetID, isGroupSkill ):#尝试使用客户端去放
			#如果还是失败了，只能使用服务器去施法
			self.__ServerSpell(skillID, spellTargetID, isGroupSkill)

	def __ServerSpell(self, skillID, targetID, isGroupSkill=False):
		"""
		服务器执行一次施法行为
		:param skillID:
		:param targetID:
		:param isGroupSkill:
		:return:
		"""
		result = self.useSkillToEntity(skillID, targetID)
		KBEDebug.DEBUG_MSG_FOR_AI(self, "Monster AI use server skill: %s, targetID:%s, result:%s" % ( skillID, targetID, result))
		if result == csstatus.SKILL_GO_ON:
			self.behDoSpellSuccess( skillID, targetID, isGroupSkill )
		else:
			self.behDoSpellFailure( skillID, targetID, isGroupSkill, result )

	def __tryClientSpell(self, skillID, targetID, isGroupSkill=False):
		"""
		客户端执行一次施法行为
		:param skillID:
		:param targetID:
		:param isGroupSkill:
		:return:
		"""

		KBEDebug.DEBUG_MSG_FOR_AI(self, "Monster AI use client skill: %s, targetID:%s" % (skillID, targetID))
		roleList = self.entitiesInRange(50.0, "Role" )
		for r in roleList:
			if r.isReal() and r.isEntityInView(self) and r.clientEntity(self.id) and not r.inDestroying():
				try:
					self.stopMoving( self.moveScriptID )
					r.clientEntity(self.id).BehClientSpell(skillID, targetID, isGroupSkill)
				except:
					KBEDebug.DEBUG_MSG("clientMovingReady: monster client not exist!",self.id)
				
				self.clientRoleID = r.id
				return True

		return False

	def behClientSpellCB(self, exposed, skillID, targetID, isGroupSkill, result):
		"""
		客户端执行施法行为回复
		:param skillID:
		:param targetID:
		:param isGroupSkill:
		:param result: 客户端使用技能结果
		:return:
		"""
		if result == csstatus.SKILL_GO_ON:
			self.behDoSpellSuccess( skillID, targetID, isGroupSkill, True )
		else:
			self.behDoSpellFailure(skillID, targetID, isGroupSkill, result, True )

	def behClientSpellOver(self, exposed, skillID):
		"""
		客户端完成施法
		:param self:
		:param skillID:
		:return:
		"""
		self.behOver(csdefine.BEHAVIOUR_TYPE_SPELL)
		self.clientRoleID = 0

	def behDoSpellSuccess(self, skillID, spellTargetID, isGroupSkill, clientSpell = False):
		"""
		成功施法
		:param self:
		:param skillID:
		:param spellTargetID:
		:param isGroupSkill:
		:return:
		"""
		self.lastRandomSkillID = str(skillID)

	def behDoSpellFailure(self, skillID, spellTargetID, isGroupSkill, result, clientSpell = False ):
		"""
		施法失败
		:param self:
		:param skillID:
		:param spellTargetID:
		:param isGroupSkill:
		:param result:
		:return:
		"""
		# 表示是否是释放一组技能，如果是释放一组技能，失败的话则不移除当前技能，继续释放当前技能
		# 如果是单个释放技能，则不管成功或者失败，都移除当前已经释放多的技能
		self.behOver(csdefine.BEHAVIOUR_TYPE_SPELL)
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_SKILL_FAILURE, [skillID, ])

		#执行追击(非客户端施法)
		if result == csstatus.SKILL_TOO_FAR and clientSpell == False:
			targetEntity = KBEngine.entities[spellTargetID]
			if not self.isMovingType(csdefine.MOVE_TYPE_CHASE):
				if self.chaseDistance > 0:
					chaseDistance = self.chaseDistance
				else:
					skill = self.getSkill(skillID)
					chaseDistance = float(skill.getRangeMax(self, targetEntity)) * 0.667

				self.chaseEntity(targetEntity, chaseDistance)
				
				
	def behRoleClientLostOver(self):
		"""
		玩家客户端丢失，中断施法行为
		"""
		self.behOver(csdefine.BEHAVIOUR_TYPE_SPELL)
		self.clientRoleID = 0


	def checkSkillIsExit( self, skillID ):
		"""
		检查配置的技能是否存在
		"""
		skillObj = SkillLoader.g_skills[ skillID ]
		if skillObj == None:
			return False
		else:
			return True