
# -*- coding: utf-8 -*-


"""
usage:
	技能作用区域

attribute:
	pass

member function:
	pass

callback:
	pass

"""



#python
import math
#engine
import KBEngine
import Math
#common
import csdefine
import KBEDebug
import csarithmetic
#cell
import SkillTargetObjImpl

# Area的朝向基准
AREA_DIRE_REFERENCE_LIST = [csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE, csdefine.SKILL_HIT_AREA_DIRE_TARGET, csdefine.SKILL_HIT_AREA_DIRE_CASTER, \
csdefine.SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET, csdefine.SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER]

# Ghost的朝向基准
GHOST_DIRE_REFERENCE_LIST = [csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE, csdefine.SKILL_HIT_AREA_DIRE_TARGET, csdefine.SKILL_HIT_AREA_DIRE_CASTER, \
csdefine.SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET, csdefine.SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER, csdefine.SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET_3D,\
csdefine.SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER_3D]

class Area:
	def __init__( self ):
		"""构造函数。"""
		self.unitReference = csdefine.SKILL_HIT_AREA_UNIT_CASTER			# 单位位置基准
		self.direReference = csdefine.SKILL_HIT_AREA_DIRE_CASTER			# 单位朝向基准
		self.maxHeight	 = 3.0												# AOE技能加入一个高度的检测，如果策划配置了一个 高度则使用策划同学的配置

		#{偏移类型:[向前偏移量, 向左偏移量, 向上偏移量, 偏移角度]...}
		self.offset = {
						csdefine.SKILL_HIT_OFFSET_RESULT:	[0.0, 0.0, 0.0, 0.0],
						csdefine.SKILL_HIT_OFFSET_START	:	[0.0, 0.0, 0.0, 0.0],
						csdefine.SKILL_HIT_OFFSET_END	:	[0.0, 0.0, 0.0, 0.0]
						}

	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		if dictDat["Param1"]:
			tempList = dictDat["Param1"].split("|")
			if tempList[0]:
				self.unitReference = int( tempList[0] )
				self.direReference = int( tempList[0] )
			if len( tempList ) >= 2 and tempList[1]:
				self.direReference = int( tempList[1] )
			if self.direReference not in AREA_DIRE_REFERENCE_LIST:
				KBEDebug.ERROR_MSG("%s Config Param1(%s) is ERROR!!! Please Check it!!"%(self.__class__.__name__, dictDat["Param1"]))

		Param3 = dictDat["Param3"].split(";")
		for index, i in enumerate(Param3):
			offset = i.split("|")
			if offset[0]:
				self.offset[index][0] = float( offset[0] )
			if len(offset) >= 2 and offset[1]:
				self.offset[index][1] = float( offset[1] )
			if len(offset) >= 3 and offset[2]:
				self.offset[index][2] = float( offset[2] )
			if len(offset) >= 4 and offset[3]:
				self.offset[index][3] = float(offset[3]) % 360
			
	def getPositionAndDirection( self, caster, target ):
		"""
		获取坐标和朝向
		"""
		#计算开始和结束偏移
		casterDir = Math.Vector3(caster.direction)
		targetDir = Math.Vector3(caster.direction)
		if target.getType() != csdefine.SKILL_TARGET_OBJECT_POSITION:
			targetDir = Math.Vector3(target.getObject().direction)
		casterPos = Math.Vector3(caster.position)
		targetPos = Math.Vector3(target.getObjectPosition())
		casterPos = self.calculateOffset(casterPos, casterDir, csdefine.SKILL_HIT_OFFSET_START)
		targetPos = self.calculateOffset(targetPos, targetDir, csdefine.SKILL_HIT_OFFSET_END )
		casterDir.z = self.calculateYaw(casterDir.z, csdefine.SKILL_HIT_OFFSET_START)
		targetDir.z = self.calculateYaw(targetDir.z, csdefine.SKILL_HIT_OFFSET_END)
		position = casterPos
		direction = casterDir

		if self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_ABSOLUTE:
			position = Math.Vector3(0.0, 0.0, 0.0)
		elif self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_CASTER:
			position = casterPos
		elif self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_TARGET:
			position = targetPos
		else:
			KBEDebug.ERROR_MSG("%s Config HitAreaType is ERROR"%(self.__class__.__name__))
			
			
		if self.direReference == csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE:
			direction = Math.Vector3(0.0, 0.0, 0.0)
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_TARGET:			# 施法目标
			direction = targetDir
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET:	# 施法者->施法目标(朝向)
			if casterPos.flatDistTo(targetPos) < 0.1:
				direction = casterDir		#位置一样时，使用施法者朝向
			else:
				direction = (0, 0, csarithmetic.getYawByVector3( targetPos - casterPos ))
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER:	# 施法目标->施法者(朝向)
			if casterPos.flatDistTo(targetPos) < 0.1:
				direction = targetDir		#位置一样时，使用施法目标朝向
			else:
				direction = (0, 0, csarithmetic.getYawByVector3( casterPos - targetPos ))
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_CASTER:
			direction = casterDir
		else:
			KBEDebug.ERROR_MSG("%s config HitAreaType is ERROR"%(self.__class__.__name__))
			
		return Math.Vector3(position), Math.Vector3(direction)
		
	def calculateOffset( self, position, direction, offsetType = csdefine.SKILL_HIT_OFFSET_RESULT ):
		"""计算偏移量"""
		yaw = direction.z
		if self.offset[offsetType][0]:
			position.x += self.offset[offsetType][0] * math.sin( yaw )
			position.z += self.offset[offsetType][0] * math.cos( yaw )
		if self.offset[offsetType][1]:
			position.x += self.offset[offsetType][1] * math.sin( yaw - math.pi/2 )
			position.z += self.offset[offsetType][1] * math.cos( yaw - math.pi/2 )
		if self.offset[offsetType][2]:
			position.y += self.offset[offsetType][2]
		return position

	def calculateYaw(self, yaw, offsetType = csdefine.SKILL_HIT_OFFSET_RESULT ):
		"""计算偏移角度"""
		return yaw - math.radians(self.offset[offsetType][3])
		
	def filterHeight( self, position, receivers ):
		"""
		筛选受术对象 和 法术接收者之间的高度
		@param position: 位置
		@type  position: Vector3
		@param receivers: 法术接收者
		@type  receivers: []
		"""
		entityInArea = []
		if position == ( 0.0, 0.0, 0.0 ):
			return receivers
		
		if self.height:											# 如果策划配置了高度，则用策划配置！否则使用默认值
			height = self.height
		else:
			height = self.maxHeight
		for receiver in receivers:
			if abs(position.y - receiver.position.y) <= height:
				entityInArea.append( receiver )
				
		return entityInArea

	def filterCircular(self, es, centerPos, radius ):
		"""
		筛选圆形范围
		"""
		return [e for e in es if e.position.flatDistTo(centerPos) < radius]

