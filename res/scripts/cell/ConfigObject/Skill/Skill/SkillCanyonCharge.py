# -*- coding: utf-8 -*-

import Math
import csdefine
import csstatus
from ConfigObject.Skill.SkillBase.CombatSkill import CombatSkill


class SkillCanyonCharge( CombatSkill ):
	"""
	穿越峡谷——玩家冲刺
	"""
	def __init__( self ):
		CombatSkill.__init__( self )
		self.casterMoveSpeed	= 0.0	# 冲刺速度
		self.casterMoveTime		= 0.0	# 冲刺时间
		self._buffID			= 0		# 在获得灵气时，获得Buff
		self._tempKey			= ""	# temp值

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.init( self, dictDat )
		if dictDat["Param1"]:
			self.casterMoveSpeed = float( dictDat["Param1"] )
		if dictDat["Param2"]:
			self.casterMoveTime = float( dictDat["Param2"] )
		if dictDat["Param3"]:
			self._buffID = int( dictDat["Param3"] )
		self._tempKey = dictDat["Param4"]

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		CombatSkill.onSkillBegin( self, caster, target )
		
		FORWARD_DIRE = 5
		moveTime = self.casterMoveTime
		ChargeTimer = caster.queryTemp( self._tempKey, 0 )
		if ChargeTimer > 0:
			caster.setTemp( self._tempKey, ChargeTimer - 1 )
			moveTime *= 2
			if self._buffID:
				caster.addBuff( caster, self._buffID)
			
		caster.allClients.AddFlyForce( FORWARD_DIRE, self.casterMoveSpeed, moveTime )
	
