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

class TeamDropBox( NPCBaseObject.NPCBaseObject, SystemDropBoxPickUpInterface.SystemDropBoxPickUpInterface ):
	"""
	队伍宝箱
	"""
	def __init__( self ):
		"""
		"""
		NPCBaseObject.NPCBaseObject.__init__( self )
		SystemDropBoxPickUpInterface.SystemDropBoxPickUpInterface.__init__(self)
		
		#统计队长分配物品情况
		self.itemAllocations = {}
		self.addTimerCallBack( 0.5, "onMovePoint", () )
		
	def isFreedomAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TEAM_PICKUP_TYPE_FREEDOM
		
	def isLeaderAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TEAM_PICKUP_TYPE_CAPTAIN
		
	def isRalldomAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TEAM_PICKUP_TYPE_TEAM
		
	def isAuctionAllocation(self):
		"""
		"""
		return self.allocation == csdefine.TEAM_PICKUP_TYPE_AUCTION
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_DROP_BOX )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX)
		
	def onInitDropBox(self):
		"""
		"""
		if self.isRalldomAllocation() or self.isAuctionAllocation():
			#掷点分配和竞拍分配的逻辑转base进行处理
			if len(self.notAllocationItems) > 0:
				entityFlagExt = self.getEntityFlagExt()
				notAllocationItems = list(self.notAllocationItems.values())
				KBEngine.globalData["DropBoxManager"].onAddDropBox(self, entityFlagExt, self.allocation, self.ownerDBIDs, notAllocationItems, self.teamID)
		
		#记录玩家信息
		for role in self.getEntityByNearby(self.ownerDBIDs):
			self.owners[role.playerDBID] = role.playerName
			if self.isRalldomAllocation() or self.isAuctionAllocation():
				#自身身上也记录一下，重新登录上线的时候直接获取相应的数据，不然如果不在箱子边上就没法获取数据了
				role.onDropBoxRegister(self.id)
		
		#直接发送相应的界面数据(因为这里存在一个拍卖的先后顺序问题)
		#这里不要合并到上面，因为上面需要注册所有数据，这里才能获取到完整的数据信息（比如所有玩家的名字等）
		if self.isAuctionAllocation():
			for role in self.getEntityByNearby(self.ownerDBIDs):
				if role.getClient():
					role.onReqDropBoxData(self.id)
		
	def onMovePoint(self):
		"""
		"""
		self.onInitDropBox()
		
		if not self.hasEffect:
			self.addTimerCallBack( 0.5, "onOpenDropbox", () )
			return
		
		dragActionID = ""
		levitateActionID = ""
		position = self.position
		positionList = self.getRandomPoints( self.position, 6, 1, self.layer, 0xFFFF )								#在死亡怪物周边6米的范围内
		if len(positionList): 
			position = positionList[0]
			position.y += Const.GREEN_DROPBOX_XUANFU_HIGHT	#绿色品质道具的宝箱需浮空
			dragActionID = Const.GREEN_DROPBOX_DRAG_ACTION
			levitateActionID = Const.GREEN_DROPBOX_LEVITATE_ACTION
		
		#只给拥有者发送通知
		StartPosition = KBEMath.KBEngine2UnrealPosition(self.position)
		EndPosition = KBEMath.KBEngine2UnrealPosition(position)
		roleList = self.getEntityByNearby(self.ownerDBIDs)
		for role in roleList:
			if role.getClient():
				role.client.CLIENT_dropBoxMoveToPoint(self.id, StartPosition, EndPosition, Const.DROPBOX_MOVE_SPEED, Const.GREEN_DROPBOX_END_SCALE, Const.DROPBOX_GRAVITY, dragActionID, levitateActionID)
		
		#延时一定的时间，让客户端有做飞行表现的时间
		distance = abs(self.position.flatDistTo(position))
		timeValue = distance * 100 / Const.DROPBOX_MOVE_SPEED if distance * 100 / Const.DROPBOX_MOVE_SPEED > 0.5 else 0.5
		self.addTimerCallBack( timeValue, "onSetPosAndScale", (position,) )
		
	def onSetPosAndScale(self, position):
		"""
		"""
		#设置宝箱允许打开了
		self.isCanOpen = True
		self.position = position
		self.modelScale = Const.GREEN_DROPBOX_END_SCALE
		
		#浮空效果
		if self.isRalldomAllocation() or self.isAuctionAllocation() or self.isLeaderAllocation():
			self.levitateActionID = Const.GREEN_DROPBOX_LEVITATE_ACTION
			
			if self.isLeaderAllocation() or self.isRalldomAllocation():
				for role in self.getEntityByNearby(self.ownerDBIDs):
					if role.getClient(): 
						role.clientEntity(self.id).onOpenDropbox()
						
	def onOpenDropbox(self):
		"""
		"""
		#设置宝箱允许打开了
		self.isCanOpen = True
		if self.isLeaderAllocation() or self.isRalldomAllocation():
			for role in self.getEntityByNearby(self.ownerDBIDs):
				if role.getClient(): 
					role.clientEntity(self.id).onOpenDropbox()
		
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
		if role.playerDBID != self.teamCaptainDBID:
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
		
		#通知周边玩家物品分配情况，更新宝箱可见性
		msg = self.getPickupMsg(dstRoleName, itemInst)
		entityList = self.getEntityByNearby(ownerDBIDs)
		for entity in entityList:
			if entity.getClient() is None: continue
			entity.clientEntity(self.id).onPickUpByLeader(str(uid), str(dstRoleDBID))
			entity.clientEntity(self.id).onUpdateDropBoxModelVisible()
			if dstRole and entity.id == dstRole.id: continue
			entity.statusMessage(csstatus.PICK_UP_ITEM_GET_ITEM, msg)
		
		self.checkDestroy()
		return
	