# -----------------------------------无基准------------------------------------------------------------------
class NoRange( Area ):
	"""
	无范围(空打击)
	"""
	def __init__( self ):
		"""
		构造函数。
		"""
		pass
		
	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		if dictDat["Param1"]:
			KBEDebug.ERROR_MSG("NoRange config Param1(%s) is error!!!"%dictDat["Param1"])

	def getObjectList( self, caster, target ):
		return []

# -----------------------------------基单位------------------------------------------------------------------
class Single( Area ):
	"""单体"""
	def __init__( self ):
		self.unitReference = csdefine.SKILL_HIT_AREA_UNIT_CASTER
		
	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		if dictDat["Param1"]:
			self.unitReference = int( dictDat["Param1"] )
		if len(dictDat["Param1"].split("|")) > 1:
			KBEDebug.ERROR_MSG("Single config Param1(%s) is error!!!"%dictDat["Param1"])

	def getObjectList( self, caster, target ):
		if self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_TARGET:
			if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
				return [target.getObject()]
			else:
				KBEDebug.ERROR_MSG("Single Area cant hit to position!!!")
				return []
		elif self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_CASTER:
			return [caster]
		else:
			return []

class Owner( Area ):
	"""目标主人（幻兽、随从、替身限定）"""
	def __init__( self ):
		self.unitReference = csdefine.SKILL_HIT_AREA_UNIT_CASTER
		self.distance = -1
		
	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		if dictDat["Param1"]:
			self.unitReference = int( dictDat["Param1"] )
		if len(dictDat["Param1"].split("|")) > 1:
			KBEDebug.ERROR_MSG("Single config Param1(%s) is error!!!"%dictDat["Param1"])
		if dictDat["Param2"]:
			self.distance = int( dictDat["Param2"] )

	def getObjectList( self, caster, target ):
		if self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_TARGET:
			if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
				if not hasattr(target.getObject(), "getOwnerEntity"):
					return []
				owner = target.getObject().getOwnerEntity()
				if owner and (self.distance < 0 or target.getObject().position.distTo( owner.position ) <= self.distance):
					return [owner]
				return []
			else:
				KBEDebug.ERROR_MSG("Single Area cant hit to position!!!")
				return []
		elif self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_CASTER:
			if not hasattr(caster, "getOwnerEntity"):
				return []
			owner = caster.getOwnerEntity()
			if owner and (self.distance < 0 or caster.position.distTo( owner.position ) <= self.distance):
				return [owner]
			return []
		else:
			return []


