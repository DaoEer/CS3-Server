# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import Math
import math
import csdefine
import ObjectScript.Monster.Monster as Monster

class MonsterExtMain( Monster.Monster ):
	"""
	联合怪物：主怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self._partScriptID = ""
		self._offset = []

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		if configData["Param1"]:
			Param1 =configData["Param1"].split(";")
			if len(Param1) != 2:
				return
			self._partScriptID = Param1[0]
			offsetParam = Param1[1].split("|")
			for i in offsetParam:
				v = i.split(":")
				self._offset.append((float(v[0]), float(v[1]), float(v[2])))


	def createMonterPart(self, selfEntity):
		"""
		创建副怪
		"""
		if not self._partScriptID:
			return
		for i in self._offset:
			pos = self.offsetMonterPartPos(selfEntity, i[0], i[1], i[2])
			params = {}
			params[ "spawnPos" ] = pos
			params[ "spawnDir" ] = selfEntity.direction
			entity = selfEntity.createMonster( self._partScriptID, pos, selfEntity.direction, params )
			if entity:
				entity.setOwner(selfEntity.id)
				entity.parent = selfEntity
				selfEntity.partMonsterIDs.append(entity.id)


	def offsetMonterPartPos( self, selfEntity, offsetFront, offsetLeft, offsetUp ):
		"""计算偏移量"""
		yaw = selfEntity.direction.z
		position = Math.Vector3( selfEntity.position )
		if offsetFront:
			position.x += offsetFront * math.sin( yaw )
			position.z += offsetFront * math.cos( yaw )
		if offsetLeft:
			position.x += offsetLeft * math.sin( yaw - math.pi/2 )
			position.z += offsetLeft * math.cos( yaw - math.pi/2 )
		if offsetUp:
			position.y += offsetUp

		return position