# -*- coding: utf-8 -*-

from ConfigObject.SpaceEffect import SpaceEffectCondition
import KBEDebug

class SpaceEffectObjectBase( object ):
	_TYPE_DICT = {}
	@classmethod
	def getEffectObject( SELF, configSection ):
		effectType = configSection[ "effectType" ]
		if effectType:
			effectObj = SELF._TYPE_DICT.get( effectType )( configSection )
			return effectObj

	@classmethod
	def addEffectType( SELF, typeName, typeClass ):
		SELF._TYPE_DICT[ typeName ] = typeClass

	def __init__( self, configSection ):
		self.effectID = configSection[ "effectID" ]
		self.effectCnds = []
		for cndCfg in configSection[ "effectCondition" ]:
			self.effectCnds.append( SpaceEffectCondition.SpaceEffectConditionBase.getEffectCndObj( cndCfg ) )

	def doEnterSpaceCheck( self,spaceEntity,playerEntity ):
		"""
		"""
		for cndObj in self.effectCnds:
			if cndObj:
				if not cndObj.check( spaceEntity, playerEntity ):
					return False
		return True

class SpaceEffectObjectHold( SpaceEffectObjectBase ):
	"""
	固定效果
	"""
	pass


class SpaceEffectObjectTemp( SpaceEffectObjectBase ):
	"""
	临时效果
	"""
	pass

SpaceEffectObjectBase.addEffectType( "SpaceEffectObjectHold", SpaceEffectObjectHold )
SpaceEffectObjectBase.addEffectType( "SpaceEffectObjectTemp", SpaceEffectObjectTemp )