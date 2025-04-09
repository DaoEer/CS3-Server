# -*- coding: utf-8 -*-


"""
usage:
	技能事件类

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



class BaseEvent:
	"""
	基类
	"""
	eventType = 0
	def __init__( self ):
		"""
		"""
		pass

	def init( self, args ):
		"""
		以字符串作为参数加载；

		@param args: 各字符串具体意义由各派生类自己定义
		@type  args: STRING
		"""
		pass

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件

		@param caster: 施法者
		@type  caster: Entity
		@param skillInstance: 使用的技能实例
		@type  skillInstance: Skill
		"""
		return True

class OnDieEvent( BaseEvent ):
	"""死亡事件"""
	eventType = csdefine.SKILL_EVENT_ON_DIE
	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		self._actForbid = None if param1 == "" else int(param1)
		self._type = int( args["Param2"] ) if args["Param2"] else 1
	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._actForbid == None:
			if not self._actForbid == pDict["actForbid"]:
				return False
				
		if self._type != None and "type" in pDict and pDict["type"] != self._type:
			return False
		return True
	
class StateChangeEvent( BaseEvent ):
	"""基础状态发送改变"""
	eventType = csdefine.SKILL_EVENT_STATE_CHANGE

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self._oldState = None if param1 == "" else int(param1)
		self._newState = None if param2 == "" else int(param2)

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._oldState == None:
			if not self._oldState == pDict["oldState"]:
				return False
				
		if not self._newState == None:
			if not self._newState == pDict["newState"]:
				return False

		return True

class SkillPostureChangeEvent( BaseEvent ):
	"""心法状态改变时"""
	eventType = csdefine.SKILL_EVENT_SKILL_POSTURE_CHANGE

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self._oldPosture = None if param1 == "" else int(param1)
		self._newPosture = None if param2 == "" else int(param2)

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._oldPosture == None:
			if not self._oldPosture == pDict["oldSkillPosture"]:
				return False
				
		if not self._newPosture == None:
			if not self._newPosture == pDict["newSkillPosture"]:
				return False

		return True

class ActWorldChangeEvent( BaseEvent ):
	"""技能开关状态改变"""
	eventType = csdefine.SKILL_EVENT_ACT_WORD_CHANGE

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self._actWord = None if param1 == "" else int(param1)
		self._disable = None if param2 == "" else bool(int(param2))

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._actWord == None:
			if not self._actWord == pDict["actWord"]:
				return False
				
			if not self._disable == None:
				if not self._disable == pDict["disabled"]:
					return False

		return True

class EffectStateChangeEvent( BaseEvent ):
	"""技能开关状态改变"""
	eventType = csdefine.SKILL_EVENT_EFFECT_STATE_CHANGE

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self._actWord = None if param1 == "" else int(param1)
		self._disable = None if param2 == "" else bool(int(param2))

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._actWord == None:
			if not self._actWord == pDict["effectState"]:
				return False
				
			if not self._disable == None:
				if not self._disable == pDict["disabled"]:
					return False

		return True
		
class CustomEvent( BaseEvent ):
	"""自定义事件"""
	eventType = csdefine.SKILL_EVENT_PLAN_CUSTOM

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self._id = None if param1 == "" else int(param1)
		self._actWord = None if param2 == "" else int(param2)

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._id == None:
			if not self._id == pDict["id"]:
				return False
		if not self._actWord == None:
			actFb = pDict.get( "actWord", None )
			if actFb == None or self._actWord != actFb:
				return False

		return True

class MoveChangeEvent( BaseEvent ):
	"""玩家移动模式（主动或被动）改变事件"""
	eventType = csdefine.SKILL_EVENT_ROLE_MOVE_CHANGE

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self._movetype = None if param1 == "" else int(param1)
		self._movestate = None if param2 == "" else int(param2)

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._movetype == None:
			if not self._movetype == pDict["MoveType"]:
				return False
				
		if not self._movestate == None:
			if not self._movestate == pDict["MoveState"]:
				return False

		return True


