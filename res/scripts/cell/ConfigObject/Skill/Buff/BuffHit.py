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
from ConfigObject.Skill.Buff.BuffHold import BuffHold
import ConfigObject.Skill.SkillBase.HitDefine as HitDefine
#common
import SkillTargetObjImpl




class BuffHit( BuffHold ):
	"""
	打击buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._beginHitList = HitDefine.BuffHitData()
		self._endHitList = HitDefine.BuffHitData()
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._beginHitList.init( dictDat["BeginHitList"], self )
		self._endHitList.init( dictDat["EndHitList"], self )
	
	def doBeginHit( self, receiver, buffData ):
		"""
		开始打击
		"""
		ghostCaster = KBEngine.entities.get( buffData.casterID, None )
		target = SkillTargetObjImpl.createTargetObjEntity( receiver )
		if ghostCaster:
			self._beginHitList.onHit( self, ghostCaster, target, "_beginHitList" )
	
	def doEndHit( self, receiver, buffData ):
		"""
		结束打击
		"""
		ghostCaster = KBEngine.entities.get( buffData.casterID, None )
		target = SkillTargetObjImpl.createTargetObjEntity( receiver )
		if ghostCaster:
			self._endHitList.onHit( self, ghostCaster, target, "_endHitList" )
	