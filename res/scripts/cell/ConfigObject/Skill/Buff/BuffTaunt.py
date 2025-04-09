# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop
import FightRuleMgr
import csdefine


class BuffTaunt( BuffLoop ):
	"""
	嘲讽Buff
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self._dist = 10.0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		if dictDat["Param1"]:
			self._dist = float(dictDat["Param1"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if caster.canBuildEnemyRelation(receiver) == False:
			return False
		if caster.position.distTo( receiver.position ) > self._dist:	#这里检测一下距离，避免距离过远时buff也能持有1个周期
			return False
		return BuffLoop.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffTaunt ):
				receiver.removeBuffByID( buffData.buffID )
		BuffLoop.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffLoop.doBegin( self, receiver, buffData )
		buffCast = KBEngine.entities.get( buffData.casterID )	#我给被嘲讽者加的buff，但是我才是发起嘲讽的一方
		if buffCast:
			FightRuleMgr.g_fightMgr.buildEnemyRelation( buffCast, receiver )
			receiver.setTauntID(buffData.casterID)
			if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
				receiver.client.OnTauntBegin()
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.setTauntID(0)
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.OnTauntEnd()
		BuffLoop.doEnd( self, receiver, buffData, reason )
	
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )
		tauntID = receiver.getTauntID()
		taunter = KBEngine.entities.get( tauntID )
		if not taunter or not taunter.isReal() or taunter.isState(csdefine.ENTITY_STATE_DEAD):
			receiver.removeBuff( buffData.index )
		elif self._dist > 0:
			if receiver.position.distTo( taunter.position ) > self._dist:			#超过距离了
				receiver.removeBuff( buffData.index )
		elif receiver.hasEnemy( tauntID ) == False:
			receiver.removeBuff( buffData.index )