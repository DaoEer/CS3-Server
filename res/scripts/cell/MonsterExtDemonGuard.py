# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import csstatus
import Math
import math
import random
import csarithmetic
import copy
import FightRuleMgr

import Monster
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
from ConfigObject import PatrolRouteLoader


#额外增加的搜索范围，加上次搜索范围是为了检测：光墙中心位置在玩家和妖卫的外侧，但两边却挡在玩家和妖卫之间的情况
SEARCH_RANGE_EXTRA = 10
VIEW_HEIGTH = 10.0   #视野高度

class MonsterExtDemonGuard(Monster.Monster ):
	"""
	妖卫，CST-3248
	"""

	def __init__( self ):
		"""
		Monster.json配置表
		param1:  radius|angle，半径|角度（扇形）
		"""
		Monster.Monster.__init__( self )
		self.warningList = []
		if self.getScript().param1:
			param1 = self.getScript().param1.split("|")
		else:
			param1 = [30, 90]
		self.viewRadius = float(param1[0])
		self.viewAngle = float(param1[1])
		self.moveTargetPos = self.position 		#移动目标点
		self.movePathPoints = [] 		#移动路径点
		self.doMoveTickTimerID = 0 	    #循环定时器 定时向客户端请求移动位置信息
		self.onDormancyTimerID = 0      #巡逻休眠移动定时器
		self.isPlayerInView = False 			#玩家是否在视野范围 交给客户端tick检测
		self.patrolRouteInfo = None 	#巡逻数据
		self.moveRoutePoint = 1 		#当前巡逻移动路点


	def checkWarningList(self):
		"""
		检查警告列表，并清理已经不在视野内的所有警告列表
		"""
		for entity in range(len(self.warningList)-1, -1, -1):
			if not self.monsterAICheckInViewRange(entity.id):
				self.warningList.remove(entity)
				
	def hasBaffle(self, dstPos, srcPos):
		"""
		检查两个位置键是否有光墙阻挡
		"""
		#只考虑光墙的长度，不考虑高度和宽度
		dist = srcPos.distTo(dstPos)
		entities = self.entitiesInRangeExt(dist + SEARCH_RANGE_EXTRA, "MonsterExtLightWall")
		entitiesExt = self.entitiesInRangeExt(dist + SEARCH_RANGE_EXTRA, "MonsterExtCanPush")
		entities.extend(entitiesExt)
		if entities:
			for entity in entities:
				length = float(entity.param1)
				#怪物到玩家间的线段和光墙两端之间的线段相交，则有光墙阻挡
				(p1, p2) = self.getBothEndPos(length, entity.position, entity.direction.z)
				if self.isIntersect(srcPos, dstPos, p1, p2):
					return True
		return False
		
	def getBothEndPos(self, length, centerPos, yaw):
		"""
		根据线条长度和中心点坐标以及yaw获取两端坐标
		"""
		#计算线段A、B两点的坐标，先计算中心点O到A、B的单位向量
		OA = Math.Vector3(math.sin(yaw+math.pi/2),0,math.cos(yaw+math.pi/2))
		OB = Math.Vector3(math.sin(yaw-math.pi/2),0,math.cos(yaw-math.pi/2))
		#A点坐标
		posA = centerPos + OA*(length/2)
		#B点坐标
		posB= centerPos + OB*(length/2)
		return (posA, posB)
		
	def mult(self, p1, p2, p3):
		"""
		叉积
		"""
		return (p1.x - p3.x) * (p2.z - p3.z) - (p2.x - p3.x) * (p1.z - p3.z)
		
	def isIntersect(self, p1, p2, p3, p4):
		"""
		判断两条线段(p1p2和p3p4)是否相交
		"""
		#p1, p2为一条线段两端点 p3, p4为另一条线段的两端点 相交返回true, 不相交返回false
		if max(p1.x, p2.x) < min(p3.x, p4.x ):
			return False
		if max(p1.z, p2.z) < min(p3.z, p4.z):
			return False
		if max(p3.x, p4.x) < min(p1.x, p2.x):
			return False
		if max(p3.z, p4.z) < min(p1.z, p2.z):
			return False
		if self.mult(p3, p2, p1) * self.mult(p2, p4, p1) < 0:
			return False
		if self.mult(p1, p4, p3) * self.mult(p4, p2, p3) < 0:
			return False
		return True
		
	def isInSameLine(self, p1, p2, p3, p4):
		"""
		判断两个坐标(p3，p4)是否在直线上p1p2
		"""
		#如果p1p3和p1p4的斜率和p1p2的斜率相等，则p3p4都在p1p2的直线上
		k = (p2.z - p1.z) / (p2.x - p1.x)
		if (p3.z - p1.z) / (p3.x - p1.x) == k and (p4.z - p1.z) / (p4.x - p1.x):
			return True
		return False
		
	def getForwardLightWall(self, pos, yaw, m = 1):
		"""
		获取pos位置yaw方向m米内的光墙entity
		param1: m，默认为1
		"""
		x = m * math.cos(yaw)
		z = m * math.sin(yaw)
		p = Math.Vector3(pos.x + x, pos.y, pos.z + z) #pos位置yaw方向m米的坐标
		entities = self.entitiesInRangeExt(m + SEARCH_RANGE_EXTRA, "MonsterExtLightWall")
		if entities:
			for entity in entities:
				length = float(entity.param1)
				#怪物到玩家间的线段和光墙两端之间的线段相交，则有光墙阻挡
				(p1, p2) = self.getBothEndPos(length, entity.position, entity.direction.z)
				if self.isIntersect(pos, p, p1, p2):
					pass
		