class JumpStateChangeEvent( BaseEvent ):
	"""玩家跳跃模式（主动或被动）改变事件"""
	eventType = csdefine.SKILL_EVENT_ROLE_JUMP_STATE_CHANGE
	jumpType1 = 1
	jumpType2 = 2
	jumpType3 = 3
	jumpTypeList = [jumpType1, jumpType2, jumpType3]
	
	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		param2 = args["Param2"]
		self.jumpType = self.jumpType1 if param1 == '' else int(param1)
		self.isStart = True if param2 == '' else bool(int(param2))

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self.jumpType1 in self.jumpTypeList:
			return False
		oldState = pDict["oldState"]
		newState = pDict["newState"]


		if self.jumpType == self.jumpType1:
			#0->!0
			if self.isStart:
				if oldState == csdefine.JUMP_SHOW_STATE_STAND and newState != csdefine.JUMP_SHOW_STATE_STAND:
					return True
				return False
			#!0->0
			else:
				if oldState != csdefine.JUMP_SHOW_STATE_STAND and newState ==  csdefine.JUMP_SHOW_STATE_STAND:
					return True
				return False
		elif self.jumpType == self.jumpType2:
			#!7->7
			if self.isStart:
				if oldState != csdefine.JUMP_SHOW_STATE_AIR_UP and newState == csdefine.JUMP_SHOW_STATE_AIR_UP:
					return True
				return False
			#7->!7
			else:
				if oldState == csdefine.JUMP_SHOW_STATE_AIR_UP and newState != csdefine.JUMP_SHOW_STATE_AIR_UP:
					return True
				return False
		elif self.jumpType == self.jumpType3:
			#8->!8
			if not self.isStart:
				if oldState == csdefine.JUMP_SHOW_STATE_AIR_DOWN and newState != csdefine.JUMP_SHOW_STATE_AIR_DOWN:
					return True
				return False
			#!8->8
			else:
				if oldState != csdefine.JUMP_SHOW_STATE_AIR_DOWN and newState == csdefine.JUMP_SHOW_STATE_AIR_DOWN:
					return True
				return False
		
		return False

class StopPatrolFly( BaseEvent ):
	"""飞行传送结束事件"""
	eventType = csdefine.SKILL_EVENT_STOP_FLY

class SkillNpcMoveChangeEvent( BaseEvent ):
	"""NPC移动改变事件"""
	eventType = csdefine.SKILL_EVENT_NPC_MOVE_CHANGE

class PerSecondTriggerEvent(BaseEvent):
	"""每秒触发事件"""
	eventType = csdefine.SKILL_EVENT_PER_SECOND_TRIGGER

class OnDestoryEvent(BaseEvent):
	"""销毁时事件"""
	eventType = csdefine.SKILL_EVENT_DESTROY

class SpaceChangeEvent( BaseEvent ):
	"""地图改变事件"""
	eventType = csdefine.SKILL_EVENT_SPACE_CHANGE
	
	def __init__( self ):
		"""
		"""
		self._oldIsIn = 0			#1表示“旧地图”是某些地图；0表示不是某些地图
		self._oldSpaceList = []		#旧地图ID列表
		self._newIsIn = 0			#1表示“新地图”是某些地图；0表示不是某些地图
		self._newSpaceList = []		#新地图ID列表
		self.triggerInSpace = 1		# 0：（触发者）离开地图前，还在旧地图中  1：（触发者）离开地图后，已在新地图中

	def init( self, args ):
		BaseEvent.init( self, args )
		if args["Param1"] != "":					# 格式："1|space1:space2:..."
			list_param1 = args["Param1"].split("|")
			self._oldIsIn = int( list_param1[0] )
			self._oldSpaceList = list_param1[1].split(":")
		
		if args["Param2"] != "":					# 格式："1|space1:space2:..."
			list_param2 = args["Param2"].split("|")
			self._newIsIn = int( list_param2[0] )
			self._newSpaceList = list_param2[1].split(":")

		if args["Param3"] != "":
			self.triggerInSpace = int( args["Param3"] )

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if len(self._oldSpaceList):
			if self._oldIsIn:
				if pDict["OldSpaceID"] not in self._oldSpaceList:
					return False
			else:
				if pDict["OldSpaceID"] in self._oldSpaceList:
					return False
		
		if len(self._newSpaceList):
			if self._newIsIn:
				if pDict["NewSpaceID"] not in self._newSpaceList:
					return False
			else:
				if pDict["NewSpaceID"] in self._newSpaceList:
					return False

		if self.triggerInSpace != pDict["isInNewSpace"]:
			return False
		
		return True

