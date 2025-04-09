# -*- coding: utf-8 -*-


"""
usage:
	施法者/受术者条件

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#python
import random
import math
#common
import csdefine
import csstatus
import csconst
import KBEDebug
import Functions
import Math
import csarithmetic

def _Compare( x, y, operation ):
	if operation == 0:
		if x == y:
			return True
		return False
	elif operation == 1:
		if x > y:
			return True
		return False
	elif operation == 2:
		if x < y:
			return True
		return False
	elif operation == 3:
		if x >= y:
			return True
		return False
	elif operation == 4:
		if x <= y:
			return True
		return False
	elif operation == 5:
		if x != y:
			return True
		return False
	return False

class ConditionBase:
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
		
	def getSkillFailCode( self, failCode, isCastValidCheck ):
		"""
		"""
		#这样写主要是施法者和施法对象的条件判断不通过时，需要清晰的提示是哪个不满足条件
		messages = csconst.SKILL_CONDITION_MESSAGE.get(failCode, [csstatus.SKILL_CAST_FAILED, csstatus.SKILL_CAST_FAILED])
		if len(messages) <= 0: return csstatus.SKILL_CAST_FAILED
		return messages[0] if isCastValidCheck else messages[1]
		
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		return csstatus.SKILL_GO_ON

class ConditionTypeRelation( ConditionBase ):
	"""
	目标类型、关系
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.entityTypes = list( filter( lambda x:x!="", dictDat["Param1"].split("|") ) )
		relationTypes = filter( lambda x:x!="", dictDat["Param2"].split("|") )
		self.relationTypes = list( map( lambda x:int(x), relationTypes ) )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY

		entityType = csconst.ENTITY_TYPE_DICT.get(target.getEntityFlag(),"")
		#目标类型判断
		if self.entityTypes and entityType not in self.entityTypes:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		#目标关系判断
		if self.relationTypes and caster.queryRelation( target ) not in self.relationTypes:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		
		return csstatus.SKILL_GO_ON


class ConditionState( ConditionBase ):
	"""
	是否处于某状态
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.state =  [int(i) for i in dictDat["Param1"].split("|")]
		self.isThisState = int( dictDat["Param2"] )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if not hasattr(target,"getState"):
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if self.isThisState:
			if target.getState() in self.state:
				return csstatus.SKILL_GO_ON
		else:
			if target.getState() not in self.state:
				return csstatus.SKILL_GO_ON
		return csstatus.SKILL_STATE_CANT_CAST


class ConditionRate( ConditionBase ):
	"""
	概率检测
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.rate = float( dictDat["Param1"] )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if random.random() < self.rate:
			return csstatus.SKILL_GO_ON
		
		return csstatus.SKILL_OUT_RATE_FAIL

class ConditionPropertyCount( ConditionBase ):
	"""
	属性数量关系类
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._property = ""
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if not hasattr(target, self._property):
			return self.getSkillFailCode("SKILL_NOT_PROPERTY_COUNT_FAIL", isCastValidCheck)
		_property = getattr(target,self._property)
		if _Compare(_property, self._scale, self._operation):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_PROPERTY_COUNT_FAIL", isCastValidCheck)

class ConditionPropertyPercent( ConditionBase ):
	"""
	属性所占比例关系类
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._property = ""
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		_property_Max = "%s%s"%(self._property,"_Max")
		if not hasattr(target, self._property) or not hasattr(target, _property_Max):
			return self.getSkillFailCode("SKILL_NOT_PROPERTY_PERCENT_FAIL", isCastValidCheck)
		Percent = getattr(target,self._property)/getattr(target,_property_Max)
		if _Compare(Percent, self._scale, self._operation):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_PROPERTY_PERCENT_FAIL", isCastValidCheck)

