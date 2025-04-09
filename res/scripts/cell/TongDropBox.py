# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
import time
import Define
import csdefine
import KBEMath
import Const
import csstatus

#script
import CoreObject.NPCBaseObject as NPCBaseObject
import CoreInterface.SystemDropBoxPickUpInterface as SystemDropBoxPickUpInterface

class TongDropBox( NPCBaseObject.NPCBaseObject, SystemDropBoxPickUpInterface.SystemDropBoxPickUpInterface ):
	"""
	帮会宝箱
	"""
	def __init__( self ):
		"""
		"""
		NPCBaseObject.NPCBaseObject.__init__( self )
		SystemDropBoxPickUpInterface.SystemDropBoxPickUpInterface.__init__(self)
		
		#统计帮主分配物品情况
		self.itemAllocations = {}
		self.dropRemainTime = 12 * 60 * 60	#12H不销毁
		#宝箱开启计时
		self.openBoxTimerID = self.addTimerRepeat( 1.0, "onOpenDropbox", () )
		
	def onDestroyBox(self):
		"""
		"""
		self.dropRemainTime -= 1
		if self.dropRemainTime <= 0:
			self.popTimer(self.destroyTimerID)
			self.destroyTimerID = 0
			self.destroySelf()
		
	def checkDestroy(self):
		"""
		"""
		if len(self.allocationItems) == 0 and len(self.notAllocationItems) == 0 and len(self.freeAllocationItems) == 0:
			self.addTimerCallBack( 10.0, "destroySelf", () )
		
	def isFreedomAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TONG_PICKUP_TYPE_FREEDOM
		
	def isLeaderAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TONG_PICKUP_TYPE_LEADER
		
	def isRalldomAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TONG_PICKUP_TYPE_RALLDOM
		
	def isAuctionAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TONG_PICKUP_TYPE_AUCTION
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_DROP_BOX )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_TONG_DROPBOX)
		
	def onOpenDropbox(self):
		"""
		自动开启宝箱
		"""
		if self.openBoxTime > 0:
			self.openBoxTime -= 1
			return
		
		if self.openBoxTimerID > 0:
			self.popTimer(self.openBoxTimerID)
			self.openBoxTimerID = 0
		
		owners = []
		isTongLeaderIn = False
		#存在分配权且当时在指定范围内的玩家才有可能参与分配
		roleList = self.entitiesInRangeExt( Const.TONG_DROPBOX_OPEN_RANGE, "Role" )
		for role in roleList:
			if role.playerDBID not in self.joinDBIDs:
				continue
			
			owners.append(role)
			self.owners[role.playerDBID] = role.playerName
			if role.isTongLeader(): isTongLeaderIn = True
		
		#设置宝箱允许打开了
		self.isCanOpen = True
		self.ownerDBIDs = list(self.owners.keys())
		
		#如果是帮主分配，而当时帮主不在则改为掷点分配
		#如果参赛人员都不在，也改为自由拾取
		if (self.isLeaderAllocation() and not isTongLeaderIn) or len(owners) <= 1:
			for uid, itemInst in self.notAllocationItems.items():
				self.freeAllocationItems[uid] = itemInst
			self.notAllocationItems.clear()
			
			#没人在的话，那就是参赛人员都能拾取
			if len(owners) <= 0:
				self.ownerDBIDs = list(self.joinDBIDs)
		
		#掷点分配和竞拍分配的逻辑转base进行处理
		if len(self.notAllocationItems) > 0:
			if self.isRalldomAllocation() or self.isAuctionAllocation():
				entityFlagExt = self.getEntityFlagExt()
				notAllocationItems = list(self.notAllocationItems.values())
				KBEngine.globalData["DropBoxManager"].onAddDropBox(self, entityFlagExt, self.allocation, self.ownerDBIDs, notAllocationItems, self.tongDBID)
		
		for role in owners:
			if role.getClient():
				role.clientEntity(self.id).onOpenDropbox()
			
			#自身身上也记录一下，重新登录上线的时候直接获取相应的数据，不然如果不在箱子边上就没法获取数据了
			if len(self.notAllocationItems) > 0:
				if self.isRalldomAllocation() or self.isAuctionAllocation():
					role.onDropBoxRegister(self.id)
				
	def onReqDropBoxData(self, role):
		"""
		"""
		if self.isLeaderAllocation():
			dbidList = []
			itemList = []
			for itemInst, dbid in self.itemAllocations.items():
				dbidList.append(str(dbid))
				itemList.append(itemInst.getDictForClient(role))
			notAllocationItems = []
			for itemInst in list(self.notAllocationItems.values()):
				notAllocationItems.append(itemInst.getDictForClient(role))
			#已分配的物品数据，未分配的物品数据
			role.clientEntity(self.id).recvDropBoxNoAllocationData(dbidList, itemList, notAllocationItems)
			return
		
		#获取宝箱中掷点分配或竞拍物品数据
		if self.isAuctionAllocation() or self.isRalldomAllocation():
			role.onReqDropBoxData(self.id)
		
	def onReqPickUpToMember(self, uid, dstRole, role, dstRoleDBID):
		"""
		"""
		if not role.isTongLeader():
			return
		
		dstRoleName = self.owners.get(dstRoleDBID, "") 
		itemInst = self.notAllocationItems[uid]
		if dstRole:
			dstRoleName = dstRole.getName()
			if dstRole.addItemCheck( itemInst ) == csstatus.ITEM_GO_ON:
				dstRole.addItem(itemInst, csdefine.ITEM_ADD_BY_PICKUP)
			else:
				dstRole.sendRemainItemWithMail([itemInst], csdefine.REMAIN_ITEM_DROPBOX, csdefine.ITEM_ADD_BY_PICKUP)	
		else:
			if dstRoleName:
				sender, title, content = self.getMailInfo(csdefine.REMAIN_ITEM_DROPBOX, "")
				KBEngine.globalData["MailManager"].send( None, dstRoleName, csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, 0, 0, [itemInst], 0, 0 )
		
		#反过来存，有可能一个玩家有多个物品
		self.itemAllocations[itemInst] = dstRoleDBID
		self.notAllocationItems.pop( uid )
		ownerDBIDs = list(self.ownerDBIDs)
		self.updateOwnerDBIDs()
		
		dstRoleID = dstRole.id if dstRole else 0
		#通知周边玩家物品分配情况，更新宝箱可见性
		msg = self.getPickupMsg(dstRoleName, itemInst)
		entityList = self.getEntityByNearby(ownerDBIDs)
		for entity in entityList:
			if entity.getClient() is None: continue
			entity.clientEntity(self.id).onPickUpByLeader(str(uid), str(dstRoleDBID), dstRoleID)
			entity.clientEntity(self.id).onUpdateDropBoxModelVisible()
			if dstRole and entity.id == dstRole.id: continue
			entity.statusMessage(csstatus.TONG_DROPBOX_LEADER_ALLOCATION, msg)
		
		self.checkDestroy()
		return
	