# ------------------------------------------基位置--------------------------------------------------------
class Sphere( Area ):
	"""球形状"""
	def __init__( self ):
		"""
		构造函数。
		"""
		Area.__init__( self )
		self.unitReference = csdefine.SKILL_HIT_AREA_UNIT_CASTER			# 单位位置基准
		self.direReference = csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE			# 单位朝向基准
		self.radius 	 = 0.0			#半径
		
	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		Area.load( self, dictDat )
		if len(dictDat["Param1"].split("|")) > 1:
			KBEDebug.ERROR_MSG("Sphere config Param1(%s) is error!!!"%dictDat["Param1"])
		if dictDat["Param2"]:
			self.radius = float( dictDat["Param2"] )

	def getObjectList( self, caster, target ):
		centerPos,direction = self.getPositionAndDirection( caster, target )
		centerPos = self.calculateOffset( centerPos, direction )
		
		es = caster.entityInRangeForSkill( self.radius, None, centerPos )
		#circularList = self.filterCircular(es, centerPos, self.radius )
		circularList = [e for e in es if e.position.distTo(centerPos) < self.radius]
		return circularList

class Rectangle( Area ):
	"""	以自身为起点的矩形 """
	def __init__( self ):
		"""
		构造函数。
		"""
		Area.__init__( self )
		self.length = 0.0				#长
		self.width	= 0.0				#宽
		self.height = 0.0				#高

	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		Area.load( self, dictDat )
		tempList = dictDat["Param2"].split("|")
		if len(tempList) >= 2 and tempList[0] and tempList[1]:
			self.length = float(tempList[0])
			self.width = float(tempList[1])
		else:
			KBEDebug.ERROR_MSG("Rectangle config Param2(%s) is error!"%dictDat["Param2"])
		if len( tempList ) >= 3 and tempList[2]:
			self.height = float(tempList[2])
		

	def inArea( self, dst, src, yaw ):
		"""
		判断位置dst是否在矩形区域内。
		"""
		dstP = Math.Vector3(dst)
		dstP.y = src.y
		return csarithmetic.isInRectangle( dstP, src, yaw, self.width, self.length )
		
	def getObjectList( self, caster, target ):
		"""
		获取区域中的对象列表。
		@param target: 施展对象
		"""	
		centerPos,direction = self.getPositionAndDirection( caster, target )
		centerPos = self.calculateOffset( centerPos, direction )
		
		yaw = self.calculateYaw( direction.z )
		entityList = caster.entityInRangeForSkill( math.sqrt( pow( self.length, 2 ) + pow( self.width /2, 2 ) ) , None, centerPos )
		entitys = [ e for e in entityList if self.inArea( e.position, centerPos, yaw ) ]

		return self.filterHeight( centerPos, entitys )

