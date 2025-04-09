#engine
import KBEngine
import KBEDebug
import KST
import random
import time, json
import csstatus
import Define
import csdefine
import ItemTypeEnum
import Functions

import Const
import SpaceScriptIdToName
from ItemFactory import ItemFactoryInst
from RemainItemMailInfo import Datas as MailInfos


class SystemDropBoxPickUpInterface:
	"""
	"""
	def __init__( self ):
		"""
		"""
		self.owners = {}
		self.destroyTimerID = self.addTimerRepeat( 1.0, "onDestroyBox", () )
		
	def onDestroyBox(self):
		"""
		"""
		self.dropRemainTime -= 1
		if self.dropRemainTime <= 0:
			self.popTimer(self.destroyTimerID)
			self.destroyTimerID = 0
			self.destroySelf()
		
	def beforeDestroy(self):
		"""
		"""
		if self.isAuctionAllocation() or self.isRalldomAllocation():
			KBEngine.globalData["DropBoxManager"].onDropBoxDestroy(self.id)
		
	def checkDestroy(self):
		"""
		"""
		if len(self.allocationItems) == 0 and len(self.notAllocationItems) == 0 and len(self.freeAllocationItems) == 0:
			self.destroySelf()
			
	def updateOwnerDBIDs(self):
		"""
		更新宝箱所有者
		"""
		#如果还有未分配的物品，则不需要更新
		if len(self.notAllocationItems) > 0 or len(self.freeAllocationItems) > 0:
			return
			
		lenth = len(self.ownerDBIDs)
		for index in range(lenth):
			dbid = self.ownerDBIDs[lenth - index - 1]
			if dbid not in self.allocationItems:
				self.ownerDBIDs.remove(dbid)
				
	def onPickUpToRoleByMgr(self, uid, roleDBID):
		"""
		物品竞拍/掷点分配成功/失败
		"""
		uid = int(uid)
		#如果分配成功，则检查是否能销毁箱子
		itemInst = self.notAllocationItems.pop(uid, None)
		if roleDBID > 0:
			self.checkDestroy()
			return
		
		KBEDebug.DEBUG_MSG("DropBox[%s] %s" %(self.id, uid))
		#竞拍/掷点分配失败,进入到自由分配
		if roleDBID <= 0 and itemInst:
			self.freeAllocationItems[uid] = itemInst
			entityList = self.getEntityByNearby(self.ownerDBIDs)
			for entity in entityList:
				if entity.getClient():
					entity.clientEntity(self.id).updateFreeAllocationItem(itemInst.getDictForClient(entity))
			
	def onPickUpDropBoxEnd(self):
		"""
		define method
		竞拍/掷点结束
		"""
		#理论上这个时候不应该再有这种未分配的物品
		#如果还有直接清理一下报个错
		if len(self.notAllocationItems) > 0:
			KBEDebug.ERROR_MSG("DropBox[%s] has notAllocationItems" %(self.id))
			self.notAllocationItems.clear()
		
		#如果还有其他，更新可见性
		if len(self.freeAllocationItems) > 0 or len(self.allocationItems) > 0:
			ownerDBIDs = list(self.ownerDBIDs)
			self.updateOwnerDBIDs()
			entityList = self.getEntityByNearby(ownerDBIDs)
			for entity in entityList:
				if entity.getClient():
					entity.clientEntity(self.id).onUpdateDropBoxModelVisible()
			return
		
		#销毁箱子
		self.checkDestroy()
		
	def getEntityByNearby(self, ownerDBIDs):
		"""
		"""
		entityList = []
		tempList = self.entitiesInRangeExt( Define.TEAM_ITEM_PICKUP_RANGE, "Role" )
		for entity in tempList:
			if entity.playerDBID in ownerDBIDs:
				entityList.append( entity )
		return entityList
		
	def isFreedomAllocation(self):
		"""
		"""
		return False
		
	def isLeaderAllocation(self):
		"""
		"""
		return False
		
	def isRalldomAllocation(self):
		"""
		"""
		return False
		
	def isAuctionAllocation(self):
		"""
		"""
		return False
		
	def isHasAllocation(self, playerDBID):
		"""
		是否可参与分配
		"""
		if not self.isCanOpen:	
			return False
		
		return playerDBID in self.ownerDBIDs
		
	def reqDropBoxData(self, srcEntityID):
		"""
		Exposed method
		请求获取宝箱数据
		"""
		if srcEntityID == self.id:
			return
		
		role = KBEngine.entities.get(srcEntityID)
		if not self.isHasAllocation(role.playerDBID):
			return
		
		#宝箱能获取分配物品的玩家
		ownersInfo = {"dictData" : []}
		for dbid, name in self.owners.items():
			data = {"key" : str(dbid), "value" : name}
			ownersInfo["dictData"].append(data)
		
		#自由拾取的物品
		freeAllocationItems = []
		itemList = list(self.allocationItems.get(role.playerDBID, {}).values())
		for itemInst in itemList:
			freeAllocationItems.append(itemInst.getDictForClient(role))
		for itemInst in list(self.freeAllocationItems.values()):
			freeAllocationItems.append(itemInst.getDictForClient(role))
		
		role.clientEntity(self.id).recvDropBoxData(ownersInfo, freeAllocationItems)
		self.onReqDropBoxData(role)
		
	def onReqDropBoxData(self, role):
		"""
		"""
		pass
		
	def reqPickUp(self, srcEntityID, uidList):
		"""
		Exposed method
		请求自由拾取
		"""
		if srcEntityID == self.id:
			return
		
		role = KBEngine.entities.get(srcEntityID)
		if not self.isHasAllocation(role.playerDBID):
			return
		
		uidList = [int(uid) for uid in uidList]
		self.onReqPickUp(uidList, role)
		
	def onReqPickUp(self, uidList, role):
		"""
		"""
		itemList = []
		for uid in uidList:
			if uid in self.freeAllocationItems:
				itemList.append(self.freeAllocationItems[uid])
				
		for uid in uidList:
			if role.playerDBID in self.allocationItems:
				if uid in self.allocationItems[role.playerDBID]:
					itemList.append(self.allocationItems[role.playerDBID][uid])
		
		#如果要是实际的物品少于想要拾取的
		if len(itemList) < len(uidList):
			return
		
		#看看背包中是否能放下
		status = role.addItemListCheck(itemList)
		if status != csstatus.ITEM_GO_ON:
			role.statusMessage(status)
			return
		
		#从列表中先移除
		for uid in uidList:
			self.freeAllocationItems.pop(uid, None)
			if role.playerDBID in self.allocationItems:
				self.allocationItems[role.playerDBID].pop(uid, None)
				if len(self.allocationItems[role.playerDBID]) <= 0:
					self.allocationItems.pop(role.playerDBID, None)
		
		ownerDBIDs = list(self.ownerDBIDs)
		self.updateOwnerDBIDs()
		for itemInst in itemList:
			role.addItem(itemInst, csdefine.ITEM_ADD_BY_PICKUP)
			#通知周边玩家物品分配情况，更新宝箱可见性
			msg = self.getPickupMsg(role.getName(), itemInst)
			entityList = self.getEntityByNearby(ownerDBIDs)
			for entity in entityList:
				if entity.getClient() is None: continue
				entity.clientEntity(self.id).onPickUp(str(itemInst.uid), str(role.playerDBID))
				entity.clientEntity(self.id).onUpdateDropBoxModelVisible()
				if entity.id == role.id: continue
				entity.statusMessage(csstatus.PICK_UP_ITEM_ROLE_GET_ITEM, msg)
				
		self.checkDestroy()
		
	def reqPickUpToMember(self, srcEntityID, uid, playerDBID):
		"""
		Exposed method
		请求分配物品
		"""
		if srcEntityID == self.id:
			return
			
		if not self.isLeaderAllocation():
			return
		
		role = KBEngine.entities.get(srcEntityID)
		if not self.isHasAllocation(role.playerDBID):
			return
		
		if not self.isHasAllocation(playerDBID):
			return
			
		uid = int(uid)
		if uid not in self.notAllocationItems:
			return
			
		dstRole = None
		if role.playerDBID == playerDBID:
			dstRole = role
		else:
			entityList = self.getEntityByNearby(self.ownerDBIDs)
			for r in entityList:
				if r.playerDBID == playerDBID:
					dstRole = r
					break
		
		self.onReqPickUpToMember(uid, dstRole, role, playerDBID)
		
	def onReqPickUpToMember(self, uid, dstRole, role, dstRoleDBID):
		"""
		"""
		pass	
		
	def getPickupMsg(self, roleName, itemInst):
		"""
		"""
		tempStr = ""
		colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
		tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
		return roleName + "|" + tempStr + "|" + str( itemInst.amount )
		
	def getMailInfo(self, remianType, titleKey):
		"""根据不同类型的奖励获取方式和内容关键字获取邮件的信息"""
		sender = MailInfos[remianType]["sender"]
		if remianType == csdefine.REMAIN_ITEM_GIFT or remianType == csdefine.REMAIN_ITEM_DROPBOX:
			title = MailInfos[remianType]["title"]
			content = MailInfos[remianType]["content"]
		else:
			title = MailInfos[remianType]["title"].replace("{0}", titleKey)
			content = MailInfos[remianType]["content"].replace("{0}", titleKey)
		return sender, title, content
			