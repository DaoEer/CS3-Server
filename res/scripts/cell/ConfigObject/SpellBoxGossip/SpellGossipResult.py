# -*- coding: utf-8 -*-

import csdefine
import Math
import math
import csarithmetic
import random
import KBEDebug
import csstatus
import Define
import KBEngine
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
import Const
import Functions
import KBEMath
import ItemFactory
import cschannel_msgs
import functools
import KST

class SpellGossipResultBase:
	"""
	交互效果脚本基类
	"""
	def __init__( self ):
		pass
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		pass

class SpellGossipResultRandom( SpellGossipResultBase ):
	"""
	随机出现结果
	"""
	def __init__( self ):
		self._param1 = []
		self._param2 = [] #每个结果的随机概率
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._param1 = configDict["param1"].split("|")
		self._param2 = configDict["param2"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if len(self._param1) < csdefine.SPELL_BOX_RESULT_ADDITEM + 1 or len(self._param2) < csdefine.SPELL_BOX_RESULT_ADDITEM + 1:
			KBEDebug.ERROR_MSG(" SpellGossipResultRandom config is error ")
			return
		def random_pick(tempList,probabilityList):
			temp = random.uniform(0,1)
			tempProbability = 0.0
			for item,item_probability in zip(tempList,probabilityList):
				if item_probability == "":
					item_probability = 0
				tempProbability += float(item_probability)
				if temp < tempProbability:break
			return item
		result = random_pick(csdefine.SPELL_BOX_RESULT_LIST,self._param2)
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity and playerCell.isInSpaceCopy() and not (spaceEntity.queryTemp("IsGetKey") == True):
			boxEntityList = spaceEntity.getEntityRecord(boxEntity.scriptID)
			if spaceEntity.queryTemp("AmountOfGetKey") == None:
				spaceEntity.setTemp("AmountOfGetKey",0)
			if spaceEntity.queryTemp("AmountOfGetKey") < csdefine.SPELL_BOX_RESULT_AFTER_THE_NUMBER_OF_GETKEY and boxEntity.scriptID != str(csdefine.SPELL_BIG_BOX) and spaceEntity.scriptID == "fu_ben_fengmingxunbao1":
				result = random.randint(csdefine.SPELL_BOX_RESULT_ADDEXP,csdefine.SPELL_BOX_RESULT_ADDITEM)
			if len(boxEntityList) == 1 and boxEntity.scriptID != str(csdefine.SPELL_BIG_BOX):
				result = csdefine.SPELL_BOX_RESULT_GETKEY
				

		position = boxEntity.position
		direction = boxEntity.direction
		tempTime = 0.0
		if boxEntity.destroyTime > 0.2:
			tempTime = boxEntity.destroyTime - 0.2
		if result == csdefine.SPELL_BOX_RESULT_GETKEY and spaceEntity.queryTemp("IsGetKey") == True:
			result = random.randint(csdefine.SPELL_BOX_RESULT_ADDEXP,csdefine.SPELL_BOX_RESULT_ADDITEM)
		if result != csdefine.SPELL_BOX_RESULT_GETKEY and spaceEntity and playerCell.isInSpaceCopy():
			spaceEntity.setTemp("AmountOfGetKey",spaceEntity.queryTemp("AmountOfGetKey") + 1)
		if result == csdefine.SPELL_BOX_RESULT_GETKEY and boxEntity.scriptID != str(csdefine.SPELL_BIG_BOX) and not (spaceEntity.queryTemp("IsGetKey") == True) and playerCell.isInSpaceCopy():
			if self._param1[0]:
				spaceEntity.setTemp("IsGetKey",True)
				boxEntity.addTimerCallBackForScript( tempTime, "delyGetResult",(playerCell.id,result,self._param1[0]))
		elif result == csdefine.SPELL_BOX_RESULT_ADDEXP:
			if self._param1[1]:
				boxEntity.addTimerCallBackForScript( tempTime ,"delyGetResult",(playerCell.id,result,int(self._param1[1])) )
		elif result == csdefine.SPELL_BOX_RESULT_ADDBUFF:
			if self._param1[2]:
				buffList = self._param1[2].split(";")
				index = random.randint(0,len(buffList)-1)
				boxEntity.addTimerCallBackForScript( tempTime,"delyGetResult",(playerCell.id,result,int(buffList[index])) )
		elif result == csdefine.SPELL_BOX_RESULT_CREATEMONSTER:
			if self._param1[3]:
				idList = self._param1[3].split(";")
				index = random.randint(0,len(idList)-1)
				playerCell.addTimerCallBack(tempTime,"createEntityByScriptID",(idList[index],position, direction, { "spawnPos":tuple(Math.Vector3(position)), "spawnDir":tuple(Math.Vector3(direction))}))
		elif result == csdefine.SPELL_BOX_RESULT_ADDITEM:
			if self._param1[4]:
				itemIDList = self._param1[4].split(";")
				index = random.randint(0,len(itemIDList)-1)
				playerCell.addTimerCallBack(tempTime,"addItemByOpenSpellBox",(int(itemIDList[index]),1,csdefine.ITEM_ADD_BY_OPEN_SPELLBOX))

				
class SpellGossipResultRandomFromMoreBox( SpellGossipResultBase ):
	"""
	CS-4021 程序功能需求（35级）——幻阵迷宫奇遇副本藏宝库程序需求
	多种宝箱开出一种钥匙
	随机出现结果
	"""
	def __init__( self ):
		self._param1 = []
		self._param2 = [] 	#每个结果的随机概率
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._param1 = configDict["param1"].split("|")
		self._param2 = configDict["param2"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if len(self._param1) < csdefine.SPELL_BOX_RESULT_ADDITEM + 1 or len(self._param2) < csdefine.SPELL_BOX_RESULT_ADDITEM + 1:
			KBEDebug.ERROR_MSG(" SpellGossipResultRandomFromMoreBox config is error ")
			return
			
		def random_pick(tempList,probabilityList):
			temp = random.uniform(0,1)
			tempProbability = 0.0
			for item,item_probability in zip(tempList,probabilityList):
				if item_probability == "":
					item_probability = 0
				tempProbability += float(item_probability)
				if temp < tempProbability:break
			return item
			
		result = random_pick(csdefine.SPELL_BOX_RESULT_LIST,self._param2)
		afterNumGetKey = "AfterNumGetKey_{}".format(self._param1[0])
		amountGetKey = "AmountGetKey_{}".format(self._param1[0])
		
		spaceEntity = playerCell.getCurrentSpace()
		dct = spaceEntity.queryTemp(self._param1[0], None)
		times = dct.get("times", 0)						#最大次数
		securityTimes = dct.get("securityTimes", 0)		#保底次数
		spellBoxIDList = dct.get("spellBoxIDList", [])
		
		if playerCell.isInSpaceCopy() and (spaceEntity.queryTemp(amountGetKey, 0) < times):
			amount = 0
			for spellBoxID in spellBoxIDList:
				amount += len(spaceEntity.getEntityRecord(spellBoxID))
			
			#达到保底次数还没获得过一次，那么就给钥匙
			if spaceEntity.queryTemp(afterNumGetKey, 0) >= (securityTimes - 1) and spaceEntity.queryTemp(amountGetKey, 0) <= 0:
				result = csdefine.SPELL_BOX_RESULT_GETKEY
				
			#如果剩下的宝箱跟已经获得过的次数之和等于最大次数，那么这些剩下的宝箱应该都给钥匙
			if amount + spaceEntity.queryTemp(amountGetKey, 0) <= times:
				result = csdefine.SPELL_BOX_RESULT_GETKEY
		
		position = boxEntity.position
		direction = boxEntity.direction
		tempTime = 0.0
		if boxEntity.destroyTime > 0.2:
			tempTime = boxEntity.destroyTime - 0.2
		
		#已经获得了指定次数钥匙的话，那就再随一次，给一些其他东西
		if result == csdefine.SPELL_BOX_RESULT_GETKEY and spaceEntity.queryTemp(amountGetKey, 0) >= times:
			result = random.randint(csdefine.SPELL_BOX_RESULT_ADDEXP,csdefine.SPELL_BOX_RESULT_ADDITEM)
		#记录当前已经开过的次数
		spaceEntity.setTemp(afterNumGetKey,spaceEntity.queryTemp(afterNumGetKey, 0) + 1)
			
		if result == csdefine.SPELL_BOX_RESULT_GETKEY and boxEntity.scriptID != str(csdefine.SPELL_BIG_BOX) and (spaceEntity.queryTemp(amountGetKey, 0) < times) and playerCell.isInSpaceCopy():
			if self._param1[0]:
				spaceEntity.setTemp(amountGetKey, spaceEntity.queryTemp(amountGetKey, 0) + 1)
				boxEntity.addTimerCallBackForScript( tempTime, "delyGetResult",(playerCell.id,result,self._param1[0]))
		elif result == csdefine.SPELL_BOX_RESULT_ADDEXP:
			if self._param1[1]:
				boxEntity.addTimerCallBackForScript( tempTime ,"delyGetResult",(playerCell.id,result,int(self._param1[1])) )
		elif result == csdefine.SPELL_BOX_RESULT_ADDBUFF:
			if self._param1[2]:
				buffList = self._param1[2].split(";")
				index = random.randint(0,len(buffList)-1)
				boxEntity.addTimerCallBackForScript( tempTime,"delyGetResult",(playerCell.id,result,int(buffList[index])) )
		elif result == csdefine.SPELL_BOX_RESULT_CREATEMONSTER:
			if self._param1[3]:
				idList = self._param1[3].split(";")
				index = random.randint(0,len(idList)-1)
				playerCell.addTimerCallBack(tempTime,"createEntityByScriptID",(idList[index],position, direction, { "spawnPos":tuple(Math.Vector3(position)), "spawnDir":tuple(Math.Vector3(direction))}))
		elif result == csdefine.SPELL_BOX_RESULT_ADDITEM:
			if self._param1[4]:
				itemIDList = self._param1[4].split(";")
				index = random.randint(0,len(itemIDList)-1)
				playerCell.addTimerCallBack(tempTime,"addItemByOpenSpellBox",(int(itemIDList[index]),1,csdefine.ITEM_ADD_BY_OPEN_SPELLBOX))

class SpellGossipResultGetItem( SpellGossipResultBase ):
	"""
	交互获得物品
	"""
	def __init__( self ):
		self.itemList = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.itemList = configDict["param1"].split(";")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for item in self.itemList:
			itemData = item.split("|")
			tempProbability = random.uniform(0,1)
			if float(itemData[2]) < tempProbability:
				return
			playerCell.addItemByOpenSpellBox(int(itemData[0]),int(itemData[1]),csdefine.ITEM_ADD_BY_OPEN_SPELLBOX)

class SpellGossipResultGetBuff( SpellGossipResultBase ):
	"""
	交互获得若干Buff
	"""
	def __init__( self ):
		self._param1 = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._param1 = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for buffID in self._param1:
			playerCell.addBuff( boxEntity,int(buffID) )

class SpellGossipResultBunchDoorTeleport( SpellGossipResultBase ):
	"""
	副本串传送门对话后传送
	"""
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = boxEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().spaceBunch_doorTeleport( spaceEntity )

class SpellGossipResultCreateMonster( SpellGossipResultBase ):
	"""
	交互创建怪物
	"""
	def __init__( self ):
		self._param1 = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._param1 = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for scriptID in self._param1:
			playerCell.createEntityByScriptID( scriptID, boxEntity.position,boxEntity.direction,{ "spawnPos":tuple(boxEntity.position)} )

class SpellGossipCreatePieceEntity( SpellGossipResultBase ):
	"""
	交互创建相反棋子
	"""
	def __init__( self ):
		pass
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		boxEntityID = boxEntity.id
		createTime = boxEntity.destroyTime +0.2
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addTimerCallBack(createTime,"createPiece",(boxEntityID,))
			#spaceEntity.createPiece( boxEntity.id )


class SpellGossipResultSpellSelf( SpellGossipResultBase ):
	"""
	玩家对自身使用技能
	"""
	def __init__( self ):
		self.skillID = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.skillID = int(configDict["param1"].strip())
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		playerCell.useSkillToEntity(self.skillID,playerCell.id)


class SpellGossipResultGotoSpacePlane( SpellGossipResultBase ):
	"""
	传送进入位面
	"""
	def __init__( self ):
		self.spaceScriptID = ""
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.spaceScriptID = configDict["param1"].strip()
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		playerCell.gotoSpacePlane(self.spaceScriptID)


class SpellGossipResultCompleteTask( SpellGossipResultBase ):
	"""
	完成某任务目标
	"""
	def __init__( self ):
		self.questID = ""
		self.taskID	 = []
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.questID = int(configDict["param1"].strip())
		self.taskID = [int(i) for i in configDict["param2"].strip().split("|")]


	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for ID in self.taskID:
			playerCell.forceQuestTaskIncreaseState(self.questID, ID)

class SpellGossipResultRemoveItemByScriptID( SpellGossipResultBase ):
	"""
	通过scriptID移除一定数量的物品
	"""
	def __init__( self ):
		self.itemID = 0
		self.amount = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.itemID = int(configDict["param1"].strip())
		self.amount = int(configDict["param2"].strip())
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		_amount = self.amount
		itemList = playerCell.getItemInstsByID(self.itemID)
		playerCell.removeItemListByAmount( itemList, self.amount, csdefine.ITEM_REMOVE_BY_SPELL_BOX)
		
class SpellGossipResultReduceItemByScriptID( SpellGossipResultBase ):
	"""
	减少物品使用次数（按品质、绑定方式 顺序减少）
	"""
	def __init__( self ):
		self.itemIDs = []
		self.amount = 1

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.itemIDs = [int(i) for i in configDict["param1"].split("|") ]
		if configDict["param2"]:
			self.amount = int(configDict["param2"])
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		def reversed_cmp(x, y):
			if x.getQuality() < y.getQuality():return 1
			if x.getQuality() > y.getQuality():return -1
			return x.bindType >= y.bindType
		_amount = self.amount
		itemList = playerCell.getItemInstsByIDList( self.itemIDs )
		sorted(itemList, key = functools.cmp_to_key( reversed_cmp ))
		for item in itemList:
			if item.amount >= _amount:
				item.reduce( playerCell, item.amount )
				return
			else:
				item.reduce( playerCell, _amount - item.amount)
				_amount -= item.amount

class SpellGossipResultTeleportTeammate( SpellGossipResultBase ):
	"""
	传送其它玩家到自己身边
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for mb in self.getAllTeamMemberMB():
			entity = KBEngine.entities.get( mb.id, None )
			if not entity or entity.spaceID != self.spaceID:
				continue
			entity.client.RoleTeamSpellBoxFollow(playerCell.id)
		
class SpellGossipResultAddIntegral( SpellGossipResultBase ):
	"""
	晶石狩猎场 获得积分(金精)
	"""
	def __init__( self ):
		self._integral = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._integral = int(configDict["param1"])
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addPlayerIntegral( playerCell,self._integral )
			boxEntity.setTemp("BoxReward",self._integral)

class SpellGossipResultSparHunTingRandom( SpellGossipResultBase ):
	"""
	晶石狩猎场 随机结果
	"""
	def __init__( self ):
		self._buffList = []
		self._scriptIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._buffList = configDict["param1"].split("|")
		self._scriptIDList = configDict["param2"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		buffList = list(self._buffList)
		scriptIDList = list(self._scriptIDList)
		totalList = []
		buffList.extend(scriptIDList)
		totalList.extend(buffList)
		random.shuffle(totalList)
		result = random.choice(totalList)
		if result in self._buffList:
			playerCell.addBuff( playerCell,int(result) )
		else:
			entity = playerCell.createEntityByScriptID(result,boxEntity.position,boxEntity.direction, { "spawnPos":boxEntity.position, "spawnDir":boxEntity.direction})
			if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				integral = boxEntity.queryTemp("BoxReward")
				entity.setTemp("MonsterReward",integral)

class SpellGossipResultExChangeIntegral( SpellGossipResultBase ):
	"""
	晶石狩猎场 兑换积分(金精)
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.playerExchangeToMoney( playerCell )

class SpellGossipResultHunTingCampGetMoney(SpellGossipResultBase):
	"""
	晶石狩猎场 获得金钱
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.taoSimCamp = configDict["param1"]	#仙道陷阱
		self.demonCamp = configDict["param2"]	#仙道陷阱
		self.rewardMoney = int(configDict["param3"])		#奖励的金钱

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		scriptID = ""
		if playerCell.getCamp() == csdefine.CAMP_TAOSIM:
			scriptID = self.taoSimCamp
		else:
			scriptID = self.demonCamp
		entity = boxEntity.createEntityByScriptID( scriptID,boxEntity.position,boxEntity.direction,{ "spawnPos":boxEntity.position,"spawnDir":boxEntity.direction } )
		spaceEntity = boxEntity.getCurrentSpace()
		if spaceEntity and entity:
			boxEntity.setTemp("rewardCamp",playerCell.getCamp())
			boxEntity.setTemp("trapID",entity.id)
			entity.setTemp("rewardMoney",0)
			entity.setTemp( "rewardCamp", [playerCell.getCamp(),self.rewardMoney] )
			playerCell.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_HAS_CAMP_GOSSIP)

class SpellGossipResultMoveBack(SpellGossipResultBase):
	"""
	箱子后退（用于灵岛危机推滚石玩法）
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._moveSpeed = float(configDict["param1"])		#移动速度
		self._backDistance = float(configDict["param2"])	#后退距离
		self._actionID = ""
		if configDict["param3"]:
			self._actionID = configDict["param3"]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		yaw = csarithmetic.getYawByVector3( boxEntity.position - playerCell.position )		# 击退朝向
		dest = Math.Vector3( self._backDistance * math.sin( yaw ), 0, self._backDistance * math.cos( yaw ) )
		dstPosition = Math.Vector3( boxEntity.position + dest )		#目标位置
		raycastList = boxEntity.navmeshRaycast( boxEntity.position, Math.Vector3(boxEntity.position + dest) )
		if raycastList:
			dstPosition = raycastList[0]
		actionTime = self._backDistance / self._moveSpeed
		boxEntity.allClients.CLIENT_OnPlayAction(self._actionID,actionTime)
		boxEntity.navigate( dstPosition, self._moveSpeed, 0.0, 0xFFFF, 0xFFFF, True, 0, 0xFFFF,0 )

class SpellGossipResultGetShield( SpellGossipResultBase ):
	"""
	CST-2149 获得化元盾
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.countKey = configDict["param1"]		#接收灵箭计数的Key
		self.shieldValueKey = configDict["param2"]	#化元盾耐久度Key

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.setTemp("ShieldMaxValue",100)
			spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.countKey ,0 )	#0代表吸收的灵箭数
			spaceEntity.getScript().spaceEvent_addCount( spaceEntity,self.shieldValueKey ,100)#100代表化元盾耐久度初始值为
			playerCell.client.OnAddShield(100,100) #这里100 代表化元盾耐久度初始值为100


class SpellGossipResultSendAICmdToSpace( SpellGossipResultBase ):
	"""
	CST-3260 给副本发送通知
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.key = configDict["param1"]	#string类型
		self.extraValue = configDict["param2"]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "AI", boxEntity.scriptID, self.key, self.extraValue )
			KBEDebug.DEBUG_MSG("AI notify space condition change. entity id:%s. "%boxEntity.id, spaceEntity.id, self.key )

class SpellGossipResultOpenStone( SpellGossipResultBase ):
	"""
	CST-3236 激活封印石
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		configData = configDict["param1"].split("|")
		self.destroyTime = float(configData[0])
		self.actionID = ""
		if len(configData) > 1:
			self.actionID = configData[1]
		self.conditionKey = configDict["param2"] 	#失败通知ID
		self.buffIDList = [int(i) for i in configDict["param3"].split("|")] #BuffID列表

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return
		recordScriptIDList = spaceEntity.queryTemp("recordScriptIDList")
		if not recordScriptIDList: return
		if not len(recordScriptIDList): return
		if boxEntity.scriptID == recordScriptIDList[0]:
			boxEntity.allClients.CLIENT_OnPlayAction(self.actionID,-1.0)
			boxEntity.delayDestroy(self.destroyTime)
			recordScriptIDList.pop(0)
			spaceEntity.setTemp("recordScriptIDList",recordScriptIDList)
		else:
			for buffID in self.buffIDList:
				playerCell.addBuff(boxEntity,buffID)
			boxEntity.setInteract(0)
			boxEntity.addTimerCallBack(5.0,"setInteract",(1,))
			spaceEntity.getScript().onConditionChange( spaceEntity,"",boxEntity.scriptID,self.conditionKey,"" )

class SpellGossipResultMountHeHua( SpellGossipResultBase ):
	"""
	CST-3660 上荷花
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = boxEntity.getCurrentSpace()
		if not spaceEntity:
			KBEDebug.ERROR_MSG("spaceEntity is None!!")
			return
		point = spaceEntity.getPointInCoord( boxEntity.id )
		if point == None:
			KBEDebug.ERROR_MSG("point is None!!")
			return
		pointPieceType = spaceEntity.getPointPiece( point )
		spaceEntity.removePiece(point)
		spaceEntity.setPointPiece( point, pointPieceType )
		playerCell.setTemp("CurrentPos",[point,pointPieceType])
		yaw = spaceEntity.getForwardDir()
		direction = playerCell.direction
		direction.z = yaw
		playerCell.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		playerCell.position = boxEntity.position
		playerCell.position.y += 0.9
		boxEntity.destroySelf()
		playerCell.client.OnMountHeHua((pointPieceType - 2)) #客户端需要根据这个来实现荷花模型 1代表红荷花 0代表白荷花
		playerCell.mountHeHuaAddBuff()

class SpellGossipResultSparHunTingRecordTrap( SpellGossipResultBase ):
	"""
	晶石狩猎场 销毁记录陷阱ID
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		trapID = boxEntity.queryTemp("trapID")
		if not trapID:
			return
		trapEntity = KBEngine.entities.get(trapID,None)
		if not trapEntity:
			return
		spaceEntity = trapEntity.getCurrentSpace()
		data = trapEntity.queryTemp("rewardCamp")
		if spaceEntity:
			spaceEntity.campTotalMoney( data[0],trapEntity.queryTemp("rewardMoney") )
		trapEntity.destroySelf()

class SpellGossipResultPlayParticles( SpellGossipResultBase ):
	"""
	播放光效
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.effectID = configDict["param1"].strip()		#光效ID
		self.delayTime = ""
		if configDict["param2"].strip():
			self.delayTime = float(configDict["param2"])	#延迟时间
			
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if self.delayTime:
			boxEntity.addTimerCallBack(self.delayTime, "playParticles", (self.effectID, ))
		else:
			boxEntity.allClients.CLIENT_OnPlayParticles(boxEntity.id, self.effectID, "", 1.0, Math.Vector3(0,0,0))
			
class SpellGossipResultPlayAction( SpellGossipResultBase ):
	"""
	播放动作
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.actionID = configDict["param1"].strip()		#动作ID
		self.delayTime = ""
		if configDict["param2"].strip():
			self.delayTime = float(configDict["param2"])	#延迟时间
			
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if self.delayTime:
			boxEntity.addTimerCallBack(self.delayTime, "playAction", (self.actionID, ))
		else:
			boxEntity.allClients.CLIENT_OnPlayAction(self.actionID, -1.0)

class SpellGossipResultGetReward( SpellGossipResultBase ):
	"""
	交互获得奖励
	"""
	def __init__( self ):
		self.itemList = []
		self.isRanks = False
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.rewardID = configDict["param1"]
		if len( configDict["param2"] ):
			self.isRanks = bool(int( configDict["param2"] ))
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		player = KBEngine.entities.get( playerCell.id,None )
		if not self.isRanks:	#奖励所有权为个人,并且参数2为零
			datas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":player} )
			RewardMgr.g_rewardMgr.doRewards( datas, player.id, csdefine.ITEM_ADD_BY_OPEN_SPELLBOX )
		else:	#参数配置为1时
			if player.isInTeam():	#玩家在队伍里
				inRangeMem = player.getInRangeTeammate( Define.TEAM_ITEM_PICKUP_RANGE )
				for inRangPlay in inRangeMem:
					datas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":inRangPlay} )
					RewardMgr.g_rewardMgr.doRewards( datas, inRangPlay.id, csdefine.ITEM_ADD_BY_OPEN_SPELLBOX )
			else:	#玩家没有组队
				datas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":player} )
				RewardMgr.g_rewardMgr.doRewards( datas, player.id, csdefine.ITEM_ADD_BY_OPEN_SPELLBOX )


class SpellGossipResultGetEnergy( SpellGossipResultBase ):
	"""
	CST-3740 交互获得能量点
	"""
	def __init__( self ):
		self.addEnergy = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.addEnergy = int(configDict["param1"])

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		maxEnergyValue = playerCell.queryTemp("MaxEnergyValue")
		curEnergyValue = playerCell.queryTemp("CurEnergyValue")
		if not maxEnergyValue and curEnergyValue == None:
			KBEDebug.ERROR_MSG("player spaceEvent is error")
			return
		curEnergyValue += self.addEnergy
		if curEnergyValue > maxEnergyValue:
			curEnergyValue = maxEnergyValue
			
		playerCell.client.ShowEnergyMessage(True)
		#playerCell.setTemp("CurEnergyValue",curEnergyValue)
		playerCell.updateEnergyBar(curEnergyValue,maxEnergyValue)

class SpellGossipResultMagicMazeEnterChildSpace( SpellGossipResultBase ):
	"""
	CST-3185 进入幻阵迷宫子副本
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onStartTeleportToChild( spaceEntity )	#貌似废弃了。没有改这里的参数，见svn10618
			spaceEntity.getScript().onStopOtherPlayerFly( spaceEntity )
			
class SpellGossipResultRandomEnterTongSpaceCopy( SpellGossipResultBase ):
	"""
	一定概率进入下一个帮会副本
	"""
	def __init__( self ):
		self._rand = 0.0

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._rand = float( configDict["param1"] )

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if playerCell.getActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY ) <= 1 and self._rand >= random.random():
			validSpace = []
			
			import ObjectScript.Space as space
			tongSpaceCopy = space.getTongSpaceCopyScriptIDs()
			for reqLevel, spaceList in tongSpaceCopy.items():
				if playerCell.getLevel() >= reqLevel:
					validSpace.extend( spaceList )
			
			spaceEntity = playerCell.getCurrentSpace()
			if spaceEntity.scriptID in validSpace:
				validSpace.remove( spaceEntity.scriptID )
			
			if validSpace:
				playerCell.gotoSpaceEnterPos( random.choice( validSpace ),{} )
			else:
				playerCell.gotoExitSpacePos()
		else:
			playerCell.gotoExitSpacePos()
			
