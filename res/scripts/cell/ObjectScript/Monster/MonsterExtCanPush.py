# -*- coding: utf-8 -*-
import math
import Math
import KBEDebug
import ObjectScript.Monster.Monster as Monster


class MonsterExtCanPush( Monster.Monster ):
	"""
	可以被玩家推动的怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.pushBuffID = {1:{}, 2:{}}

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		self.moveDistance = float(configData["Param1"])
		self.checkRange = float(configData["Param2"])
		self.scriptIDList = configData["Param3"].split("|")
		if configData["Param4"]:
			Param4 = configData["Param4"].split("|")
			k = 1
			for i in Param4[0].split(":"):
				self.pushBuffID[1][k] = int(i)
				k += 1
			if len(Param4) > 1:
				j = 1
				for v in Param4[1].split(":"):
					self.pushBuffID[2][j] = int(v)
					j += 1

	def getPushBuffID(self, player):
		profession = player.getProfession()
		gender = player.getGender()
		if profession in self.pushBuffID[gender]:
			return self.pushBuffID[gender][profession]
		return 0

	def isCanPush(self, selfEntity, yaw):
		"""
		检测是否可以推动
		"""
		result = True
		centerPos = self.getPushPosition(selfEntity, yaw)
		entityList = selfEntity.entityInRangeForSkill( self.checkRange , None, centerPos )
		for i in entityList:
			if i.scriptID in self.scriptIDList:
				result = False
		return result

	def getPushPosition(self, selfEntity, yaw):
		"""
		获得推动的位置
		"""
		centerPos = Math.Vector3(selfEntity.position)
		if yaw > 0-math.pi/4 and yaw < 0 + math.pi/4:
			centerPos.z += self.moveDistance
		elif yaw > math.pi/2 -math.pi/4 and yaw < math.pi/2 + math.pi/4:
			centerPos.x += self.moveDistance
		elif yaw > -math.pi/2 -math.pi/4 and yaw < -math.pi/2 + math.pi/4:
			centerPos.x -= self.moveDistance
		elif (yaw > -math.pi and yaw < -math.pi + math.pi/4) or (yaw > math.pi - math.pi/4  and yaw < math.pi):
			centerPos.z -= self.moveDistance
		return centerPos

	def isOtherMoving(self, player):
		"""
		是否有其他的在移动
		"""
		entities = player.entitiesInRangeExt( 10.0, "MonsterExtCanPush" )
		for entity in entities:
			if entity.moveControlID != 0:
				return True
		return False