# -*- coding: utf-8 -*-


import csdefine
import KBEDebug
import Math
import csconst
import csstatus
from ConfigObject.ReviveCost.ReviveCostLoader import g_reviveCostLoader
import Functions
import Const
import KBEngine

class RoleReviveInterface():
	"""
	玩家复活接口
	"""
	def __init__( self ):
		self.role_die_teleport = False							# 死亡标记
		self.recoverReviveOriginData()

	def CELL_revive( self, srcEntityID, type ):
		"""
		<Exposed method>
		复活 接口
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		try:
			intType = int( type )
		except:
			KBEDebug.ERROR_MSG( "Can not change type(%s)" %type )
			return
		
		if intType == csdefine.REVIVE_ON_ORIGIN_BY_COST_ITEM:
			self.useItemToRevive()
		elif intType == csdefine.REVIVE_ON_CITY:
			self.reviveOnCity()
		elif intType == csdefine.REVIVE_ON_REVIVE_SPACE:
			self.reviveOnReviveSpace()
		elif intType == csdefine.REVIVE_ON_SPACE_COPY:
			self.reviveOnSpaceCopy()
		elif intType == csdefine.REVIVE_ON_RETURN_POINT:
			self.reviveOnRturnPoint()
		elif intType == csdefine.REVIVE_ON_ORIGIN_BY_COST_MONEY:
			self.useMoneyToRevive()
		elif intType == csdefine.REVIVE_ON_LING_MAI_COPY:		# 灵脉战场的特殊复活方式
			self.reviveOnLingMai()
		elif intType == csdefine.REVIVE_ON_FROZEN_FIGHT_COPY:		# 冰雪之战的特殊复活方式
			self.reviveOnFrozenFight()
		elif intType == csdefine.REVIVE_ON_SECOND_TONG_STARCRAFT: # 帮会争霸第二场的复活方式
			self.reviveOnSecondTongStarcraft()
		elif intType == csdefine.REVIVE_ON_LING_QI:		# 灵气迷宫复活方式
			self.reviveOnLingQi()
		elif intType == csdefine.REVIVE_ON_YXLM: # 英雄联盟复活方式
			self.reviveOnYXLM()
		elif intType == csdefine.REVIVE_ON_THIRD_TONG_STARCRAFT: #帮会争霸第三场的复活方式
			self.reviveOnThirdTongStarcraft()
		elif intType == csdefine.REVIVE_ON_YCJMD: #勇闯绝命岛复活方式
			self.reviveOnYCJMD()
		elif intType == csdefine.REVIVE_ON_SGMZ: #上古密阵复活方式
			self.reviveOnSGMZ()
		elif intType == csdefine.REVIVE_ON_FHLT: #烽火连天复活方式
			self.reviveOnFHLT()
		elif intType == csdefine.REVIVE_ON_GCZ: #攻城战复活方式
			self.reviveOnGCZ()
		elif intType == csdefine.REVIVE_ON_HLBCPVP: #高级练兵场PVP复活方式
			self.reviveOnHLBCPVP()
		elif intType == csdefine.REVIVE_ON_LBCPVP: #练兵场PVP复活方式
			self.reviveOnLBCPVP()
		elif intType == csdefine.REVIVE_ON_LHMJ: # 轮回秘境复活方式
			self.reviveOnLHMJ()
		elif intType == csdefine.REVIVE_ON_DF: # 洞府复活方式
			self.reviveOnDF()
		elif intType == csdefine.REVIVE_ON_TONG_PLUNDER: #帮会掠夺战复活方式
			self.reviveOnTongPlunder()
		elif intType == csdefine.REVIVE_ON_BHZBPOINTWAR_PVP: #帮会争霸 据点争夺战 PVP 复活
			self.reviveOnBHZBPointWar()
		
	def reviveOnOrigin( self ):
		"""
		<define method>
		原地复活
		"""
		if self.isState( csdefine.ENTITY_STATE_DEAD ):
			self.onRevive()
			self.changeState( csdefine.ENTITY_STATE_FREE )
			self.setHP( self.HP_Max )
			self.setMP( self.MP_Max )
	
	def reviveOnCity( self ):
		"""
		<define method>
		回城复活
		"""
		self.role_die_teleport = True
		self.gotoSpace( self.reviveSpaceScriptID, Math.Vector3(self.revivePosition), self.reviveDirection )
	
	def reviveOnReviveSpace( self ):
		"""
		<define method>
		space文件中reviveScriptID配置的地图复活
		"""
		self.role_die_teleport = True
		spaceObject = self.getCurrentSpaceObject()
		spaceScriptID, position, direction = spaceObject.getReviveInfo()
		self.gotoSpace( spaceScriptID, Math.Vector3(position), direction )
		
	def reviveOnSpaceCopy( self ):
		"""
		<define method>
		副本复活
		"""
		if not self.isState( csdefine.ENTITY_STATE_DEAD ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			try:																									# 大地图不支持，此类复活方式！防止策划同学配错，加个容错处理
				dynamicReviverPos, dynamicReviverDir = spaceEntity.getDynamicReviverInfo(self.getCamp())
				self.role_die_teleport = True
				self.gotoSpace( spaceEntity.scriptID, dynamicReviverPos, dynamicReviverDir )
			except:
				KBEDebug.ERROR_MSG( "space(%s) getDynamicReviverInfo fail!!"%spaceEntity.scriptID )
				return

	def reviveOnSpaceCopyYXLM(self):
		"""
		英雄联盟复活
		"""
		if not self.isState( csdefine.ENTITY_STATE_DEAD ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			try:																									# 大地图不支持，此类复活方式！防止策划同学配错，加个容错处理
				dynamicReviverPos, dynamicReviverDir = spaceEntity.getDynamicReviverInfo(self.getCamp())

				self.setPosition(dynamicReviverPos)
				self.setDirection(dynamicReviverDir)
				self.reviveOnOrigin()
			except:
				KBEDebug.ERROR_MSG( "space(%s) getDynamicReviverInfo fail!!"%spaceEntity.scriptID )
				return		
	
	def reviveOnSpaceCopyLBCPVP(self):
		"""
		高级练兵场PVP复活
		"""
		if not self.isState( csdefine.ENTITY_STATE_DEAD ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			try:																									# 大地图不支持，此类复活方式！防止策划同学配错，加个容错处理
				dynamicReviverPos, dynamicReviverDir = spaceEntity.getDynamicReviverInfo(self.getBelongSide())

				self.setPosition(dynamicReviverPos)
				self.setDirection(dynamicReviverDir)
				self.reviveOnOrigin()
			except:
				KBEDebug.ERROR_MSG( "space(%s) getDynamicReviverInfo fail!!"%spaceEntity.scriptID )
				return		


	def reviveOnRturnPoint( self ):
		"""
		<define method>
		space文件中ExitSpace配置的地图复活(复活到返回点)
		"""
		self.role_die_teleport = True
		spaceObject = self.getCurrentSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( self )
		self.gotoSpaceUseArg( exitScriptID, Math.Vector3(exitPosition), exitDirection,{} )
			
	def CELL_setRevivePos( self, srcEntityID ):
		"""
		设置复活点
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.reviveSpaceScriptID = csconst.REVIVE_SPACE_SCRIPTID
		self.revivePosition = Math.Vector3( csconst.REVIVE_POSITION )
		self.reviveDirection = Math.Vector3( csconst.REVIVE_DIRECTION )

	def setRevivePos( self, spaceScriptID, position, direction ):
		"""
		<Define Method>
		NPC设置回城复活点
		"""
		self.reviveSpaceScriptID = spaceScriptID
		self.revivePosition = Math.Vector3(position)
		self.reviveDirection = direction

	def CELL_reviveOnArea( self, srcEntityID, reviveSpace, revivePosition, reviveDirection ):
		"""
		<Exposed method>
		区域复活点复活（优先）
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceScriptID = reviveSpace
		if not reviveSpace:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				spaceScriptID = spaceEntity.scriptID
		position = eval( revivePosition )
		direction = eval( reviveDirection )
		if spaceScriptID:
			self.role_die_teleport = True
			self.gotoSpaceUE4( spaceScriptID, position, direction )

	def onRevive( self ):
		"""
		玩家复活后，处理一些事情
		"""
		self.client.CLIENT_OnHideRevive()
		self.addBuff( self, csconst.TELEPORT_PROTECT_BUFFID )     #添加传送保护buff
		
	def revive_roleEnterSpace( self ):
		"""
		玩家进入地图是否需要复活
		"""
		if self.role_die_teleport:										# 在传送完后，再设置复活。是因为先设置复活，再传送，人物会先复活站起来 再传送
			self.reviveOnOrigin()
			self.role_die_teleport = False
		if self.isState( csdefine.ENTITY_STATE_DEAD ):					# 玩家第一次进入游戏就死亡
			self.calcReviveTime()
			
	def onEnterDead( self ):
		"""
		玩家死亡
		"""
		self.calcReviveTime()

	def onTeleportCompleted( self, isFirst ):
		"""
		在副本死亡重新上线弹出复活选项(CST-3626)
		"""
		if self.isState( csdefine.ENTITY_STATE_DEAD ):
			self.calcReviveTime()

	def calcReviveTime( self ):
		"""
		玩家死亡 计算下次使用 金钱或物品 复活的时间
		"""
		if self.nextUseItemToReviveTime > 0 and Functions.getTime() < self.nextUseItemToReviveTime:
			self.remainUseItemTime = (self.nextUseItemToReviveTime - Functions.getTime()) / csconst.TIME_ENLARGE_MULTIPLE
		else:
			self.remainUseItemTime = 0.0
		if self.nextUseMoneyToReviveTime > 0 and Functions.getTime() < self.nextUseMoneyToReviveTime:
			self.remainUseMoneyTime = (self.nextUseMoneyToReviveTime - Functions.getTime()) / csconst.TIME_ENLARGE_MULTIPLE
		else:
			self.remainUseMoneyTime = 0.0

		self.calcYXLMReviveTime() #英雄联盟特殊复活方式
		self.calcGCZReviveTime() # 攻城战复活方式

	def checkCanUseItemToRevive( self, number ):
		"""
		检查是否可以使用物品复活
		"""
		costData = g_reviveCostLoader.getCostItemData( number )
		if costData == None:
			KBEDebug.ERROR_MSG("RoleReviveCostConfig UseItem has not this config(number = %i)"%number)
			return False
		if Functions.getTime() < self.nextUseItemToReviveTime:
			KBEDebug.ERROR_MSG(" has not already to revive ")
			return False
		itemInstList = self.getItemInstsByID( Const.REVIVE_ITEMID )
		totalAmount = 0
		for itemInst in itemInstList:
			totalAmount += itemInst.amount
		if totalAmount < costData["costAmount"]:
			#通知界面提示“原地复活需要使用归命符箓，您可以在道具商城购买到归命符箓”
		 	self.statusMessage( csstatus.RIVIVE_ITEM_NOT_ENOUGN,"" )
		 	return False
		return True

	def useItemToRevive( self ):
		"""
		<Define method>
		使用道具原地复活
		"""
		if not self.checkCanUseItemToRevive( self.reviveByCostItemNumber + 1 ):
			return

		self.reviveByCostItemNumber += 1
		costData = g_reviveCostLoader.getCostItemData( self.reviveByCostItemNumber )
		self.lastTimeReviveByCostItem = Functions.getTime()
		self.nextUseItemToReviveTime = self.lastTimeReviveByCostItem + costData["coolDownTime"] * csconst.TIME_ENLARGE_MULTIPLE
		itemInstList = self.getItemInstsByID( Const.REVIVE_ITEMID )
		self.removeItemListByAmount( itemInstList, costData["costAmount"], csdefine.ITEM_REMOVE_BY_USE )
		self.reviveOnOrigin()
		self.onUseItemToRevive()

	def onUseItemToRevive(self):
		"""
		"""
		#更新 “重置物品复活数据”的倒计时			
		if self.resetUseItemReviveDataTimerID:
			self.popTimer(self.resetUseItemReviveDataTimerID)
		self.resetUseItemReviveDataTimerID = self.addTimerCallBack(Const.RECOVER_REVIVE_DATA_TIME,"resetUseItemReviveData",())

	def useMoneyToRevive( self ):
		"""
		使用金币原地复活
		"""

		if not self.checkCanUseMoneyToRevive( self.reviveByCostMoneyNumber + 1 ):
			return
		
		costData = g_reviveCostLoader.getCostMoneyData( self.reviveByCostMoneyNumber + 1 )	
		if self.subBindMoney( costData["costAmount"], csdefine.MONEY_SUB_REASON_ROLE_REVIVE ):
			self.reviveByCostMoneyNumber += 1
			self.lastTimeReviveByCostMoney = Functions.getTime()
			self.nextUseMoneyToReviveTime = self.lastTimeReviveByCostMoney + costData["coolDownTime"] * csconst.TIME_ENLARGE_MULTIPLE
			self.reviveOnOriginByMoney()
			self.onUseMoneyToRevive()
		
	def onUseMoneyToRevive(self):
		"""
		"""
		#更新 “重置金币复活数据”的倒计时			
		if self.resetUseMoneyReviveDataTimerID:
			self.popTimer(self.resetUseMoneyReviveDataTimerID)
		self.resetUseMoneyReviveDataTimerID = self.addTimerCallBack(Const.RECOVER_REVIVE_DATA_TIME,"resetUseMoneyReviveData",())	

	def checkCanUseMoneyToRevive( self, number ):
		"""
		检查是否可以使用金币复活
		"""
		costData = g_reviveCostLoader.getCostMoneyData( number )
		if costData == None:
			KBEDebug.ERROR_MSG("RoleReviveCostConfig UseMoney has not this config(number = %i)"%number)
			return False
		if Functions.getTime() < self.nextUseMoneyToReviveTime:
			KBEDebug.ERROR_MSG(" has not already to revive ")
			return False
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		if self.getBindMoney() < costData["costAmount"]:
			self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(costData["costAmount"])], "replacePayRevive", costData["costAmount"],)
			return False

		return True

	def replacePayRevive(self, reply, cost):
		"""金币代付绑定金币复活"""
		if reply:
			if self.subMoney( cost, csdefine.MONEY_SUB_REASON_ROLE_REVIVE ):
				self.reviveByCostMoneyNumber += 1
				costData = g_reviveCostLoader.getCostMoneyData(self.reviveByCostMoneyNumber)
				self.lastTimeReviveByCostMoney = Functions.getTime()
				self.nextUseMoneyToReviveTime = self.lastTimeReviveByCostMoney + costData["coolDownTime"] * csconst.TIME_ENLARGE_MULTIPLE
				self.reviveOnOriginByMoney()
				self.onUseMoneyToRevive()
			else:
				self.statusMessage(csstatus.NPCSHOP_ROLE_MONEY_ERROR, "")


	def reviveOnOriginByMoney( self ):
		"""
		<define method>
		原地复活 通过使用金钱
		"""
		if self.isState( csdefine.ENTITY_STATE_DEAD ):
			self.changeState( csdefine.ENTITY_STATE_FREE )
			self.setHP( int(self.HP_Max * 0.3) )  # 只恢复30%的血量
			self.setMP( int(self.MP_Max * 0.3) )  # 只恢复30%的蓝量
			self.onRevive()

	def resetUseItemReviveData( self ):
		"""
		重置使用消耗道具的复活数据
		"""
		self.reviveByCostItemNumber = 0
		self.nextUseItemToReviveTime = 0
		self.remainUseItemTime = 0.0
		self.lastTimeReviveByCostItem = 0
		self.resetUseItemReviveDataTimerID = 0

	def resetUseMoneyReviveData(self):
		"""
		重置使用消耗金币的复活数据
		"""
		self.nextUseMoneyToReviveTime = 0
		self.reviveByCostMoneyNumber = 0
		self.remainUseMoneyTime = 0.0
		self.lastTimeReviveByCostMoney = 0
		self.resetUseMoneyReviveDataTimerID = 0

	def recoverReviveOriginData( self ):
		"""
		恢复原地复活的数据 不需要考虑是否在复活状态
		"""
		#消耗金币复活数据
		if self.lastTimeReviveByCostMoney > 0:
			if Functions.getTime() >= self.lastTimeReviveByCostMoney + Const.RECOVER_REVIVE_DATA_TIME * csconst.TIME_ENLARGE_MULTIPLE:
				self.resetUseMoneyReviveData()
			else:
				remainRecoverUseItemTime = (self.lastTimeReviveByCostMoney + Const.RECOVER_REVIVE_DATA_TIME * csconst.TIME_ENLARGE_MULTIPLE - Functions.getTime())/csconst.TIME_ENLARGE_MULTIPLE
				self.resetUseMoneyReviveDataTimerID = self.addTimerCallBack(remainRecoverUseItemTime,"resetUseMoneyReviveData",())	
				
		#消耗道具复活数据
		if self.lastTimeReviveByCostItem > 0:
			if Functions.getTime() >= self.lastTimeReviveByCostItem + Const.RECOVER_REVIVE_DATA_TIME * csconst.TIME_ENLARGE_MULTIPLE:
				self.resetUseItemReviveData()
			else:
				remainRecoverUseItemTime = (self.lastTimeReviveByCostItem + Const.RECOVER_REVIVE_DATA_TIME * csconst.TIME_ENLARGE_MULTIPLE - Functions.getTime())/csconst.TIME_ENLARGE_MULTIPLE
				self.resetUseItemReviveDataTimerID = self.addTimerCallBack(remainRecoverUseItemTime,"resetUseItemReviveData",())

		if self.nextUseItemToReviveTime > 0 and Functions.getTime() < self.nextUseItemToReviveTime:
			self.remainUseItemTime = (self.nextUseItemToReviveTime - Functions.getTime()) / csconst.TIME_ENLARGE_MULTIPLE
		if self.nextUseMoneyToReviveTime > 0 and Functions.getTime() < self.nextUseMoneyToReviveTime:
			self.remainUseMoneyTime = (self.nextUseMoneyToReviveTime - Functions.getTime()) / csconst.TIME_ENLARGE_MULTIPLE

	def reviveOnLingMai( self ):
		"""灵脉战场的特殊复活方式"""
		spaceObject = self.getCurrentSpaceObject()
		if spaceObject.scriptID == Const.LMZC_SPACE_SCRIPTID:
			reviveInfo = spaceObject.getReviveInfo( self )
			self.position = reviveInfo[0]
			self.changeDirection(reviveInfo[1], csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()
#			self.role_die_teleport = True
#			self.gotoSpace( Const.LMZC_SPACE_SCRIPTID, reviveInfo[0], reviveInfo[1] )
		else:
			KBEDebug.ERROR_MSG("Player(name:%s,id:%d) revive err!!this revive type is speciel"%(self.playerName,self.id))

	def reviveOnFrozenFight( self ):
		"""冰雪之战的特殊复活方式"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity.scriptID == Const.FROZEN_FIGHT_SPACE_SCRIPTID:
			reviveInfo = spaceEntity.getReviveInfo(self)
			self.position = reviveInfo[0]
			self.changeDirection(reviveInfo[1], csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()
		else:
			KBEDebug.ERROR_MSG("Player(name:%s,id:%d) revive err!!this revive type is speciel"%(self.playerName,self.id))

	def reviveOnSecondTongStarcraft( self ):
		"""
		帮会争霸第二场的复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			reviveInfo = spaceEntity.getScript().getEnterInfo( spaceEntity, self.tongDBID )
			self.position = reviveInfo[0]
			self.changeDirection(reviveInfo[1], csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()

	def reviveOnLingQi( self ):
		"""
		灵气迷宫复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			reviveInfo = spaceEntity.getScript().getEnterInfo()
			self.position = reviveInfo[0]
			self.changeDirection(reviveInfo[1], csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()

	def reviveOnYXLM( self ):
		"""
		英雄联盟复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_YXLM:
			return
		member = spaceEntity.memberDatas.getMemberByPlayerDBID( self.playerDBID )
		if not member:
			return
		if not self.checkReviveOnYXLM( (member.reviveYXLMNumber + 1) ):
			return
		member.reviveYXLMNumber += 1
		self.reviveOnSpaceCopyYXLM()

	def reviveOnHLBCPVP( self ):
		"""
		高级练兵场PVP复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_YXLM:
			return
		member = spaceEntity.memberDatas.getMemberByPlayerDBID( self.playerDBID )
		if not member:
			return
		if not self.checkReviveOnYXLM( (member.reviveYXLMNumber + 1) ):
			return
		member.reviveYXLMNumber += 1
		self.reviveOnSpaceCopyLBCPVP()

	def checkReviveOnYXLM( self, number ):
		"""
		检查在英雄联盟中的复活
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_YXLM:
			return False
		member = spaceEntity.memberDatas.getMemberByPlayerDBID( self.playerDBID )
		if not member:
			return False
		costData = g_reviveCostLoader.getCostYXLMData( number )
		if costData == None:
			KBEDebug.ERROR_MSG("RoleReviveCostConfig YXLM has not this config(number = %i)"%number)
			return False
		if Functions.getTime() < member.nextYXLMToReviveTime:
			KBEDebug.ERROR_MSG(" has not already to revive ")
			return False
		return True

	def calcYXLMReviveTime( self ):
		"""
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_YXLM:
			member = spaceEntity.memberDatas.getMemberByPlayerDBID( self.playerDBID )
			if not member:
				return
			if member.reviveYXLMNumber == 0:
				self.remainYXLMReviveTime = 0.0
				return
			costData = g_reviveCostLoader.getCostYXLMData( member.reviveYXLMNumber )
			member.nextYXLMToReviveTime = Functions.getTime() + costData["coolDownTime"] * csconst.TIME_ENLARGE_MULTIPLE
			if member.nextYXLMToReviveTime > 0 and Functions.getTime() < member.nextYXLMToReviveTime:
				self.remainYXLMReviveTime = (member.nextYXLMToReviveTime - Functions.getTime()) / csconst.TIME_ENLARGE_MULTIPLE
			else:
				self.remainYXLMReviveTime = 0.0

	def reviveOnThirdTongStarcraft( self ):
		"""
		帮会争霸第三场的复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			reviveInfo =spaceEntity.getReviveInfoByTongDBID( self.tongDBID )
			self.position = reviveInfo[0]
			self.changeDirection(reviveInfo[1], csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()

	def reviveOnYCJMD( self ):
		"""
		勇闯绝命岛的复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			reviveInfo = spaceEntity.getScript().getReviveInfos( self.position )
			self.position = reviveInfo[0]
			self.changeDirection(reviveInfo[1], csdefine.REASON_CHANGE_DIR_FORCE)
			if self.isState( csdefine.ENTITY_STATE_DEAD ):
				self.changeState( csdefine.ENTITY_STATE_FREE )
				self.setHP( int(self.HP_Max/2) )
				self.setMP( int(self.MP_Max/2) )
				self.onRevive()

	def reviveOnSGMZ( self ):
		"""
		上古密阵复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			revivePos,reviveDir = spaceEntity.getScript().getReviveInfos( spaceEntity, self )
			self.position = revivePos
			self.changeDirection(reviveDir, csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()

	def reviveOnFHLT( self ):
		"""
		烽火连天复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			revivePosInfo, reviveDirInfo = spaceEntity.getScript().getEnterInfoByCamp()
			self.position = revivePosInfo
			self.changeDirection(reviveDirInfo, csdefine.REASON_CHANGE_DIR_FORCE)
			self.reviveOnOrigin()

	def requestReviveSpaceScriptID( self, srcEntityID, type ):
		"""
		<Exposed method>
		请求复活地图对应的ScriptID
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		try:
			intType = int( type )
		except:
			KBEDebug.ERROR_MSG( "Can not change type(%s)" %type )
			return

		if intType == csdefine.REVIVE_ON_RETURN_POINT:
			spaceObject = self.getCurrentSpaceObject()
			exitScriptID = spaceObject.getReviveToExitInfo( self )[0]
			self.client.NotifyReviveSpaceScriptID( exitScriptID )

	def reviveOnGCZ( self ):
		"""
		攻城战复活方式
		"""
		if not self.isState( csdefine.ENTITY_STATE_DEAD ):
			return
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_GCZ:
			return

		reviveNum, nextReviveTime = spaceEntity.getRecordRoleReviveData( self.playerDBID )
		if not self.checkReviveOnGCZ():
			return
		costData = g_reviveCostLoader.getCostGCZData(reviveNum +1)
		if costData == None:
			self.reviveOnOrigin()
			self.gotoExitSpacePos()
			return
		buffID = spaceEntity.getScript().getReviveAddBuffIDByReviveNum( reviveNum )
		spaceEntity.addRecordRoleReviveNum( self.playerDBID )
		position = spaceEntity.getRevivePosition( self )
		self.position = position
		self.reviveOnOrigin()
		self.callArmyOnRevive()
		if buffID:
			self.addBuff( self, buffID )

	def checkReviveOnGCZ( self ):
		"""
		检查攻城战中的复活
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_GCZ:
			return False
		reviveNum, nextReviveTime = spaceEntity.getRecordRoleReviveData( self.playerDBID )
		if Functions.getTime() < nextReviveTime:
			return False
		return True

	def calcGCZReviveTime( self ):
		"""
		计算玩家下次的复活时间
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_GCZ:
			return
		reviveTypeStr = spaceEntity.getCurrentSpaceData(Const.SPACE_DATA_REVIVE_TYPE)
		if csdefine.REVIVE_ON_BHZBPOINTWAR_PVP in [int(i) for i in reviveTypeStr.split("|")]:
			spaceEntity.updateRoleNextReviveTime(self.playerDBID)
			reviveNum, nextReviveTime = spaceEntity.getRecordRoleReviveData( self.playerDBID )
			if nextReviveTime > 0 and Functions.getTime() < nextReviveTime:
				self.remainYXLMReviveTime = ( nextReviveTime - Functions.getTime() ) / csconst.TIME_ENLARGE_MULTIPLE
			else:
				self.remainYXLMReviveTime = 0.0

			if reviveNum >= spaceEntity.getScript().getMaxDieNum():
				self.remainReviveNum = 0
				self.statusLeaveBHZBSpace()
			else:
				self.remainReviveNum = spaceEntity.getScript().getMaxDieNum() - reviveNum
				self.addTimerCallBack( self.remainYXLMReviveTime +3.1,"reviveOnBHZBPointWar",() )
			return
		reviveNum, nextReviveTime = spaceEntity.getRecordRoleReviveData( self.playerDBID )
		if reviveNum == 0:
			self.remainYXLMReviveTime = 0.0
			return

		costData = g_reviveCostLoader.getCostGCZData( reviveNum )
		tempNextReviveTime = Functions.getTime() + costData["coolDownTime"] * csconst.TIME_ENLARGE_MULTIPLE
		spaceEntity.updateRoleNextReviveTime( self.playerDBID, tempNextReviveTime ) 
		if tempNextReviveTime > 0 and Functions.getTime() < tempNextReviveTime:
			self.remainYXLMReviveTime = ( tempNextReviveTime - Functions.getTime() ) / csconst.TIME_ENLARGE_MULTIPLE
		else:
			self.remainYXLMReviveTime = 0.0
			
	def campFitTeleport( self, spaceScriptID, position, direction ):
		"""
		<define method>
		阵营随机匹配传送
		"""
		if self.isState( csdefine.ENTITY_STATE_DEAD ):
			self.role_die_teleport = True
		self.gotoSpace( spaceScriptID, position, direction )
		
	def reviveOnLBCPVP( self ):
		"""
		练兵场PVP复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		spaceObject = spaceEntity.getScript()
		position, direction = spaceEntity.getRevivePosition( self )
		self.position = position
		self.reviveOnOrigin()
		self.callArmyOnRevive()
		
	def reviveOnLHMJ( self ):
		"""
		轮回秘境复活方式
		"""
		if self.occupySpaceDF == csdefine.SPACE_TYPE_NONE:								# 回绑定点
			self.reviveOnCity()
		elif self.occupySpaceDF ==  csdefine.SPACE_TYPE_PUBLIC:
			self.reviveOnRturnPoint()													# 有玲珑玉林，在轮回秘境大地图复活
		else:
			self.role_die_teleport = True
			packArgs = {}
			packArgs["lineNumber"] = self.caveHouseLine
			packArgs["group"] = self.getBuildIndex()
			packArgs["belongDBID"] = self.playerDBID
			self.gotoSpaceEnterPos( csconst.DONGFU_MAP_SPACESCRIPTID[self.occupySpaceDF], packArgs)
	
	def reviveOnDF( self ):
		"""
		洞府复活方式
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		self.role_die_teleport = True
		spaceObject = spaceEntity.getScript()
		if self.playerDBID == spaceEntity.belongDBID:
			if KBEngine.globalData.get("LHMJ_PlunderActive", 0) or KBEngine.globalData.get("LHMJ_ChallengeActive",0):			# 掠夺战\争夺战开启
				position, direction = spaceObject.getActiveReviveInfo()
				self.gotoSpaceUseArg( spaceObject.scriptID, position, direction, {"belongDBID" : self.playerDBID} )
			else:
				self.gotoSpaceEnterPos( spaceObject.scriptID, {"belongDBID" : self.playerDBID} )
		else:
			self.reviveOnLHMJ()					# 其他人在别人洞府里，复活方式跟在 轮回秘境大地图复活方式相同

	def leaveTongPlunderSpace(self, reply):
		"""
		复活次数已达最大值，离开帮会掠夺战副本
		"""
		if reply:
			self.reviveOnOrigin()
			self.gotoExitSpacePos()
			KBEngine.globalData["TongPlunderManager"].onReviveNumUseup(self.playerDBID)
			
	def reviveOnTongPlunder(self):
		"""
		帮会掠夺战复活方式
		"""
		if not self.isState( csdefine.ENTITY_STATE_DEAD ):
			return
			
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_TYPE_CHILD_TONG_PLUNDER:
			return

		remainReviveNum, nextReviveTime = spaceEntity.getRecordRoleReviveData(self.playerDBID)	
		if remainReviveNum == -1:
			self.reviveOnOrigin()
			self.gotoExitSpacePos()
			KBEngine.globalData["TongPlunderManager"].onReviveNumUseup(self.playerDBID)
			return
		
		position = spaceEntity.getRevivePosition(self)
		self.position = position
		self.reviveOnOrigin()
		self.callArmyOnRevive()
		
		self.remainYXLMReviveTime = nextReviveTime
		self.remainReviveNum = remainReviveNum
		spaceEntity.addRecordRoleReviveNum(self.playerDBID)
		spaceEntity.getScript().onPlayerRevive(spaceEntity, self)

	def reviveOnBHZBPointWar( self ):
		"""
		帮会争霸 据点争夺战 PVP 复活
		"""
		if not self.isState( csdefine.ENTITY_STATE_DEAD ):
			return

		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return

		reviveNum, nextReviveTime = spaceEntity.getRecordRoleReviveData( self.playerDBID )
		if Functions.getTime() < nextReviveTime:
			return
		if reviveNum > spaceEntity.getCurrentSpaceObject().getMaxDieNum():
			self.leaveBHZBSpace(1)
			return
		spaceEntity.addRecordRoleReviveNum( self.playerDBID )
		position,direction = spaceEntity.getRevivePosition(self)
		self.position = position
		self.reviveOnOrigin()
		self.callArmyOnRevive()