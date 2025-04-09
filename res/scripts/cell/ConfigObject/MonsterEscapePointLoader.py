# -*- coding:utf-8 -*-
import MonsterEscapePointCfg
import KBEDebug
import csarithmetic
import random
import Math
import Functions
import KBEMath

class MonsterEscapePointLoader:
	"""
	读取怪物逃跑点配置
	"""
	def __init__(self):
		self.monsterEscapePointMap = {}

	def loadConfig( self ):
		pointCfg = MonsterEscapePointCfg.Datas
		for spaceScriptID, datas in pointCfg.items():
			if spaceScriptID not in self.monsterEscapePointMap:
				self.monsterEscapePointMap[spaceScriptID] = {}
			tempData = {}
			for index,data in datas.items():
				posData = {}
				pos = Functions.vector3TypeConvert( data["position"] )
				pos = KBEMath.Unreal2KBEnginePosition( tuple( pos ) )
				posData["position"] = pos
				posData["priority"] = data["priority"]
				tempData[index] = posData
			self.monsterEscapePointMap[spaceScriptID] = tempData

	def reloadConfig(self):
		self.monsterEscapePointMap.clear()
		self.loadConfig()

	def getMonsterEscapePoints( self, monsterEntity,roleList,searchRadius,searchAngle,searchTimes,escapePointNum ):
		"""
		获得怪物的逃跑点
		"""
		currentScriptID = monsterEntity.getCurrentSpaceScriptID()
		if currentScriptID not in self.monsterEscapePointMap:
			KBEDebug.ERROR_MSG("scriptID(%s) is not in MonsterEscapePointCfg"%currentScriptID)
			return []
		pointMaps = self.monsterEscapePointMap[currentScriptID]
		yaw = 0.0
		if len(roleList) == 1:
			yaw = self.getMonsterEscapeYawByPosition( monsterEntity, roleList[0].position )
		elif len(roleList) == 2:
			yaw = self.getMonsterEscapeYawByTwoRole( monsterEntity, roleList )
		else:
			yaw = self.getMonsterEscapeYawByThreeRole( monsterEntity, roleList )

		inAreaIndexs = []
		realSearchTimes = 1
		while searchTimes > 0 and len(inAreaIndexs) <= 0:
			for index, positionData in pointMaps.items():
				if csarithmetic.isInSector(positionData["position"],monsterEntity.position,yaw,searchRadius,(searchAngle * realSearchTimes)) and Math.Vector3(positionData["position"]).flatDistTo(monsterEntity.position) > 3.0:
					inAreaIndexs.append(index)
			realSearchTimes += 1
			searchTimes -= 1

		if not len(inAreaIndexs):
			return []

		priorityIndexs = []
		for index in inAreaIndexs:
			if pointMaps[index]["priority"] > 0:
				priorityIndexs.append(index)

		if len(priorityIndexs) > 0: #如果有特殊点 先按优先级排序  如果优先级最高的只有一个 就取优先级最高的，如果有多个，则按照取距离最远的且优先级最高的
			allPrioritys = []
			resultPriorityDict = {}
			for index in priorityIndexs: 
				resultPriorityDict[index] = pointMaps[index]["priority"]
				allPrioritys.append( pointMaps[index]["priority"] )
			tempIndexs = sorted(resultPriorityDict.keys(), key = lambda s:resultPriorityDict[s],reverse=True)
			maxPrioritys = max( allPrioritys )
			resultPriorityIndexs = []
			for index in tempIndexs:
				if pointMaps[index]["priority"] == maxPrioritys:
					resultPriorityIndexs.append( index )

			if len( resultPriorityIndexs ) == 1:
				index = resultPriorityIndexs[0]
				return [pointMaps[index]["position"]]
			else:
				resultDistDict = {}
				for index in resultPriorityIndexs:
					resultDistDict[index] = Math.Vector3(pointMaps[index]["position"]).flatDistTo( monsterEntity.position )
				resultIndexs = sorted(resultDistDict.keys(), key = lambda s:resultDistDict[s],reverse=True)
				index = resultIndexs[0]
				return [pointMaps[index]["position"]]

		#没有特殊点就随机取 escapePointNum 数
		resultIndexs = []
		if len(inAreaIndexs) >= escapePointNum:
			resultIndexs = random.sample(inAreaIndexs,escapePointNum)
		else:
			resultIndexs = inAreaIndexs

		resultPosList = []
		resultDistDict = {}
		for index in resultIndexs:
			resultDistDict[index] = Math.Vector3(pointMaps[index]["position"]).flatDistTo( monsterEntity.position )

		resultIndexs = sorted(resultDistDict.keys(), key = lambda s:resultDistDict[s])
		for index in resultIndexs:
			resultPosList.append(pointMaps[index]["position"])
		return resultPosList

	def getMonsterEscapeYawByPosition( self, monsterEntity,position ):
		"""
		"""
		vec = monsterEntity.position - position
		return csarithmetic.getYawByVector3(vec)

	def getMonsterEscapeYawByTwoRole( self, monsterEntity, roleList ):
		"""
		方向为两名玩家坐标点连线中点与BOSS坐标点形成的连线的反方向
		"""
		vec = roleList[0].position - roleList[1].position
		vec.normalise()
		length = roleList[0].position.flatDistTo( roleList[1].position )
		vec.x *= (length/2)
		vec.y *= (length/2)
		vec.z *= (length/2)
		centerPos = roleList[1].position + vec
		return self.getMonsterEscapeYawByPosition( monsterEntity, centerPos )

	def getMonsterEscapeYawByThreeRole( self, monsterEntity, roleList ):
		"""
		当有三名玩家时，方向为三名玩家坐标点组成的三角形的中点与BOSS坐标点形成的连线的反方向
		"""
		L1 = roleList[0].position.flatDistTo( roleList[1].position )
		L2 = roleList[1].position.flatDistTo( roleList[2].position )
		L3 = roleList[0].position.flatDistTo( roleList[2].position )
		if (L1 + L2) <= L3 or (L1 + L3) <= L2 or (L2 + L3) <= L1:
			randomRoleList = random.sample( roleList, 2 )
			return self.getMonsterEscapeYawByTwoRole( monsterEntity, randomRoleList )
		x = (L2 * roleList[0].position.x + L1 * roleList[2].position.x + L3 * roleList[1].position.x) / (L1+L2+L3)
		z = (L2 * roleList[0].position.z + L1 * roleList[2].position.z + L3 * roleList[1].position.z) / (L1+L2+L3)
		centerPos = Math.Vector3(x,monsterEntity.position.y,z)
		return self.getMonsterEscapeYawByPosition( monsterEntity, centerPos )
		
g_MonsterEscapePoint = MonsterEscapePointLoader()