class SpellGossipResultMagicMazeOpenZhuanPan( SpellGossipResultBase ):
	"""
	CST-3190 开启幻阵迷宫天命和气运转盘
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().randomZhuanPan( spaceEntity )

class SpellGossipResultYeZhanFengQiGetIntegral( SpellGossipResultBase ):
	"""
	CST-4463 个人竞技 至尊争霸-血斗凤栖镇
	玩家被击杀 掉落箱子获得积分
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addPlayerIntegral( playerCell, boxEntity.queryTemp("RewardIntegral") )

class SpellGossipResultActBunchJoin( SpellGossipResultBase ):
	"""
	CST-4514 至尊争霸 十方城
	参加某活动串的某活动
	"""
	def __init__( self ):
		self.bunchName = ""
		self.activityName = ""

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.bunchName = configDict["param1"]
		self.activityName = configDict["param2"]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		playerCell.actBunch_join(self.bunchName,self.activityName,"")

class SpellGossipResultOccupyPagoda( SpellGossipResultBase ):
	"""
	CST-4054 灵脉战场玩法
	占领极阴(阳)灵塔
	"""
	def __init__( self ):
		self.type = 1
		self.xianBuffID = 0
		self.moBuffID = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.type = int( configDict["param1"] )
		if configDict["param2"]:
			self.xianBuffID = int( configDict["param2"] )
		if configDict["param3"]:
			self.moBuffID = int( configDict["param3"] )

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		playerCell.getCurrentSpace().occupyPagoda( self.type, boxEntity.scriptID, playerCell.id, playerCell.getFinalCamp() )
		if playerCell.getFinalCamp() == csdefine.CAMP_TAOSIM:
			if self.xianBuffID:
				boxEntity.addBuff( boxEntity, self.xianBuffID )
		else:
			if self.moBuffID:
				boxEntity.addBuff( boxEntity, self.moBuffID )