class ConditionDistance( ConditionBase ):
	"""
	距离关系类
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._property = ""
		self._operation = 0
		self._distance = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		self._distance = float(dictDat["Param3"])

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not caster or not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		_dist = 0
		if self._property == "3D":
			_dist = caster.position.distTo( target.position )
		elif self._property == "2D":
			_dist = caster.position.flatDistTo( target.position )
		elif self._property == "Z":
			_dist = abs(caster.position.y - target.position.y)
		if _Compare(_dist, self._distance, self._operation):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_DISTANCE_FAIL", isCastValidCheck)

class ConditionPropertySubtract( ConditionBase ):
	"""
	属性差值关系类
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._distance = 0.0
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""	
		if not caster or not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if not hasattr(caster, self._property):
			return self.getSkillFailCode("SKILL_NOT_PROPERTY_SUBTRACT_FAIL", isCastValidCheck)
		if not hasattr(target, self._property):
			return self.getSkillFailCode("SKILL_TARGET_NOT_PROPERTY_SUBTRACT_FAIL", isCastValidCheck)
		_difference = getattr(caster,self._property) - getattr(target,self._property)
		if _Compare(_difference, self._scale, self._operation):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_PROPERTY_SUBTRACT_FAIL", isCastValidCheck)

class ConditionBuffCount( ConditionBase ):
	"""
	指定ID的Buff的个数
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._buffIdList = []
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""
		buffIdList = dictDat["Param1"].split("|")
		for buffID in buffIdList:
			self._buffIdList.append(int(buffID))
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""	
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:		# NPC不能加buf，所以不用检测
			return self.getSkillFailCode("SKILL_TARGET_NPC_BUFF_COUNT_FAIL", isCastValidCheck)
		for buffID in self._buffIdList:
			_buffCount = len(target.findBuffsByBuffID(buffID))
			if _Compare(_buffCount, self._scale, self._operation):
				return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_BUFF_COUNT_FAIL", isCastValidCheck)

class ConditionBuffLayer( ConditionBase ):
	"""
	指定ID的Buff的层数
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._buffID = 0
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._buffID = int(dictDat["Param1"])
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""	
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:		# NPC不能加buf，所以不用检测
			return self.getSkillFailCode("SKILL_TARGET_NPC_BUFF_LAYER_FAIL", isCastValidCheck)
		_layer = 0
		if len(target.findBuffsByBuffID(self._buffID)):
			_buffIndex = target.findBuffsByBuffID(self._buffID)[0]
			_buffData = target.getBuffData(_buffIndex)
			_layer = _buffData.layer
		if _Compare(_layer, self._scale, self._operation):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_BUFF_LAYER_FAIL", isCastValidCheck)

class ConditionPropertyAssemble( ConditionBase ):
	"""
	属性集合关系类
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._property = ""
		self._operation = 0
		self._assemble = []

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._property = dictDat["Param1"]
		self._operation = int(dictDat["Param2"])
		self._assemble = [int(i) for i in dictDat["Param3"].split("|")]

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if not hasattr(target, self._property):
			return self.getSkillFailCode("SKILL_NOT_PROPERTY_ASSEMBLE_FAIL", isCastValidCheck)
		if self._operation:
			if getattr(target, self._property) in self._assemble:
				return csstatus.SKILL_GO_ON
		else:
			if getattr(target, self._property) not in self._assemble:
				return csstatus.SKILL_GO_ON			
		return self.getSkillFailCode("SKILL_ASSEMBLE_FAIL", isCastValidCheck)

class ConditionEnemy( ConditionBase ):
	"""
	敌对关系
	"""
	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._assemble = [int(i) for i in dictDat["Param1"].split("|")]
		self._operation = int(dictDat["Param2"])		

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if self._operation:
			if caster.queryRelation(target) in self._assemble:
				return csstatus.SKILL_GO_ON	
		else:
			if caster.queryRelation(target) not in self._assemble:
				return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_ENEMY_FAIL", isCastValidCheck)

class ConditionRelationAssemble( ConditionBase ):
	"""
	社交关系
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._relation = ""
		self._operation = 0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		if dictDat["Param1"] == "Self":
			self._relation =  "id"
		elif dictDat["Param1"] == "Pet":
			self._relation =  "pet"
		elif dictDat["Param1"] == "Enemy":
			self._relation = "enemyList"
		elif dictDat["Param1"] == "Team":
			self._relation = "teamMembers"
		elif dictDat["Param1"] == "CallMonster":
			self._relation = "callMonsterMBList"
		elif dictDat["Param1"] == "Owner":
			self._relation = "getOwnerEntity"

		self._operation = int(dictDat["Param2"])

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		_flag = False
		if self._relation == "id":
			if caster.id == target.id:
				_flag = True
		elif self._relation == "pet":
			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
				if caster._activePetUID == target.uid:
					_flag = True
		elif self._relation == "enemyList":
			if not hasattr(caster, self._relation):
				return self.getSkillFailCode("SKILL_NOT_ENEMYLIST_FAIL", isCastValidCheck)
			if target.id in getattr(caster, self._relation):
				_flag = True
		elif self._relation == "teamMembers":
			if not hasattr(caster, self._relation):
				return self.getSkillFailCode("SKILL_NOT_TEAMMEMBERS_FAIL", isCastValidCheck)
			for e in getattr(caster, self._relation):
				if e["mailbox"].id == target.id:
					_flag = True
		elif self._relation == "callMonsterMBList":
			if not hasattr(caster, self._relation):
				return self.getSkillFailCode("SKILL_NOT_CALLMONSTERMBLIST_FAIL", isCastValidCheck)
			for value in getattr(caster, self._relation).values():
				for baseMB in value:
					if baseMB.id == target.id:
						_flag = True
		elif self._relation == "getOwnerEntity":
			if not hasattr(caster, self._relation):
				return self.getSkillFailCode("SKILL_RELATION_ASSEMBLE_FAIL", isCastValidCheck)
			owner = caster.getOwnerEntity()
			if owner.id == target.id:
				_flag = True
				
		if self._operation and _flag:
			return csstatus.SKILL_GO_ON
		elif not self._operation and not _flag:
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_RELATION_ASSEMBLE_FAIL", isCastValidCheck)

