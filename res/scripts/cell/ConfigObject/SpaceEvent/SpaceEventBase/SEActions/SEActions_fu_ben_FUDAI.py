# -*- coding: utf-8 -*-

# 副本事件行为  福袋副本
import csdefine
import csconst
import random
import KBEDebug
import KBEngine
import Math
import math
import Functions
import ItemFactory
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from ConfigObject.SpaceCopyNPCFuDaiDataLoader import g_SpaceCopyNPCFuDaiData


class SEAction219( SEActionBase ):
	"""
	金枝玉庭: 通知所有Entity往下落
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|")
		self.drag = float(section["param2"]) if section["param2"] else 0.0

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for scriptID in self.scriptIDs:
			idList = spaceEntity.getEntityRecord(scriptID)
			for id in idList:
				entity = KBEngine.entities.get(id,None)
				if entity == None:
					return
				entity.delayStartMove( self.drag )

class SEAction220( SEActionBase ):
	"""
	金枝玉庭: 在触发者出生位置，重新随机刷一个Entity
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID,None)
		random.shuffle( self.scriptIDs )
		if entity and spaceEntity:
			position = entity.spawnPos
			direction = entity.direction
			newEntity= spaceEntity.createEntityByScriptID(self.scriptIDs[0],position,direction,{"spawnPos":position, "spawnDir": direction})
			spaceEntity.allFuDaiScriptIDList.append(newEntity.scriptID)
			
class SEAction221( SEActionBase ):
	"""
	金枝玉庭:通知触发者向下
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.drag = float(section["param1"]) if section["param1"] else 0.0

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(triggerID ,None)
		if entity == None:
			return
		entity.delayStartMove(self.drag)

class SEAction249( SEActionBase ):
	"""
	金枝玉庭:随机事件界面显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._key = section["param1"]
		self._time = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowJinZhiYuTingRandomEvent(self._key, str(self._time * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()))

class SEAction250( SEActionBase ):
	"""
	金枝玉庭:副本结算
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		rewardStr = ""
		for key, value in spaceEntity.spaceRewards.items():
			rewardStr += str(key)+":"+str(value)+"|"
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowJinZhiYuTingRewards(spaceEntity.spaceRewardAmount, rewardStr)

class SEAction283( SEActionBase ):
	"""
	金枝玉庭:阶段提示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._stage = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.spaceJZYTStage = self._stage
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_OnShowJZYTStageTips(self._stage)

class SEAction286( SEActionBase ):
	"""
	金枝玉庭:玩家减少随机数量的金币
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		numList = [int(i) for i in section["param1"].split("|")]
		self._minNum = numList[0]
		self._maxNum = numList[1]
		self._soundID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entity = KBEngine.entities.get(eventParams["extraValue"]["receiverID"] ,None)
		num = random.randint(self._minNum, self._maxNum)
		if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entity.subMoney(num, csdefine.MONEY_SUB_REASON_SPACE_RANDOM)
			entity.showMessagePlaySound(self._soundID)

class SEAction287( SEActionBase ):
	"""
	金枝玉庭:设置副本内玩家获得奖品的倍率
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._rate = float(section["param1"])
		self._soundID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.spaceRewardRate = self._rate
		entity = KBEngine.entities.get(eventParams["extraValue"]["receiverID"] ,None)
		if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entity.showMessagePlaySound(self._soundID)