class SpellGossipResultMonsterGetBuff( SpellGossipResultBase ):
	"""
	交互后特定怪物获得某Buff
	"""
	def __init__( self ):
		self.scriptID = ""
		self.buffID = 0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.scriptID = configDict["param1"]
		self.buffID = int( configDict["param2"] )
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			idList = spaceEntity.getEntityRecord(self.scriptID)
			for id in idList:
				entity = KBEngine.entities.get(id,None)
				if entity == None:
					return
				entity.addBuff( boxEntity, self.buffID )

class SpellGossipResultOccupyTower( SpellGossipResultBase ):
	"""
	CST-4056 冰雪之战
	交互哨塔 夺取或者夺回哨塔
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		from SpaceCopyFrozenFight import SpaceCopyFrozenFight as SpaceCopyFrozenFight
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity or not isinstance(spaceEntity, SpaceCopyFrozenFight):
			return
		spaceEntity.gossipResultWithTower(boxEntity.scriptID, playerCell)


class SpellGossipResultOccupyRivivePos( SpellGossipResultBase ):
	"""
	CST-4056 冰雪之战
	占领复活点
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		from SpaceCopyFrozenFight import SpaceCopyFrozenFight as SpaceCopyFrozenFight
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity or not isinstance(spaceEntity, SpaceCopyFrozenFight):
			return
		spaceEntity.occupyRivivePos(boxEntity.scriptID, playerCell)