class Circular( Area ):
	"""圆柱形"""
	def __init__( self ):
		Area.__init__( self )
		self.unitReference = csdefine.SKILL_HIT_AREA_UNIT_CASTER			# 单位位置基准
		self.direReference = csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE			# 单位朝向基准
		self.radius = 0.0						# 半径
		self.height = 0.0						# 高度
		
	def load( self, dictDat ):
		Area.load( self, dictDat )
		if len(dictDat["Param1"].split("|")) > 1:
			KBEDebug.ERROR_MSG("Circular config Param1(%s) is error!!!"%dictDat["Param1"])
		tempList = dictDat["Param2"].split("|")
		if len(tempList) >= 1 and tempList[0]:
			self.radius = float(tempList[0])
		else:
			KBEDebug.ERROR_MSG("Circular config Param2(%s) is error!"%dictDat["Param2"])
			
		if len( tempList ) >= 2 and tempList[1]:
			self.height = float(tempList[1])
			
	def getObjectList( self, caster, target ):
		"""
		获取区域中的对象列表。
		@param target: 施展对象
		"""
		centerPos,direction = self.getPositionAndDirection( caster, target )
		centerPos = self.calculateOffset( centerPos, direction )
		
		es = caster.entityInRangeForSkill( self.radius, None, centerPos )
		circularList = self.filterCircular(es, centerPos, self.radius )

		return self.filterHeight( centerPos, circularList )

class Sector( Area ):
	"""扇形 """
	def __init__( self ):
		"""
		构造函数。
		"""
		Area.__init__( self )
		self.radius	= 0.0				#半径
		self.angle	= 0.0				#夹角
		self.height = 0.0				#高度

	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		Area.load( self, dictDat )
		tempList = dictDat["Param2"].split("|")
		if len( tempList ) >= 2 and tempList[0] and tempList[1]:
			self.radius = float(tempList[0])
			self.angle = float(tempList[1])
		else:
			KBEDebug.ERROR_MSG("Sector config Param2(%s) is error!"%dictDat["Param2"])
		if len( tempList ) >= 3 and tempList[2]:
			self.height = float(tempList[2])

	def inArea( self, dst, src, yaw ):
		"""
		判断位置dstPos是否在扇形范围内
		"""
		dstP = Math.Vector3(dst)
		dstP.y = src.y
		return csarithmetic.isInSector( dstP, src, yaw, self.radius, self.angle )
		
	def getObjectList( self, caster, target ):
		"""
		获取区域中的对象列表。
		@param target: 施展对象
		"""
		centerPos,direction = self.getPositionAndDirection( caster, target )
		centerPos = self.calculateOffset( centerPos, direction )
		es = caster.entityInRangeForSkill( self.radius, None, centerPos )
		circularList = self.filterCircular(es, centerPos, self.radius )
		yaw = self.calculateYaw( direction.z )
		entitys = [ en for en in circularList if self.inArea( en.position, centerPos, yaw ) ]
		return self.filterHeight( centerPos, entitys )

