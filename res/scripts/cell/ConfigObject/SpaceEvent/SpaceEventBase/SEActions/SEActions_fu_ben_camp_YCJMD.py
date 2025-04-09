# -*- coding: utf-8 -*-

# 副本事件行为:勇闯绝命岛
import random
import math
import Math
import KBEMath
import KBEDebug
import KBEngine
import Functions
import csarithmetic
import csdefine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase


class SEAction378( SEActionBase ):
	"""
	CST-9960 玩家登上仙舟
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		boatEntityList = spaceEntity.getEntityRecord(self._scriptID)
		if len(boatEntityList) != 1:
			return
		entity = KBEngine.entities.get( boatEntityList[0] )
		pos = KBEMath.KBEngine2UnrealPosition( entity.position )
		trigger.client.OnCampYCJMDBoardBoat(boatEntityList[0], pos)


class SEAction379( SEActionBase ):
	"""
	CST-9960 阵营战场“勇闯绝命岛” 显示双方阵营存活人数
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.showCampYCJMDPopulationUI()


class SEAction380( SEActionBase ):
	"""
	CST-9960 异宝现世
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"] #宝箱ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		curLayer = 0
		layerMax = spaceEntity.getScript().getNavmeshLayers()
		if (layerMax - 1):
			for i in range(layerMax):
				PositionList = KBEngine.collideVertical(spaceEntity.spaceID, i, spaceEntity.position, 2, -2)
				if PositionList and len(PositionList):
					curLayer = i
					break
		spaceEntity.layer = curLayer  # layer动态获取
		fixedPosition = Math.Vector3(spaceEntity.getEndCenterPos())  # 固定点。
		position = fixedPosition
		account = 20  # 用于循环次数 20次还没有找到点，直接刷在固定的点
		while account >= 0:
			account -= 1
			radius = spaceEntity.getEndRadius()
			if radius == 0:
				radius = spaceEntity.getOriginRadius()
			position = csarithmetic.getPositionByCircular(spaceEntity.getEndCenterPos(), radius)  # 随机取点
			checkpos = Math.Vector3(position.x, position.y + 50, position.z)  # 选上方的位置 射线检测
			raycastList = spaceEntity.navmeshRaycast(checkpos, position)
			if raycastList:
				position = raycastList[0]
				break
		direction = Math.Vector3(0.0, 0.0, 0.0)
		spaceEntity.createSpellBox(self._scriptID, position, direction,  {} )

		for player in spaceEntity._spaceRoles:
			player.client.showCampYCJMDBoxPosition(KBEMath.KBEngine2UnrealPosition(position))


class SEAction381( SEActionBase ):
	"""
	CST-9960 毒气失控
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self._amount = 0

	def init( self, section ):
		SEActionBase.init( self, section )
		self._buffID = int(section["param1"])		#中毒buffID
		self._scriptID = section["param2"] 			#陷阱ID
		self._radius = int(section["param3"]) 		#灵气圈的半径
		if section["param4"]:
			self._amount = int(section["param4"]) 		#灵气圈的数量

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for player in spaceEntity._spaceRoles:
			player.addBuff( player, self._buffID)

		curLayer = 0
		layerMax = spaceEntity.getScript().getNavmeshLayers()
		if (layerMax - 1):
			for i in range(layerMax):
				PositionList = KBEngine.collideVertical(spaceEntity.spaceID, i, spaceEntity.position, 2, -2)
				if PositionList and len(PositionList):
					curLayer = i
					break
		spaceEntity.layer = curLayer #layer动态获取

		positionList = []
		# 将圆转化成内接矩形,来取随机圆
		Pos = spaceEntity.getEndCenterPos()
		currRadius = spaceEntity.getEndRadius()
		if currRadius == 0:
			currRadius = spaceEntity.getOriginRadius()
		dist = currRadius * math.sin(math.pi/4)
		p = Math.Vector3(Pos.x - dist - self._radius, Pos.y, Pos.z - dist - self._radius)
		pz = p.z
		radius = self._radius * 2
		for i in range(int(dist/radius)):
			p.x += radius
			p.z = pz
			for j in range(int(dist/radius)):
				p.z += radius
				#对创建的点 进行碰撞检测
				checkpos = Math.Vector3(p.x, p.y + 50, p.z)
				raycastList = spaceEntity.navmeshRaycast(checkpos, p)
				if raycastList:
					positionList.append(Math.Vector3(raycastList[0]))
		random.shuffle(positionList)
		randomPosList = positionList[:self._amount]
		for pos in randomPosList:
			spaceEntity.createTrap(self._scriptID, pos, Math.Vector3(0.0, 0.0, 0.0),  {} )

		for player in spaceEntity._spaceRoles:
			for pos in randomPosList:
				player.client.showCampYCJMDReikiCircle( KBEMath.KBEngine2UnrealPosition(pos), self._radius * 100)

