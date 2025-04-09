# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csstatus
import csdefine
import time
import Functions
import ItemFactory
import ItemTypeEnum
from ItemSystemExp import g_ToolCompose
from ConfigObject.Trade.TradeMgr import g_tradeMgr
from LunHuiMiJin.LunHuiMiJinCfg import Datas as LunHuiMiJinDatas
from LunHuiMiJin.LHMJShopCostCfg import Datas as LHMJShopCostDatas
from ConfigObject.LingQuanProduceLoader import g_LingQuanProduceLoader
from ConfigObject.BuildDepleteLoader import g_BuildDepleteLoader
import ImpInterface.RoleLHMJActiveInterface as RoleLHMJActiveInterface
import Const
import csconst
import Math
import random
import QuestEventDefine



class RoleLunHuiMiJinInterface( RoleLHMJActiveInterface.RoleLHMJActiveInterface ):
	"""
	玩家轮回秘境接口
	"""
	def __init__( self ):
		RoleLHMJActiveInterface.RoleLHMJActiveInterface.__init__( self )
		self.timeID = 0
		self._checkBuildProtectState()

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		itemInst = self._getActiveChartItem()
		if itemInst:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onOpenBFPlayerOutLine(self.playerDBID, self.psionic, itemInst.getPerCosume())
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].onPlayerOffLine(self.playerDBID)
		if self.challengeDBID:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onChallengePlayerOffLine( self.challengeDBID )
		
	def initClientData( self ):
		""""""
		RoleLHMJActiveInterface.RoleLHMJActiveInterface.initClientData( self )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].onPlayerOnline( self.base, self.playerDBID )
		if self.challengeDBID:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onChallengePlayerOnLine( self.base, self.playerDBID, self.challengeDBID )
		
	def onNewDayLogin( self ):
		"""玩家在新的一天登录, 清理数据"""
		self.isChallenge = 0
		self.layerNumber = 0
		self.removeQuestType( csdefine.QUEST_TYPE_TTD )
		self.clearAbandonQuest()
	
	def initDongFuDatas( self, dongFuType, lineNumber, group, position, buildLevels, destroyBuilds, repairBuildTime, reviveTime ):
		"""
		define method
		初始化洞府
		"""
		self.occupySpaceDF = dongFuType
		self.caveHouseLine = lineNumber
		self.groundPosDict = { group : position }
		self.dongFuBuilds = buildLevels
		self.destroyBuilds = destroyBuilds
		self.repairBuildTime = repairBuildTime
		self.guardReviveTime = reviveTime
		self.client.CLIENT_initLHMJBuild( dongFuType, buildLevels )
		
		if self.buildUpgradeTime:
			for buildType, beginTime in self.buildUpgradeTime.items():
				endTime = int(g_BuildDepleteLoader.getBuildUpgradeTime( buildType, self.getLHMJBuildLevel( buildType ) + 1 ))
				if int(time.time()) - beginTime >= endTime:
					self.upgradeBuildSuccess( buildType )
				else:
					self.client.StartBuildUpgrade( buildType, str( (endTime - ( int(time.time()) - beginTime )) * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime() ))
		
	def hasDongFu( self ):
		"""是否占领洞府\高级洞府"""
		return self.occupySpaceDF in [csdefine.SPACE_TYPE_PRIVATE, csdefine.SPACE_TYPE_HIGH_DF]
		
	def onInitDongFuErr( self ):
		"""
		define method
		洞府可能被占领了
		"""
		self.occupySpaceDF = csdefine.SPACE_TYPE_NONE
		self.buildUpgradeTime = {}
		self.caveHousePsionic = 0
		self.lingQuanCurrHP = 0
		self.activeChartID = 0
		self.setJadeIsValid( 1 )				# 如果背包有玲珑玉林设置有效
		
	def requestPlayerDFDatas( self, srcEntityID ):
		"""
		exposed method
		请求洞府数据(返回玩家所在的线)
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		offset = 0
		if self.challengeDBID and self.challengeLineNumber:
			offset += 1
		if self.hasDongFu():
			offset += 1
		lineNumber = self.caveHouseLine if self.caveHouseLine else 1
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestPlayerDFDatas(self, self.playerDBID, lineNumber, offset)
		
	def requestDFDatas( self, srcEntityID, lineNumber ):
		"""
		exposed method
		请求洞府数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		offset = 0
		if self.challengeDBID:
			offset += 1
		if self.hasDongFu():
			offset += 1
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestDFDatas(self, self.playerDBID, lineNumber, offset)
		
	def requestDFDatasByPage( self, srcEntityID, lineNumber, page ):
		"""
		exposed method
		请求洞府数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		offset = 0
		if self.challengeDBID:
			offset += 1
		if self.hasDongFu():
			offset += 1
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestDFDatasByPage(self, self.playerDBID, lineNumber, page, offset)
		
	def getSalary( self ):
		"""领取俸禄"""
		if not self.occupySpaceDF == csdefine.SPACE_TYPE_PUBLIC:
			KBEDebug.ERROR_MSG("player(%d) cannot get salary!as no in public(%d) space"%self.id, self.occupySpaceDF)
			return
		
		level = self.getLHMJBuildLevel(csdefine.LHMJ_BUIILD_LING_QUAN)
		_time = g_ToolCompose.getSalaryInterval(level)
		if self.salaryInterval and self.salaryInterval < time.time() + _time:
			self.statusMessage(csstatus.CANNOT_GETSALARY_AS_CD_TIME)
			return
		self.salaryInterval = time.time()
		psionic = g_ToolCompose.getSalary(level)
		self.addPsionic(psionic)
		
	def addPsionic( self, psionic):
		"""添加灵能"""
		if psionic:
			self.psionic += psionic
			self.statusMessage(csstatus.PLAYER_GET_LING_NENG, psionic)
		
	def hasEmoughPsionic( self, psionic):
		"""是否有足够灵能"""
		return self.psionic >= psionic
		
	def subPsionic( self, psionic):
		"""减少灵能"""
		if psionic:
			self.psionic -= psionic
			self.statusMessage(csstatus.PLAYER_COST_LING_NENG, psionic)

	def onEnterHSBZModelTPS( self, srcEntityID ):
		"""
		exposed method
		玩家点击进入射击模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.useSkillToEntity( self.shotSkillID, self.id )
		
	def onLeaveHSBZModelTPS( self, srcEntityID ):
		"""
		exposed method
		玩家离开射击模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.useSkillToEntity( self.interruptSkillID, self.id )
		
#----------------------------------轮回秘境建筑部分-----------------------------------------------------
	def getLHMJBuildLevel( self, dongFuType ):
		"""获取 建筑等级"""
		if self.occupySpaceDF == csdefine.SPACE_TYPE_PUBLIC:
			return self.dongFuBuilds[csdefine.LHMJ_BUIILD_LING_QUAN]
		return self.dongFuBuilds[dongFuType]

	def occupyLHMJSpace(self, spaceType, buildsDict = {}):
		"""占领了洞府/仙府"""
		self.occupySpaceDF = spaceType
		self.dongFuBuilds = buildsDict
		self.client.CLIENT_initLHMJBuild( spaceType, buildsDict )
		
	def addJadeItem( self, itemID, money, potential ):
		"""消耗金钱、潜能，获得玲珑玉令"""
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		freeOrderList = self.getAllFreeOrder(ItemTypeEnum.BAG_COMMON)
		if not freeOrderList:
			self.statusMessage( csstatus.NPCSHOP_BAG_ENOUGH )
			return
		self.inquireMessage(csstatus.COST_MONEY_POTENTIAL_GET_JADE , [money, potential], "replyAddJadeItem",money, potential, itemID)
		
	def replyAddJadeItem(self, reply,money, potential, itemID):
		"""玩家回应 回调"""
		if not reply:return
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		freeOrderList = self.getAllFreeOrder(ItemTypeEnum.BAG_COMMON)
		if not freeOrderList:
			self.statusMessage( csstatus.NPCSHOP_BAG_ENOUGH )
			return
		pyItems = {}
		pyItems[csdefine.TRADE_PAY_ITEM_MONEY] = money
		pyItems[csdefine.TRADE_PAY_ITEM_POTENTIAL] = potential
		self.requestPay(csdefine.TRADE_TYPE_GET_JADE, 0, pyItems, itemID)
		
	def onAddJadeItem(self, itemID):
		""""""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, 1)
		if itemInst is None:
			ERROR_MSG("add jade item err!!item(%d) is None"%itemID)
			return
		self.addItem( itemInst, csdefine.ITEM_ADD_BY_ADD_JADE )
	
	def getJadeItem( self ):
		"""获取玲珑玉令"""
		jadeList = self.getItemInstsByItemClass("ItemJadeCommand")
		if jadeList:
			return jadeList[0]
		return None
		
	def upgradeJadeItem( self ):
		"""玲珑玉令升级"""
		if not self.occupySpaceDF == csdefine.SPACE_TYPE_PUBLIC:		# 是否占有该地图
			KBEDebug.ERROR_MSG("player(%d) must occupySpaceDF public space!not spaceType(%d)"%(self.id, self.occupySpaceDF))
			return
		jadeItem = self.getJadeItem()
		if not jadeItem:
			KBEDebug.ERROR_MSG("Player(%d) cannot upgrade jade item!cannot get it!"%self.id)
			return
		jadeLevel = jadeItem.getJadeLevel()
		maxLevel = g_ToolCompose.getJadeMaxLevel()
		if jadeLevel >= maxLevel:
			self.statusMessage(csstatus.CANNOT_UPGRADE_JADE_MAX_LEVEL)
			return
			
		cost = g_ToolCompose.getJadeCfg( jadeLevel + 1 )
		self.inquireMessage(csstatus.JADE_UPGRADE_COST , [cost["money"], cost["potential"], jadeLevel + 1], "replyUpgradeJadeItem", jadeItem)
		
	def replyUpgradeJadeItem( self, reply, jadeItem ):
		"""回应玲珑玉令升级"""
		if not reply:return
		jadeLevel = jadeItem.getJadeLevel()
		cost = g_ToolCompose.getJadeCfg( jadeLevel + 1 )
		pyItems = {}
		pyItems[csdefine.TRADE_PAY_ITEM_MONEY] = cost["money"]
		pyItems[csdefine.TRADE_PAY_ITEM_POTENTIAL] = cost["potential"]
		self.requestPay(csdefine.TRADE_TYPE_JADE_UPGRADE, 0, pyItems, jadeItem)
		
	def onUpgradeJadeItem(self, jadeItem):
		"""玲珑玉令升级 回调"""
		jadeItem.unGradeJade(self)
		self.dongFuBuilds[csdefine.LHMJ_BUIILD_LING_QUAN] += 1
		self.client.CLIENT_onUpgradeJadeItem( self.dongFuBuilds[csdefine.LHMJ_BUIILD_LING_QUAN] )
		
	def setJadeIsValid(self, isValid):
		"""设置玲珑玉令有效性"""
		jadeItem = self.getJadeItem()
		if jadeItem:
			jadeItem.setValid( self, isValid )
			
	def requestLHMJShop( self, NPCID, shopID ):
		"""
		由NPC对话请求打开商店获得商店的列表
		"""
		self.ShopNPCID = NPCID
		self.shopID = shopID
		self.client.CLIENT_reflashLHMJShopTime( self.reflashLHMJShopNum )
		self.base.requestLHMJShop( NPCID, shopID )
		
	def CELL_requestBuyLHMJShopItem( self, srcEntityID, slot, itemID, amount ):
		"""
		<exposed method>
		请求购买物品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		# 验证与NPC的距离
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
			KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
			return
		item = g_tradeMgr.getShopItemConfig( self.shopID, slot )
		if not item:return
		if item["itemID"] != itemID:
			KBEDebug.ERROR_MSG("Buy NPC item err!slot(%s) item id is not same!(sell itemID:%d,buy itemID:%d)"%(slot,item["itemID"],itemID))
			return
			
		if not g_tradeMgr.checkCondition(self, self.shopID, slot, itemID):
			return
			
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount , {"uid":0})
		if itemInst is None:
			KBEDebug.ERROR_MSG("Buy item err!!item(%d) not find!"%itemID)
			return
		result = self.addItemCheck(itemInst)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(result)
			return
		payItems = dict( item["price"] )
		payItems[csdefine.TRADE_PAY_ITEM_LHMJ_SHOP] = {"slot":slot,"amount":amount}
		
		if csdefine.TRADE_PAY_ITEM_BIND_MONEY in payItems:			#如果支付方式为绑金，计算绑金是否足够支付。
			if not self.isEnoughBindMoney(payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY]):
				cost = payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY] - self.bindMoney
				payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY] = self.bindMoney
				payItems[csdefine.TRADE_PAY_ITEM_MONEY] = cost
				self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(cost)], "replacePayLHMJShop", csdefine.TRADE_TYPE_NPC_SHOP,self.ShopNPCID, payItems, self.shopID, slot, itemID, amount)
				return
		
		self.requestPay(csdefine.TRADE_TYPE_NPC_SHOP, self.ShopNPCID, payItems, self.shopID, slot, itemID, amount)
		
	def replacePayLHMJShop(self, reply,tradeType, targetID, payDict, *args):
		"""金币代付绑定金币"""
		if reply:
			self.requestPay(tradeType, targetID, payDict, *args)
		
	def onSuccessBuyLHMJShop(self, slot, itemID, amount):
		"""成功购买商品"""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount)
		self.addItem( itemInst,csdefine.ITEM_ADD_BY_NPCTRADE )
		self.client.CLIENT_OnSuccessBuyLHMJShopItem( slot, amount )
		
	def CELL_reflashLHMJShop( self, srcEntityID ):
		"""
		<exposed method>
		刷新商店
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		localtime_ = time.localtime()
		flashtime = time.localtime(self.reflashLHMJShopTime)
		if localtime_.tm_year != flashtime.tm_year or localtime_.tm_mon != flashtime.tm_mon or localtime_.tm_mday != flashtime.tm_mday:
			self.reflashLHMJShopTime = time.time()
			self.reflashLHMJShopNum = 0
		
		if self.reflashLHMJShopNum >= max(LHMJShopCostDatas):
			KBEDebug.ERROR_MSG("Cannot reflash lhmj shop item!as reflash max!")
			return
		
		money = LHMJShopCostDatas[self.reflashLHMJShopNum + 1]
		self.inquireMessage(csstatus.COST_MONEY_REFLASH_LHMJ_SHOP, [money], "onReplyReflashLHMJShop" )
		
	def onReplyReflashLHMJShop(self, isReply):
		""""""
		if not isReply:return
		money = LHMJShopCostDatas[self.reflashLHMJShopNum + 1]
		if self.money < money:
			self.statusMessage(csstatus.STORE_NO_ENOUGHMONEY)
			return
		self.subMoney(money, csdefine.MONEY_SUB_REASON_REFLASH_LHMJ_SHOP)
		self.reflashLHMJShopNum += 1
		self.base.requestReflashLHMJShop()
#------------------------------------通天塔----------------------------------------------------
	def onAgainChallengeCurrentLayer( self, srcEntityID ):
		"""
		exposed method
		重新挑战当前层
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		KBEngine.globalData["SpaceTongTianDaMgr"].onEnterTongTianDa( self.base, self.layerNumber )

	def onContinueChallengeLayer( self, srcEntityID ):
		"""
		exposed method
		继续挑战
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		# 有一定的概率跳层挑战
		if self.layerNumber < self.getLevel():
			num = random.uniform( 0, 100 )
			if num < Const.TTD_JUMP_LAYER_PROBABILITY:
				self.layerNumber += 1
				if self.layerNumber > self.getLevel():
					self.layerNumber = self.getLevel()
		KBEngine.globalData["SpaceTongTianDaMgr"].onEnterTongTianDa( self.base, self.layerNumber )

#------------------------------------洞府----------------------------------------------------
	def getBuildProtectTime(self):
		"""
		获取洞府地基保护时间
		"""
		return Functions.getTime() if self.buildProtectTime < time.time() else Functions.getTime(self.buildProtectTime - time.time())

	def getBuildIndex( self ):
		"""洞府索引（对应建筑组数group）"""
		for index, pos in self.groundPosDict.items():
			return index
		return -1
		
	def getBuildPos( self ):
		"""
		"""
		if len(self.groundPosDict):
			return list(self.groundPosDict.values())[0]
		return self.position
		
	def _checkBuildProtectState( self ):
		"""检查洞府占领保护状态，可能过时了"""
		if self.buildProtectTime:
			if time.time() - self.buildProtectTime >= csconst.LHMJ_BUILD_OCCUPY_TIME:
				self.onProtectTimeOut()

	def onCliskExplore( self, srcEntityID ):
		"""
		exposed method
		点击探索按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		if self.hasDongFu():
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestOccupiedFoundation( self, int( spaceEntity.spaceKey ), self.getBuildIndex() )

	def updateGroundPosDict( self, index, position ):
		"""
		<define method>
		更新数据
		"""
		self.groundPosDict = {index: position}
		spaceEntity = self.getCurrentSpace()
		if spaceEntity: self.caveHouseLine = int( spaceEntity.spaceKey )

	def onCliskOccupyBuild( self, srcEntityID ):
		"""
		exposed method
		点击占领按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestOccupyBuild( self.base, int( spaceEntity.spaceKey ), self.getBuildIndex(), self.playerDBID, self.getName() )

	def onRequestOccupyBuild( self, NPCID ):
		"""
		<define method>
		占领回调
		"""
		npc = KBEngine.entities.get( NPCID )
		if npc is None: 
			KBEDebug.ERROR_MSG("Can not find npc(%d)"%NPCID)
			return
		npc.startOccupyTime( self )
		scriptIDs, nums, radius = g_BuildDepleteLoader.getBuildMonsterDatas( self.getBuildIndex() )
		self.buildProtectTime = csconst.LHMJ_BUILD_OCCUPY_TIME + time.time()
		self.acceptQuest( csconst.KILL_LINGFUXIAOYAO_QUESTID[npc.getScript().getDongFuType()] )
		self.removeItemsByItemID( csconst.LHMJ_LUN_PAN_ITEMID, 1, csdefine.ITEM_REMOVE_BY_SYS )
		scriptIDList = scriptIDs.split("|")
		numList = [int(i) for i in nums.split("|")]
		position = self.getBuildPos()
		for index, scriptID in enumerate( scriptIDList ):
			self.createBulidMonster( scriptID, numList[index], radius, position )
		
		self.client.OccupyBuildResult( 1 )
	
	def onProtectTimeOut( self ):
		"""
		define method
		保护时间已过
		"""
		self.groundPosDict = {}
		self.caveHouseLine = 0
		self.buildProtectTime = 0.0
		self.removeQuestType( csdefine.QUEST_TYPE_QIYUAN )
	
	def createBulidMonster( self, scriptID, num, radius, position ):
		"""
		创建灵府小妖
		"""
		def getRandPosInCircle( centerPos, radius, num ):
			"""
			在圆内获得随机点坐标
			"""
			posList = []
			while num:
				x = centerPos[2]+random.uniform(-1,1) * radius
				y = centerPos[0]+random.uniform(-1,1) * radius
				posList.append(Math.Vector3( y, centerPos[1], x ))
				num-=1
			return posList
			
		posList = []
		posList = getRandPosInCircle( position, radius, num )
		for tarPosition in posList:
			newEntity = self.createEntityByScriptID( scriptID, Math.Vector3(tarPosition), Math.Vector3(0.0, 0.0, 0.0), { "spawnPos":Math.Vector3( tarPosition ), "spawnDir":Math.Vector3(0.0, 0.0, 0.0)} )
			newEntity.setBootyOwner( self )

	def onCliskBuildCaveHouse( self, srcEntityID, enityID ):
		"""
		exposed method
		点击建造洞府
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.buildProtectTime <= time.time():				# 过了保护时间
			return
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_LING_NENG] = g_BuildDepleteLoader.getBuildDepletePsionicData( 1, csdefine.LHMJ_BUIILD_LING_QUAN )
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = g_BuildDepleteLoader.getBuildDepleteData( 1, csdefine.LHMJ_BUIILD_LING_QUAN )
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = g_BuildDepleteLoader.getBuildDepleteMoneyData( 1, csdefine.LHMJ_BUIILD_LING_QUAN )
		self.requestPay( csdefine.TRADE_TYPE_BUILD_LINGQUAN, 0, payItems, enityID )

	def onBuildDongFuCB( self, enityID ):
		"""
		支付成功开始建造
		"""
		npc = KBEngine.entities.get( enityID, None )
		if npc == None: return
		npc.onStartBuildDongFu()
		buildsDict = {}
		buildsDict[csdefine.LHMJ_BUIILD_LING_QUAN] = 1
		buildsDict[csdefine.LHMJ_BUIILD_GONG_FANG] = 1
		buildsDict[csdefine.LHMJ_BUIILD_QIAN_KU_DING] = 1
		buildsDict[csdefine.LHMJ_BUIILD_SHOU_LAN] = 1
		buildsDict[csdefine.LHMJ_BUIILD_LING_TIAN] = 1
		self.occupyLHMJSpace( npc.getScript().getDongFuType(), buildsDict )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].onBuildDongFuFinish( self.caveHouseLine, npc.group, self.playerDBID )			# 管理器直接记录已经完成建造（没有建造中的状态）
		self.lingQuanCurrHP = g_LingQuanProduceLoader.getLingQuanMaxHP( self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN ))
		self.gainLingNengTime = time.time()
		self.setJadeIsValid( False )
		self.triggerQuestEvent(QuestEventDefine.EVENT_BUILD_DONGFU, None)

	def onCliskEnterCaveHouse( self, srcEntityID, enityID ):
		"""
		exposed method
		点击进入洞府
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( enityID, None )
		if npc == None: return
		self.goBackDongFu()
		
	def goBackDongFu( self, packArgs = {} ):
		"""回到自己的洞府"""
		if self.hasDongFu():
			scriptID = csconst.DONGFU_MAP_SPACESCRIPTID[self.occupySpaceDF]
			packArgs["lineNumber"] = self.caveHouseLine
			packArgs["group"] = self.getBuildIndex()
			packArgs["belongDBID"] = self.playerDBID
			self.gotoSpaceEnterPos( scriptID, packArgs )
		else:
			KBEDebug.ERROR_MSG("player(%d) has not dongfu(%d)"%(self.id, self.occupySpaceDF))
		
	def _calcelateTotalGainLingNeng( self ):
		"""计算可获得的总灵能"""
		LQLevel = self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN )
		sec = g_LingQuanProduceLoader.getLingQuanTimeKey( LQLevel )
		perPsionic = g_LingQuanProduceLoader.getOutLingQuanAmount( LQLevel )
		maxPsionic = g_LingQuanProduceLoader.getLingNengMaxAmount( LQLevel )
		return min(int((time.time() - self.gainLingNengTime) / sec ) * perPsionic + self.caveHousePsionic, maxPsionic)

	def requestLHMJLinqQuanUI( self, NPCID ):
		"""
		对话打开灵泉界面
		"""
		self.client.OpenLingQuanUI( self.activeChartID, self.lhmj_CoverHP, self._calcelateTotalGainLingNeng(),self.lingQuanCurrHP, self.destroyBuilds, NPCID )
		if self.guardReviveTime:
			self.client.OnGuardReviveTime( self.guardReviveTime )
		for buildType, endTime in self.repairBuildTime.items():
			self.client.OnBeginRepairDFBuild(buildType, endTime)
	
	def onReceiveLingNeng( self, srcEntityID ):
		"""
		exposed method
		领取灵能
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.addPsionic( self._calcelateTotalGainLingNeng() )
		self.caveHousePsionic = 0
		self.gainLingNengTime = time.time()
		
	def onDFBuildDestroy( self, buildType, itemDict ):
		"""
		define method
		洞府建筑被破坏了
		"""
		self.destroyBuilds[buildType] = itemDict
		if buildType in self.buildUpgradeTime:
			self.buildUpgradeTime.pop( buildType )
			
		npc = None
		if buildType == csdefine.LHMJ_BUIILD_QIAN_KU_DING and self.recordTripodNPCID:
			npc = KBEngine.entities.get( self.recordTripodNPCID )
		elif buildType == csdefine.LHMJ_BUIILD_GONG_FANG and self.recordToolNPCID:
			npc = KBEngine.entities.get( self.recordToolNPCID )
		if npc and npc.spaceID == self.spaceID:
			npc.onBuildDestroy( self )

	def repairDFBuild( self, srcEntityID, buildType ):
		"""
		exposed method
		修复建筑
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.repairBuildTime:
			self.statusMessage( csstatus.DF_BUILD_IS_REPAIRING, "" )
			return
		if self.buildUpgradeTime:
			self.statusMessage( csstatus.DF_BUILD_IS_REPAIRING, "" )
			return
		if buildType in self.destroyBuilds:
			payItems = {}
			payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = self.destroyBuilds[buildType]
			self.requestPay( csdefine.TRADE_TYPE_REPAIR_DF_BUILD, 0, payItems, buildType )
		else:
			KBEDebug.ERROR_MSG("Can not repair build!as build is not destroy!!")
			
	def beginRepairDFBuild( self, buildType ):
		"""开始修复建筑"""
		buildLevel = self.getLHMJBuildLevel( buildType )
		endTime = g_BuildDepleteLoader.getBuildRepairTime( buildType, buildLevel ) + int(time.time())
		self.repairBuildTime[buildType] = endTime
		self.client.OnBeginRepairDFBuild(buildType, endTime)
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].beginRepairDFBuild( self.playerDBID, buildType, endTime)
		
	def onRepairDFBuildFinish( self, buildType ):
		"""
		define method
		修复好建筑
		"""
		self.repairBuildTime.pop( buildType )
		self.destroyBuilds.pop( buildType )
		self.client.OnRepairDFBuildFinish( buildType )

	def gmSetDFRepairTime( self, second ):
		"""
		gm指令设置建筑修复时间
		"""
		if not self.repairBuildTime:
			KBEDebug.DEBUG_MSG("No building is repairing.")
			return
		
		#虽然现在同时只能修一个建筑，但以后可能允许同时修多个建筑，所以这里还是排一下序然后取剩余时间最少的建筑
		tempList = [(bType, endTime) for bType, endTime in self.repairBuildTime.items()]
		tempList.sort( key = lambda item:item[1] )
		buildType = tempList[0][0]
		endTime = int(time.time() + second)
		
		self.repairBuildTime[buildType] = endTime
		self.client.OnBeginRepairDFBuild(buildType, endTime)
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].GM_setBuildRepairTime( self.playerDBID, buildType, endTime )

	def onUpgradeBuild( self, srcEntityID, buildType ):
		"""
		exposed method
		建筑升级
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.buildUpgradeTime:
			self.statusMessage( csstatus.DF_BUILD_IS_REPAIRING, "" )
			return
		if self.repairBuildTime:
			self.statusMessage( csstatus.DF_BUILD_IS_REPAIRING, "" )
			return
		if buildType in self.destroyBuilds:
			self.statusMessage( csstatus.DF_BUILD_IS_DESTROY )
			return
			
		buildLevel = self.getLHMJBuildLevel( buildType ) + 1
		maxLevel = g_BuildDepleteLoader.getMaxBuildLevel()
		if buildLevel > maxLevel:
			KBEDebug.ERROR_MSG("Can not upgrade build again!level is max(%d)"%maxLevel)
			return

		if buildType == csdefine.LHMJ_BUIILD_LING_QUAN:
			LQLevel = self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN )
			if LQLevel != self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_GONG_FANG ) or LQLevel != self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_QIAN_KU_DING ) or\
			LQLevel != self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_SHOU_LAN ) or LQLevel != self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_TIAN ):
				self.statusMessage( csstatus.DONG_FU_OTHER_BUILD_LEVEL_LOW, "" )
				return
		else:
			if self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN ) <= self.getLHMJBuildLevel( buildType ):
				self.statusMessage( csstatus.DONG_FU_LINGQUAN_LEVEL_LOW, "" )
				return

		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = g_BuildDepleteLoader.getBuildDepleteData( buildLevel,buildType )
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = g_BuildDepleteLoader.getBuildDepleteMoneyData( buildLevel, buildType )
		payItems[csdefine.TRADE_PAY_ITEM_LING_NENG] = g_BuildDepleteLoader.getBuildDepletePsionicData( buildLevel, buildType )
		self.requestPay( csdefine.TRADE_TYPE_LINGQUAN_UPGRADE, 0, payItems, buildType )

	def onUpgradeBuildCB( self, buildType ):
		"""
		支付成功 开始升级建筑
		"""
		buildLevel = self.getLHMJBuildLevel( buildType ) + 1
		self.buildUpgradeTime[buildType] = int(time.time())
		self.client.StartBuildUpgrade( buildType, str( g_BuildDepleteLoader.getBuildUpgradeTime( buildType, buildLevel ) * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime() ))

	def onUpgradeBuildSuccess( self, srcEntityID, buildType ):
		"""
		exposed method
		建筑成功
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if buildType in self.destroyBuilds:				# 建筑被破坏了，不能升级
			return
		if buildType in self.buildUpgradeTime:
			buildLevel = self.getLHMJBuildLevel( buildType ) + 1
			if time.time() - self.buildUpgradeTime[buildType] >= g_BuildDepleteLoader.getBuildUpgradeTime( buildType, buildLevel ): 
				self.upgradeBuildSuccess( buildType )

	def upgradeBuildSuccess( self, buildType ):
		self.dongFuBuilds[buildType] += 1
		self.buildUpgradeTime = {}
		if self.hasDongFu():
			self.caveHousePsionic = self._calcelateTotalGainLingNeng()				# 因为升级后获取的灵能不同，所以先记录
			self.gainLingNengTime = time.time()
			self.lingQuanCurrHP = g_LingQuanProduceLoader.getLingQuanMaxHP( self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN ))
			self.client.CLIENT_OnLHMJBuildLevelChange(buildType, self.dongFuBuilds[buildType])
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].updateDongFuLevel(self.playerDBID, buildType, self.dongFuBuilds[buildType] )
			
			space = self.getCurrentSpace()
			if space and space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
				space.onPlayerUngradeBuild( self, buildType, self.dongFuBuilds[buildType])

	#---------------------------- 阵图功能 ------------------------------------------------------------			
	def onInitBFCallBack(self, remainPsionic, isActive):
		"""
		define method
		阵图初始化 回调
		"""
		self.psionic = remainPsionic
		if isActive:
			itemInst = self._getActiveChartItem()
			if self.hasEmoughPsionic( itemInst.getPerCosume() ):
				self.chartTimer = self.addTimerRepeat( csconst.LUN_HUI_MI_JING_SOUME_TIME, "onArriveOneMinute", () )
				return
		self.activeChartID = 0
	
	def openBattleFormations( self, srcEntityID, itemID ):
		"""
		exposed method
		开启 阵图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if KBEngine.globalData.get( "LHMJ_ChallengeActive") or KBEngine.globalData.get( "LHMJ_PlunderActive" ):
			self.statusMessage( csstatus.CAN_NOT_SET_BATTLE_CUR_STATE )
			return
		if self.activeChartID:
			KBEDebug.ERROR_MSG("player(%d) have activeChartID(%d) !!"%(self.id, self.activeChartID))
			return
		itemList = self.getItemInstsByID( itemID )
		if not itemList:
			KBEDebug.ERROR_MSG("player(%d) can not get item(%d)"%(self.id, itemID))
			return
		item = itemList[0]
		if item.__class__.__name__ != "ItemBattleFormations":
			KBEDebug.ERROR_MSG("item(%d) item script must be ItemBattleFormations!")
			return
		result = item.checkUse( self )
		if result != csstatus.ITEM_USE_GO_ON_MSG:
			self.statusMessage(result)
			return
		
		pyItems = {}
		pyItems[csdefine.TRADE_PAY_ITEM_LING_NENG] = item.getActiveCosume()
		pyItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = { itemID : 1 }
		self.requestPay( csdefine.TRADE_TYPE_OPEN_BATTLE_FORMATIONS, 0, pyItems, itemID )
		
	def _getActiveChartItem( self ):
		"""获取 激活的阵图 物品"""
		if self.activeChartID:
			return ItemFactory.ItemFactoryInst.createDynamicItem(self.activeChartID, 1, {"uid" : 0})
		return None
		
	def activeBatteleFormations( self, itemID ):
		"""激活 阵图"""
		self.activeChartID = itemID
		itemInst = self._getActiveChartItem()
		space = self.getCurrentSpace()
		if space and space.__class__.__name__ == "SpaceCopyDongFu":
			space.createBattleformation(itemInst.insScriptID, itemInst.insPos, itemInst.insDir )
			
		self.chartTimer = self.addTimerRepeat( csconst.LUN_HUI_MI_JING_SOUME_TIME, "onArriveOneMinute", () )
		self.client.CLIENT_OnActiveBatteleFormations( itemID, itemInst.outObjectHP )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].activeBatteleFormations(  self.playerDBID, itemID, itemInst.outScriptID )
		
	def closeBattleFormations( self, srcEntityID ):
		"""
		exposed method
		关闭 阵图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.chartTimer:
			self.popTimer( self.chartTimer )
			self.chartTimer = 0
			
		space = self.getCurrentSpace()
		if space and space.__class__.__name__ == "SpaceCopyDongFu":
			space.destroyBattleformation()
			
		if self.activeChartID:
			self.activeChartID = 0
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].closeBattleFormations( self.playerDBID )
		
	def onArriveOneMinute( self ):
		"""一分钟 消耗一次"""
		item = self._getActiveChartItem()
		if item and self.hasEmoughPsionic( item.getPerCosume() ):
			self.psionic -= item.getPerCosume() 
			
			if self.hasEmoughPsionic( item.getPerCosume() ):			# 如果下次还够消耗
				return
		# 消耗不足
		self.statusMessage( csstatus.HAS_NOT_ENOUGHT_LING_NENG_CLOSE_BATTLE )
		self.client.CLIENT_OnCloseBatteleFormations()
		self.closeBattleFormations( self.id )
		
		
	def updateLHMJCoverHP( self, HP ):
		"""
		define method
		更新防护罩的血量
		"""
		self.lhmj_CoverHP = HP
		
	def onGuardReviveTime( self, reviveTime ):
		"""
		define method
		守卫复活时间
		"""
		self.guardReviveTime = reviveTime
		if reviveTime == 0:
			space = self.getCurrentSpace()
			if space and space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU and space.belongDBID == self.playerDBID:
				space.onGuardRevive()

	