class InitiaiveStopSkillEvent( BaseEvent ):
	"""玩家主动停止技能事件"""
	eventType = csdefine.SKILL_EVENT_INITIATIVE_STOP_SKIL

class InitiaiveStopBuffEvent( BaseEvent ):
	"""玩家主动停止Buff事件"""
	eventType = csdefine.SKILL_EVENT_INITIATIVE_STOP_BUFF

class BuffProcessEvent( BaseEvent ):
	"""Buff流程事件"""
	eventType = csdefine.BUFF_EVENT_PROCESS

	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		self._actForbid = None if param1 == "" else int(param1)
		self._type = int( args["Param2"] ) if args["Param2"] else 1
		self._buffID = int( args["Param3"] ) if args["Param3"] else None

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._actForbid == None:
			if not self._actForbid == pDict["actForbid"]:
				return False

		if self._type != None and "type" in pDict and pDict["type"] != self._type:
			return False

		if self._buffID != None and "buffID" in pDict and pDict["buffID"] != self._buffID:
			return False

		return True

class SkillEvent( BaseEvent ):
	"""技能流程事件"""
	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		self._actForbid = None if param1 == "" else int(param1)
		self._type = int( args["Param2"] ) if args["Param2"] else 1
		self._skillID = int( args["Param3"] ) if args["Param3"] else None

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._actForbid == None:
			if not self._actForbid == pDict["actForbid"]:
				return False
				
		if self._type != None and "type" in pDict and pDict["type"] != self._type:
			return False

		if self._skillID != None and "skillID" in pDict and pDict["skillID"] != self._skillID:
			return False

		return True

class CureEvent( SkillEvent ):
	"""治疗事件"""
	eventType = csdefine.SKILL_EVENT_CURE
	
class HurtEvent( SkillEvent ):
	"""伤害事件"""
	eventType = csdefine.SKILL_EVENT_HURT
	def init( self, args ):
		BaseEvent.init( self, args )
		param1 = args["Param1"]
		self._actForbid = None if param1 == "" else int(param1)
		self._type = int( args["Param2"] ) if args["Param2"] else 1
		self._conditions = []
		if args["Param3"]:
			self._conditions = args["Param3"].split("|")

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if not self._actForbid == None:
			if not self._actForbid == pDict["actForbid"]:
				return False
				
		if self._type != None and "type" in pDict and pDict["type"] != self._type:
			return False

		for i in self._conditions:
			if i not in pDict:
				KBEDebug.ERROR_MSG("HurtEvent: %s is not a correct tag name "%i)
				return False
			elif not pDict[i]:
				return False

		return True

class SkillProcessEvent( SkillEvent ):
	"""技能主流程事件"""
	eventType = csdefine.SKILL_EVENT_PROCESS

