# -*- coding: utf-8 -*-


"""
usage:
	技能作用对象类

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#python
import math
#common
import csdefine
#cell
import ConfigObject.Skill.SkillBase.AreaDefine as AreaDefine
import ConfigObject.Skill.SkillBase.ObjectCondition as ObjectCondition
import ConfigObject.Skill.SkillBase.FilterCondition as FilterCondition
import ConfigObject.Skill.EffectLoader as EffectLoader

from ConfigObject.Skill.SkillBase.HitTypeDefine import g_hitTypeDefine
#data
import csstatus
import Settings

HIT_TIME_ACCURACY	= 1000			# 打击时间 hitTime 精确度，保留小数后三位


class HitDefine:
	"""
	作用对象是entity
	"""
	def __init__( self ):
		self._hitType = csdefine.SKILL_HIT_TYPE_DODGE
		self._hitArea = None
		self._receiverCondition = ObjectCondition.ObjectCondition()
		self._fliterCondition = FilterCondition.FilterCondition()
		self._effectList = []

	def init( self, dictDat, skill ):
		"""
		virtual method.
		技能打击的配置dictDat
		"""
		self._hitType = dictDat[ "HitType" ]
		self._hitArea = AreaDefine.newInstance( dictDat[ "HitArea" ] )
		
		if len( dictDat[ "ReceiverCondition" ] ) > 0: 							# 受术者条件
			self._receiverCondition.init( dictDat[ "ReceiverCondition" ] )
		
		if len( dictDat[ "FilterCondition" ] ) > 0: 							# 受术者列表过滤条件
			self._fliterCondition.init( dictDat[ "FilterCondition" ] )
		
		for effectData in dictDat[ "EffectList" ]:							# 打击效果列表
			effect = EffectLoader.g_effects.createEffect( effectData, skill )
			self._effectList.append( effect )
	
	def getEffectList( self ):
		"""
		"""
		return self._effectList
	
	def receive( self, skill, caster, receiver ):
		"""
		接受打击效果
		"""
		if g_hitTypeDefine.isHit( self._hitType, caster, receiver ) == csdefine.SKILL_HIT_ERROR: # 命中错误 无效
			return
		elif g_hitTypeDefine.isHit( self._hitType, caster, receiver ) == csdefine.SKILL_HIT_FAILED:	# 命中失败 闪避
			receiver.allClients.onDodgeSkillHit(caster.id)
			return
		if not caster:  # 施法者不在了,整个打击放弃掉
			return
		for effect in self._effectList:
			if effect.canEffect( skill, caster, receiver ):
				effect.onReceive( skill, caster, receiver )

	def validReceiver( self, caster, receiver ):
		"""
		判断目标是否有效
		@return: INT，see also csdefine.SKILL_*
		@rtype:  INT
		"""
#		import CoreInterface.CombatInterface as CombatInterface
#		if not isinstance( receiver, CombatInterface.CombatInterface ):
#			return csstatus.SKILL_NOT_ENEMY_ENTITY
		if receiver == None:
			return csstatus.SKILL_MISS_TARGET
		
		if receiver.inDestroying():
			return csstatus.SKILL_NOT_ENEMY_ENTITY
		
		if receiver.spaceID != caster.spaceID:
			return csstatus.SKILL_NOT_ENEMY_ENTITY
		
		return self._receiverCondition.valid( caster, receiver, True )

	def filterReceiver( self, skill, caster, target, receivers ):
		"""
		筛选出所有合法者
		@param   caster: 施法者
		@type    caster: Entity
		@param receivers: 受击者
		@type  receivers: list of Entity
		"""
		receiverlist = self._fliterCondition.filter( skill, caster, target, receivers )
		return receiverlist

	def getReceivers( self, skill, caster, target ):
		"""
		virtual method
		取得所有的符合条件的受术者Entity列表；
		所有的onArrive()方法都应该调用此方法来获取有效的entity。
		@return: array of Entity

		@param   caster: 施法者
		@type    caster: Entity
		@param target: 受击者
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py

		@rtype: list of Entity
		"""	
		receivers = self._hitArea.getObjectList( caster, target )
		receivers = list( filter( lambda e: self.validReceiver( caster, e ) == csstatus.SKILL_GO_ON, receivers ) )
		return self.filterReceiver( skill, caster, target, receivers )


class SkillHitDefine( HitDefine ):
	def __init__( self ):
		HitDefine.__init__( self )
		self._hitTime = 0

	def init( self, dictDat, skill ):
		"""
		virtual method.
		技能打击的配置dictDat
		"""
		HitDefine.init( self, dictDat, skill )
		if not skill.isInstantSkill():	# 瞬发技能忽略打击时间配置
			self._hitTime = math.floor( float("%.3f" % dictDat["HitTime"]) * HIT_TIME_ACCURACY )

	def onHit( self, skill, caster, target, index ):
		"""
		开始打击
		"""		
		caster.onTimerDelayArrive( skill.getID(), target, self._hitTime, index )

	def onHitArrive( self, skill, caster, target, index ):
		"""
		打击到达
		"""
		receivers = self.getReceivers( skill, caster, target )
		if caster not in receivers and skill.getTargetType() != csdefine.SKILL_CAST_OBJECT_TYPE_POSITION and len(receivers) > 0 and caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			caster.equipWeaponAbrasion(100)
		for receiver in receivers:
			receiver.receiveSkillHit( caster.id, skill.getID(), self._hitTime, index )

class PassiveSkillHitDefine( HitDefine ):
	def __init__( self ):
		HitDefine.__init__( self )
		
	def onHitArrive( self, skill, caster, target ):
		"""
		打击到达
		"""
		receivers = self.getReceivers( skill, caster, target )
		for receiver in receivers:
			self.receive( skill, caster, receiver )

class BuffHitDefine( HitDefine ):
	def onHitArrive( self, buff, caster, target, attrName, index ):
		"""
		打击到达
		"""
		receivers = self.getReceivers( buff, caster, target )
		for receiver in receivers:
			receiver.receiveBuffHit( caster.id, buff.getID(), attrName, index )


class SkillHitData:
	def __init__( self ):
		self._data = {}
	
	def init( self, hitList, skill ):
		"""
		virtual method.
		技能打击列表的配置dictDat
		"""
		for data in hitList:
			hitInstance = SkillHitDefine()
			hitInstance.init( data, skill )
			hitTime = 0
			if not skill.isInstantSkill():	# 瞬发技能忽略打击时间配置
				hitTime = math.floor( float("%.3f" % data["HitTime"]) * HIT_TIME_ACCURACY )
			if hitTime not in self._data:
				self._data[ hitTime ] = [ hitInstance ]
			else:
				self._data[ hitTime ].append( hitInstance )
	
	def getHit( self, hitTime, index ):
		return self._data[ hitTime ][ index ]
	
	def getTotalTime( self ):
		if self._data:
			return max( self._data.keys() ) / HIT_TIME_ACCURACY
		return 0.0
		
	def getHitData( self ):
		return self._data
	
	def begin( self, skill, caster, target ):
		"""
		开始
		"""
		if not self._data:				# CST-9374 策划没配置打击
			skill.onSkillEnd( caster, target, True )
			return
		for hitTime in self._data:
			caster.addSkillHitTimer( hitTime / HIT_TIME_ACCURACY, skill.getID(), target, hitTime )
	
	def onHit( self, skill, caster, target, hitTime ):
		"""
		开始某一时刻的打击
		"""
		for index, hit in enumerate( self._data[ hitTime ] ):
			hit.onHit( skill, caster, target, index )

	def onHitArrive( self, skill, caster, target, hitTime, index ):
		"""
		打击到达
		"""
		self._data[ hitTime ][ index ].onHitArrive( skill, caster, target, index )
		if hitTime == max( self._data.keys() ) and index == len( self._data[ hitTime ] ) - 1:#最后一个时间点的打击中的最后一个打击
			skill.onSkillEnd( caster, target, True )

class PassiveSkillHitData:
	def __init__( self ):
		self._data = []
		
	def init( self, hitList, skill ):
		"""
		virtual method.
		技能打击列表的配置dictDat
		"""
		for data in hitList:
			hitInstance = PassiveSkillHitDefine()
			hitInstance.init( data, skill )
			self._data.append(hitInstance)
	
	def onHit( self, skill, caster, target ):
		"""
		开始
		"""
		for data in self._data:
			data.onHitArrive( skill, caster, target )
		skill.onSkillEnd( caster, target, True )
	
class BuffHitData:
	def __init__( self ):
		self._data = []

	def init( self, hitList, buff ):
		"""
		virtual method.
		buff打击列表的配置dictDat
		"""
		for data in hitList:
			hitInstance = BuffHitDefine()
			hitInstance.init( data, buff )
			self._data.append( hitInstance )

	def getHit( self, index ):
		return self._data[ index ]

	def onHit( self, buff, caster, target, attrName ):
		"""
		开始某一时刻的打击
		"""
		for index, hit in enumerate( self._data ):
			hit.onHitArrive( buff, caster, target, attrName, index )