#---------------------------重载方法-----------------------------------------------------

	def onEnterReset( self ):
		"""
		virtual method
		进入重置状态
		"""
		for bufIdx in list( self.getAttrBuffs().keys() ):#回走部分buff不移除 CST-1998
			buffData = self.getBuffData( bufIdx )
			if buffData and buffData.buffID not in self.resetKeepBuffs:
				self.removeBuffByIndex( bufIdx  )
		
		self.monsterAIReset()
		self.resetEnemyList()
		#重写重置 直接原地进入自由状态
		self.changeState(csdefine.ENTITY_STATE_FREE)

	def monsterAICheckInTerritory(self):
		"""
		是否在领域范围，这里的领域范围是主动整张地图
		"""
		return True
		
	def onViewRange( self ):
		"""
		视野范围，这里的视野范围是整个地图，玩家和妖卫之间没有光墙就在视野范围之内
		"""
		return

		#清理已经不在视野内的所有敌人
		for id in list(self.enemyList):
			if not self.monsterAICheckInViewRange( id ):
				enemyEntity = KBEngine.entities.get( id, None )
				if enemyEntity:
					FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemyEntity )
				else:
					self.removeEnemy(id)
		self.checkWarningList()

	def monsterAICheckInViewRange(self, id):
		"""
		是否在视野范围
		"""
		return self.isPlayerInView

		# entity = KBEngine.entities.get( id, None )
		# if entity:
		# 	if not self.hasBaffle(entity.position, self.position):
		# 		return True
		# return False

	def moveGoBack(self):
		"""
		"""
		self.goback()

	def stopMovingForType( self, moveType ):
		"""
		停止移动，使用移动等级
		"""
		self.stopMove()

	def moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs  = () ):
		"""
		"""
		return

