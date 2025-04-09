# -*- coding: utf-8 -*-
#
import random
from ConfigObject.Quest.QuestBase.QuestFunction import QuestFuncBase
import Math
import ItemFactory
import csdefine
import ItemTypeEnum
import KBEDebug
import KBEMath
import csstatus
import KBEngine

# ----------------------------------------------------------
# 任务动作类型扩展 继承父类QuestFuncBase
# ----------------------------------------------------------
class QuestFuncTeleportSpace( QuestFuncBase ):
	"""
	传送到某处
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._spaceName = ""
		self._position = ()
		self._direction = ()

	def init(self, data):
		self._spaceName = data["param1"]

		position = data["param2"].split(" ")
		direction = data["param3"].split(" ")

		self._position = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
		self._direction = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.gotoSpaceUE4(self._spaceName, Math.Vector3(self._position), self._direction)

class QuestFuncAddItems( QuestFuncBase ):
	"""
	给与物品
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)
		self._items = ()

	def init(self, data):
		itemIDParams = data["param1"].split("|")
		itemIDList = []
		for i in itemIDParams:
			if i != "":
				itemIDList.append(int(i))

		amountParams = data["param2"].split("|")
		amountList = []
		for j in amountParams:
			if j != "":
				amountList.append(int(j))
		
		#CST-12052 增加概率参数，默认为1
		ratioList = [1 for i in range(len(itemIDList))]
		if data["param3"]:
			ratioParams = data["param3"].split("|")
			for index in range(min(len(ratioParams), len(itemIDList))):
				ratio = float(ratioParams[index])
				ratioList[index] = ratio
		
		self._items = tuple(zip(itemIDList, amountList, ratioList))

	def check(self, player, params = {}):
		result = True
		for (id, amount, ratio) in self._items:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(id, amount)
			if player.addItemCheck(itemInst) != csstatus.ITEM_GO_ON:
				result = False
				break
				
		return result
		
	def do(self, player, params = {}):
		for (id, amount, ratio) in self._items:
			if ratio < 1.0 and ratio <= random.uniform(0, 1):
				continue
			
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(id, amount)
			if itemInst: player.addItem(itemInst, csdefine.ITEM_ADD_BY_QUESTACTION)

class QuestFuncRemoveItems( QuestFuncBase ):
	"""
	删除物品
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)
		self._items = ()

	def init(self, data):
		itemIDParams = data["param1"].split("|")
		itemIDList = []
		for i in itemIDParams:
			if i != "":
				itemIDList.append(int(i))

		amountParams = data["param2"].split("|")
		amountList = []
		for j in amountParams:
			if j != "":
				amountList.append(int(j))

		self._items = tuple(zip(itemIDList, amountList))

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		for (id, amount) in self._items:
			# 先根据物品ID删除该物品
			ItemList = player.getItemInstsByID(id)
			player.removeItemListByAmount( ItemList, amount, csdefine.ITEM_REMOVE_BY_QUESTACTION)
			
			if not amount:
				KBEDebug.ERROR_MSG("QuestFuncRemoveItems::do: ItemInst with id %i dosen't exist!" % id)
				continue

class QuestFuncUseSkill( QuestFuncBase ):
	"""
	使用技能
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)
		self._skillID = 0

	def init(self, data):
		self._skillID = int(data["param1"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 调用使用技能方法
		player.useSkillToEntity(self._skillID, player.id)

class QuestFuncRemoveBuffer( QuestFuncBase ):
	"""
	移除一个buffer
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)
		self._bufferID = 0

	def init(self, data):
		self._bufferID = int(data["param1"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 调用移除buffer的方法
		player.removeBuffByID(self._bufferID )
		
class QuestFuncAddBuffer( QuestFuncBase ):
	"""
	增加一个buffer
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)
		self._bufferID = 0

	def init(self, data):
		self._bufferID = int(data["param1"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.addBuff( player, self._bufferID )
		
class QuestFuncEnterPlane( QuestFuncBase ):
	"""
	进入位面
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._spaceName = ""

	def init(self, data):
		self._spaceName = data["param1"]

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.gotoSpacePlane( self._spaceName )
		
class QuestFuncLeavePlane( QuestFuncBase ):
	"""
	离开位面
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._spaceName = ""

	def init(self, data):
		self._spaceName = data["param1"]

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.leaveSpacePlane( self._spaceName )
		
class QuestFuncPlaySound( QuestFuncBase ):
	"""
	播放语音
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._soundIDs = ""

	def init(self, data):
		self._soundIDs = data["param1"].split("|")

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		for sound in self._soundIDs:
			player.showMessagePlaySound( sound )
			
class QuestFuncPlaySoundBySex( QuestFuncBase ):
	"""
	根据性别播放语音
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._soundIDs = ""

	def init(self, data):
		self._soundIDs = data["param1"]

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		gender = player.getGender()
		idList = self._soundIDs.split("|")
		if gender == csdefine.MALE and len(idList) >= 1:
			player.showMessagePlaySound( idList[0] )
		elif gender == csdefine.FEMALE and len(idList) >=2:
			player.showMessagePlaySound( idList[1] )
		else:
			KBEDebug.ERROR_MSG("QuestFunc::QuestFuncPlaySoundBySex player(sex:%i) can not play sound, as sound(%s)"%(gender, self._soundIDs))

class QuestFuncTriggerMemoirCG( QuestFuncBase ):
	"""
	触发播放仙魔录CG
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._memoirCGIDs = ""
		self._memoirIDs = ""
		self._spaceName = ""
		self._position = ""
		self._direction = ""

	def init(self, data):
		self._memoirCGIDs = data["param1"]
		self._memoirIDs = data["param2"]
		self._spaceName = data["param3"]
		self._position = data["param4"]
		self._direction = data["param5"]

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		camp = player.getCamp()
		memoirCGIDList = self._memoirCGIDs.split("|")
		memoirIdList = self._memoirIDs.split("|")
		if camp == csdefine.CAMP_TAOSIM and len(memoirCGIDList) >= 1 and len(memoirIdList) >= 1:
			player.startPlayMemoirCG( memoirCGIDList[0],memoirIdList[0],self._spaceName,self._position,self._direction )
		elif camp == csdefine.CAMP_DEMON:
			player.startPlayMemoirCG( memoirCGIDList[1],memoirIdList[1],self._spaceName,self._position,self._direction )
		else:
			KBEDebug.ERROR_MSG("QuestFunc::QuestFuncTriggerMemoirCG player(camp:%i) can not play CG, as CG(%s)"%(camp, self._memoirCGIDs))

class QuestFuncSetTeleportPointOpen( QuestFuncBase ):
	"""
	设置传送点开启
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._openPoint = ""

	def init(self, data):
		self._openPoint = data["param1"].split("|")

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		for point in self._openPoint:
			player.addTeleportPoint(point)

class QuestFuncSetTeleportPointClose( QuestFuncBase ):
	"""
	设置传送点关闭
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._openPoint = ""

	def init(self, data):
		self._openPoint = data["param1"].split("|")

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		for point in self._openPoint:
			player.removeTeleportPoint(point)
	
class QuestFuncDisMountPet( QuestFuncBase ):
	"""
	下坐骑
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )

	def init(self, data):
		pass

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		if player._activePetUID:
			if player.isMountOnPet():
				player._dismountPet( player._activePetUID )
				
class QuestFuncGetSkill( QuestFuncBase ):
	"""
	获得技能
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)
		self._skillID = 0

	def init(self, data):
		self._skillID = int(data["param1"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 调用增加技能方法
		player.addSkill(self._skillID)

class QuestFuncRefreshSpellBoxCondition( QuestFuncBase ):
	"""
	刷新spellbox对话条件
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )

	def init(self, data):
		pass

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_QUEST_CHANGE )