class SEAction382( SEActionBase ):
	"""
	CST-9960 无所遁形
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._time = float(section["param1"])		 #显示时间
		self._refreshTime = float(section["param2"]) #刷新时间

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.refreshCampYCJMDPostion(self._time, self._refreshTime)

class SEAction383( SEActionBase ):
	"""
	CST-9960 天雷之罚
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"] #陷阱ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		position = csarithmetic.getPositionByCircular( spaceEntity.getEndCenterPos(), spaceEntity.getEndRadius() )
		direction = Math.Vector3(0.0, 0.0, 0.0) 
		spaceEntity.createTrap(self._scriptID, position, direction,  {} )

class SEAction385( SEActionBase ):
	"""
	CST-9960 显示阵营战场“勇闯绝命岛”倒计时
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._countdown = int(float(section["param1"]) * 60) #时间（分钟)

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:	
			player.client.OnShowCampYCJMDCountdown(str(Functions.getTime(self._countdown)))

class SEAction386( SEActionBase ):
	"""
	CST-9960 清除地图所有scriptID的icon
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]  #scriptID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:	
			player.client.CleanCampYCJMDIcon(self._scriptID)

class SEAction387( SEActionBase ):
	"""
	CST-9960 阵营战场“勇闯绝命岛”仙舟到达
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:	
			player.client.OnCampYCJMDBoatArrive()

class SEAction399( SEActionBase ):
	"""
	CST-9960 玩家死亡，掉落掉落箱子
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.minDropItemAmount = int( section["param1"] )
		self.maxDropItemAmount = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		amount = random.randint( self.minDropItemAmount, self.maxDropItemAmount )
		dieEntity = KBEngine.entities.get(triggerID,None)
		if dieEntity == None:
			return		
		spaceEntity.onRoleDead( dieEntity, amount )

class SEAction400( SEActionBase ):
	"""
	CST-9960 大地图显示同阵营的位置
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.tickShowSameCampYCJMDPosition()
 
class SEAction401( SEActionBase ):
	"""
	CST-9960 玩家离开大地图显示同阵营的位置
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:	
			player.client.OnPlayerLeaveYCJMD(triggerID)

class SEAction458( SEActionBase ):
	"""
	CST-12212 宝箱刷新规则 指定一个批次和数量 随机刷新 废弃
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		pass


class SEAction464( SEActionBase ):
	"""
	CST-12212 玩家死亡，掉落掉落箱子
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		if dieEntity == None:
			return		
		spaceEntity.onRoleDead(dieEntity)

SEActionBase.setActionClass( "SEAction378",SEAction378 )
SEActionBase.setActionClass( "SEAction379",SEAction379 )
SEActionBase.setActionClass( "SEAction380",SEAction380 )
SEActionBase.setActionClass( "SEAction381",SEAction381 )
SEActionBase.setActionClass( "SEAction382",SEAction382 )
SEActionBase.setActionClass( "SEAction383",SEAction383 )
SEActionBase.setActionClass( "SEAction385",SEAction385 )
SEActionBase.setActionClass( "SEAction386",SEAction386 )
SEActionBase.setActionClass( "SEAction387",SEAction387 )
SEActionBase.setActionClass( "SEAction399",SEAction399 )
SEActionBase.setActionClass( "SEAction400",SEAction400 )
SEActionBase.setActionClass( "SEAction401",SEAction401 )
SEActionBase.setActionClass( "SEAction458",SEAction458 )
SEActionBase.setActionClass( "SEAction464",SEAction464 )