class SEAction295( SEActionBase ):
	"""
	金枝玉庭:盗宝小贼掉落福袋
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self.offsetList = []	#[(scriptID,pos,dir,amount)]

	def init( self, section ):
		SEActionBase.init( self, section )
		offsetList = section["param1"].split("|")
		for offsetStr in offsetList:
			offset = offsetStr.split(":")
			offsetFront = 0.0
			offsetLeft = 0.0
			offsetUp = 0.0
			if offset[0]:
				offsetFront = float( offset[0] )
			if len(offset) >= 2 and offset[1]:
				offsetLeft = float( offset[1] )
			if len(offset) >= 3 and offset[2]:
				offsetUp = float( offset[2] )
			self.offsetList.append((offsetFront, offsetLeft, offsetUp))
		self.scriptID = section["param2"]
		self.createBuffID = int(section["param3"])


	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if not entityList:
			return			
		def calculateOffset( position, direction ):
			"""计算偏移量"""
			yaw = direction.z
			posList = []
			for offset in self.offsetList:
				pos = Math.Vector3(position)
				if offset[0]:
					pos.x += offset[0] * math.sin( yaw )
					pos.z += offset[0] * math.cos( yaw )
				if offset[1]:
					pos.x += offset[1] * math.sin( yaw - math.pi/2 )
					pos.z += offset[1] * math.cos( yaw - math.pi/2 )
				if offset[2]:
					pos.y += offset[2]
				posList.append(pos)
			return posList
		for entity in entityList:
			createPosList = calculateOffset(entity.position, entity.direction)
			for pos in createPosList:			
				param = {}
				param["deathTime"] = 5.0
				param["modelNumber"] = "SK_#204"
				ent = entity.createEntityNear( "GhostReceiver", pos, entity.direction, param )
				ent.addTimerCallBack( 0.3, "addBuff", (entity, self.createBuffID) )

class SEAction296( SEActionBase ):
	"""
	金枝玉庭:盗宝小贼出来界面
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowJinZhiYuTingMonster()

class SEAction304( SEActionBase ):
	"""
	金枝玉庭：盗宝小贼速度改变
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.moveSpeed = float(section["param1"])
		self.scriptID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if not entityList:
			return
		for entity in entityList:
			entity.moveSpeed = self.moveSpeed
			entity.setTemp("moveSpeed", entity.moveSpeed)

class SEAction305( SEActionBase ):
	"""
	金枝玉庭：怪物掉落的财宝
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]
		self.index = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			if self.index == 1:	# 金币
				trigger.integralAmount = spaceEntity.integralAmount
				spaceEntity.integralAmount = 0
			elif self.index == 2:	# 潜能
				trigger.potentialAmount = spaceEntity.potentialAmount
				spaceEntity.potentialAmount = 0
			elif self.index == 3:	# 材料
				for itemID, value in spaceEntity.materialRewards.items():
					trigger.materialItem = int(itemID)
					if value == 1:
						spaceEntity.materialRewards.pop(itemID)
					else:
						spaceEntity.materialRewards[itemID] -= 1
					return
			elif self.index ==4:	# 装备
				for itemID, value in spaceEntity.equipRewards.items():
					trigger.equipItem = int(itemID)
					if value == 1:
						spaceEntity.equipRewards.pop(itemID)
					else:
						spaceEntity.equipRewards[itemID] -= 1
					return

class SEAction307( SEActionBase ):
	"""
	金枝玉庭：盗宝小贼速度加成，并且远离玩家
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.Percent = float(section["param1"])
		self.timer = float(section["param2"])
		self.scriptID = section["param3"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if not entityList:
			return
		for entity in entityList:
			entity.actCounterInc( csdefine.ACTION_FORBID_SPELL )
			entity.allClients.OnStartFarFromPlayer()
			entity.moveSpeed = entity.moveSpeed + entity.moveSpeed * self.Percent
			if entity.firstFarFrom:
				entity.firstFarFrom = False
				for e in spaceEntity._spaceRoles:
					entity.monsterAIShowMessagePlaySound( e, entity.voiceID[3] )
			entity.addTimerCallBack( self.timer, "onRecoverySpeed", ())

class SEAction313( SEActionBase ):
	"""
	金枝玉庭：守卫收取场景中的财宝
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self.amount = [int(i) for i in section["param1"].split("|")]
		if section["param2"]:
			self.materialList = [int(i) for i in section["param2"].split("|")]
		if section["param3"]:
			self.equipList = [int(i) for i in section["param3"].split("|")]
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		def notifyClientData( key, value ):
			for e in spaceEntity._spaceRoles:
				if e.getClient():
					e.client.CLIENT_NotifyDisplayItemIcon( int(key), int(value) )
		spaceEntity.MonsterPickUpLostTreasures()
		spaceEntity.integralAmount += self.amount[0]
		notifyClientData( 0, spaceEntity.integralAmount )
		materialList = random.sample( self.materialList, self.amount[1] )
		for materialID in materialList:
			if materialID not in spaceEntity.materialRewards:
				spaceEntity.materialRewards[materialID] = 1
			else:
				spaceEntity.materialRewards[materialID] += 1
			notifyClientData(materialID, spaceEntity.materialRewards[materialID])
		equipList = random.sample( self.equipList, self.amount[2] )
		for equipID in equipList:
			if equipID not in spaceEntity.equipRewards:
				spaceEntity.equipRewards[equipID] = 1
			else:
				spaceEntity.equipRewards[equipID] += 1
			notifyClientData(equipID, spaceEntity.equipRewards[equipID])

