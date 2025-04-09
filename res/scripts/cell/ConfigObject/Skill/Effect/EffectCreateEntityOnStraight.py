# -*- coding: utf-8 -*-

from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug
import Math
import math
import KBEngine
import random

class EffectCreateEntityOnStraight( EffectSkillBase ):
	"""
	召唤指定类型数量怪物在一条随机直线上
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.callList = []   	# 召怪列表 [(ScriptID;number)|]
		self.callSumNumber = 0 	# 召怪总数
		self.radius = 0.0	  	# 半径范围
		self.spacing = 0.0		# 每两个怪间距
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		for data in dictDat["Param1"].split("|"):
			scriptID,number = data.split(":")
			self.callSumNumber += int(number)
			self.callList.append((scriptID,int(number)))

		data = dictDat["Param2"].split("|")
		if len(data) >= 2:
			self.radius = float( data[0] )
			self.spacing = float( data[1] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		direction,points = self._getCallInfos( receiver )
		random.shuffle(points) # 打乱直线上点的顺序,使之随机刷怪
		index = 0
		for scriptID, number in self.callList:
			for i in range( number ):
				pos = points[index]
				caster.createEntityByScriptID( scriptID,pos,direction,{"spawnPos":pos, "parent" : receiver.parent} )
				index += 1

	def _getCallInfos( self, receiver ):
		"""
		取得entitiy的位置、朝向
		"""
		firstPos = self._getFirstPos( receiver )
		yaw,allPoints = self._getStraightInfo( receiver, firstPos )
		direction = Math.Vector3( receiver.direction[0], receiver.direction[1], yaw )
		return direction, allPoints

	def _getFirstPos( self, receiver ):
		"""
		#获取得第一个位置，在半径radius范围内随机取得一个合法位置	
		"""
		randomFloatFuction = lambda x,y : x + ( y - x ) * random.random()
		dstPos = Math.Vector3()
		srcPos = receiver.position
		if self.radius > 0:		
			dstPos.x = srcPos.x + randomFloatFuction( -self.radius, self.radius )
			dstPos.z = srcPos.z + randomFloatFuction( -self.radius, self.radius )
			dstPos.y = srcPos.y
			dstPos = self._getCollidePosition( receiver, srcPos, dstPos )
		else:
			dstPos = srcPos
		return dstPos

	def _getCollidePosition( self, receiver, srcPos, dstPos ):
		"""
		"""
		dstPos = Math.Vector3(dstPos)
		rayCastList = receiver.navmeshRaycast( srcPos,dstPos )
		if rayCastList:
			dstPos = Math.Vector3(rayCastList[0])
		highRayCastList = receiver.navmeshRaycast( Math.Vector3( dstPos.x, dstPos.y + 10.0, dstPos.z ), Math.Vector3( dstPos.x, dstPos.y - 10.0, dstPos.z ) )
		if highRayCastList:
			dstPos.y = Math.Vector3(highRayCastList[0]).y
		return dstPos

	def _getStraightInfo( self, receiver, firstPos ):
		"""
		根据第一个位置，获取随机直线上的所有位置信息
		"""
		randomFloatFuction = lambda x,y : x + ( y - x ) * random.random()
		distanceMax = self.callSumNumber * self.spacing
		lastPos = Math.Vector3()

		yaw = randomFloatFuction( -math.pi, math.pi )
		lastPos.x = firstPos.x + distanceMax * math.sin(yaw)
		lastPos.z = firstPos.z + distanceMax * math.cos(yaw)
		lastPos.y = firstPos.y
		result = False
		rayCast = receiver.navmeshRaycast( firstPos, lastPos )
		if rayCast:
			result = True
		circleCount = 0
		# 最大只循环处理 10 次
		while result and circleCount < 10 :
			yaw = randomFloatFuction( -math.pi, math.pi )
			lastPos.x = firstPos.x + distanceMax * math.sin(yaw)
			lastPos.z = firstPos.z + distanceMax * math.cos(yaw)
			lastPos.y = firstPos.y
			rayCast = receiver.navmeshRaycast( firstPos, lastPos )
			circleCount += 1
			if rayCast:
				result = True
			else:
				result = False
	
		allPostions = []
		for n in range( self.callSumNumber ) :
			pos = Math.Vector3()
			pos.x = firstPos.x + n * self.spacing * math.sin(yaw)
			pos.z = firstPos.z + n * self.spacing * math.cos(yaw)
			pos.y = firstPos.y
			pos = self._getCollidePosition( receiver, firstPos, pos )
			allPostions.append( pos )
		return yaw,allPostions