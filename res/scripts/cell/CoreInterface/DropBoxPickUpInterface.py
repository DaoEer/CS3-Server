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
#script
import Functions
from ItemFactory import ItemFactoryInst
import Const
import SpaceScriptIdToName


class DropBoxPickUpInterface:

	def __init__( self ):
		"""
		"""
		self.dropTime = time.time()
		self.rollTimers = {}
		self.rollResults = {}
		self.rollResultRoleIDs = {}
		self.playerInfos = {}

	def getEntityByNearby( self, ownershipIDs ):
		"""
		获取附近符合添加的玩家
		"""
		entityList = []
		tempList = self.entitiesInRangeExt( Define.TEAM_ITEM_PICKUP_RANGE, "Role" )
		for entity in tempList:
			if entity.playerDBID in ownershipIDs:
				entityList.append( entity )
		return entityList
		
	def getPlayerDropItems( self, playerDBID ):
		"""
		获取玩家的 可拾取的掉落物品
		"""
		allocationItems = [] if playerDBID not in self.allocationItems else list(self.allocationItems[playerDBID])
		return allocationItems, list(self.notAllocationItems)
		
	def checkDestroy( self ):
		"""
		"""
		if len( self.allocationItems ) == 0 and len( self.notAllocationItems ) == 0:
			self.destroySelf()
		
	def reqSendItemInfoListToClient( self, roleID ):
		"""
		<define method>
		发送掉落物品列表数据到客户端
		"""
		reqRole = KBEngine.entities.get(roleID, None)
		if not reqRole:
			KBEDebug.WARNING_MSG( "DropBox( %d ) roleID( %d ) is error!!!"%( self.id, roleID ) )
			return
			
		itemList = []
		#已分配的
		if reqRole.playerDBID in self.allocationItems:
			items = self.allocationItems[ reqRole.playerDBID ]
			itemList.extend( [ itemInst for itemInst in items ] )
		
		#未分配的
		itemList.extend( [ itemInst for itemInst in self.notAllocationItems ] )
		#根据品质进行排序
		itemList = sorted( itemList, key = lambda itemInst: itemInst.getQuality(), reverse = 1 )
		
		itemInfoList = {"pickUpItemList":[]}
		for itemInst in itemList:
			tempdict = {
				"id" 		: itemInst.id,
				"uid"		: str(itemInst.uid),
				"amount"	: itemInst.amount,
				"bindType"	: itemInst.bindType,
				"quality"		: itemInst.getQuality(),
				"dynamicData": itemInst.getDynamicDataForClient( self ),
			}
			itemInfoList["pickUpItemList"].append( tempdict )
		
		if reqRole.getClient():
			reqRole.getClient().FPickup_GetItemInfoList( self.id,  itemInfoList )

	def reqPickUp( self, roleID, itemUIDStr ):
		"""
		拾取物品请求，进行检测处理，返回能否拾取成功，返回拾取物品的uid列表
		"""	
		#服务器不能相信客户端发过来的数据格式就一定是正确的
		#所以这里需要处理一下
		try:
			itemList = itemUIDStr.split('|')
			itemList = [ int(uid) for uid in itemList ]
			KBEDebug.DEBUG_MSG("itemList = %s"%itemList)
		except:
			return
			
		allPick = True
		pickState = csstatus.ITEM_GO_ON
		role = KBEngine.entities.get( roleID )
		if role.playerDBID in self.allocationItems:
			itemInstList = []
			for uid in list(itemList):
					for itemInst in self.allocationItems.get(role.playerDBID):
						if uid == itemInst.uid:
							itemInstList.append(itemInst)
			#如果背包满了的话，只捡roll点道具
			pickState =role.addItemListCheck(itemInstList)
			if pickState != csstatus.ITEM_GO_ON:
				allPick = False

				for uid in list(itemList):
					for itemInst in self.allocationItems.get(role.playerDBID):
						if uid == itemInst.uid:
							itemList.remove(uid)
		
		self.pickUp( roleID, itemList )
		if not allPick: role.statusMessage(pickState)
		

	def pickUp( self, roleID, itemUIDList ):
		"""
		"""
		#拾取物品处理
		role = KBEngine.entities.get( roleID, None )
		if not role:
			KBEDebug.ERROR_MSG( "role pick up error" )
			return
		
		isSucceed = 1
		itemList = []
		if role.playerDBID in self.allocationItems:
			itemList = self.allocationItems[role.playerDBID]
			
		for uid in itemUIDList:
			findFlag = False
			
			#如果是已分配的物品，直接添加到玩家背包
			for itemInst in itemList:
				if uid != itemInst.uid:
					continue
				
				status = role.addItemCheck( itemInst )
				result = self._addItemForRole( role, itemInst, csdefine.ITEM_ADD_BY_PICKUP )
				
				tempStr = ""
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
				tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
				msg = role.getName() + "|" + tempStr + "|" + str( itemInst.amount )
				
				if result == csstatus.ITEM_GO_ON:
					leftamount = 0
					entityList = self.getEntityByNearby( self.ownershipIDs )
					for entity in entityList:
						if entity.id != role.id and itemInst.getQuality() == ItemTypeEnum.QUALITY_PINK:
							entity.statusMessage( csstatus.PICK_UP_ITEM_ROLE_GET_ITEM, msg )
					self.highValueDrop(role, itemInst)
					itemList.remove( itemInst )
					if not itemList:
						self.allocationItems.pop( role.playerDBID )
						self.updataOwnershipIDs()
						role.clientEntity(self.id).updateDropBoxModelVisible( )
				#背包不能装下所有的物品，则表示添加失败。
				else:
					leftamount = itemInst.amount
					if status == csstatus.ITEM_SPACE_LESS:
						role.statusMessage( csstatus.CIB_MSG_FULL )
					elif status == csstatus.ITEM_IS_REACH_MAX_TAKE_LIMIT:
						role.statusMessage( csstatus.ITEM_UPPER_NOT_CARRIED, tempStr )
				
				if role.getClient():
					role.getClient().PickUp( self.id, isSucceed, str(uid), leftamount )
					
				findFlag = True
				break
			
			#不是已分配的物品
			if not findFlag:
				#自由拾取
				if self.allocation == csdefine.TEAM_PICKUP_TYPE_FREEDOM:
					for itemInst in self.notAllocationItems:
						if uid != itemInst.uid:
							continue
							
						#使用tempOwnershipIDs，可以避免调用updataOwnershipIDs时清除了某些玩家而无法通知该玩家的客户端更新宝箱
						tempOwnershipIDs = []
						tempOwnershipIDs.extend( self.ownershipIDs )
						
						result = self._addItemForRole( role, itemInst, csdefine.ITEM_ADD_BY_PICKUP )
						if result != csstatus.ITEM_GO_ON:
							leftamount = itemInst.getAmount()
							role.statusMessage( csstatus.BAG_NOT_ENOUGHSPACE,"")
						else:
							leftamount = 0
							self.notAllocationItems.remove( itemInst )
							self.updataOwnershipIDs()
							self.highValueDrop(role, itemInst)
							
							if role.getClient():
								role.getClient().PickUp( self.id, isSucceed, str(uid), leftamount )
								#role.clientEntity( self.id ).updateDropBoxModelVisible()
							
						tempStr = ""
						colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
						tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
						msg = role.getName() + "|" + tempStr + "|" + str( itemInst.amount )
						
						#更新到附近玩家的客户端
						entityList = self.getEntityByNearby( tempOwnershipIDs )
						for entity in entityList:
							if not entity.getClient():
								continue
							
							entity.client.PickUp( self.id, isSucceed, str(uid), leftamount )
							if entity.isEntityInView(self):
								entity.clientEntity( self.id ).updateDropBoxModelVisible( )
						if itemInst.getQuality() >= ItemTypeEnum.QUALITY_PINK and role.isInTeam():
							for mb in role.getAllTeamMemberMB():
								if mb.id == self.id:
									continue
								member = KBEngine.entities.get( mb.id, None )
								if member:
									member.statusMessage( csstatus.PICK_UP_ITEM_ROLE_GET_ITEM, msg )
						break
						
				#队伍拾取			
				elif self.allocation == csdefine.TEAM_PICKUP_TYPE_TEAM:
					#已经通知过掷骰子了
					if str(uid) in self.rollResults:
						break
				
					itemInst = None
					for inst in self.notAllocationItems:
						if uid != inst.uid:
							continue
						itemInst = inst
						break
							
					#掷骰子
					memberIDs = []
					entityList = self.getEntityByNearby( self.ownershipIDs )
					for entity in entityList:
						if not str(uid) in self.rollResults:
							self.rollResults[str(uid)] = {}
						if not str( uid ) in self.rollResultRoleIDs:
							self.rollResultRoleIDs[ str(uid) ] = []
							
						self.rollResults[str(uid)][entity.playerDBID] = 0
						self.rollResultRoleIDs[ str(uid) ].append( entity.id )
						self.playerInfos[entity.playerDBID] = entity.getName()
						
						if not itemInst:
							KBEDebug.ERROR_MSG("pickUp:not found item(uid:%d)" %(uid))
						else:
							if hasattr(entity, "client") and entity.client:
								tempdict = {
									"id" 		: itemInst.id,
									"uid"		: str(itemInst.uid),
									"amount"	: itemInst.amount,
									"bindType"	: itemInst.bindType,
									"quality"	: itemInst.getQuality(),
									"dynamicData": itemInst.getDynamicDataForClient( entity ),
								}
								entity.client.FRollRandom( self.id, str( uid ), tempdict, self.rollRemainTime )	#通知所有具有奖励权的玩家客户端弹出掷骰子界面
					
					rollTimerID = self.addTimerRepeat( 1.0, "rollRandomTime", ( str( uid ), ) )
					self.rollTimers[ str(uid) ] = [ rollTimerID, self.rollRemainTime + 1 ] #加1是为了防止客户端延迟的情况
					
					#掷骰子开始后，宝箱销毁倒计时暂停
					if self.dropTimerID != 0:
						self.popTimer( self.dropTimerID )
						self.dropTimerID = 0
						
				#队长分配
				elif self.allocation == csdefine.TEAM_PICKUP_TYPE_CAPTAIN:
					for itemInst in self.notAllocationItems:
						if uid != itemInst.uid:
							continue
							
						tempStr = ""
						colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
						tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
						msg = role.getName() + "|" + tempStr + "|" + str( itemInst.amount )
						
						if role.playerDBID == self.teamCaptainDBID:
							#让队长分配给队员
							tempOwnershipIDs = []
							entityList = self.getEntityByNearby( self.ownershipIDs )
							for entity in entityList:
								tempOwnershipIDs.append( { "id": entity.id, "name": entity.getName() } )
								if entity.id != role.id and itemInst.getQuality() == ItemTypeEnum.QUALITY_PINK:
									entity.statusMessage( csstatus.PICK_UP_ITEM_ROLE_GET_ITEM, msg )
							
							if role.getClient():
								role.client.pickUpToMember( self.id, str( uid ), Functions.toJsonString( tempOwnershipIDs ) )
						else:	
							#向玩家提示队长才能拾取
							role.statusMessage( csstatus.PICK_UP_ITEM_ONLY_CAPTAIN, tempStr )
						break
						
		self.checkDestroy()	

	def pickUpToMember( self, roleID, uid, dstEntityID ):
		"""
		<define method>
		队长分配物品给队员或自己
		@param uid: STRING,物品uid
		@param dstEntityID: INT32,将得到物品的玩家的entity id
		"""
		captain = KBEngine.entities.get( roleID, None )
		if not captain:
			return
			
		dstEntity = KBEngine.entities.get( dstEntityID, None )
		if not dstEntity:
			#通知队长该玩家距离过远，无法分配
			captain.statusMessage( csstatus.PICK_UP_ITEM_ALLOCATION_FAILED,"")	
			return
		
		#不是队伍成员了
		if not captain.isTeammate(dstEntityID):
			captain.statusMessage( csstatus.TEAM_IS_NOT_MEMBER, "" )
			return
			
		for itemInst in self.notAllocationItems:
			if uid != str( itemInst.uid ):
				continue
				
			if  dstEntity.addItemCheck( itemInst ) != csstatus.ITEM_GO_ON:
				captain.statusMessage( csstatus.BAG_NOT_ENOUGHSPACE,"")
			else:
				result = self._addItemForRole( dstEntity, itemInst, csdefine.ITEM_ADD_BY_PICKUP )
				self.notAllocationItems.remove( itemInst )
				
				tempOwnershipIDs = []
				tempOwnershipIDs.extend( self.ownershipIDs )
				self.updataOwnershipIDs()
				self.highValueDrop(dstEntity, itemInst)
				tempStr = ""
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
				tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
				msg = dstEntity.getName() + "|" + tempStr + "|" + str( itemInst.amount )
				
				#更新到所有玩家的客户端
				entityList = self.getEntityByNearby( tempOwnershipIDs )
				for entity in entityList:
					if entity.getClient():
						entity.client.PickUp( self.id, 1, str(uid), 0 )
						entity.clientEntity( self.id ).updateDropBoxModelVisible()
						
					if entity.id != dstEntity.id:
						entity.statusMessage( csstatus.PICK_UP_ITEM_GET_ITEM, msg )
			break
			
		self.checkDestroy()
		
	def rollRandom( self, roleID, uid ):
		"""
		<define method>
		玩家掷骰子
		
		@param uid: STRING,物品uid
		"""
		#非法操作
		if uid not in self.rollResults:
			return
			
		role = KBEngine.entities.get( roleID, None )
		if not role:
			return
			
		#无权参与掷骰子
		if role.playerDBID not in self.rollResults[ uid ]:
			return
			
		point = 0
		while True:
			point = random.randint( 1, 100 )
			if point not in self.rollResults[ uid ].values():
				break
	
		self.rollResults[ uid ][ role.playerDBID ] = point
		ownershipIDs = self.rollResults[ uid ]
		
		for itemInst in self.notAllocationItems:	
			if uid != str(itemInst.uid):
				continue
				
			tempStr = ""
			colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
			tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
			msg = role.getName() + "|" + tempStr + "|" + str( point )
			
			#通知参与本次掷骰子的玩家
			for id in self.rollResultRoleIDs[uid]:
				entity = KBEngine.entities.get( id, None )
				if entity and entity.playerDBID in self.rollResults[ uid ].keys() and self.rollResults[ uid ][ entity.playerDBID ] != -1:
					entity.statusMessage( csstatus.PICK_UP_ITEM_ROLL_POINT, msg )
			return
	
	def abandonRoll( self, roleID, uid ):
		"""
		<define method>
		放弃参与掷骰子
		
		@param uid: STRING, 放弃的物品uid
		"""
		#非法操作
		if uid not in self.rollResults:
			return
			
		role = KBEngine.entities.get( roleID, None )
		if not role:
			return
			
		#无权参与掷骰子
		if role.playerDBID not in self.rollResults[ uid ]:
			return
	
		for itemInst in self.notAllocationItems:
			if uid != str( itemInst.uid ):
				continue
			
			#已经掷过骰子了
			if self.rollResults[uid][role.playerDBID] != 0:
				return
				
			#放弃掷骰子的玩家，将其掷骰子值设为-1
			self.rollResults[ uid ][ role.playerDBID ] = -1
				
			tempStr = ""
			colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
			tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
			msg = role.getName() + "|" + tempStr
			
			for id in self.rollResultRoleIDs[uid]:
				entity = KBEngine.entities.get( id, None )
				if not entity: continue
				
				if entity.playerDBID in self.rollResults[ uid ].keys() and self.rollResults[ uid ][ entity.playerDBID ] != -1:
					entity.statusMessage( csstatus.PICK_UP_ITEM_ROLL_ABANDON, msg )
				
			return
			
	def onRollRandomResult( self, uid ):
		"""
		得出最终获得物品的玩家
		"""
		#调用该方法有两种可能：
		#1.所有玩家都响应了（放弃或参与）掷骰子
		#2.掷骰子响应时间结束
		if uid not in self.rollResults:
			return
		
		rollTimerID = self.rollTimers.pop( uid )[0]
		if rollTimerID != 0:
			self.popTimer( rollTimerID )
			rollTimerID = 0
		
		maxPoint = -1
		roleDBID = -1
		
		roleData = self.rollResults.pop( uid )
		for key, value in roleData.items():
			if value > maxPoint:
				maxPoint = value
				roleDBID = key
		
		itemInst = None
		for inst in self.notAllocationItems:
			if uid != str( inst.uid ):
				continue
			itemInst = inst
			break
			
		if not itemInst:
			return
	
		if maxPoint >= 1:
			msg = ""				
			role = None
			entityList = self.getEntityByNearby( self.ownershipIDs )
			dbidList = [ r.playerDBID for r in entityList ]
			
			#玩家不在范围内，先将物品放到其宝箱中
			if not roleDBID in dbidList:
				if roleDBID not in self.allocationItems:
					self.allocationItems[ roleDBID ] = []
				self.allocationItems[ roleDBID ].append( itemInst )
				
				tempStr = ""
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
				tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
				msg = self.playerInfos.get(roleDBID, "") + "|" + str( maxPoint ) + "|" + tempStr + "|" + str( itemInst.amount )
			else:
				for entity in entityList:
					if entity.playerDBID == roleDBID:
						role = entity
				
				tempStr = ""
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
				tempStr += Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
				msg = role.getName() + "|" + str( maxPoint ) + "|" + tempStr + "|" + str( itemInst.amount )
				
				result = self._addItemForRole( role, itemInst, csdefine.ITEM_ADD_BY_PICKUP )
				if result != csstatus.ITEM_GO_ON:
					role.sendRemainItemWithMail([itemInst], csdefine.REMAIN_ITEM_DROPBOX, csdefine.ITEM_ADD_BY_PICKUP)
					leftamount = 0
					
					"""
					#拾取失败
					if role.playerDBID not in self.allocationItems:
						self.allocationItems[ role.playerDBID ] = []
					self.allocationItems[ role.playerDBID ].append( itemInst )
					role.statusMessage( csstatus.BAG_NOT_ENOUGHSPACE, "" )
					"""
				else:
					leftamount = 0
					self.highValueDrop(role, itemInst)
				if role.getClient():
					role.client.receiverRollResult( self.id, str( uid ), itemInst.id, 1, leftamount )
			
			self.notAllocationItems.remove( itemInst )
			self.updataOwnershipIDs()
			
			#通知所有参与掷骰子的队员
			for id in self.rollResultRoleIDs[ uid ]:
				entity = KBEngine.entities.get( id, None )
				if entity and entity.getClient() and entity.clientEntity( self.id ):
					#所有打开宝箱的玩家都有更新界面
					if not role or ( role.id != entity.id ):
						entity.client.receiverRollResult( self.id, str( uid ), itemInst.id, 0, 0 )
					
					if not self.isOutOwnerAOI(entity):
						entity.clientEntity( self.id ).updateDropBoxModelVisible()
					if entity.playerDBID in roleData and ( roleData[entity.playerDBID] != -1 and roleData[entity.playerDBID] != 0 ) and maxPoint > 1:	
						#只有参与掷骰子的玩家才需要接收掷骰子结果消息
						if role: 
							if role.id != entity.id:
								entity.statusMessage( csstatus.PICK_UP_ITEM_ROLL_MAX_POINT, msg )
						else:#找不到玩家
							entity.statusMessage( csstatus.PICK_UP_ITEM_ROLL_MAX_POINT, msg )
			
		#最大值小于1，表示所有玩家都放弃参与掷骰子
		elif maxPoint <= -1:
			#self.notAllocationItems.remove( itemInst )
			#self.updataOwnershipIDs()
			
			#通知所有参与掷骰子的队员
			for id in self.rollResultRoleIDs[ uid ]:
				entity = KBEngine.entities.get( id, None )
				if entity and entity.getClient():
					#所有打开宝箱的玩家都有更新界面
					entity.client.receiverRollResult( self.id, str( uid ), itemInst.id, 0, 0 )
					#try:
					#	entity.clientEntity( self.id ).updateDropBoxModelVisible()
					#except:
					#	pass
			
			self.rollResultRoleIDs.pop(uid)	
		#没有玩家响应掷骰子
		else:
			pass
			
		#如果没有物品正在进行掷骰子，那么重新开始宝箱销毁倒计时
		if len( self.rollTimers ) == 0:	
			if self.dropRemainTime < 30:
				self.dropRemainTime = 30
			self.dropTimerID = self.addTimerRepeat( 1.0, "timerCallBack", () )	
			
		self.checkDestroy()
	
	def onCheckRoll( self, uid ):
		"""
		检查是否所有玩家已参与或放弃掷骰子
		"""
		if uid not in self.rollResults:
			return False
		
		roleIDlists = self.rollResults[ uid ]
		for dbid, point in roleIDlists.items():
			if point == 0:
				return False
				
		return True
	
	def rollRandomTime( self, uid ):
		"""
		掷骰子响应时间倒计时
		"""
		if self.onCheckRoll( uid ):
			self.onRollRandomResult( uid )
			return
			
		rollRemainTime = self.rollTimers[ uid ][1]
		tempRollResults = self.rollResults[uid]
		
		rollRemainTime -= 1
		if rollRemainTime <= 0:
			self.onRollRandomResult( uid )
			return
			
		self.rollTimers[ uid ][1] = rollRemainTime
		
	def updataOwnershipIDs( self ):
		"""
		更新宝箱拥有者列表
		"""
		if len( self.notAllocationItems ) == 0:
			ownershipIDs = []
			for dbid in self.allocationItems:
				ownershipIDs.append( dbid )	
			self.ownershipIDs = ownershipIDs


	def highValueDrop(self, role,itemInst):
		"""
		判断是否为高价值物品，是则推送高价值世界公告
		"""
		msgID = itemInst.getItemDir("HighValue")
		if msgID > 0:
			if role.spaceScriptID in SpaceScriptIdToName.Datas:
				spaceName=""
				spaceName = SpaceScriptIdToName.Datas[role.spaceScriptID]
				tempStr = ""
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
				tempStr += Const.MSG_FORMAT_COLOR_STRING % (colorStr, "%s" % itemInst.getItemDir("ItemName"))

				msg = role.getName() + "|" + spaceName + "|" + tempStr
				KBEngine.globalData["GMNoticeManager"].globalWorld(msgID, msg)
			else:
				spaceName = ""
				spaceObj = KST.g_objFactory.getSpaceObject(role.spaceScriptID)
				if spaceObj:
					spaceName = spaceObj.getSpaceName()
					tempStr = ""
					colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
					tempStr += Const.MSG_FORMAT_COLOR_STRING % (colorStr, "%s" % itemInst.getItemDir("ItemName"))
					msg = role.getName() + "|" + spaceName + "|" + tempStr
					KBEngine.globalData["GMNoticeManager"].globalWorld(msgID, msg)
	
	def _addItemForRole(self, role, itemInst, reason):
		"""
		"""
		return role.addItem(itemInst, reason)
		"""
		if result != csstatus.ITEM_GO_ON:
			return result
			
		dropRewardOrSpaceReward = self.params.get("dropRewardOrSpaceReward", 1) #区分掉落:0 / 副本奖励:1
		if dropRewardOrSpaceReward == 0:										#掉落的话，绿色品质以上只需要显示一个光效
			if itemInst.getQuality() < ItemTypeEnum.QUALITY_GREEN:
				return result
			
			if role.getClient():
				role.client.CLIENT_PlayEffect(Const.GREEN_DROPBOX_GET_EFFECTID)
			
			if role.isInTeam():
				#在队友的客户端也需要播放光效
				for teamMate in role.getInRangeTeammate(150):
					if teamMate.id == role.id:
						continue
					
					if teamMate.getClient() and teamMate.isEntityInView(role):
						teamMate.clientEntity(role.id).CLIENT_PlayEffect(Const.GREEN_DROPBOX_GET_EFFECTID)
		
		if itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN_SHENG:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity: 
				spaceEntity.getScript().addShengJieItemNotify(spaceEntity, itemInst, dropRewardOrSpaceReward, role, self.params)
		return result
		"""
	