class SEAction314( SEActionBase ):
	"""
	金枝玉庭：守卫掉落收取的所有财宝
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]
		self.radius = float(section["param2"])
		self.extraTreasure = []
		if section["param3"]:
			self.extraTreasure = [int(i) for i in section["param3"].split("|")]
		self.createBuffID = [int(i) for i in section["param4"].split("|")]
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if not entityList:
			return

		def getRandPosInCircle( centerPos, radius, entity ):
			"""在圆内获得随机点坐标"""
			x = centerPos[2] + random.uniform( -1,1 ) * radius
			y = centerPos[0] + random.uniform( -1,1 ) * radius
			return Math.Vector3( y, entity.position[1], x )

		def createNPCEntityNear( pos, entity, buffID ):
			"""创建"""
			param = {}
			param["deathTime"] = 5.0
			param["modelNumber"] = "SK_#204"
			ent = entity.createEntityNear( "GhostReceiver", pos, entity.direction, param )
			ent.addTimerCallBack( 0.3, "addBuff", (entity, buffID) )

		for entity in entityList:
			if entity.id != spaceEntity.tempMonsterID:
				return
			if len(self.extraTreasure) > 0:
				spaceEntity.integralAmount += self.extraTreasure[0]
				self.extraTreasure.pop(0)
				for treasure in self.extraTreasure:
					itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(treasure)
					if itemInst.isEquip():
						if treasure not in spaceEntity.equipRewards:
							spaceEntity.equipRewards[treasure] = 1
						else:
							spaceEntity.equipRewards[treasure] += 1
					else:
						if data["goodsid"] not in spaceEntity.materialRewards:
							spaceEntity.materialRewards[treasure] = 1
						else:
							spaceEntity.materialRewards[treasure] += 1
			# 创建jinj
			if spaceEntity.integralAmount > 0:
				createPos = getRandPosInCircle( entity.position, self.radius, entity )
				createNPCEntityNear( createPos, entity, self.createBuffID[0])
			# 创建潜能
			if spaceEntity.potentialAmount > 0:
				createPos = getRandPosInCircle( entity.position, self.radius, entity )
				createNPCEntityNear( createPos, entity, self.createBuffID[1])
			# 创建装备
			for key, value in spaceEntity.equipRewards.items():
				for i in range(value):
					createPos = getRandPosInCircle( entity.position, self.radius, entity )
					createNPCEntityNear( createPos, entity, self.createBuffID[2])
			# 创建材料
			for key, value in spaceEntity.materialRewards.items():
				for i in range(value):
					createPos = getRandPosInCircle( entity.position, self.radius, entity )
					createNPCEntityNear( createPos, entity, self.createBuffID[3])
			for e in spaceEntity._spaceRoles:
				e.client.StopDisplayItemIcon()

class SEAction315( SEActionBase ):
	"""
	金枝玉庭：停止显示怪物提示界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.client.StopShowJinZhiYuTingMonster()

SEActionBase.setActionClass("SEAction219", SEAction219)
SEActionBase.setActionClass("SEAction220", SEAction220)
SEActionBase.setActionClass("SEAction221", SEAction221)
SEActionBase.setActionClass("SEAction249", SEAction249)
SEActionBase.setActionClass("SEAction250", SEAction250)
SEActionBase.setActionClass("SEAction283", SEAction283)
SEActionBase.setActionClass("SEAction286", SEAction286)
SEActionBase.setActionClass("SEAction287", SEAction287)
SEActionBase.setActionClass("SEAction295", SEAction295)
SEActionBase.setActionClass("SEAction296", SEAction296)
SEActionBase.setActionClass("SEAction304", SEAction304)
SEActionBase.setActionClass("SEAction305", SEAction305)
SEActionBase.setActionClass("SEAction307", SEAction307)
SEActionBase.setActionClass("SEAction313", SEAction313)
SEActionBase.setActionClass("SEAction314", SEAction314)
SEActionBase.setActionClass("SEAction315", SEAction315)