class Ghost( Area ):
	"""
	创建一个傀儡作为受术者
	"""
	def __init__( self ):
		"""
		构造函数。
		"""
		Area.__init__( self )
		self.deathTime = 1.0
	
	def load( self, dictDat ):
		"""
		加载配置
		dictDat={ "Param1": str, "Param2": str, "Param3": str }
		"""
		if dictDat["Param1"]:
			tempList = dictDat["Param1"].split("|")
			if tempList[0]:
				self.unitReference = int( tempList[0] )
				self.direReference = int( tempList[0] )
			if len( tempList ) >= 2 and tempList[1]:
				self.direReference = int( tempList[1] )
			if self.direReference not in GHOST_DIRE_REFERENCE_LIST:
				KBEDebug.ERROR_MSG("%s Config Param1(%s) is ERROR!!! Please Check it!!"%(self.__class__.__name__, dictDat["Param1"]))

		Param3 = dictDat["Param3"].split(";")
		for index, i in enumerate(Param3):
			offset = i.split("|")
			if offset[0]:
				self.offset[index][0] = float( offset[0] )
			if len(offset) >= 2 and offset[1]:
				self.offset[index][1] = float( offset[1] )
			if len(offset) >= 3 and offset[2]:
				self.offset[index][2] = float( offset[2] )
			if len(offset) >= 4 and offset[3]:
				self.offset[index][3] = float(offset[3]) % 360

		if dictDat["Param2"]:
			self.deathTime = float( dictDat["Param2"] )


	def getPositionAndDirection( self, caster, target ):
		"""
		获取坐标和朝向
		"""
		#计算开始和结束偏移
		casterDir = Math.Vector3(caster.direction)
		targetDir = Math.Vector3(caster.direction)
		if target.getType() != csdefine.SKILL_TARGET_OBJECT_POSITION:
			targetDir = Math.Vector3(target.getObject().direction)
		casterPos = Math.Vector3(caster.position)
		targetPos = Math.Vector3(target.getObjectPosition())
		casterPos = self.calculateOffset(casterPos, casterDir, csdefine.SKILL_HIT_OFFSET_START)
		targetPos = self.calculateOffset(targetPos, targetDir, csdefine.SKILL_HIT_OFFSET_END )
		casterDir.z = self.calculateYaw(casterDir.z, csdefine.SKILL_HIT_OFFSET_START)
		targetDir.z = self.calculateYaw(targetDir.z, csdefine.SKILL_HIT_OFFSET_END)
		position = casterPos
		direction = casterDir

		if self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_ABSOLUTE:
			position = Math.Vector3(0.0, 0.0, 0.0)
		elif self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_CASTER:
			position = casterPos
		elif self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_TARGET:
			position = targetPos
		else:
			KBEDebug.ERROR_MSG("%s Config HitAreaType is ERROR"%(self.__class__.__name__))
			
		if self.direReference == csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE:
			direction = Math.Vector3(0.0, 0.0, 0.0)
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_TARGET:			# 施法目标
			direction = targetDir
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_CASTER:
			direction = casterDir
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET:	# 施法者->施法目标(朝向2D)
			if casterPos.flatDistTo(targetPos) < 0.1:
				direction = casterDir		 #位置一样时，使用施法者朝向
			else:
				direction = (0, 0, csarithmetic.getYawByVector3( targetPos - casterPos ))
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER:	# 施法目标->施法者(朝向2D)
			if casterPos.flatDistTo(targetPos) < 0.1:
				direction = targetDir		#位置一样时，使用施法目标朝向
			else:
				direction = (0, 0, csarithmetic.getYawByVector3( casterPos - targetPos ))
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET_3D:	# 施法者->施法目标(朝向3D)
			if casterPos.distTo(targetPos) < 0.1:
				direction = casterDir		 #位置一样时，使用施法者朝向
			else:			
				direction = (0, csarithmetic.getPitchByVector3( targetPos - casterPos ), csarithmetic.getYawByVector3( targetPos - casterPos ))
		elif self.direReference == csdefine.SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER_3D:	# 施法目标->施法者(朝向3D)
			if casterPos.distTo(targetPos) < 0.1:
				direction = targetDir		 #位置一样时，使用施法目标朝向
			else:	
				direction = (0, csarithmetic.getPitchByVector3( casterPos - targetPos ), csarithmetic.getYawByVector3( casterPos - targetPos ))
		else:
			KBEDebug.ERROR_MSG("%s config HitAreaType is ERROR"%(self.__class__.__name__))
			
		return Math.Vector3(position), Math.Vector3(direction)

	def isGhostFly(self, caster, target):
		"""
		判断创建的傀儡是否浮空
		"""
		if self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_CASTER:
			if caster.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
				# 当PC是“非跳跃状态，站立状态”时，PC在地上，傀儡的表现应当是贴地的, 反之浮空
				if caster.jumpShowState == csdefine.JUMP_SHOW_STATE_STAND:
					return False
				else:
					return True
			else:
				#若怪物有#9浮空标志物时，怪物本身是浮空的，傀儡的表现应当是浮空的， 反之贴地
				if caster.hasFlag(csdefine.FLAG_CAN_FLY):
					return True
				else:
					return False				

		# 当位置基准，是一个“单位”
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if target.getObject().isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
				# 当PC是“非跳跃状态，站立状态”时，PC在地上，傀儡的表现应当是贴地的, 反之浮空
				if target.getObject().jumpShowState == csdefine.JUMP_SHOW_STATE_STAND:
					return False
				else:
					return True
			else:
				#若怪物有#9浮空标志物时，怪物本身是浮空的，傀儡的表现应当是浮空的， 反之贴地
				if target.getObject().hasFlag(csdefine.FLAG_CAN_FLY):
					return True
				else:
					return False

		return False
		
	def setParent( self, caster, target, ghost ):
		"""设置移动平台"""
		if self.unitReference == csdefine.SKILL_HIT_AREA_UNIT_TARGET:
			if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:			# 只有 受术者是 单位，并且以 目标坐标作为基准
				targetEnt = target.getObject()
				if targetEnt.parent:
					
					rayPosList = targetEnt.navmeshRaycast( targetEnt.position, ghost.position )
					if rayPosList and ghost.position.flatDistTo( rayPosList[0]) <= 1:		# 如果距离小于1，就默认还在移动平台上
						ghost.parent = targetEnt.parent
				return
		if caster.parent:
			rayPosList = caster.navmeshRaycast( caster.position, ghost.position )
			if rayPosList and ghost.position.flatDistTo( rayPosList[0]) <= 1:
				ghost.parent = caster.parent

	def getObjectList( self, caster, target ):
		"""
		获取区域中的对象列表。
		@param target: 施展对象
		"""
		position, direction = self.getPositionAndDirection( caster, target )
		position = self.calculateOffset( position, direction )
		
		direction.z = self.calculateYaw( direction.z )
		param = {}
		param["deathTime"] = self.deathTime
		param["modelNumber"] = "SK_#204"
		ent = caster.createEntityNear( "GhostReceiver", position, direction, param )
		
		if ent:
			ent.setOwner(caster.id)
			if not self.isGhostFly(caster, target):
				ent.removeFlag(csdefine.FLAG_CAN_FLY)
				self.setParent( caster, target, ent )
			return [ent]
		return []

