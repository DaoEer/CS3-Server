# -*- coding: utf-8 -*-


"""
usage:
	受术者筛选条件

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#python
import random
#common
import csdefine
import csstatus
import KBEDebug
#data
import Skill.SkillReceiverDefine as SkillReceiverDefine


class FilterBase:
	"""
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		pass

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		pass

	def filter( self, caster, target, receiverList ):
		"""
		virtual method.
		条件检测
		"""
		return receiverList



class OrderByRandom( FilterBase ):
	"""
	随机最大受术人数
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self._maxNumber = 0
	
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		if dictDat["Param1"]:
			self._maxNumber = int(dictDat["Param1"])
	
	def filter( self, caster, target, receiverList ):
		"""
		virtual method.
		条件检测
		"""
		newList = []
		random.shuffle( receiverList )
		if len( receiverList ) <= self._maxNumber or self._maxNumber<= 0:
			newList = receiverList
		else:
			newList = receiverList[ 0 : self._maxNumber ]
		return newList

class OrderByProperty( FilterBase ):
	"""
	单位属性排序
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self._property = ""
		self._operation = 0
		self._maxNumber = 0

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		if dictDat["Param3"]:
			self._maxNumber = int(dictDat["Param3"])

	def filter( self, caster, target, receiverList ):
		"""
		virtual method.
		条件检测
		"""
		newList = []

		if self._operation:
			list1 = list(filter(lambda x:hasattr(x,self._property), receiverList))
			list2 = list(filter(lambda x:not hasattr(x,self._property), receiverList)) # 缺少指定属性时,移到列表的队末
			list3 = sorted(list1, key = lambda x:getattr(x,self._property))
			list3.extend(list2)	

			if self._maxNumber > 0:
				newList = list3[0 : self._maxNumber]
			else:
				newList = list3
		else:
			list1 = list(filter(lambda x:hasattr(x,self._property), receiverList))
			list2 = list(filter(lambda x:not hasattr(x,self._property), receiverList)) # 缺少指定属性时,移到列表的队末
			list3 = sorted(list1, key = lambda x:getattr(x,self._property), reverse=True)
			list3.extend(list2)

			if self._maxNumber > 0:
				newList = list3[0 : self._maxNumber]
			else:
				newList = list3

		return newList

class OrderByDistanceToCaster( FilterBase ):
	"""
	距离排序
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self._property = ""
		self._operation = 0
		self._maxNumber = 0

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		if dictDat["Param3"]:
			self._maxNumber = int(dictDat["Param3"])

	def filter( self, caster, target, receiverList ):
		"""
		virtual method.
		条件检测
		"""
		newList = []
		list1 = []
		if self._operation:
			if self._property == "3D":
				list1 = sorted(receiverList, key = lambda x:caster.position.distTo( x.position ))
			elif self._property == "2D":
				list1 = sorted(receiverList, key = lambda x:caster.position.flatDistTo( x.position ))
			elif self._property == "Z":
				list1 = sorted(receiverList, key = lambda x:abs(caster.position.y - x.position.y))

			if self._maxNumber > 0:
				newList = list1[0 : self._maxNumber]
			else:
				newList = list1
		else:
			if self._property == "3D":
				list1 = sorted(receiverList, key = lambda x:caster.position.distTo( x.position ), reverse=True)
			elif self._property == "2D":
				list1 = sorted(receiverList, key = lambda x:caster.position.flatDistTo( x.position ), reverse=True)
			elif self._property == "Z":
				list1 = sorted(receiverList, key = lambda x:abs(caster.position.y - x.position.y), reverse=True)

			if self._maxNumber > 0:	
				newList = list1[0 : self._maxNumber]
			else:
				newList = list1

		return newList

class OrderByDistanceToTarget( FilterBase ):
	"""
	距离排序
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self._property = ""
		self._operation = 0
		self._maxNumber = 0

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		if dictDat["Param3"]:
			self._maxNumber = int(dictDat["Param3"])

	def filter( self, caster, target, receiverList ):
		"""
		virtual method.
		条件检测
		"""
		targetPosition = target.getObjectPosition()
		newList = []
		list1 = []
		if self._operation:
			if self._property == "3D":
				list1 = sorted(receiverList, key = lambda x:targetPosition.distTo( x.position ))
			elif self._property == "2D":
				list1 = sorted(receiverList, key = lambda x:targetPosition.flatDistTo( x.position ))
			elif self._property == "Z":
				list1 = sorted(receiverList, key = lambda x:abs(targetPosition.y - x.position.y))

			if self._maxNumber > 0:
				newList = list1[0 : self._maxNumber]
			else:
				newList = list1
		else:
			if self._property == "3D":
				list1 = sorted(receiverList, key = lambda x:targetPosition.distTo( x.position ), reverse=True)
			elif self._property == "2D":
				list1 = sorted(receiverList, key = lambda x:targetPosition.flatDistTo( x.position ), reverse=True)
			elif self._property == "Z":
				list1 = sorted(receiverList, key = lambda x:abs(targetPosition.y - x.position.y), reverse=True)

			if self._maxNumber > 0:	
				newList = list1[0 : self._maxNumber]
			else:
				newList = list1

		return newList




class FilterCondition:
	"""
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self._conditions = []

	def init( self, conditionList ):
		"""
		virtual method.
		"""
		if len( conditionList ) <= 0:
			return
		for cdata in conditionList:
			instance = eval( cdata["FliterConditionType"] )()
			instance.init( cdata )
			self._conditions.append( instance )

	def filter( self, skill, caster, target, receiverList ):
		"""
		virtual method.
		条件检测
		"""
		for cnd in self._conditions:
			receiverList = cnd.filter( caster, target, receiverList )
		return receiverList