class SpellGossipResultTongStarcraftGetIntegral( SpellGossipResultBase ):
	"""
	CST-4446 帮会争霸第二场 获得积分
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addIntegral( playerCell, boxEntity.queryTemp("integral") )

class SpellGossipResultBoxToPlayerAddBuff( SpellGossipResultBase ):
	"""
	交互:SpellBox上的Buff转移给玩家
	"""
	def __init__( self ):
		self.buffIDPools = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.buffIDPools = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		for buffID in self.buffIDPools:
			if len(boxEntity.findBuffsByBuffID(int(buffID)) ):
				playerCell.addBuff( playerCell, int(buffID) )
				spaceEntity.playerMetSandmanDict[boxEntity.position] = buffID

class SpellGossipResultPlayerToBoxAddBuff( SpellGossipResultBase ):
	"""
	交互:玩家上的Buff转移给SpellBox
	"""
	def __init__( self ):
		self.buffIDPools = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.buffIDPools = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		for buffID in self.buffIDPools:
			if len(playerCell.findBuffsByBuffID(int(buffID))):
				boxEntity.addBuff( boxEntity, int(buffID) )
				playerCell.removeBuffByID(int(buffID))
				spaceEntity.playerQuestionAnswer[boxEntity.scriptID] = buffID
				spaceEntity.calculateResults()

class SpellGossipResultNightmareScrollPlay( SpellGossipResultBase ):
	"""
	梦魇画卷专用(播放光效)
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.effectID = configDict["param1"].strip()		#光效ID
		self.delayTime = ""
		if configDict["param2"].strip():
			self.delayTime = float(configDict["param2"])	#延迟时间
			
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			if self.delayTime:
				boxEntity.addTimerCallBack(self.delayTime, "playParticles", (self.effectID, ))
			else:
				boxEntity.allClients.CLIENT_OnPlayParticles(boxEntity.id, self.effectID, "", 1.0, Math.Vector3(0,0,0))
			spaceEntity.sceneObjectCoordList.insert( 0, boxEntity.id )
			spaceEntity.exChangeModelLink()

