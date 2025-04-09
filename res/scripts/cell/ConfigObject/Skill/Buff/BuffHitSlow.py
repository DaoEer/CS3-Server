# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHit import BuffHit
#common
import csdefine



class BuffHitSlow( BuffHit ):
	"""
	打击迟缓buff
	"""
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHit.init( self, dictDat )
		self._actionSpeed = float(dictDat["Param1"])
		self._actionTime = float(dictDat["Param2"])
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		casterID = caster.id
		if receiver.curHitBackCasterID != 0 and receiver.curHitBackCasterID != casterID:	# 不同玩家同时攻击一个怪物时，只表现一个玩家的击退，不叠加表现。
			return False
		return BuffHit.addBuffCheck( self, caster, receiver )
		
	def receiveSuccess( self, caster, receiver ):
		"""
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if buff.__module__ == "BuffHitSlow":	# 替换Buff
				receiver.removeBuffByID( buffData.buffID )
				
		BuffHit.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		receiver.startSkillHitSlow( self._actionSpeed, self._actionTime, max( buffData.holdTime - self._actionTime, 0.0 ) )
		BuffHit.doBegin( self, receiver, buffData )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.stopSkillHitSlow()
		BuffHit.doEnd( self, receiver, buffData,reason )

	
	