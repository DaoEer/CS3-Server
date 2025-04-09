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
import ConfigObject.Skill.SkillBase.HitDefine as HitDefine
#common
import SkillTargetObjImpl
import KBEDebug


class BuffLoop( BuffHit ):
	"""
	周期buff
	"""
	def __init__( self ):
		BuffHit.__init__( self )
		self._loopHitList = HitDefine.BuffHitData()
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHit.init( self, dictDat )
		self._loopHitList.init( dictDat["LoopHitList"], self )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		self.addBuffLoopTimer( receiver, buffData )
		BuffHit.doBegin( self, receiver, buffData )
		
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""	
		self.addBuffLoopTimer( receiver, buffData )
		BuffHit.doReload( self, receiver, buffData )
	
	def addBuffLoopTimer( self, receiver, buffData ):
		"""
		添加loop Timer
		"""
		if self.getLoopTime() > 0:
			buffData.timerID = receiver.addTimerRepeat( self.getLoopTime(), "onBuffLoop", ( buffData.index, ) )
	
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		ghostCaster = KBEngine.entities.get( buffData.casterID, None )
		target = SkillTargetObjImpl.createTargetObjEntity( receiver )
		if ghostCaster:
			self._loopHitList.onHit( self, ghostCaster, target, "_loopHitList" )

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.popTimer(buffData.timerID)
		BuffHit.doEnd( self, receiver, buffData, reason )