#-------------------------------------特殊支持--------------------------------------------------
	def chase(self):
		"""
		追击
		"""
		if not self.canMoveCheck():
			return
		self.stopMove()
		self.moveScriptID = csdefine.MOVE_TYPE_CHASE
		self.doMoveTickTimerID = self.addTimerRepeat(0.1, "onChase", ())

	def onChase(self):
		"""
		"""
		targetEntity = KBEngine.entities.get(self.targetID, None)
		if not targetEntity:
			#KBEDebug.ERROR_MSG("targetEntity is not exist!")
			return
		if self.position.flatDistTo(targetEntity.position)<=0.5:
			self.stopMove()
			return
		self.requestMoveData(targetEntity.position)

	
	def patrol(self, patrolRouteInfo, moveRoutePoint =1):
		"""
		"""
		if not self.canMoveCheck():
			return
		self.stopMove()
		self.moveScriptID = csdefine.MOVE_TYPE_PATROL
		if patrolRouteInfo:
			nodeInfo = patrolRouteInfo.get(moveRoutePoint)
			if nodeInfo:				
				self.patrolRouteInfo = patrolRouteInfo
				self.moveRoutePoint = moveRoutePoint		
		self.patrolStart()

	def patrolStart(self):
		"""
		巡逻
		"""	
		if self.patrolRouteInfo:
			nodeInfo = self.patrolRouteInfo.get(self.moveRoutePoint)
			targetPos = Math.Vector3( nodeInfo[ "position" ])
			self.requestMoveData(targetPos)
		else:
			KBEDebug.ERROR_MSG("self.patrolRouteInfo is None!")


	def onPatrolMoveOver(self):
		"""
		"""
		nodeInfo = self.patrolRouteInfo[self.moveRoutePoint]
		stayTime = nodeInfo.get("stayTime", 0.0)
		if stayTime<0.1:
			self.onDormancy()
		else:
			self.onDormancyTimerID = self.addTimerCallBack(stayTime, "onDormancy", ())
		

	def onDormancy(self):
		"""
		移动休眠结束
		"""
		nodeInfo = self.patrolRouteInfo[self.moveRoutePoint] #取出巡逻点信息
		if max( self.patrolRouteInfo.keys() ) <=  self.moveRoutePoint:
			if nodeInfo.get( "isSingle", False ): #是否是只按巡逻路线走一次
				self.stopMove()
				return
			else:
				self.moveRoutePoint = 1 #重置移动到的点
		else:
			self.moveRoutePoint += 1 #移动到下个点
			
		self.patrolStart() #移动到下个点

	def goback(self):
		"""
		回走
		"""
		if not self.canMoveCheck(True):
			return
		self.stopMove()
		if self.position.flatDistTo(self.spawnPos)<0.1:
			self.onGoBackMoveOver()
			return
		self.moveScriptID = csdefine.MOVE_TYPE_GOBACK
		self.requestMoveData(self.spawnPos)

	def onGoBackMoveOver(self):
		"""
		"""
		self.stopMove()
		self.changeState(csdefine.ENTITY_STATE_FREE)
		

	def doMove(self):
		"""
		移动
		movePathPoints: 移动坐标点列表，根据列表中的点依次移动
		"""
		if not self.canMoveCheck():
			return
		if not len(self.movePathPoints):
			return
		targetPos = self.movePathPoints[0]
		self.navigatePointExt(targetPos, self.getSpeed())


	def stopMove(self):
		"""
		"""
		self.moveStopTick()
		self.moveStopDormancy()
		if self.doMoveTickTimerID:
			self.popTimer(self.doMoveTickTimerID)
			self.doMoveTickTimerID = 0
		if self.onDormancyTimerID:
			self.popTimer(self.onDormancyTimerID)
			self.onDormancyTimerID = 0
		self.moveScriptID = csdefine.MOVE_TYPE_STOP

		self.movePathPoints.clear()
		self.cancelController("Movement")


	def doStopMove(self):
		"""
		停止移动
		"""
		if self.moveScriptID == csdefine.MOVE_TYPE_GOBACK:
			self.onGoBackMoveOver()
			return
		if self.moveScriptID == csdefine.MOVE_TYPE_PATROL:
			self.onPatrolMoveOver()
			return
		

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		if len(self.movePathPoints):
			self.movePathPoints.pop(0)

		if len(self.movePathPoints):
			self.doMove()
		else:
			self.doStopMove()

	def requestMoveData(self, targetPos):
		"""
		向客户端请求移动数据 单人副本 唯一客户端
		"""
		player = self.getPlayer()
		if not player:
			#KBEDebug.ERROR_MSG("player is not exist!")
			return
		self.moveTargetPos = targetPos
		player.clientEntity(self.id).CLIENT_GetClientNavPoint(targetPos)


	def getPlayer(self):
		"""
		获取玩家
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			KBEDebug.ERROR_MSG("getCurrentSpace is None!")
			return
		playerList = spaceEntity.getSpaceRoles()
		if not len(playerList):
			#KBEDebug.ERROR_MSG("playerList length is None!")
			return
		player = playerList[0]

		return player


	def CELL_recieveMovePointsfromClient(self, srcEntityID, data):
		"""
		接收客户端反馈的移动路点信息
		"""
		if not self.canMoveCheck():
			return
		#如果客户端取不到点 使用服务器移动
		if not data:
			self.navigatePointExt(self.moveTargetPos, self.getSpeed())
			return

		player = self.getPlayer()
		if not player or player.id != srcEntityID:
			return

		self.movePathPoints = copy.deepcopy(self.analyzeData(data))
		self.doMove()

	def analyzeData(self, data):
		"""
		分析数据
		data: 客户端发送过来的数据，解析此数据生成移动坐标点列表
		"""
		posList = []
		posStrList = data.split(";")
		for posStr in posStrList:
			pos = Math.Vector3([float(x) for x in posStr.split("|")])
			posList.append(pos)
		return posList

	def addViewShapeTrap(self):
		"""
		添加视野陷阱
		"""
		player = self.getPlayer()
		if not player:
			KBEDebug.ERROR_MSG("player is not exist!")
			return

		player.clientEntity(self.id).CLIENT_CreateViewShapeTrap(self.viewRadius, self.viewAngle, VIEW_HEIGTH)
		#player.clientEntity(self.id).CLIENT_OpenInitiactiveTrapEffect(4, self.viewRadius, int(self.viewAngle), 5.0)


	def CELL_OnPlayerEnterViewRange(self, srcEntityID, playerID):
		"""
		"""
		KBEDebug.ERROR_MSG("srcEntityID = %d, playerID=%d"%(srcEntityID, playerID))
		

	def CELL_OnPlayerLeaveViewRange(self, srcEntityID, playerID):
		"""
		"""
		KBEDebug.ERROR_MSG("srcEntityID = %d, playerID=%d"%(srcEntityID, playerID))
		

	def CELL_SetIsPlayerInViewRange(self, srcEntityID, isPlayerInView):
		"""
		"""
		oldState = self.isPlayerInView
		self.isPlayerInView = isPlayerInView

		#从无到有 建立战斗关系 从有到无移除战斗关系
		player = self.getPlayer()
		if not player:
			return
		if self.isPlayerInView:
			if self.canBuildEnemyRelation(player) :
				FightRuleMgr.g_fightMgr.buildEnemyRelation( self, player)
		else:
			FightRuleMgr.g_fightMgr.breakEnemyRelation( self, player )


	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady(self, srcEntityID)
		self.addViewShapeTrap()
		