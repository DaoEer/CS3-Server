# -*- coding: utf-8 -*-

import csdefine
import csstatus
import KBEngine
import KBEDebug
import csconst
import Const
import ItemFactory
import cschannel_msgs
import LogDefine
from MsgLogger import g_logger
from ObjectScript.ObjectScriptFactory import g_objFactory
from LunHuiMiJin.DFGuard import Datas as DFGuardDatas
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr


class RoleLHMJActiveInterface:
	"""
	玩家轮回秘境 活动 接口
	"""
	def __init__( self ):
		pass
		
	def requestLHMJChallenge( self, srcEntityID, lineNumber, group ):
		"""
		exposed method
		对洞府发起挑战
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if KBEngine.globalData.get("LHMJ_ChallengeActiveReady") or KBEngine.globalData.get("LHMJ_PlunderActiveReady"):
			if self.occupySpaceDF == csdefine.SPACE_TYPE_NONE:
				self.statusMessage( csstatus.NO_DONG_FU_OR_JADE )
				return
			if self.challengeDBID:
				self.statusMessage( csstatus.CHALLENGE_HAS_INVITE )
				return
				
			lqLevel = self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestLHMJChallenge( self.base, self.getName(), self.playerDBID, self.accountDBID, self.getLevel(), lqLevel, lineNumber, group )
		
	def initClientData( self ):
		""""""
		pass
				
	def onRequestLHMJChallenge( self, playerDBID ):
		"""
		define method
		发起挑战回调
		"""
		self.challengeDBID = playerDBID
		
	def replayLHMJChallenge( self, srcEntityID, replay ):
		"""
		exposed method
		回应洞府挑战
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].replayLHMJChallenge( self.playerDBID, self.accountDBID, self.getLevel(), replay)
		
	def onRequestLHMJChallengeReplyNo( self ):
		"""
		define method
		被拒绝挑战
		"""
		self.challengeDBID = 0
		
	def onRequestLHMJChallengeReplyYes( self, lineNumber ):
		"""
		define method
		同意挑战
		"""
		self.challengeLineNumber = lineNumber
		
	def autoGoToChallengeSpaceDongFu( self, srcEntityID ):
		"""
		exposed method
		自动传送到挑战洞府 所在轮回秘境的线路
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.challengeLineNumber:
			self.setTemp("lineNumber",self.challengeLineNumber)
			self.gotoSpace(csconst.LUN_HUI_MI_JIN_SCRIPTID, Const.LHMJ_ENTER_POS, (0.0,0.0,0.0) )
			self.removeTemp("lineNumber")
		
	def autoGoToLHMJSpace( self, srcEntityID ):
		"""
		exposed method
		自动传送到轮回秘境的线路，并自动移动到洞府建筑处
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.hasDongFu():
			KBEDebug.ERROR_MSG("player has not dongfu!!")
			return
		self.setTemp("lineNumber",self.caveHouseLine)
		self.gotoSpace(csconst.LUN_HUI_MI_JIN_SCRIPTID, Const.LHMJ_ENTER_POS, (0.0,0.0,0.0) )
		self.removeTemp("lineNumber")
		
	def onCliskEnterChallengeCaveHouse( self, srcEntityID, enityID ):
		"""
		exposed method
		点击进入挑战洞府
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( enityID, None )
		if npc == None: return
		packArgs = {}
		packArgs["lineNumber"] = self.challengeLineNumber
		packArgs["group"] = npc.group
		packArgs["belongDBID"] = self.challengeDBID
		self.gotoSpaceEnterPos( npc.getScript().spaceScriptID, packArgs )

	def onOccupyPlayerDF( self, srcEntityID, isOccupy ):
		"""
		exposed method
		占领其他玩家的洞府
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		space = self.getCurrentSpace()
		if space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			if not isOccupy:						# 不占领
				space.onOccupyPlayerDFCallBack()
				return
			
			if space.isCapture:
				KBEngine.globalData["SpaceLunHuiMiJinMgr"].onOccupyPlayerDF(self.base, self.getName(), self.playerDBID, space.belongDBID)
				
	def onOccupyPlayerDFCallBack( self ):
		"""
		define method
		占领回调
		"""
		self.setJadeIsValid( 0 )				# 玲珑玉令无效
		space = self.getCurrentSpace()
		if space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			space.onOccupyPlayerDFCallBack()
			
		if self.activeChartID:			# 清除阵图数据
			self.activeChartID = 0
			self.popTimer( self.chartTimer )
			self.chartTimer = 0
			self.client.CLIENT_OnCloseBatteleFormations()
		
	def upgradeDFGuard( self, srcEntityID, monsterID, mType ):
		"""
		exposed method
		升级洞府 守卫
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		space = self.getCurrentSpace()
		if space.getScript().getSpaceType() != csdefine.SPACE_TYPE_DONG_FU:			# 不在洞府，就升级不了洞府守卫
			return
		monster = KBEngine.entities.get( monsterID )
		if not monster:
			return
		level = self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN )
		if not level in DFGuardDatas:
			KBEDebug.ERROR_MSG("LunHuiMiJin/DFGuard.py cannot find level(%d)"%level)
			return
		if not mType in Const.DONG_FU_GUARD_TYPE:
			KBEDebug.ERROR_MSG("type(%d) err! must be in Const.DONG_FU_GUARD_TYPE"%mType)
			return
		data = DFGuardDatas[level]
		oldType = None
		scriptID = monster.scriptID
		for type, strKey in Const.DONG_FU_GUARD_TYPE.items():
			if data[strKey] == scriptID:
				oldType = type
				break
		if oldType is None:
			KBEDebug.ERROR_MSG("cannot find monster(%s) type in config!"%scriptID)
			return
		psionic = data["psychic"]
		if not self.hasEmoughPsionic( psionic ):
			self.statusMessage( csstatus.BUILD_NEED_PSIONIC_NOT_ENOUGH_LN )
			return
		
		self.subPsionic( psionic )
		pos = monster.position
		dir = monster.direction
		monster.destroySelf()
		param = {}
		param["belongDBID"] = self.playerDBID
		param["spawnPos"] = pos
		param["spawnDir"] = dir
		self.createEntityByScriptID( data[Const.DONG_FU_GUARD_TYPE[mType]], pos, dir, param )
		space.changeGuardType( oldType, mType, monsterID, scriptID)
		
	def doActiveReward( self, isChallengeActive, result, rewardIDs, destroyBuilds, startTime, activeTime, deadNum ):
		"""
		define method
		执行活动奖励
		"""
		action = LogDefine.ACTIVE_SPACE_TYPE_DFLDZ
		actResult = LogDefine.ACTIVE_STATE_TYPE_SUCCESS
		if isChallengeActive:
			action = LogDefine.ACTIVE_SPACE_TYPE_DFZDZ
			
		if result not in [1,3, 4]:
			actResult = LogDefine.ACTIVE_STATE_TYPE_FAIL
			
		self.onDFActiveEnd()
		rewardStr = ""
		money = 0
		lingNeng = 0
		rewardItem = {}
		for rewardID in rewardIDs:
			rewardDatas = RewardMgr.g_rewardMgr.getReward( str(rewardID), {"player":self} )
			failAddItem = RewardMgr.g_rewardMgr.doRewards( rewardDatas, self.id, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT )
			for data in rewardDatas:
				rewardType = ""
				if data["type"] == csdefine.REWARD_TYPE_ITEM:
					rewardType = LogDefine.ACTIVE_REWARD_TYPE_ITEM
					if not data["goodsid"] in rewardItem:
						rewardItem[data["goodsid"]] = 0
					rewardItem[data["goodsid"]] += data["amount"]
				elif data["type"] == csdefine.REWARD_TYPE_MONEY:
					rewardType = LogDefine.ACTIVE_REWARD_TYPE_MONEY
					money += data["amount"]
				elif data["type"] == csdefine.REWARD_TYPE_PSIONIC:
					rewardType = LogDefine.ACTIVE_REWARD_TYPE_PSIONIC
					lingNeng += data["amount"]
				if rewardType != LogDefine.ACTIVE_REWARD_TYPE_ITEM:
					g_logger.roleActiveRecord(action, self.accountDBID, self.playerDBID, self.getLevel(), rewardType, data["amount"], startTime, activeTime, actResult)
			for itemID, amount in rewardItem.items():
				if rewardStr:
					rewardStr += "|"
				rewardStr += str(itemID) + ":"  + str(amount)
				g_logger.roleActiveRecord(action, self.accountDBID, self.playerDBID, self.getLevel(), LogDefine.ACTIVE_REWARD_TYPE_ITEM, itemID, startTime, activeTime, actResult)
			if failAddItem:
				if isChallengeActive:
					titleKey = cschannel_msgs.DF_ACTIVE_CHALLENGE_TITLE
				else:
					titleKey = cschannel_msgs.DF_ACTIVE_PLUNDER_TITLE
				self.sendRemainItemWithMail( failAddItem, csdefine.REMAIN_ITEM_ACTIVITY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT, titleKey )
		self.client.OnShowDFActtiveResult(isChallengeActive, result, rewardStr, money, lingNeng, destroyBuilds, activeTime, deadNum )
		
	def updateDFActiveStage( self, stageIndex, isChallengeActive, belongSide, endTime ):
		"""
		define method
		更新活动阶段
		"""
		spaceObj = g_objFactory.getSpaceObject( csconst.DONGFU_MAP_SPACESCRIPTID[csdefine.SPACE_TYPE_PRIVATE] )
		if spaceObj:
			spaceObj.showPlayerDFActiveStage( self, stageIndex, isChallengeActive, belongSide, endTime )
		
	def onDFActiveEnd( self ):
		"""
		define method
		洞府活动结束
		"""
		self.challengeDBID = 0
		self.challengeLineNumber = 0
		self.client.onDFActiveEnd()
		
	def onDFBeingOccupy( self, dfLevel ):
		"""
		define method
		洞府被占领（且对方没洞府）
		"""
		self.onInitDongFuErr()
		item = self.getJadeItem()
		if item:
			item.setJadeLevel( self, dfLevel )
		else:
			item = ItemFactory.ItemFactoryInst.createDynamicItem( Const.LHMJ_JADE_ITEM_ID, 1, {} )
			item.setJadeLevel( None, dfLevel )
			self.sendRemainItemWithMail([item], 6, csdefine.ITEM_ADD_BY_ADD_JADE)
		self.client.OnDFBeingOccupy()
		
		if self.activeChartID:			# 清除阵图数据
			self.activeChartID = 0
			self.popTimer( self.chartTimer )
			self.chartTimer = 0
			self.client.CLIENT_OnCloseBatteleFormations()
