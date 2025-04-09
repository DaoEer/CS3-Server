# -*- coding: utf-8 -*-


"""
usage:
	施法目标的封装

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#python
import weakref
#common
import csdefine
import csconst
#data
import csstatus



"""
			#如果配置上CastObjectType == 2 或者必须在<CastObjectType>中配置出条件为entity与相关的条件
			#如果<ReceiverCondition>条件为RECEIVER_CONDITION_ENTITY_SELF 那么CastObjectType必须为2且条件必须为RECEIVER_CONDITION_ENTITY_SELF
			#因为<ReceiverCondition>条件为RECEIVER_CONDITION_ENTITY_SELF其实隐含说明了这个技能影响的是单个entity
"""

#施法目标的封装

class TargetNothing:
	"""
	无施法位置和对象
	"""
	def __init__( self, parent ):
		"""
		"""
		self.parent = weakref.proxy( parent )

	def init( self, dictDat ):
		"""
		virtual method.
		spell配置dict
		"""
		pass
		
	def valid( self, caster, target ):
		"""
		virtual method.
		校验目标是否符合选择要求。
		@param target: 施展对象
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py
		"""
		return csstatus.SKILL_GO_ON


class TargetPosition( TargetNothing ):
	"""
	施法目标为位置
	"""
	def __init__( self, parent ):
		"""
		"""
		TargetNothing.__init__( self, parent )

	def init( self, dictDat ):
		"""
		virtual method.
		spell配置dictDat
		"""
		pass
		
	def valid( self, caster, target ):
		"""
		virtual method.
		校验目标是否符合选择要求。
		@param target: 施展对象
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py
		"""
		if not target or target.getObject() is None :
			# 请选择一个施法位置
			return csstatus.SKILL_MISS_POSITION

		if target.getType() != csdefine.SKILL_TARGET_OBJECT_POSITION:
			return csstatus.SKILL_CAST_POSITION_ONLY

		# 距离是必须判断的
		distance = caster.position.flatDistTo( target.getObjectPosition() )

		maxRange = self.parent.getRangeMax( caster, target.getObject() )
		if maxRange > 0.0 and distance > maxRange + csconst.ATTACK_RANGE_BIAS:		# 必须加上偏移
			# 距离目标太远
			return csstatus.SKILL_TOO_FAR

		return csstatus.SKILL_GO_ON

class TargetLock( TargetNothing ):
	"""
	施法目标为锁定的Entity
	"""
	def __init__( self, parent ):
		"""
		"""
		TargetNothing.__init__( self, parent )

	def init( self, dictDat ):
		"""
		virtual method.
		spell配置dictDat
		"""
		pass
		
	def valid( self, caster, target ):
		"""
		virtual method.
		@param target: 施展对象
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py
		校验目标是否符合选择要求。
		"""
		tObject = target.getObject()
		
		if not ( target or tObject ):
			return csstatus.SKILL_MISS_TARGET
		
		if target.getType() != csdefine.SKILL_TARGET_OBJECT_ENTITY:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		
		# 距离是必须判断的
		distanceBB = caster.getDistToEntityForSkill( tObject )
		maxRange = self.parent.getRangeMax(caster,target.getObject())
		if maxRange > 0.0 and distanceBB > maxRange + csconst.ATTACK_RANGE_BIAS:		# 加上偏移
			return csstatus.SKILL_TOO_FAR

		return csstatus.SKILL_GO_ON
		


g_objects = {
	csdefine.SKILL_CAST_OBJECT_TYPE_NONE		:	TargetNothing,			# 无位置无目标
	csdefine.SKILL_CAST_OBJECT_TYPE_POSITION	:	TargetPosition,		# 位置
	csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY		:	TargetLock,		# entity
}

def newInstance( objectType, spellInstance ):
	"""
	获取对象选择实例。
	@type objectType:	string
	"""
	return g_objects[objectType]( spellInstance )

