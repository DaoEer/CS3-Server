# -*- coding: utf-8 -*-


"""
usage:
	命中类型定义

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#common
import csdefine
import KBEDebug
#data
import csstatus
import ItemTypeEnum
import random


class HitBase:
	def __init__( self ):
		pass
	
	def isHit( self, caster, receiver ):
		return csdefine.SKILL_HIT_SUCCEED
		
class HitDirect( HitBase ):
	"""直接命中"""
	def __init__( self ):
		HitBase.__init__( self )
	
	def isHit( self, caster, receiver ):
		return csdefine.SKILL_HIT_SUCCEED
		
class HitDodge( HitBase ):
	"""判断闪避"""
	def __init__( self ):
		HitBase.__init__( self )
	
	def isHit( self, caster, receiver ):
		if not hasattr( caster, "hitrate"):
			KBEDebug.WARNING_MSG( "caster(type:%d) has not hitrate!!"%(caster.getEntityFlag()) )
			return csdefine.SKILL_HIT_ERROR
		if not hasattr( receiver, "dodgerate"):
			KBEDebug.WARNING_MSG( "receiver(type:%d) has not dodgerate!!"%(receiver.getEntityFlag()) )
			return csdefine.SKILL_HIT_ERROR
		hitrate = caster.hitrate - receiver.hitrate_ignore
		dodgerate = receiver.dodgerate - caster.dodgerate_ignore
		hitrate = max(0, hitrate)
		dodgerate = max(0, dodgerate)
		hitValue = hitrate - dodgerate
		if hitValue < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
			return csdefine.SKILL_HIT_FAILED
		return csdefine.SKILL_HIT_SUCCEED

class HitTypeDefine:
	"""
	"""
	_instance = None
	def __init__( self ):
		assert self._instance is None,"HitTypeDefine is aready exit!!"
		self._instance = self
	
	@staticmethod
	def instance():
		if not HitTypeDefine._instance:
			HitTypeDefine._instance = HitTypeDefine()
		return HitTypeDefine._instance
		
	def isHit( self, hitType, caster, receiver ):
		"""
		是否命中
		"""
		return g_hitType[hitType].isHit( caster, receiver )
		
		
g_hitTypeDefine = HitTypeDefine.instance()
g_hitType = { csdefine.SKILL_HIT_TYPE_DIRECT : HitDirect(),
			csdefine.SKILL_HIT_TYPE_DODGE : HitDodge() }