class Annulus( Area ):
	"""
	环形
	"""
	def __init__( self ):
		Area.__init__( self )
		self.unitReference = csdefine.SKILL_HIT_AREA_UNIT_CASTER			# 单位位置基准
		self.direReference = csdefine.SKILL_HIT_AREA_DIRE_ABSOLUTE			# 单位朝向基准
		self.outerDiameter = 0.0				# 外径
		self.innerDiameter = 0.0				# 内径
		self.height = 0.0						# 高度

	def load( self, dictDat ):
		Area.load( self, dictDat )
		if len(dictDat["Param1"].split("|")) > 1:
			KBEDebug.ERROR_MSG("Annulus config Param1(%s) is error!!!"%dictDat["Param1"])		
		tempList = dictDat["Param2"].split("|")
		if len(tempList) >= 1 and tempList[0]:
			self.innerDiameter = float(tempList[0])
		else:
			KBEDebug.ERROR_MSG("Annulus config Param2(%s) is error!!!"%dictDat["Param2"])			
		if len( tempList ) >= 2:
			self.outerDiameter = self.innerDiameter + float(tempList[1])
		if len( tempList ) >= 3:
			self.height = float(tempList[2])

	def getObjectList( self, caster, target ):
		"""
		获取区域中的对象列表。
		@param target: 施展对象
		"""
		radius = self.outerDiameter
		centerPos,direction = self.getPositionAndDirection( caster, target )
		centerPos = self.calculateOffset( centerPos, direction )	
		es = caster.entityInRangeForSkill( radius, None, centerPos )
		circularList = self.filterCircular(es, centerPos, radius )
		entityList = [e for e in circularList if e.position.flatDistTo(centerPos)>=self.innerDiameter]
		return self.filterHeight( centerPos, entityList )

def newInstance( data ):
	"""
	获取对象选择实例。
		@param areaName:	名称
		@type areaName:		string
	"""
	instance = eval( data["HitAreaType"] )()
	instance.load( data )
	return instance