class ConditionType( ConditionBase ):
	"""
	单位类型
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.entityTypes = list( filter( lambda x:x!="", dictDat["Param1"].split("|") ) )
		self._operation = int(dictDat["Param2"])

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		entityType = csconst.ENTITY_TYPE_DICT.get(target.getEntityFlag(),"")
		if self._operation and entityType in self.entityTypes:
			return csstatus.SKILL_GO_ON
		elif not self._operation and entityType not in self.entityTypes:
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_TYPE_FAIL", isCastValidCheck)

class ConditionScriptID( ConditionBase ):
	"""
	是否指定的ID
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self.needRole = 0

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.appointID =  [int(i) for i in dictDat["Param1"].split("|")]
		self._isThisType = int( dictDat["Param2"] )
		if dictDat["Param3"]:
			self.needRole = int( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if target.entityFlag == csdefine.ENTITY_FLAG_ROLE:
			if self.needRole:
				return csstatus.SKILL_GO_ON
			else:
				return self.getSkillFailCode("SKILL_ROLE_SCRIPTID_FAIL", isCastValidCheck)
		if not target.getScriptID():		# 玩家没有ScriptID，所以不用检测
			return self.getSkillFailCode("SKILL_NOT_SCRIPTID_FAIL", isCastValidCheck)
		targetScriptID = int(target.getScriptID())
		if self._isThisType and targetScriptID in self.appointID:
			return csstatus.SKILL_GO_ON
		elif not self._isThisType and targetScriptID not in self.appointID:
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_SCRIPTID_FAIL", isCastValidCheck)
		
class ConditionCoolDownTime( ConditionBase ):
	"""
	指定ID的CD时间
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._cdID = 0
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._cdID = int(dictDat["Param1"])
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""	
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		CDList = target.getCooldown()
		_scaleTime = Functions.getTime(self._scale)
		_now = Functions.getTime()
		_endTime = _now
		for CDDict in CDList:
			if self._cdID == CDDict["id"]:
				_endTime = CDDict["endTime"] if CDDict["endTime"] > _now else _now
		if _Compare(_endTime, _scaleTime, self._operation):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_COOLDOWN_TIME_FAIL", isCastValidCheck)

class ConditionSkillPosture( ConditionBase ):
	"""
	心法状态条件
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._propertyList = []
		self._operation = 0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		propertyList = dictDat["Param1"].split("|")
		for _property in propertyList:
			self._propertyList.append(int(_property))
		self._operation = int(dictDat["Param2"])

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""	
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if target.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:		# 只有玩家有心法
			return self.getSkillFailCode("SKILL_ROLE_SKILL_POSTURE_FAIL", isCastValidCheck)
		for _property in self._propertyList:
			if self._operation and target.skillPosture == _property:
				return csstatus.SKILL_GO_ON
			elif not self._operation and target.skillPosture not in self._propertyList:
				return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_SKILL_POSTURE_FAIL", isCastValidCheck)

class ConditionDirection( ConditionBase ):
	"""
	朝向范围条件
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._datum = 0
		self._leftAngle = 0
		self._rightAngle = 0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._datum = int(dictDat["Param1"])
		strList = dictDat["Param2"].split("|")
		self._leftAngle = int(strList[0]) % 360
		self._rightAngle = int(strList[0]) % 360
		if len(strList) > 1:
			self._rightAngle = int(strList[1]) % 360

	def getDiffAngle( self, caster, target ):
		angle = (caster.direction.z * 180 / math.pi) % 360

		if self._datum == 1:	# 目标的绝对水平方向
			angle = (target.direction.z * 180 / math.pi) % 360

		elif self._datum == 2:	# 受者在施者哪个水平方向
			if not caster.position.distTo( target.position ): # 在同一个位置时，默认在正前方
				return 0
			yaw = caster.direction.z
			dstYaw = csarithmetic.getYawByVector3( target.position - caster.position )
			dstAngle = (dstYaw * 180 / math.pi) % 360
			datumAngle = (yaw * 180 / math.pi) % 360
			angle = (datumAngle - dstAngle) % 360

		elif self._datum == 3:	# 施者在受者哪个水平方向
			if not target.position.distTo( caster.position ): # 在同一个位置时，默认在正前方
				return 0
			yaw = target.direction.z
			dstYaw = csarithmetic.getYawByVector3( caster.position - target.position )
			dstAngle = (dstYaw * 180 / math.pi) % 360
			datumAngle = (yaw * 180 / math.pi) % 360
			angle = (datumAngle - dstAngle) % 360

		return angle

	def isInAngle( self, caster, target ):	
		diffAngle = self.getDiffAngle(caster, target )
		if self._rightAngle > self._leftAngle:
			if diffAngle <= self._rightAngle and diffAngle >= self._leftAngle:
				return True
		elif self._rightAngle < self._leftAngle:
			if diffAngle <= self._rightAngle or diffAngle >= self._leftAngle:
				return True
		elif self._rightAngle == self._leftAngle:
			if diffAngle == self._rightAngle:
				return True
		return False

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if self.isInAngle(caster, target):
			return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_DIRECTION_FAIL", isCastValidCheck)



class ConditionJumpShowState( ConditionBase ):
	"""
	是否处于某跳跃状态
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.state =  [int(i) for i in dictDat["Param1"].split("|")]
		self.isThisState = int( dictDat["Param2"] )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
			
		#跟家伟讨论后，约定如果是分身怪则默认其是在地面上。
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			return csstatus.SKILL_GO_ON
		
		if not target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		
		if self.isThisState:
			if target.jumpShowState in self.state:
				return csstatus.SKILL_GO_ON
		else:
			if target.jumpShowState not in self.state:
				return csstatus.SKILL_GO_ON
		return csstatus.SKILL_STATE_CANT_CAST

class ConditionEffectState( ConditionBase ):
	"""
	效果状态要求
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.effectStateList =  [int(i) for i in dictDat["Param1"].split("|")]
		self.isThisState = int( dictDat["Param2"] )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY

		for i in self.effectStateList:
			if self.isThisState and not target.hasEffectState(csdefine.EFFECT_STATE_LIST[i]):
				return csstatus.SKILL_STATE_CANT_CAST
			elif not self.isThisState and target.hasEffectState(csdefine.EFFECT_STATE_LIST[i]):
				return csstatus.SKILL_STATE_CANT_CAST
		return csstatus.SKILL_GO_ON

class ConditionActForbid( ConditionBase ):
	"""
	开关状态条件要求
	"""
	def init( self, dictDat ):
		"""
		virtual method.
		"""
		self.actForbidList =  [int(i) for i in dictDat["Param1"].split("|")]
		self.isThisState = int( dictDat["Param2"] )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY

		for i in self.actForbidList:
			if self.isThisState and not target.actionForbidSign(csdefine.ACTION_FLAG_LIST[i]):
				return csstatus.SKILL_STATE_CANT_CAST
			elif not self.isThisState and target.actionForbidSign(csdefine.ACTION_FLAG_LIST[i]):
				return csstatus.SKILL_STATE_CANT_CAST
		return csstatus.SKILL_GO_ON

class ConditionRoleMoveState( ConditionBase ):
	"""
	玩家是否处于某移动状态
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self.states = []

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		Param1List =  [int(i) for i in dictDat["Param1"].split("|")]
		for i in Param1List:
			if i == 0:
				self.states.append(csdefine.MOVE_TYPE_NONE)
			elif i == 1:
				self.states.extend(csdefine.ACTIVE_MOVE_LIST)
			elif i == 2:
				self.states.extend(csdefine.PASSIVE_MOVE_LIST)

		self.isThisState = int( dictDat["Param2"] )
	
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY

		if self.isThisState:
			if target.roleMoveType in self.states:
				return csstatus.SKILL_GO_ON
		else:
			if target.roleMoveType not in self.states:
				return csstatus.SKILL_GO_ON
		return csstatus.SKILL_STATE_CANT_CAST

class ConditionBuffEnergy( ConditionBase ):
	"""
	能量值条件
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self._buffID = 0
		self._operation = 0
		self._scale = 0.0

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self._buffID = int(dictDat["Param1"])
		self._operation = int(dictDat["Param2"])
		self._scale = float( dictDat["Param3"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:		# NPC不能加buf，所以不用检测
			return self.getSkillFailCode("SKILL_TARGET_NPC_BUFF_LAYER_FAIL", isCastValidCheck)

		for buffData in list(target.getAttrBuffs().values()):
			if buffData.className == "BuffEnergyLevel" and self._buffID == buffData.buffID:
				buff = target.getBuff(self._buffID)
				if not buff._isLocal or (buff._isLocal and buffData.casterID == caster.id):
					if _Compare(buffData.getTempData( "EnergyVale"), self._scale, self._operation):
						return csstatus.SKILL_GO_ON
		return self.getSkillFailCode("SKILL_BUFF_ENERGY_FAIL", isCastValidCheck)

class ConditionBelongSide( ConditionBase ):
	"""
	是否是 攻（守）方
	(0：攻方，1：守方)
	"""
	def __init__(self):
		"""
		virtual method
		"""
		self.belongSide = csdefine.BELONG_SIDE_ATTACK

	def init( self, dictDat):
		"""
		virtual method.
		"""	
		self.belongSide = int( dictDat["Param1"] )

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if not target:
			return csstatus.SKILL_CAST_ENTITY_ONLY
		if target.isBelongSide( self.belongSide ):
				return csstatus.SKILL_GO_ON
		return csstatus.SKILL_STATE_CANT_CAST

class ObjectCondition:
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
			self.add( cdata )

	def add( self, conditionData ):
		"""
		增加一个条件
		"""
		instance = eval( conditionData["ConditionType"] )()
		instance.init( conditionData )
		self._conditions.append( instance )
		
	def getSkillFailCode( self, failCode, isCastValidCheck ):
		"""
		"""
		#这样写主要是施法者和施法对象的条件判断不通过时，需要清晰的提示是哪个不满足条件
		messages = csconst.SKILL_CONDITION_MESSAGE.get(failCode, [csstatus.SKILL_CAST_FAILED, csstatus.SKILL_CAST_FAILED])
		if len(messages) <= 0: return csstatus.SKILL_CAST_FAILED
		return messages[0] if isCastValidCheck else messages[1]

	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		for cnd in self._conditions:
			state = cnd.valid( caster, target, isCastValidCheck )
			if state != csstatus.SKILL_GO_ON:
				return state
		return csstatus.SKILL_GO_ON

	def isHasConditions(self):
		"""
		是否有条件
		"""
		return self._conditions != []

class BuffReplaceCondition( ObjectCondition ):
	"""
	buff替换效果条件
	"""
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if len(self._conditions) == 0:		#没配条件时不应该执行替换效果
			return self.getSkillFailCode("SKILL_BUFF_REPLACE_FAIL", isCastValidCheck)
		return ObjectCondition.valid( self, caster, target, isCastValidCheck )

class BuffExtraCondition( ObjectCondition ):
	"""
	buff额外效果条件
	"""
	def valid( self, caster, target, isCastValidCheck ):
		"""
		virtual method.
		条件检测
		"""
		if len(self._conditions) == 0:		#没配条件时不应该执行额外效果
			return self.getSkillFailCode("SKILL_BUFF_EXTRA_FAIL", isCastValidCheck)
		return ObjectCondition.valid( self, caster, target, isCastValidCheck )