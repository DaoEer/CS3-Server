# -*- coding: utf-8 -*-
#
# $Id: SkillTargetObjImpl.py,v 1.11 2008-02-23 01:25:25 kebiao Exp $

"""
接收者，如果用C++角度来看，则我们可以视这个参数为一个抽象对象CReceiver，
						该对象的作用就是抽象对于施法来说所需要的一些接口，然后让一切可能的接收者都
						继承于它，如位置（CReceiverPosition）、entity（CReceiverEntity）、
						玩家身上物品（CReceiverItem）等，可以根据抽象的接口实现自己的实现，
						这样技能在施展时就能统一接口，且不关心具体的施展对象，一切皆由施展对象的接口自己处理，
						或由需要特定类型的技能自己判断。
"""

#engine
import KBEngine
#common
import csdefine
import KBEDebug


_g_skillTargetObjClassMap = {}



class SkillTargetObjImpl:
	"""
	实现cell部份的SkillTargetObjImpl数据创建、还原
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		if obj == None:
			return { "objType" : 0, "param" : None }
		return obj.addToPacket()

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		# 如果skillID为0，则我们认为其没有附上skill，因此直接返回None
		sk = _g_skillTargetObjClassMap[ dict["objType"] ]()
		sk.loadFromPacket( dict )
		return sk

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return (obj is None) or isinstance( obj, SkillTargetObjImpl )
		
	def onSkillBegin( self, caster ):
		pass
#--------------------------------------------------------------------------------------------------------------------------------------
class SkillTargetObjNone( SkillTargetObjImpl ):
	"""
	技能对无目标和位置的施法对象的封装
	"""
	type = csdefine.SKILL_TARGET_OBJECT_NONE
	def __init__( self ):
		pass

	def init( self ):
		"""
		virtual method.
		"""
		pass

	def getType( self ):
		"""
		virtual method.
		"""
		return self.type

	def getObject( self ):
		"""
		virtual method.
		获取真正被封装的对象
		如果封装的是一个entity 那么返回entity ，封装的是position返回的是 类似(0,0,0)
		"""
		return None

	def calcDelay( self, caster, flySpeed ):
		"""
		virtual method.
		@return: 返回法术击中目标的延迟，单位：秒
		@rtype:  float
		"""
		entity = self.getObject()
		if flySpeed > 1.0 :		# 至少1m/s，小于1米/秒则当作是瞬发处理
			dis = (self.getObjectPosition() - caster.position).length
			return  dis/ flySpeed
		return 0.0

	def getObjectPosition( self ):
		"""
		virtual method.
		获取目标所在位置（用于施法 位置转向）
		对于包装者是一个位置的 直接返回包装者， 对于包装者是一个entity的则返回entity所在位置
		对与包装者是无位置属性特殊包装 则直接返回(0,0,0)
		"""
		return ( 0.0, 0.0, 0.0 )

	def convertReference( self, caster ):
		"""
		virtual method.
		转换一个参考者，提供给AreaDefine作为目标参照， 对于封装者是一个位置的对象
		这个参考者是caster,对与封装的是一个entity这个参考者是entity
		"""
		return caster

	def addToPacket( self ):
		"""
		virtual method.
		打包自身需要传输的数据，数据必须是一个dict，具体参数详看SkillTargetObjImpl；
		"""
		return { "objType" : self.getType(), "param" : None }

	def loadFromPacket( self, valDict ):
		"""
		load from Item type.

		@param valDict: dict
		@type  valDict: dict
		"""
		pass
#-----------------------------------------------------------------------------------------------
class SkillTargetObjEntity( SkillTargetObjNone ):
	"""
	技能对entity的受术或目标的封装
	"""
	type = csdefine.SKILL_TARGET_OBJECT_ENTITY
	def __init__( self ):
		self._entityID = 0

	def init( self, entity ):
		"""
		virtual method.
		"""
		self._entityID = entity.id

	def getObject( self ):
		"""
		virtual method.
		获取真正被封装的对象
		如果封装的是一个entity 那么返回entity ，封装的是position返回的是 类似(0,0,0)
		"""
		return KBEngine.entities.get( self._entityID, None )

	def getType( self ):
		"""
		virtual method.
		"""
		return self.type

	def getObjectPosition( self ):
		"""
		virtual method.
		获取目标所在位置（用于施法 位置转向）
		对于包装者是一个位置的 直接返回包装者， 对于包装者是一个entity的则返回entity所在位置
		对与包装者是无位置属性特殊包装 则直接返回(0,0,0)
		"""
		entity = self.getObject()
		if not hasattr( entity, "isDestroyed" ):
			if entity is None:
				return ( 0.0, 0.0, 0.0 )
		else:
			if entity.isDestroyed:
				return ( 0.0, 0.0, 0.0 )
		return entity.position

	def calcDelay( self, caster, flySpeed ):
		"""
		virtual method.
		@return: 返回法术击中目标的延迟，单位：秒
		@rtype:  float
		"""
		entity = self.getObject()
		if flySpeed > 1.0 and entity != None:		# 至少1m/s，小于1米/秒则当作是瞬发处理
			return caster.distanceBB( entity ) / flySpeed
		return 0.0

	def convertReference( self, caster ):
		"""
		virtual method.
		转换一个参考者，提供给AreaDefine作为目标参照， 对于封装者是一个位置的对象
		这个参考者是caster,对与封装的是一个entity这个参考者是entity
		"""
		return self.getObject()

	def addToPacket( self ):
		"""
		virtual method.
		打包自身需要传输的数据，数据必须是一个dict，具体参数详看SkillTargetObjImpl；
		"""
		id = None
		if self.getObject() != None:
			id = self._entityID
		return { "objType" : self.getType(), "param" : id }

	def loadFromPacket( self, valDict ):
		"""
		virtual method.
		load from Item type.

		@param valDict: dict
		@type  valDict: dict
		"""
		eid = valDict[ "param" ]
		if type( eid ) == int and KBEngine.entities.has_key( eid ):
			self._entityID = eid
		else:
			self._entityID = 0
			KBEDebug.DEBUG_MSG( "entity object is lost!", valDict[ "param" ] )
		
	def onSkillBegin( self, caster ):
		""""""
		caster.setReceiverID( self.getObject().id )
#-----------------------------------------------------------------------------------------------
class SkillTargetObjPosition( SkillTargetObjNone ):
	"""
	技能对位置的受术或目标的封装
	"""
	type = csdefine.SKILL_TARGET_OBJECT_POSITION
	def __init__( self ):
		self._entityPosition = ( 0.0,0.0,0.0 )

	def init( self, position ):
		"""
		virtual method.
		"""
		self._entityPosition = position

	def getObject( self ):
		"""
		virtual method.
		获取真正被封装的对象
		如果封装的是一个entity 那么返回entity ，封装的是position返回的是 类似(0,0,0)
		"""
		return self._entityPosition

	def getType( self ):
		"""
		virtual method.
		"""
		return self.type

	def getObjectPosition( self ):
		"""
		virtual method.
		获取目标所在位置（用于施法 位置转向）
		对于包装者是一个位置的 直接返回包装者， 对于包装者是一个entity的则返回entity所在位置
		对与包装者是无位置属性特殊包装 则直接返回(0,0,0)
		"""
		return self._entityPosition

	def convertReference( self, caster ):
		"""
		virtual method.
		转换一个参考者，提供给AreaDefine作为目标参照， 对于封装者是一个位置的对象
		这个参考者是caster,对与封装的是一个entity这个参考者是entity
		"""
		return caster

	def calcDelay( self, caster, flySpeed ):
		"""
		virtual method.
		@return: 返回法术击中目标的延迟，单位：秒
		@rtype:  float
		"""
		if flySpeed > 1.0:		# 至少1m/s，小于1米/秒则当作是瞬发处理
			return caster.position.flatDistTo( self._entityPosition ) / flySpeed
		return 0.0

	def addToPacket( self ):
		"""
		virtual method.
		打包自身需要传输的数据，数据必须是一个dict，具体参数详看SkillTargetObjImpl；
		"""
		return { "objType" : self.getType(), "param" :  self._entityPosition  }

	def loadFromPacket( self, valDict ):
		"""
		virtual method.
		load from Item type.

		@param valDict: dict
		@type  valDict: dict
		"""
		self._entityPosition = valDict[ "param" ]



#-----------------------------------------------------------------------------------------------
#创建技能施展封装对象，无目标位置
def createTargetObjNone():
	return SkillTargetObjNone()

#创建技能施展封装对象，单entity
def createTargetObjEntity( entity ):
	if entity == None:return None
	inst = SkillTargetObjEntity()
	inst.init( entity )
	return inst


#创建技能施展封装对象，位置
def createTargetObjPosition( position ):
	if position == None:return None
	inst = SkillTargetObjPosition()
	inst.init( position )
	return inst



# 自定义类型实现实例
instance = SkillTargetObjImpl()

_g_skillTargetObjClassMap[csdefine.SKILL_TARGET_OBJECT_NONE] 			= SkillTargetObjNone
_g_skillTargetObjClassMap[csdefine.SKILL_TARGET_OBJECT_ENTITY] 			= SkillTargetObjEntity
_g_skillTargetObjClassMap[csdefine.SKILL_TARGET_OBJECT_POSITION]		= SkillTargetObjPosition