class SpellGossipResultHoldJinDan( SpellGossipResultBase ):
	"""
	抱金丹
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.buffID = int(configDict["param1"]) 	#抱金丹buff

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if boxEntity.getRemainLifeTime() == -1:
			playerCell.addBuff( boxEntity, self.buffID )
			boxEntity.delayDestroy( 0.1 )	#延时0.1秒销毁，避免加buff期间销毁
		elif boxEntity.getRemainLifeTime() >= 0.2:	#小于0.2秒就不打断生存时间倒计时了，让它自己炸掉
			boxEntity.allClients.CLIENT_HideTopCountDown()
			playerCell.addBuff( boxEntity, self.buffID )
			boxEntity.delayDestroy( 0.1 )	#延时0.1秒销毁，避免加buff期间销毁

class SpellGossipResultTeleportSpace( SpellGossipResultBase ):
	"""
	传送到某处
	"""
	def __init__( self ):
		self._spaceName = ""
		self._position = ()
		self._direction = ()

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._spaceName = configDict["param1"]

		position = configDict["param2"].split(" ")
		direction = configDict["param3"].split(" ")

		self._position = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
		self._direction = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceName = self._spaceName if self._spaceName else playerCell.getCurrentSpaceScriptID()
		playerCell.gotoSpaceUE4(spaceName, Math.Vector3(self._position), self._direction)
		
class SpellGossipResultSpecialTeleport( SpellGossipResultBase ):
	"""
	鬼域迷阵:交互传送
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onSendTheResults( boxEntity.id, playerCell.id )

class SpellGossipResultAddBuffSelf( SpellGossipResultBase ):
	"""
	交互后箱子自身获得若干Buff
	"""
	def __init__( self ):
		self._param1 = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._param1 = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for buffID in self._param1:
			boxEntity.addBuff( boxEntity,int(buffID) )

