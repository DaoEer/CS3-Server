# -*- coding: utf-8 -*-

import time

import KBEngine
import KBEDebug
import csdefine 


class BehaviourBase( dict ):
	"""
	怪物行为管理器，用于怪物行为排队功能
	"""
	def __init__( self ):
		dict.__init__( self )
		self.behType = 0
		self.currentDoLevel = -1
	
	def reset( self, entity ):
		"""
		重置
		"""
		self.clear()
		self.currentDoLevel = -1
	
	def clearAll( self ):
		self.clear()
		self.currentDoLevel = -1
	
	def isCanAddBehavior( self, entity, args, priorityLevel = csdefine.BEHAVIOUR_COMMON ):
		if priorityLevel not in self or len( self[ priorityLevel ] ) == 0:
			return True
		return False

	def add( self, entity, args, priorityLevel = csdefine.BEHAVIOUR_COMMON ):
		"""
		添加一个行为
		"""
		if self.isCanAddBehavior(entity, args, priorityLevel):
			self[ priorityLevel ] = [ args, ]
			self.doNext( entity )
			return True
			
		return False
	
	def addList( self, entity, argsList, priorityLevel = csdefine.BEHAVIOUR_COMMON ):
		"""
		添加一组行为
		"""
		if priorityLevel not in self or len( self[ priorityLevel ] ) == 0:
			self[ priorityLevel ] = argsList
			self.doNext( entity )
			return True
			
		return False
	
	def doNext( self, entity ):
		if self.currentDoLevel > 0:
			return
			
		selectLevel = self._select()
		if selectLevel > 0:
			args = self[ selectLevel ][0]
			self.currentDoLevel = selectLevel
			self._do( entity, args )
	
	def _do( self, entity, args ):
		"""
		执行
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) behaviour do ( behaviourType:%d, args:%s )!"\
		%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self.behType, str( args ) ))
		
	def _select( self ):
		"""
		选择要执行的等级
		"""
		if len( self ):
			selectLevel = min( self.keys() ) 
			if len( self[ selectLevel ] ):
				return selectLevel
			else:
				self.pop( selectLevel ) #如果是空的，则弹出
				return self._select()
		else:
			return -1
	
	def doOver( self, entity ):
		if self.currentDoLevel in self :
			temp = self[ self.currentDoLevel ].pop( 0 )

		self.currentDoLevel = -1


class BehaviourMoving( BehaviourBase ):
	"""
	移动
	"""
	def __init__( self ):
		BehaviourBase.__init__( self )
		self.behType = csdefine.BEHAVIOUR_TYPE_MOVING
	
	def _do( self, entity, args ):
		"""
		执行
		"""
		BehaviourBase._do( self, entity, args )
		moveScriptID,  moveSpeed, isUpdateSpeed, moveArgs  = args
		entity.moveStart( moveScriptID,  moveSpeed, isUpdateSpeed, moveArgs )

	def reset( self, entity ):
		"""
		重置
		"""
		BehaviourBase.reset( self, entity )
		if entity.isMoving():
			hasbuffhitback = False
			for index, buff in entity.attrBuffs.items():
				buffname = entity.getBuff(buff.buffID).__class__.__name__
				if buffname == "BuffHitBack":
					hasbuffhitback = True
		
class BehaviourSpell( BehaviourBase ):
	"""
	放技能
	"""
	def __init__( self ):
		BehaviourBase.__init__( self )
		self.behType = csdefine.BEHAVIOUR_TYPE_SPELL
		self._curDoingTime = 0
	
	def _do( self, entity, args ):
		"""
		执行
		"""
		self._curDoingTime = int( time.time() )
		BehaviourBase._do( self, entity, args )
		entity.behDoSpell( *args )
	
	def doOver( self, entity ):
		self._curDoingTime = 0
		if self.currentDoLevel in self :
			skillID, targetID, isGroupSkill = self[ self.currentDoLevel ].pop( 0 )
			if isGroupSkill: # 如果使用了组技能
				if entity.monsterAIIsCanAttackUseID( entity.getTargetID() ): #目前来说组技能只用于攻击，所以加入判断
					self[ self.currentDoLevel ].append( ( skillID, entity.getTargetID(), True ) )

		self.currentDoLevel = -1

	def add( self, entity, args, priorityLevel = csdefine.BEHAVIOUR_COMMON ):
		"""
		添加一个行为
		"""
		if entity.behIsOptimize( self.behType,  args[0] ):
			if self._curDoingTime != 0 and int( time.time() ) - self._curDoingTime > 2 :
				self.doOver(entity)

		if self.isCanAddBehavior(entity, args, priorityLevel):
			self[ priorityLevel ] = [ args, ]
			self.doNext( entity )
			return True
			
		return False


class Behaviours( dict ):
	def __init__( self ):
		self[ csdefine.BEHAVIOUR_TYPE_MOVING ] = BehaviourMoving()
		self[ csdefine.BEHAVIOUR_TYPE_SPELL ] = BehaviourSpell()

#-----------------------------------for KBEngine--------------------------------------------------------

	def getDictFromObj( self, obj ):
		"""
		"""
		result = None
		if KBEngine.component == "cellapp":
			dataList = []
			for behType, behTypeObj in obj.items():
				tempDict = {}
				tempDict[ "behType" ] = behType
				tempDict[ "currentDoLevel" ] = behTypeObj.currentDoLevel
				tempList = []
				for behLevel, behData in behTypeObj.items():
					tempList.append( { "behLevel":behLevel, "behData":behData } )
					
				tempDict[ "datas" ] = tempList
				dataList.append( tempDict )
			
			proDict = {}
			proDict[ "datas" ] = dataList
			result = proDict
		else:
			result = obj
		
		return result
		
	def createObjFromDict( self, proDict ):
		"""
		"""
		result = None
		if KBEngine.component == "cellapp":
			obj = Behaviours()
			for behTypeDatas in proDict[ "datas" ]:
				behType = behTypeDatas[ "behType" ]
				behTypeObj = obj[ behType ]
				behTypeObj.currentDoLevel = behTypeDatas[ "currentDoLevel" ]
				for data in behTypeDatas[ "datas" ]:
					behTypeObj[ data[ "behLevel" ] ] = data[ "behData" ]

			result = obj
		else:
			result = proDict
	
		return result
		
	def isSameType( self, obj ):
		"""
		"""
		result = True
		if KBEngine.component == "cellapp":

			result = isinstance( obj, Behaviours )

		return result


inst = Behaviours()