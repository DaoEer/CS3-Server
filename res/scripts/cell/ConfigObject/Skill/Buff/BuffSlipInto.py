# -*- coding: utf-8 -*-

import KBEngine
import csconst
import csdefine
import FightRuleMgr

from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffSlipInto( BuffHold ):
	"""
	潜入buff：与其他战斗单位的关系为友好
	"""
	def __init__( self ):
		BuffHold.__init__( self )
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		
	def receiveSuccess( self, caster, receiver ):
		"""
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if buff.__module__ == "BuffSlipInto":	# 替换Buff
				receiver.removeBuffByID( buffData.buffID )
				
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.addStateFlag(csdefine.STATE_FLAG_SLIPINTO)
		#触发一下关系改变接口
		receiver.updateRelation()
		
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.removeStateFlag(csdefine.STATE_FLAG_SLIPINTO)
		receiver.updateRelation()
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.addTimerCallBack( 1, "reTriggerNearTrap", () )	#1秒后再触发陷阱，因为此时buff还未移除，关系还未恢复，如果触发陷阱会因为关系不为敌对而加不了敌人
		
		elif receiver.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			receiver.addTimerCallBack( 1, "monsterAIReTriggerNearTrap", () )
	