class QuestFuncSetPlayerRevivePos( QuestFuncBase ):
	"""
	设置玩家复活点
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)

	def init(self, data):
		self._spaceName = data["param1"]
		position = data["param2"].split(" ")
		direction = data["param3"].split(" ")
		self._position = KBEMath.Unreal2KBEnginePosition((eval(position[0]), eval(position[1]), eval(position[2])))
		self._direction = KBEMath.Unreal2KBEngineDirection(Math.Vector3(eval(direction[0]), eval(direction[1]), eval(direction[2])))

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.setRevivePos( self._spaceName,self._position,self._direction )
		player.client.CLIENT_SetRevivePosStatus( csstatus.TALK_SET_REVIVE_POS, self._spaceName )

class QuestFuncAddPlayerTitle( QuestFuncBase ):
	"""
	添加玩家称号
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)

	def init(self, data):
		self.titleID = int(data["param1"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.addTitle(self.titleID )


class QuestFuncRingTaskEnterParentScene( QuestFuncBase ):
	"""
	进入环任务秘境父副本
	"""
	def __init__(self):
		QuestFuncBase.__init__(self)

	def init(self, data):
		self.mainSpaceList = data["param1"].split("|")
		
	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		belongType = csdefine.SPACE_BELONG_PERSON
		spaceKey = str( player.playerDBID )
		pickArg = { "packBelongType": belongType, "spaceKey":spaceKey }
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			KBEngine.globalData["RingTaskSpaceMgr"].setIsInMainScene( spaceKey, True )
			questID = player.loopQuest["loopQuestList"][0]
			KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( player.base, spaceKey, str(questID), 1 )
			pickArgs = { "packBelongType": belongType, "spaceKey":spaceKey }
			player.gotoRingTaskSpace( spaceEntity.scriptID, str(questID), pickArgs, True )

class QuestFuncCompleteWhisperQuestTask( QuestFuncBase ):
	"""
	完成传话任务目标(自定义目标进度)
	"""
	def __init__(self):
		QuestFuncBase.__init__( self )
		self._progress = 0

	def init(self, data):
		self._questID = int(data["param1"])
		self._taskID = int(data["param2"])
		if data["param3"]:
			self._progress = int(data["param3"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		player.completeWhisperQuestTask(self._questID, self._taskID, self._progress)