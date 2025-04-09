# -*- coding: utf-8 -*-

import csconst
import csdefine
from ConfigObject.Skill.Buff.BuffReplace import BuffReplace

class BuffAttackEnemy( BuffReplace ):
	"""
	周期性攻击（敌对列表中的敌人）
	"""
	def __init__( self ):
		BuffReplace.__init__( self )
		self._skillID = 0
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.scriptIDs = []
		self.entityType = ""
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffReplace.init( self, dictDat )
		param5 = dictDat["Param5"].split("|")
		if param5[0] != "":
			self.radius = float(param5[0])
		if len(param5)>1:
			self.entityType = param5[1]
		if len(param5)>2:
			self.height = float(param5[2])
		self._skillID = int(dictDat["Param3"])
		if dictDat["Param4"].strip()!="":
			self.scriptIDs = dictDat["Param4"].strip().split("|")

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffReplace.doBegin( self, receiver, buffData )
		if self._skillID:
			if receiver.enemyList:
				enemyID = receiver.findFirstEnemyByTime()
				receiver.useSkillToEntity( self._skillID, enemyID )
			else:
				eid = self.detectionTarget( receiver )
				if eid:
					receiver.useSkillToEntity( self._skillID, eid )

	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffReplace.doLoopHit( self, receiver, buffData )
		if self._skillID:
			if receiver.enemyList:
				enemyID = receiver.findFirstEnemyByTime()
				receiver.useSkillToEntity( self._skillID, enemyID )
			else:
				eid = self.detectionTarget( receiver )
				if eid:
					receiver.useSkillToEntity( self._skillID, eid )

	def detectionTarget( self , receiver ):
		eid = 0
		distance = 10000.0
		entities = receiver.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs,self.removeStates  )
		for e in entities:
			if e.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue
			dis = receiver.position.flatDistTo(e.position)
			if distance > dis:
				eid = e.id
				distance = dis
		return eid