class SpellGossipResultMagicMazeEnterParentSpace( SpellGossipResultBase ):
	"""
	CST-4886 进入幻阵迷宫父副本
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onStartTeleportToParent( spaceEntity )

class SpellGossipResultThirdStarcraftCycleGetIntegral( SpellGossipResultBase ):
	"""
	帮会争霸第三场 周期获得积分
	"""
	def __init__( self ):
		pass
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return
		belongTongDIBD = boxEntity.queryTemp("belongTongDIBD")
		if belongTongDIBD and belongTongDIBD == playerCell.tongDBID:
			return
		boxEntity.setTemp("belongTongDIBD",playerCell.tongDBID)
		spaceEntity.occupySpellBox( boxEntity.scriptID, playerCell )

class SpellGossipResultCreateHerbs( SpellGossipResultBase ):
	"""
	幻阵迷宫  临渊试炼：交互后在对应的位置随机刷新的spellbox
	"""
	def __init__( self ):
		self.refrehTime = 10.0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		if configDict["param1"].strip():
			self.refrehTime = float(configDict["param1"])	#延迟时间
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.addTimerCallBack( self.refrehTime, "randomRefrehMedicine", (boxEntity.position, boxEntity.direction,) )

class SpellGossipResultSwitchArea( SpellGossipResultBase ):
	"""
	延时切换到指定的检测区域
	"""
	def __init__( self ):
		self.areaIndex = 0
		self.delayTime = 0.0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		if configDict["param1"]:
			self.areaIndex = int(configDict["param1"])	  #区域索引
		if configDict["param2"]:
			self.delayTime = float(configDict["param2"])  #延时时间
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		boxEntity.isExecuted[self.areaIndex] = False
		boxEntity.addTimerCallBack( self.delayTime, "onDelayTimeSwitchArea", (self.areaIndex,) )


class SpellGossipResult_SYDX_SubmitYueQi( SpellGossipResultBase ):
	"""
	神乐雕像 提交乐器
	"""
	def __init__( self ):
		SpellGossipResultBase.__init__(self)
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		SpellGossipResultBase.init(self, configDict)
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = boxEntity.getCurrentSpace()
		if not spaceEntity:
			return

		spaceEntity.submitYueQi(boxEntity, playerCell)

class SpellGossipResultOnEnterAimingThrowMode( SpellGossipResultBase ):
	"""
	晶石洞窟 玩家进入瞄准投掷模式
	"""
	def __init__( self ):
		self.redScriptID = ""
		self.yellowScriptID = ""
		self.blueScriptID = ""
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.redScriptID = configDict["param1"]
		self.yellowScriptID = configDict["param2"]
		self.blueScriptID = configDict["param3"]
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return

		if boxEntity.scriptID == self.redScriptID:
			spaceEntity.colorNum = 1
		if boxEntity.scriptID == self.yellowScriptID:
			spaceEntity.colorNum = 2
		if boxEntity.scriptID == self.blueScriptID:
			spaceEntity.colorNum = 3
		playerCell.client.CLIENT_OnEnterAimingThrowMode( spaceEntity.colorNum )

class SpellGossipResultGetMonsterMirror( SpellGossipResultBase ):
	"""
	环任务消灭影妖 玩家获得照妖镜
	"""
	def __init__( self ):
		self.maxLingEnergyValue = 0 #灵能点
		self.buffID = 0 #用于加个持有效果 照妖镜环绕玩家
		self.reduceLingEnergyValue = 0
		self.soundID = ""
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.maxLingEnergyValue = int(configDict["param1"])
		self.buffID = int(configDict["param2"])
		if configDict["param3"]:
			self.reduceLingEnergyValue = int(configDict["param3"].split("|")[0])
			if len(configDict["param3"].split("|")) > 1:
				self.soundID = configDict["param3"].split("|")[1]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		playerCell.addBuff(playerCell,self.buffID)
		playerCell.setTemp("curLingEnergyValue",self.maxLingEnergyValue)
		playerCell.setTemp("maxLingEnergyValue",self.maxLingEnergyValue)
		playerCell.setTemp("reduceLingEnergyValue",self.reduceLingEnergyValue)
		playerCell.setTemp("isPlaySound",0) #是否播放了语音提示
		playerCell.setTemp("mirrorSoundID",self.soundID)
		playerCell.client.CLIENT_ShowLingEnergyBar( self.maxLingEnergyValue,self.maxLingEnergyValue )

class SpellGossipResultAddMonsterMirror( SpellGossipResultBase ):
	"""
	环任务消灭影妖 充满照妖镜能量
	"""
	def __init__( self ):
		self.buffID = 0 #鼎加的Buff 为了不能交互

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.buffID = int(configDict["param1"])

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		boxEntity.addBuff(boxEntity,self.buffID)
		maxLingEnergyValue = playerCell.queryTemp("maxLingEnergyValue")
		reduceLingEnergyValue = playerCell.queryTemp("reduceLingEnergyValue")
		if not maxLingEnergyValue or not reduceLingEnergyValue:
			return
		playerCell.setTemp("isPlaySound",0)
		playerCell.setTemp("curLingEnergyValue",maxLingEnergyValue)
		playerCell.client.CLIENT_UpdateLingEnergyBar( maxLingEnergyValue, maxLingEnergyValue, reduceLingEnergyValue )

class SpellGossipResultPlayerGetBuff( SpellGossipResultBase ):
	"""
	交互后玩家自己给自己加若干Buff
	"""
	def __init__( self ):
		self._param1 = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._param1 = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		for buffID in self._param1:
			playerCell.addBuff( playerCell,int(buffID) )

class SpellGossipResultCangGongDian1( SpellGossipResultBase ):
	"""
	藏功殿:SpellBox上的Buff转移给玩家
	"""
	def __init__( self ):
		self.buffIDPools = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.buffIDPools = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return

		for buffID in self.buffIDPools:
			if len(boxEntity.findBuffsByBuffID(int(buffID)) ) > 0:
				playerCell.addBuff( playerCell, int(buffID) )

class SpellGossipResultCangGongDian2( SpellGossipResultBase ):
	"""
	藏功殿:玩家上的Buff转移给SpellBox,玩家自身移除Buff
	"""
	def __init__( self ):
		self.buffIDPools = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.buffIDPools = configDict["param1"].split("|")
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return

		for buffID in self.buffIDPools:
			if len(playerCell.findBuffsByBuffID(int(buffID))) > 0:
				boxEntity.addBuff( boxEntity, int(buffID) )
				playerCell.removeBuffByID(int(buffID))
				spaceEntity.questionAnswerDict[boxEntity.scriptID] = buffID
		spaceEntity.onCalculateResults()

class SpellGossipResultRecordGossipTong( SpellGossipResultBase ):
	"""
	交互记录玩家的帮会
	"""
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		boxEntity.setTemp( "gossipTong",playerCell.tongDBID )
		playerCell.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_HAS_TONG_GOSSIP)


class SpellGossipResultMYJXAddEnergy( SpellGossipResultBase ):
	"""
	CST-6526 冥域缉凶 弹射机关充能
	"""
	def __init__( self ):
		self.value = 1

	def init( self, configDict ):
		"""
		virtual method
		"""
		if configDict["param1"]:
			self.value = int( configDict["param1"] )
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = boxEntity.getCurrentSpace()
		if not spaceEntity:
			return
		traps = spaceEntity.getEntityMailBoxRecord( Const.MYJX_MACHINE_TRAP_SCRIPTID )
		if not len(traps):
			return
		traps[0].addEnergy( boxEntity.id,self.value )

class SpellGossipResultMYJXHideEnergy( SpellGossipResultBase ):
	"""
	CST-6526 冥域缉凶 隐藏弹射机关能量条
	"""
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = boxEntity.getCurrentSpace()
		if not spaceEntity:
			return

		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.CLIENT_HideMYJXEnergyBar()

class SpellGossipResultAddBuffByProfession( SpellGossipResultBase ):
	"""
	根据自己玩家的职业添加对应的Buff  根据策划的配置习惯从战士，剑客，链刃，法师依次填写技能ID，用“|”隔开
	"""
	def __init__( self ):
		self.professions = [csdefine.CLASS_FIGHTER, csdefine.CLASS_SWORDMAN, csdefine.CLASS_ARCHER, csdefine.CLASS_MAGE]						
		self.Dict = {}

	def init( self, configDict ):
		BuffIDs = [int(BuffID) for BuffID in configDict["param1"].strip().split("|")]
		self.Dict = dict(zip(self.professions, BuffIDs ))

	def do( self, boxEntity, playerCell ):
		playerCell.addBuff( playerCell,self.Dict[playerCell.profession])

class SpellGossipResultTeleportNearestEntity( SpellGossipResultBase ):
	"""
	传送距离最近的同scriptID的entity
	"""
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = boxEntity.getCurrentSpace()
		if not spaceEntity:
			return
		IDList = spaceEntity.getEntityRecord(boxEntity.scriptID)
		nextTrap = None
		distance = 0
		for id in IDList:
			e = KBEngine.entities.get( id, None )
			if id == boxEntity.id or not e:
				continue
			if not distance:	
				distance = boxEntity.position.distTo(e.position)
				nextTrap = e
				continue
			_dis = boxEntity.position.distTo(e.position)
			if distance > _dis:
				distance = _dis
				nextTrap = e
		if nextTrap:
			offsetFront = 4   #向前偏移
			hight = 1            #偏移高度
			yaw = nextTrap.direction.z
			position = Math.Vector3(nextTrap.position.x,  nextTrap.position.y+hight, nextTrap.position.z)
			position.x += offsetFront * math.sin( yaw )
			position.z += offsetFront * math.cos( yaw )
			playerCell.position = position
			playerCell.changeDirection(nextTrap.direction, csdefine.REASON_CHANGE_DIR_FORCE)

class SpellGossipResultTeleportRandomPos( SpellGossipResultBase ):
	"""
	随机位置传送	（位置:朝向|位置:朝向|...）
	"""
	def __init__( self ):
		self._positionList = []

	def init( self, configDict ):
		self._positionList = configDict["param1"]

	def do( self, boxEntity, playerCell ):
		teleportList = self._positionList.split( "|" )
		random.shuffle( teleportList )
		strList  = teleportList[0].split( ":" )
		Position = KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( strList[0]) )
		Direction = KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( strList[1]) )
		playerCell.gotoSpace( playerCell.getCurrentSpaceScriptID(), Position, Direction )

class SpellGossipResultGetDropPetEgg( SpellGossipResultBase ):
	"""
	交互获取掉落幻兽蛋
	"""
	def __init__( self ):
		pass
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		#配置格式： itemID1:num1:rate1|itemID2:num2:rate2|....   rate（掉落概率总和为1）
		dataStr = configDict["param1"]
		datas = dataStr.split("|")
		self.datas =[]
		for item in datas:
			#data = [int(x) for x in item.split(":")]
			data = item.split(":")
			if len(data)!=3:
				KBEDebug.ERROR_MSG("item = %s is invalid!"%item)
				return
			self.datas.append(data)
		self.datas.sort(key = lambda data: float(data[2]))
		rate = 0
		for data in self.datas:
			rate += float(data[2])
		if rate!=1:
			KBEDebug.ERROR_MSG("rate sum total not equal 1!")
			return

	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		rate = random.uniform(0,1)
		rate_t = 0
		data = None
		for item in self.datas:
			if float(item[2])+rate_t >= rate:
				data = item
				break
			else:
				rate_t += float(item[2])
		if not data:
			return
		itemID = int(data[0])
		amount = int(data[1])

		result, _ = playerCell.addItemByID( itemID, amount,  csdefine.ITEM_ADD_BY_OPEN_SPELLBOX )
		
		if result == csstatus.ITEM_GO_ON:
			playerCell.client.ShowSpellBoxResultMessage( csdefine.SPELL_BOX_RESULT_ADDITEM,itemID )
			boxEntity.destroySelf()
		else:
			playerCell.statusMessage( result )
			
class SpellGossipResultTongStarcraftRandomGetIntegral( SpellGossipResultBase ):
	"""
	CST-7904 帮会争霸第一场 随机获得积分
	"""
	def __init__( self ):
		self.minIntegral = 0
		self.maxIntegral = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.minIntegral = int(configDict["param1"])
		self.maxIntegral = int( configDict["param2"] )

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		integral = random.randint(self.minIntegral,self.maxIntegral)
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addIntegral( playerCell, integral )

class SpellGossipResultOpenShips( SpellGossipResultBase ):
	"""
	仙舟渡劫--开启仙舟
	"""
	def __init__( self ):
		self._scriptID = ""

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._scriptID = configDict["param1"]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity: return
		entityList = spaceEntity.getEntityRecord( self._scriptID )
		if len( entityList ) == 0: return
		entity = KBEngine.entities.get( entityList[0], None )
		if entity == None: return
		entity.startMove()

class SpellGossipResultRamdomGetItem( SpellGossipResultBase ):
	"""
	随机获得某个道具
	"""
	def __init__( self ):
		self.probabilityList = []
		self.itemIDList	 = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.probabilityList = [int(i) for i in configDict["param1"].split("|")]
		self.itemIDList = [int(i) for i in configDict["param2"].split("|")]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		def random_index( self, rate ):
			"""
			随机变量的概率
			"""
			start = 0
			index = 0
			randnum = random.uniform( 1, sum(rate) )
			for index, scope in enumerate(rate):
				start += scope
				if randnum <= start:
					break
			return index
		index = random_index( self.probabilityList )
		playerCell.addItemByOpenSpellBox( self.itemIDList[index], 1 , csdefine.ITEM_ADD_BY_OPEN_SPELLBOX )

class SpellGossipResultReplaceArms( SpellGossipResultBase ):
	"""
	玩家替换武器
	"""
	def __init__( self ):
		self.type = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		if configDict["param1"]:
			self.type = int( configDict["param1"] )
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if playerCell.getClient():
			playerCell.client.CLIENT_SetCopyGameWeapon( self.type )

class SpellGossipResultOccupyWarFlag( SpellGossipResultBase ):
	"""
	烽火连天 - 玩家占领战旗
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity: return
		if playerCell.camp == csdefine.CAMP_TAOSIM:
			campStr = cschannel_msgs.CAMP_TAOSIM
		else:
			campStr = cschannel_msgs.CAMP_DEMON
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.statusMessage( csstatus.ACTIVITY_CAMP_FHLT_OCCUPY_WARFLAG, campStr, role.name )
		spaceEntity.occupyWarFlag( playerCell.camp )

