# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
import Math
import KBEMath
import Const
import copy
from ConfigObject.MonsterJumpPointLoader import g_MonsterJumpPoint

MAX_MOVE_SPEED = 25.0 #添加Entity的最大移动速度限制，防止不停循环移动，导致服务器崩溃

class MoveJumpInterface:
	"""
	跳跃点移动接口类
	"""
	def __init__(self):
		self.jumpRoute = []
		self.canJumpMove = False
		self.isJumping = False 			#是否在跳跃过程中
		self.jumpArea = None
		#跳跃点结束TimerID
		self.moveJumpEndID = 0

	def initMoveJumpData(self):
		"""
		"""
		jumpArea = g_MonsterJumpPoint.getMonsterJumpPointdataNew(self.getCurrentSpaceScriptID())['jumpArea']
		if jumpArea:
			self.jumpArea = copy.deepcopy(jumpArea)
		else:
			KBEDebug.ERROR_MSG("get JumpArea error spaceScriptID:%s"%self.getCurrentSpaceScriptID())
			return


	def isCanJumpMove(self, targetPosition):
		#移动目标无效
		#targetPosition = Math.Vector3(self.getMoveScript().getMovePosition( self,  *self.moveArgs ))
		if not targetPosition:
			return False
		#不允许跳跃
		if not self.canJumpMove:
			return False
		#跳跃过程中
		if self.isJumping:
			return False
		#没有跳跃路线
		if not self.getMoveJumpRoute(targetPosition):
			return False
		return True


	def startMoveJump(self, targetPosition):
		"""
		"""
		self.initMoveJumpData()
		return self.moveNearJumpPoint()
	

	def getMoveJumpRoute(self, targetPosition):
		"""
		检测是否需要跳跃，当不在同一导航层的时候可以跳跃
		"""	
		#获取移动路线
		route = self.getNearestRoute(targetPosition)
		if not route:
			return False
		self.jumpRoute = route
		#KBEDebug.ERROR_MSG("getJumpRoute :route = %s"%self.jumpRoute)
		return True


	def moveNearJumpPoint(self):
		"""
		移动到最近的跳跃点
		"""		
		if len(self.jumpRoute)<2:
			KBEDebug.ERROR_MSG("jumpRote:%s, jumpRoute length less than 2 "%str(self.jumpRoute))
			return

		if not self.jumpArea:
			KBEDebug.ERROR_MSG("jumpArea is None!")
			return

		startPoint = self.jumpRoute[0]
		endPoint = self.jumpRoute[1]
		jumpArea = self.jumpArea

		ePosList = sorted(jumpArea[endPoint]["positionList"], key = lambda pos:self.position.distTo(Math.Vector3(pos)))
		sPosList = sorted(jumpArea[startPoint]["positionList"], key = lambda pos:self.position.distTo(Math.Vector3(pos)))

		#判断这两个点之间是否需要做跳跃
		if startPoint[0] == endPoint[0]:
			#在同一层 直接移动过去
			#选取一个离自身最近的endPos
			pos = ePosList[0]
		else:
			#在不同层 需要做跳跃
			#获取一个距离自身最近的startPos
			pos = sPosList[0]

		moveControlID =  self.navigatePointExtMoveJump( pos, self.moveSpeed, 0.1 )
		if moveControlID == 0 and self.position.flatDistTo(pos)<=0.1:
			self.onMoveNearJumpPoint()
		return moveControlID


	def onMoveNearJumpPoint( self):
		"""
		vitural  method
		移动结束
		"""
		#判断是不是从同层移动过来的
		startPoint = self.jumpRoute[0]
		endPoint = self.jumpRoute[1]

		if startPoint[0] == endPoint[0]:
			self.moveJumpOver()
		else:
			self.jumpMove(endPoint)


	def jumpMove(self, endPoint):
		"""
		"""
		#设置跳跃中标志
		self.isJumping = True
		#选择一个最近的登陆点
		jumpArea = copy.deepcopy(g_MonsterJumpPoint.getMonsterJumpPointdataNew(self.getCurrentSpaceScriptID())["jumpArea"])
		sorted(jumpArea[endPoint]["positionList"], key = lambda pos:self.position.flatDistTo(Math.Vector3(pos)), reverse = False)
		pos = jumpArea[endPoint]["positionList"][0]

		#大概计算一个移动时间 正常情况下需要等待客户端的通知
		delayTime = self.position.distTo(pos) / Const.MONSTER_JUMP_SPEED
		
		CStartPosition = KBEMath.KBEngine2UnrealPosition(self.position)
		CEndPosition = KBEMath.KBEngine2UnrealPosition(pos)
		self.allClients.CLIENT_MonsterJumpPointToPoint(CStartPosition, CEndPosition, Const.MONSTER_JUMP_SPEED*100)

		self.turnToPos(pos)
		self.position = Math.Vector3(pos)
		self.layer = endPoint[0]
		self.addFlag( csdefine.FLAG_CANT_SELECTED )
		self.addFlag(csdefine.FLAG_HIDE_FLOAT_NAME)
		self.addFlag(csdefine.FLAG_HIDE_FLOAT_HPBAR)
		self.addFlag(csdefine.FLAG_HIDE_FLOAT_LEVEL)
		self.addFlag(csdefine.FLAG_CANT_ROTATE)
		self.actCounterInc(csdefine.ACTION_FORBID_BE_ATTACK)
		self.actCounterInc(csdefine.ACTION_FORBID_MOVE)
		
		#正常情况下只会有一个timerID
		if self.moveJumpEndID:
			KBEDebug.ERROR_MSG("ERROR  entity.id = %d moveJumpEndID = %d"%(self.id, self.moveJumpEndID))
			KBEDebug.print_stack()
		self.moveJumpEndID = self.addTimerCallBack(delayTime + 10.0, "onEndMonsterJump", ())


	def onEndMonsterJump(self):
		"""
		怪物跳跃完成切回原来的移动
		"""
		#临时处理 停止当前的动作 当服务器收不到客户端跳跃停止的时候可以恢复怪物的动作（怪物此时动作可能为跳跃动作）
		self.allClients.CLIENT_StopAction()
		self.moveJumpEndID = 0
		self.removeFlag( csdefine.FLAG_CANT_SELECTED )
		self.removeFlag(csdefine.FLAG_HIDE_FLOAT_NAME)
		self.removeFlag(csdefine.FLAG_HIDE_FLOAT_HPBAR)
		self.removeFlag(csdefine.FLAG_HIDE_FLOAT_LEVEL)
		self.removeFlag(csdefine.FLAG_CANT_ROTATE)
		
		self.actCounterDec(csdefine.ACTION_FORBID_BE_ATTACK)
		self.actCounterDec(csdefine.ACTION_FORBID_MOVE)
		self.isJumping = False
		#只做一段跳跃移动就切回原移动
		self.moveJumpOver()


	def moveJumpOver(self):
		"""
		跳跃移动结束
		"""
		#切回原来的移动
		self.jumpRoute.clear()
		self.moveControlID = self.getMoveScript().start(self, *self.moveArgs)


	def getJumpRoute(self, targetPosition):
		"""
		获取跳跃路线
		"""
		jumpData = g_MonsterJumpPoint.getMonsterJumpPointdataNew(self.getCurrentSpaceScriptID())
		if not jumpData:
			return
		jumpArea = jumpData["jumpArea"]
		if not jumpArea:
			return []
		
		layers = self.getCurrentSpace().getScript().getNavmeshLayers()
		targetLayer = -1
		for i in range(layers):
			#垂直取点 判断是否在此layer上
			PositionList = KBEngine.collideVertical(self.spaceID, i, targetPosition, 2, -2 )
			#找到目标所在layer
			if PositionList:
				targetLayer = i
				break
		#没有找到目标点所在导航层 则无法寻路过去
		if targetLayer<0:
			return []
		#如果是同一层 则不需要跨层移动
		if self.layer == targetLayer:
			return []

		#找到自身当前所在层的跳跃点区域
		startPointList = [point  for point in jumpArea.keys() if point[0] == self.layer]
		#找到目标点所在导航层的跳点区域
		endPointList = [point for point in jumpArea.keys() if point[0] == targetLayer]

		route = []
		#找出一条可连通当前层与目标层的路径
		for startPoint in startPointList:
			for endPoint in endPointList:
				route = g_MonsterJumpPoint.getJumpRoute(jumpData, startPoint, endPoint)
				if len(route)>=2:
					return route
	
		return route

	def getPosLayer(self, pos, spaceID):
		"""
		获取某个点所在的导航层
		"""
		layers = self.getCurrentSpace().getScript().getNavmeshLayers()

		for i in range(layers):
			#垂直取点 判断是否在此layer上
			posList = KBEngine.collideVertical(spaceID, i, pos, 2, -2 )
			#找到目标所在layer
			if posList:
				return i
		#找不到返回 -1
		return -1


	def getNearestRoute(self, targetPosition):
		"""
		获取最短路径
		"""
		try:
			datas = g_MonsterJumpPoint.getMonsterJumpPointdataNew(self.getCurrentSpaceScriptID())
			jumpArea = datas["jumpArea"]
			jumpRoute = datas["jumpRoute"]
		except Exception as e:
			KBEDebug.ERROR_MSG("MonsterJumpPointdataNew.py is error %s:"%e)
			return []
		targetLayer = self.getPosLayer(targetPosition, self.spaceID)
		if targetLayer == -1:
			return []
		
		#如果是同一层不需要做跨层移动
		if self.layer == targetLayer:
			return []
		startPoints = [point for point in jumpArea.keys() if point[0] == self.layer]
		endPoints = [point for point in jumpArea.keys() if point[0] == targetLayer]

		
		#获取起始点与结束点的组合
		groupPoints = []
		for sPoint in startPoints:
			for ePoint in endPoints:
				groupPoints.append((sPoint, ePoint))

		#遍历所有路径
		routeList = []

		for key,route in jumpRoute.items():
			for group in groupPoints:
				if group[0] in route and group[1] in route:
					idxS = route.index(group[0])
					idxE = route.index(group[1])
					if idxS<idxE:
						_route = route[idxS:idxE+1]
						distance = self.position.distTo(Math.Vector3(jumpArea[group[0]]["centerPos"])) + Math.Vector3(targetPosition).distTo(Math.Vector3(jumpArea[group[1]]["centerPos"]))
						for index in range(len(_route)-1):
							distance += Math.Vector3(jumpArea[_route[index]]["centerPos"]).distTo(Math.Vector3(jumpArea[_route[index+1]]["centerPos"]))
						routeList.append((distance, _route))
		
		if not len(routeList):
			return []
		#KBEDebug.ERROR_MSG("routeList = %s"%routeList)
		routeList = sorted(routeList, key = lambda x: x[0])
		#KBEDebug.ERROR_MSG("the best route:%s"%str(routeList[0]))
		return routeList[0][1]


	def navigatePointExtMoveJump( self,  targetPosition, speedVal, distance = 0.0, faceMovement = True, flag = 0xFFFF, layer = 0, maxMoveDistance = 0xFFFF, maxSearchDistance = 0xFFFF):
		"""
		protected method
		引擎方法navigatet封装
		此方法不允许重载
		@param	targetPosition:    目标坐标点
		@param	faceMovement:	 是否面向目标移动
		@param	distance:	  	 距离目标点多远停止移动
		@param	flag: 			 移动区域标志
		@param	layer: 			 使用某层导航层来进行导航
		@param	userData:        传递给回调函数的参数
		@param	maxMoveDistance: 最大移动距离，目前引擎底层预留该参数，但未起作用，0xFFFF默认值
		@param	maxSearchDistance: 最大搜索距离，目前引擎底层预留该参数，但未起作用，0xFFFF默认值
		"""
		moveControlID = 0
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			flag = spaceEntity.getAreaFlags()
		
		if not self.parent:
			moveControlID = self.navigate( targetPosition, min( speedVal, MAX_MOVE_SPEED ) , float( distance ), maxMoveDistance, maxSearchDistance, faceMovement, self.layer, flag, csdefine.MOVE_TYPE_JUMP )
		else:
			moveControlID = self.navigateForParent( targetPosition, min( speedVal, MAX_MOVE_SPEED ), float( distance ), maxMoveDistance, maxSearchDistance, faceMovement, self.layer, flag, csdefine.MOVE_TYPE_JUMP )
		
		return moveControlID


	def doMoveOver( self, controllerID, moveScriptID ):
		"""
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		if moveScriptID == csdefine.MOVE_TYPE_JUMP and controllerID:
			self.onMoveNearJumpPoint()