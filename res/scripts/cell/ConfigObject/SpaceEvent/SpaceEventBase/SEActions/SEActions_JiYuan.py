# -*- coding: utf-8 -*-

# CST-12052 机缘玩法
# 副本事件行为
import time
import KBEDebug
import KBEngine
import csdefine
import Functions
import KBEMath
import Math
from ConfigObject.Drop import DropItem
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction450( SEActionBase ):
	"""
	副本通关成功
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		#奖励ID列表 
		self._rewardIDDict = {}
		if section["param1"]:
			lst = section["param1"].split("|")
			for data in lst:
				temp = data.split(":")
				self._rewardIDDict[temp[0]] = [rewardID for rewardID in temp[1].split(",")]
		
		#分档，根据通关时间 like：第一档时间，第二档时间
		self._gradeList = []
		if section["param2"]:
			lst = section["param2"].split("|")
			for data in lst:
				temp = data.split(":")
				self._gradeList.append( (int(temp[0]), temp[1]) )
		
		self.modelNumber = ""
		self.modelScale = 1.0
		self.position = Math.Vector3(0,0,0)
		self.direction = Math.Vector3( 0,0,0 )
		if section["param3"]:
			lst = section["param3"].split("|")
			self.modelNumber = lst[0]
			self.modelScale = float( lst[1] )
			self.position = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert( lst[2] ))
			self.direction = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert( lst[3] ))
		
		self.countDown = 0
		if section["param4"]:
			self.countDown = int(section["param4"])
			
		
	def do( self, spaceEntity, triggerID, eventParams ):
		"""
		"""
		if len(spaceEntity._spaceRoles) <= 0:
			return
			
		TianJiMiID = str(spaceEntity.createArgs.get("TianJiMiID", 0))
		if TianJiMiID not in self._rewardIDDict:
			KBEDebug.ERROR_MSG("%s config error %s" %(TianJiMiID, spaceEntity.scriptID))
			return
		
		grade = len(self._gradeList)
		soundID = ""
		t = int(time.time() - spaceEntity.lifeStartTime)
		timeStr = "{}分{}秒".format(int(t/60), (t%60))
		for _gradeTime, _soundID in self._gradeList:
			if t < _gradeTime * 60:
				soundID = _soundID
				break
			
			grade -= 1
		
		allocationItems = {} #已分配物品列表{"DBID": [item1, item2,...], ... }
		notAllocationItems = []	#未分配物品列表
		ascriptionID = 0
		ownershipIDs = []
		teamCaptainDBID = 0
		allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#个人则是自由拾取模式
		
		#这里面应该只有一个玩家,个人通过道具进来
		role = spaceEntity._spaceRoles[0]
		ownershipIDs.append(role.playerDBID)
		ascriptionID = role.playerDBID
		
		rewardID = self._rewardIDDict[TianJiMiID][grade - 1]
		rewardItemDatas = []
		def calcRewardDatas(rewardDatas):
			for data in rewardDatas:
				type = data["type"]
				amount = data["amount"]
				goodsid = data["goodsid"]
				# 物品奖励
				if type == csdefine.REWARD_TYPE_ITEM:
					rewardItemDatas.append( data )
		
		itemStr = ""
		rewardDatas = RewardMgr.g_rewardMgr.getReward( rewardID,{"spaceLevel":spaceEntity.spaceLevel,"player":role})
		calcRewardDatas( rewardDatas )
		for data in rewardItemDatas:
			itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
			if role.playerDBID not in allocationItems:
				allocationItems[ role.playerDBID ] = []
			allocationItems[ role.playerDBID ].append( itemInst )
			if itemStr: itemStr += "|"
			itemStr += "{}:{}".format(itemInst.id, itemInst.amount)
		
		params = {
			"modelNumber"		: self.modelNumber,
			"modelScale"		: self.modelScale,
			"ownershipIDs"		: ownershipIDs,
			"allocationItems"	: allocationItems, 
			"notAllocationItems": notAllocationItems,
			"allocation"		: allocation,
			"ascriptionID"		: ascriptionID,
			"teamCaptainDBID"	: teamCaptainDBID,
		}
		dropBoxEntiy = spaceEntity.createEntityNear( "DropBox", self.position, self.direction, params)
		
		if role.getClient():
			role.showMessagePlaySound(soundID)
			role.client.CLIENT_OnJiYuanSpaceJieSuan(itemStr, grade, timeStr, spaceEntity.recordPlayerDieNumber, self.countDown)

SEActionBase.setActionClass("SEAction450", SEAction450)