class SpellGossipResultAddFHLTIntegral( SpellGossipResultBase ):
	"""
	烽火连天 - 获得积分
	"""
	def __init__( self ):
		self.integral = 0

	def init( self, configDict ):
		"""
		virtual method
		"""
		if configDict["param1"]:
			self.integral = int( configDict["param1"] )
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity: return
		if playerCell.camp == csdefine.CAMP_TAOSIM:
			spaceEntity.addTaosimIntegral( self.integral )
		else:
			spaceEntity.addDemonIntegral( self.integral )

class SpellGossipResultAddMaterialPoints( SpellGossipResultBase ):
	"""
	烽火连天 - 获得资材分
	"""
	def __init__( self ):
		pass

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity: return
		spaceEntity.addMaterialPoints( playerCell.camp )
		
class SpellGossipResultCreateAerialLadder( SpellGossipResultBase ):
	"""
	攻城战 获得云梯
	"""
	def __init__( self ):
		self.scriptID = ""

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.scriptID = configDict["param1"]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if playerCell.queryTemp("callAerialLadder",None) != None:
			return
		belongSide = playerCell.getBelongSide()
		entity = playerCell.createEntityByScriptID( self.scriptID,boxEntity.position,boxEntity.direction,{"belongSide":belongSide} )
		if entity:
			entity.setFollowerID( playerCell.id )