class RequestActionSkillEvent( BaseEvent ):
	"""玩家申请行为事件（移动 使用物品，使用技能，幻兽相关操作，NPC/场景物件交互等）"""
	eventType = csdefine.SKILL_EVENT_REQUEST_ACTION
	def init( self, args ):
		BaseEvent.init( self, args )
		self._type = 0
		if args["Param1"]:
			self._type = int(args["Param1"])
		self._idList = []
		if args["Param2"]:
			self._idList = [ int(i) for i in args["Param2"].split("|") ]
		Param3 = args["Param3"]
		self._actForbid = None if Param3 == "" else int(Param3)

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if self._type and self._type !=  pDict["requestType"]:
			return	False

		if self._idList and "id" in pDict and pDict["id"] not in self._idList:
			return False

		if self._actForbid and "actForbid" in pDict and not self._actForbid == pDict["actForbid"]:
			return False

		return True

class PropertyPercentChangeEvent( BaseEvent ):
	""""
	资源存量改变时"技能事件
	"""
	eventType = csdefine.SKILL_EVENT_PROPERTY_PERCENT_CHANGE

	def init( self, args ):
		BaseEvent.init( self, args )
		self._propertyType = args["Param1"]
		self._operateType = int(args["Param2"])
		self._datum = float(args["Param3"])

	def canTriggerEvent( self, pDict ):
		"""
		是否符合触发事件。
		"""
		if pDict["propertyType"] == self._propertyType:
			oldValue = pDict["oldValue"]
			newValue = pDict["newValue"]
			if self._operateType:
				if oldValue <= self._datum and newValue > self._datum:
					return True
			else:
				if oldValue >= self._datum and newValue < self._datum:
					return True				
		return False


class EventDefine:
	def __init__( self ):
		self._eventList = {}			
	
	def init( self, datas ):
		for data in datas:
			inst = eval( data["EventType"] )()
			inst.init( data )
			self._eventList.setdefault( inst.eventType, []).append(inst)
			
	def registerEvent( self, skill, caster ):
		for type, event in self._eventList.items():
			caster.registerSkillEvent( type, skill.getID() )
			
	def unRegisterEvent( self, skill, caster ):
		for type, event in self._eventList.items():
			caster.unRegisterSkillEvent( type, skill.getID() )
			
	def registerBuffEvent( self, buffData, caster, receiver ):
		for type, event in self._eventList.items():
			if caster:
				caster.registerCasterBuffEvent( type, receiver.id, buffData.index )
			
	def unRegisterBuffEvent( self, buffData, caster, receiver ):
		for type, event in self._eventList.items():
			if caster:
				caster.unRegisterCasterBuffEvent( type,  receiver.id, buffData.index )
			
	def canTriggerEvent( self, eventType, pDict ):
		if eventType in self._eventList:
			for _inst in self._eventList[eventType]:
				if _inst.canTriggerEvent( pDict ):
					return True
		return False


class ReceiverEventDefine:
	def __init__( self ):
		self._receiverEventList = {}				# 受术目标事件列表
	
	def init( self, datas ):
		""""""
		for data in datas:
			inst = eval( data["EventType"] )()
			inst.init( data )
			self._receiverEventList.setdefault( inst.eventType, [] ).append(inst)
			
	def registerEvent( self, skill, caster, target ):
		"""
		由于技能流程关系
		unRegister 不在此处处理
		"""
		if skill.getTargetType() != csdefine.SKILL_CAST_OBJECT_TYPE_POSITION:
			receiver = target.getObject()
			for type, event in self._receiverEventList.items():
				receiver.registerReceiverSkillEvent( type, caster.id, skill.getID() )

	def registerBuffEvent( self, buffData, receiver ):
		for type, event in self._receiverEventList.items():
			receiver.registerBuffEvent( type, buffData.index )
			
	def unRegisterBuffEvent( self, buffData, receiver ):
		for type, event in self._receiverEventList.items():
			receiver.unRegisterBuffEvent( type, buffData.index )

	def canTriggerEvent( self, eventType, pDict ):
		if eventType in self._receiverEventList:
			for _inst in self._receiverEventList[eventType]:
				if _inst.canTriggerEvent( pDict ):
					return True
		return False