class SpellGossipResultGetRewardForYCJMD( SpellGossipResultBase ):
	"""
	勇闯绝命岛交互获得奖励（获得的物品通知给副本内所有的玩家）
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.rewardID = configDict["param1"]
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		player = KBEngine.entities.get( playerCell.id,None )
		datas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":player} )

		itemStr = ""
		for data in datas:
			if data["type"] == csdefine.REWARD_TYPE_ITEM:
				RewardMgr.g_rewardMgr.doReward( data, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_SPACE_EVENT )
				item = ItemFactory.ItemFactoryInst.getItemData(data["goodsid"])
				if item:
					colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(item["Quality"], "(255, 255, 255, 255)")
					amountStr = ""
					if data["amount"] >1:
						amountStr = "x" + str(data["amount"])
					tempStr ="[@L{t='%s';cfc=%s}]"% (item["ItemName"], colorStr) 
					itemStr += tempStr + amountStr + "、"
		
		message = itemStr[:len(itemStr)-1]
		name = playerCell.getName()
		campStr = ""
		if playerCell.getCamp() == csdefine.CAMP_TAOSIM:
			campStr = cschannel_msgs.CAMP_TAOSIM
		else:
			campStr = cschannel_msgs.CAMP_DEMON
		spaceEntity = playerCell.getCurrentSpace()
		for player in spaceEntity._spaceRoles:
			player.statusMessage( csstatus.ROLE_GET_TREASURE_BOX, campStr, name, message)

class SpellGossipResultLingTianPlant( SpellGossipResultBase ):
	"""
	灵田种植
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		pass

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		boxEntity.lingTianPlant( playerCell )
		
class SpellGossipResultTriggerLucky( SpellGossipResultBase ):
	"""
	晶石狩猎场触发机缘
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		#触发概率(0-100)
		self.probability = float(configDict["param1"])

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		probability = random.uniform(0, 100)
		if probability > self.probability: return
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity: spaceEntity.getScript().onTrigger_luckySpace(spaceEntity, playerCell)


class SpellGossipResultTriggerSmallMIjing( SpellGossipResultBase ):
	"""
	CST-10782 程序内容需求（0级）——轮回秘境机缘玩法 触发小秘境机缘
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		#触发概率
		self.odds = float(configDict["param1"])
		self.scriptID = configDict["param2"]

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		odds = random.uniform(0, 1)
		if odds > self.odds:
			return
		boxEntity.createEntityByScriptID(self.scriptID, boxEntity.position, boxEntity.direction, {"lifetime":600,"ownerDBID":playerCell.playerDBID})
		playerCell.statusMessage(csstatus.LHMJ_JYWF_NOTICE_SELF)
		#curSpace = playerCell.getCurrentSpace()
		#for role in curSpace._spaceRoles:
		#	role.statusMessage(csstatus.LHMJ_JYWF_NOTICE_ALL, role.playerName, curSpace.getScript().getSpaceName(), self.spaceName)

class SpellGossipResultAddBuffByProfessionGender( SpellGossipResultBase ):
	"""
	spellbox根据玩家的职业和性别添加对应的Buff  男战士:男剑客:男链刃:男法师|女战士:女剑客:女链刃:女法师
	"""
	def __init__( self ):						
		self.BuffIDs = {1:{}, 2:{}}

	def init( self, configDict ):
		if configDict["param1"]:
			param1 = configDict["param1"].split("|")
			k = 1
			for i in param1[0].split(":"):
				self.BuffIDs[1][k] = int(i)
				k += 1
			if len(param1) > 1:
				j = 1
				for v in param1[1].split(":"):
					self.BuffIDs[2][j] = int(v)
					j += 1

	def do( self, boxEntity, playerCell ):
		profession = playerCell.getProfession()
		gender = playerCell.getGender()
		if profession in self.BuffIDs[gender]:
			playerCell.addBuff( boxEntity, self.BuffIDs[gender][profession])

class SpellGossipCreateMovingVehicle( SpellGossipResultBase ):
	"""
	交互创建可移动载具
	"""
	def __init__( self ):
		self._scriptID = ""
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._scriptID = configDict["param1"]
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		if playerCell.carrierId or playerCell.vehicleId:
			playerCell.statusMessage( csstatus.VEHICLE_TO_MOUNT_CANNOT_GOSSIP )#骑乘状态不能上载具
			return
		if self._scriptID != "":
			vehicleEntity = playerCell.createEntityByScriptID( self._scriptID, boxEntity.position,boxEntity.direction,{ "spawnPos":tuple(boxEntity.position)} )
			if vehicleEntity != None:
				vehicleEntity.addTimerCallBack( 1.0, "gossipMountVehicle", (playerCell.id, boxEntity.getScriptID(), ))
				boxEntity.destroySelf()

class SpellGossipAddIntegral( SpellGossipResultBase ):
	"""
	晶石狩猎场机缘副本：交互获得金精奖励
	"""
	def __init__( self ):
		pass
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.JSSLC_JiYuanSpaceGetIntegral(playerCell)
			
class SpellGossipResultPlayStory( SpellGossipResultBase ):
	"""
	播放镜头
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.storyID = configDict["param1"]
		self.probability = 100
		if configDict["param2"]:
			self.probability = float(configDict["param2"])

	def do( self, boxEntity, playerCell ):
		"""
		virtual method
		"""
		playerCell.setTemp("JIYUANDATA", {"GossipEnter" : True})
		probability = random.uniform(0, 100)
		if probability <= self.probability:
			playerCell.client.StartPlayStory(self.storyID, 1)
		
	