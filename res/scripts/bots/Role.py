# -*- coding: utf-8 -*-
import KBEngine
import KST
import KBEDebug
import time, sys, math, copy, random, Math
import Functions
import botdefine
import KST_Config
from Functions import Functor
from Interface.GameObject import GameObject
from Interface.StatusMessageInterface import StatusMessageInterface
from Interface.RoleCombatInterface import RoleCombatInterface
from Interface.RoleChatInterface import RoleChatInterface
from Interface.RoleBuyNPCShopInterface import RoleBuyNPCShopInterface
from Interface.RoleEquipInterface import RoleEquipInterface
from Interface.RoleKitBagInterface import RoleKitBagInterface
from Interface.RoleQuestInterface import RoleQuestInterface
from Interface.RoleRelationInterface import RoleRelationInterface
from Interface.EntitySpaceEventInterface import EntitySpaceEventInterface
from Interface.RoleSpaceInterface import RoleSpaceInterface
from Interface.RoleSpaceStageInterface import RoleSpaceStageInterface
from Interface.RoleTalkInterface import RoleTalkInterface
from Interface.RoleTeamInterface import RoleTeamInterface
from Interface.RoleTradeInterface import RoleTradeInterface
from Interface.TestInterface import TestInterface
from Interface.RoleStallInterface import RoleStallInterface
from Interface.RoleMemoirInterface import RoleMemoirInterface
from Interface.RoleShopMallInterface import RoleShopMallInterface
from Interface.RolePerformanceInterface import RolePerformanceInterface
from Interface.RoleFacadeBagInterface import RoleFacadeBagInterface
from Interface.RoleCrondInterface import RoleCrondInterface
from Interface.RoleReviveInterface import RoleReviveInterface
from Interface.QuickBarInterface import QuickBarInterface
from Interface.RoleLingShiTradeInterface import RoleLingShiTradeInterface
from Interface.BotBehaviourInterface import BotBehaviourInterface
from Interface.RolePetInterface import RolePetInterface
from Interface.RoleTitleInterface import RoleTitleInterface
from Interface.RoleSpaceSettlementInterface import RoleSpaceSettlementInterface
from Interface.RoleAmbulantInterface import RoleAmbulantInterface
from Interface.RoleTeleportInterface import RoleTeleportInterface
from Interface.RoleAutoFightInterface import RoleAutoFightInterface
from Interface.RoleTongInterface import RoleTongInterface
from Interface.RoleDropBoxInterface import RoleDropBoxInterface
from Interface.RoleSpaceStrategyInterface import RoleSpaceStrategyInterface
from Interface.RoleSpaceContentInterface import RoleSpaceContentInterface
from Interface.RoleMailInterface import RoleMailInterface
from Interface.RoleActivityInterface import RoleActivityInterface
from Interface.RoleQTEInterface import RoleQTEInterface
from Interface.RoleGiftInterface import RoleGiftInterface
from Interface.RoleCompeteInterface import RoleCompeteInterface
from Interface.RoleRankInterface import RoleRankInterface
from Interface.RoleCampInterface import RoleCampInterface
from Interface.RolePointCardInterface import RolePointCardInterface
from Interface.RoleModelInterface import RoleModelInterface
from Interface.RoleShenTongInterface import RoleShenTongInterface
from Interface.RoleStoreInterface import RoleStoreInterface
from Interface.RoleSpellBoxDropItemInterface import RoleSpellBoxDropItemInterface
from Interface.RoleCommanderInterface import RoleCommanderInterface
from Interface.RoleBarracksInterface import RoleBarracksInterface
from Interface.RoleLunHuiMiJinInterface import RoleLunHuiMiJinInterface
from Interface.RoleMilitaryRankInterface import RoleMilitaryRankInterface
from Interface.RoleWorkShopInterface import RoleWorkShopInterface
from Interface.GMTestInterface import GMTestInterface
from Interface.RoleCrossServiceInterface import RoleCrossServiceInterface
from Interface.RoleTrainSoldierGroundInterface import RoleTrainSoldierGroundInterface
from Interface.RoleStoryInterface import RoleStoryInterface
from Interface.RoleLBCTaskInterface import RoleLBCTaskInterface
from Interface.RoleGameTimeInterface import RoleGameTimeInterface
from Interface.RoleLbcInterface import RoleLbcInterface
from Interface.RoleChuanChengInterface import RoleChuanChengInterface
#------Role------
class Role(
	RoleChuanChengInterface,
	RoleLbcInterface,
	RoleGameTimeInterface,
	RoleLBCTaskInterface,
	RoleStoryInterface,
	RoleTrainSoldierGroundInterface,
	RoleCrossServiceInterface,
	GMTestInterface,
	RoleWorkShopInterface,
	RoleMilitaryRankInterface,
	RoleLunHuiMiJinInterface,
	RoleBarracksInterface,
	RoleCommanderInterface,
	RoleSpellBoxDropItemInterface,
	RoleStoreInterface,
	RoleShenTongInterface,
	RoleModelInterface,
	RolePointCardInterface,
	RoleCampInterface,
	RoleRankInterface,
	RoleCompeteInterface,
	RoleGiftInterface,
	RoleQTEInterface,
	RoleActivityInterface,
	RoleMailInterface,
	RoleSpaceContentInterface,
	RoleSpaceStrategyInterface,
	RoleDropBoxInterface,
	KBEngine.Entity,
	GameObject,
	StatusMessageInterface,
	RoleCombatInterface,
	RoleChatInterface,
	RoleBuyNPCShopInterface,
	RoleEquipInterface,
	RoleKitBagInterface,
	RoleQuestInterface,
	RoleRelationInterface,
	RoleSpaceInterface,
	RoleSpaceStageInterface,
	EntitySpaceEventInterface,
	RoleTalkInterface,
	RoleTeamInterface,
	RoleTradeInterface,
	TestInterface,
	RoleStallInterface,
	RoleMemoirInterface,
	RoleShopMallInterface,
	RolePerformanceInterface,
	RoleFacadeBagInterface,
	RoleCrondInterface,
	RoleReviveInterface,
	QuickBarInterface,
	RoleLingShiTradeInterface,
	BotBehaviourInterface, 
	RolePetInterface,
	RoleTitleInterface,
	RoleSpaceSettlementInterface,
	RoleAmbulantInterface,
	RoleTeleportInterface,
	RoleAutoFightInterface,
	RoleTongInterface,
	):
	
	def __init__(self):
		RoleChuanChengInterface.__init__(self)
		RoleLbcInterface.__init__(self)
		RoleGameTimeInterface.__init__(self)
		RoleLBCTaskInterface.__init__(self)
		RoleStoryInterface.__init__(self)
		RoleTrainSoldierGroundInterface.__init__(self)
		RoleCrossServiceInterface.__init__(self)
		GMTestInterface.__init__(self)
		RoleWorkShopInterface.__init__(self)
		RoleMilitaryRankInterface.__init__(self)
		RoleLunHuiMiJinInterface.__init__(self)
		RoleBarracksInterface.__init__(self)
		RoleCommanderInterface.__init__(self)
		RoleSpellBoxDropItemInterface.__init__(self)
		RoleStoreInterface.__init__(self)
		RoleShenTongInterface.__init__(self)
		RoleModelInterface.__init__(self)
		RolePointCardInterface.__init__(self)
		RoleCampInterface.__init__(self)
		RoleRankInterface.__init__(self)
		RoleCompeteInterface.__init__(self)
		RoleGiftInterface.__init__(self)
		RoleQTEInterface.__init__(self)
		RoleActivityInterface.__init__(self)
		RoleMailInterface.__init__(self)
		RoleSpaceContentInterface.__init__(self)
		RoleSpaceStrategyInterface.__init__(self)
		RoleDropBoxInterface.__init__(self)
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		StatusMessageInterface.__init__(self)
		RoleCombatInterface.__init__(self)
		RoleChatInterface.__init__(self)
		RoleEquipInterface.__init__(self)
		RoleBuyNPCShopInterface.__init__(self)
		RoleKitBagInterface.__init__(self)
		RoleQuestInterface.__init__(self)
		RoleRelationInterface.__init__(self)
		EntitySpaceEventInterface.__init__(self)
		RoleSpaceInterface.__init__(self)
		RoleSpaceStageInterface.__init__(self)
		RoleTalkInterface.__init__(self)
		RoleTeamInterface.__init__(self)
		RoleTradeInterface.__init__(self)
		TestInterface.__init__(self)
		RoleStallInterface.__init__(self)
		RoleMemoirInterface.__init__(self)
		RoleShopMallInterface.__init__(self)
		RolePerformanceInterface.__init__(self)
		RoleFacadeBagInterface.__init__(self)
		RoleCrondInterface.__init__(self)
		RoleReviveInterface.__init__(self)
		QuickBarInterface.__init__(self)
		RoleLingShiTradeInterface.__init__(self)
		BotBehaviourInterface.__init__(self)
		RolePetInterface.__init__(self)
		RoleTitleInterface.__init__(self)
		RoleSpaceSettlementInterface.__init__(self)
		RoleAmbulantInterface.__init__(self)
		RoleTeleportInterface.__init__(self)
		RoleAutoFightInterface.__init__(self)
		RoleTongInterface.__init__(self)
		
	def set_money(self, old):
		"""
		"""
		if hasattr(self, "eventObj"):
			self.eventObj.fireEvent("Event_OnMoneyChanged", self.money)
		
	def getFinalCamp( self ):
		"""
		获取最终阵营：有临时阵营则返回临时阵营，否则返回原阵营
		"""
		if self.tempCamp:
			return self.tempCamp
		return self.camp
	
	def outputMsg( self, msg ):
		"""
		机器人输出信息
		"""
		if self.id in KST.roles:
			curSpace = self.getCurSpace()
			curTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			KST.roles[self.id][1] = "{} [{}]".format(curTime, curSpace)
			KST.roles[self.id][2] = int(time.time())
		KBEDebug.DEBUG_BOT_MSG("Role[%s:%s] ==> %s"%( self.playerName, self.id, msg ))
		
	def getCurSpace(self):
		return ""
		
	def StartPlayStory(self, p1, p2):
		print(p1)
	
	def StopStory(self):
		pass
		
	def PlayRandomAction(self,param):
		pass
	
	def ReTriggerNearTrap(self, range ):
		pass
		
	def OnMountTalisman( self,delayTime, modelid, InputYawScale ):
		pass
	
	def OnDismountTalisman( self):
		pass
		
	def AutoMoveByTalisman(self):
		pass
		
	def PlayOneByOneAction(self,arg0_array,arg1_array):
		pass
	
	def OnSetBlendDir(self, int1):
		pass
		
	def OnPlayerCameraRotation(self, f1):
		pass
#------PlayerRole------
	def SkillInterrupted(self,arg0_int32,arg1_int32,arg2_int32):
		pass
	def OnBeHitBackNew(self,arg0_float,arg1_float,arg2_float,arg3_float,arg4_string,arg5_float,arg6_int32):
		pass
	def inquireMessage(self,arg0_int32,arg1_unicode,arg2_int32,arg3_string):
		pass
	def EndPull(self,arg0_int32,arg1_string):
		pass
	def AddToItemUseAmountArray(self,arg0_int32,arg1_int32,arg2_string):
		pass
	def OnReceiveJoinTeamRequest(self,arg0_int32,arg1_unicode,arg2_int32,arg3_int32,arg4_int32):
		pass
	def DistortScene(self,arg0_float,arg1_string,arg2_float,arg3_float,arg4_float,arg5_string):
		pass
	def OnPull(self,arg0_float,arg1_float,arg2_float,arg3_float,arg4_string,arg5_float,arg6_int32):
		pass
	def teammateInfoNotify(self,arg0_int32,arg1_int32,arg2_int32,arg3_int32,arg4_int32,arg5_int32,arg6_string):
		pass
	def relation_addBlacklistRelation(self,arg0_unicode,arg1_unicode,arg2_unicode,arg3_int32,arg4_int32,arg5_int32,arg6_int32,arg7_int32):
		pass
	def OnRiseEnd(self,arg0_int32):
		pass
	def relation_addFoeRelation(self,arg0_unicode,arg1_unicode,arg2_unicode,arg3_int32,arg4_int32,arg5_int32,arg6_int32,arg7_int32):
		pass
	def intonateSpell(self,arg0_float, arg1_string):
		pass
	def relation_sendRelationData(self,arg0_unicode,arg1_unicode,arg2_unicode,arg3_unicode,arg4_int32,arg5_int32,arg6_int32,arg7_int32,arg8_int32):
		pass
	def onXinMoCtrlStart(self,arg0_array,arg1_array):
		pass
	def OnEndHitBack(self,arg0_int32,arg1_string,arg2_string):
		pass
	def OnMountHeHua(self,arg0_int32):
		pass
	def ShowSpaceSettlementWin(self,arg0_int32,arg1_int32,arg2_array,arg3_array):
		pass
	def OnPlayParticles(self,arg0_int32,arg1_string,arg2_string,arg3_float,arg4_vector3):
		pass
	def DismountHeHua(self):
		pass
	def HoldEffectPlayEffect(self,arg0_int32,arg1_int32,arg2_int32,arg3_array,arg4_string,arg5_string,arg6_array):
		pass
	def ClearCooldown(self,arg0_uint8):
		pass
	def relation_addFriendRelation(self,arg0_unicode,arg1_unicode,arg2_unicode,arg3_int32,arg4_int32,arg5_int32,arg6_int32,arg7_int32):
		pass
	def addHighBuyBackItem(self,arg0_string):
		pass
	def PlayJumpAction(self,arg0_int32,arg1_array,arg2_float,arg3_array):
		pass
	def OnRiseBegin(self,arg0_int32,arg1_array,arg2_array,arg3_float,arg4_float):
		pass
	def testTList(self,arg0_int32,arg1_array):
		pass
	def ZhenLongQiJu_OnBossStateChange(self,arg0_int32,arg1_int32,arg2_string):
		pass
	def OnPetReNameFail(self,arg0_string,arg1_int32):
		pass
	def UpdateItemUseAmount(self,arg0_int32,arg1_int32,arg2_string):
		pass
	def relation_receiverGroup(self,arg0_unicode,arg1_unicode,arg2_float,arg3_unicode,arg4_unicode,arg5_int32,arg6_array):
		pass
	def UpdateMoneyDataToOtherPlayer(self,arg0_int32,arg1_int32,arg2_unicode,arg3_int32,arg4_int32,arg5_int32):
		pass
	def OnPlayAction(self,arg0_string,arg1_float):
		pass
	def SetIntegralMax(self,arg0_int32):
		pass
	def HoldEffectEndEffect(self,arg0_int32,arg1_int32):
		pass
	def RoleCameraMoveToEntityCB(self):
		pass
	def ZhenLongQiJu_StopBossStateChange(self):
		pass
	def relation_receiverGroupInfo(self,arg0_unicode,arg1_unicode,arg2_int32,arg3_int32,arg4_int32,arg5_uint8):
		pass
	def OnChasePlayer(self,arg0_float):
		pass
	def ReceiveOtherMoneyData(self,arg0_int32,arg1_int32,arg2_unicode,arg3_int32,arg4_int32,arg5_int32):
		pass
	def testGList(self,arg0_int32,arg1_array):
		pass
	def testRList(self,arg0_string,arg1_array):
		pass
	def RoleCameraMoveToEntity(self,arg0_int32,arg1_string,arg2_float):
		pass
	def RoleTeamSpellBoxFollow(self,arg0_int32,arg1_float):
		pass
	def OnStartRoleAutoMove( self, p1 ):
		pass
	def ChangePosture( self, p1, p2, p3 ):
		pass
	def OnSetClientTime( self, p1, p2 ):
		pass
	def OnDisRoleAutoMove( self ):
		pass
	def OnUpdateMoveType( self, p1 ):
		pass
	def OnPlayVideo( self, p1 ):
		pass
	def OnSetJumpData( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_BreakFalling( self ):
		pass
	def CLIENT_StartConstantFall( self ):
		pass
	def CLIENT_EndConstantFall( self ):
		pass
	def FirstEnterGameNotify( self ):
		pass
	def OnNetworkTest( self ):
		pass
	def OnSetPlayerAddGravityScale( self, p1, p2 ):
		pass
	def OnDodgeRotation( self ):
		pass
	def CLIENT_StartParachuteLand( self ):
		pass
	def CLIENT_EndParachuteLand( self ):
		pass
	def OnRoleReEnterWorld( self ):
		pass
	def CLIENT_OnSetAimOffsetBlend( self, p1, p2 ):
		pass
	def CLIENT_OnRepShootState( self, p1 ):
		pass
	def SetWeapontYCJMD( self, p1 ):
		pass
	def CLIENT_OnRepYCJMDCopyState( self, p1 ):
		pass
	def CLIENT_OnRepYCJMDAimOffsetState( self, p1 ):
		pass
		
class PlayerRole(Role ):
	def __init__(self):
		Role.__init__(self)
		
	def onBecomePlayer( self ):
		"""
		KBEngine method.
		当这个entity被引擎定义为角色时被调用
		"""
		self.ai = None
		self.isFirst = True
		self.callbackID = 0
		KST.roles[self.id] = [self, "", int(time.time())]
		self.outputMsg("Login Roles:%d" %(len(KST.roles)))
		self.attachDefaultAI()
		
	def startAction( self, key, param ):
		"""
		"""
		from PlayerAI.Action.ActionBase import ActionBase
		action = ActionBase.getClassObj(key)
		if action is None:
			KBEDebug.ERROR_MSG("not found action[%s]" %(key))
			return
		
		action.doAction(self, param)
		
	def attachDefaultAI( self ):
		"""
		"""
		per = random.randint(1, 100)
		ainame = ""
		for k, v in KST_Config.aiPer.items():
			if per <= v:
				ainame = k
				break
			else:
				per = per - v
				
		if ainame == "":
			KBEDebug.ERROR_MSG("player check ai error")
			return
		
		from PlayerAI.Base.AIBase import AIBase
		self.ai = AIBase.getClassObj(ainame)
		if self.ai is None:
			KBEDebug.ERROR_MSG("not found ai[%s]" %(ainame))
			return
	
		self.ai.attache( self )
	
	def onEnterWorld( self ):
		"""
		"""
		self.outputMsg("enter world")
		self.ai and self.ai.onEnterWorld()
		
	def onLeaveWorld( self ):
		"""
		"""
		self.outputMsg("leave world")
		self.ai and self.ai.onLeaveWorld()
		
	def onEnterSpace( self ):
		"""
		"""
		self.outputMsg("enter space")
		#通知服务器客户端加载完毕
		self.cell.CELL_onClientReady()
		self.cell.loadSpaceCompleted(self.isFirst)
		self.isFirst = False
		self.ai and self.ai.onEnterSpace()
		self.outputMsg("CELL_onClientReady and loadSpaceCompleted")
		
		KBEngine.callback(2, self.onSetSpaceData)
		
	def onLeaveSpace( self ):
		"""
		"""
		self.outputMsg("leave space")
		self.ai and self.ai.onLeaveSpace()
		
	def onSetSpaceData(self):
		"""
		"""
		self.ai and self.ai.onSetSpaceData()
		
	def onMoveOver( self, controllerID, userData ):
		"""
		"""
		space = self.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		self.outputMsg("move success %s:%s" %(space, self.position))
		self.callback("onMoveOver", controllerID, userData)
	
	def onMoverFailure( self, controllerID, userData ):
		"""
		"""
		space = self.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		self.outputMsg("move Failure %s:%s" %(space, self.position))
		self.callback("onMoverFailure", controllerID, userData)
		
	#------common functions------
	def GMCommand(self, target, cmd, *params ):
		""" 使用GM命令 """
		if params:
			strParams = " ".join(params) 
		else:
			strParams = ""
		
		self.cell.onRoleSendGMCommandMessage( str(target.id), cmd, strParams )
		self.outputMsg("GMCommand:%s, %s" %(cmd, strParams))
			
	def getProfession( self ):
		"""
		获取职业
		"""
		return self.profession
		
	def entitiesInRange( self, rng, cnd = lambda ent : True ) :
		"""		搜索 entity 身边或指定点周边的所有 entity
		@type			rng : float
		@patam			rng : 搜索的半径
		@type			cnd : functor/method
		@param			cnd : 条件函数，它必须包含一个参数以表示遍历到的 entity，如果调用 cnd 返回 True，则表示参数 ent 是符合条件的 entity
		@return				: 返回所有要求的 entity		@rtype				: list
		"""
		entities = []
		for id,e in self.clientapp.entities.items() :
			if id == self.id:
				continue
			dist = e.position.distTo( self.position )
			if dist <= rng and cnd( e ):
				entities.append( e )
		return entities
	
	def monsterInRange( self, targetIDs ):
		"""
		获取指定的className
		"""
		for e in self.entitiesInRange(20):
			if e.className != "Monster":
				continue
			if e.scriptID in targetIDs:
				return e
		return None
		
	def moveToPos(self, pos):
		"""
		"""
		#self.cell.updateMoveType(2)
		return self.moveToPoint(pos, self.moveSpeed, 0.0, 0, True, True)
		
	def onDestroy(self):
		"""
		"""
		if self.id in KST.roles:
			KST.roles.remove(self.id)
			
	def onTickCallBack(self, tick):
		"""
		"""
		if self.ai is None: return
		self.ai.onTickCallBack(tick)
	
	def getCurSpace(self):
		#这里用isFirst作判断，只有在进入第一次进入space后，这个才能获取到，因为后面不管怎么样总是会在space中
		return self.clientapp.getSpaceData("SPACE_SCRIPT_ID") if not self.isFirst else ""
	def callback(self, func, *args):
		"""
		"""
		if self.callbackID: KBEngine.cancelCallback(self.callbackID)
		self.callbackID = KBEngine.callback(3, Functor(self.onCallBack, func, *args))
		
	def onCallBack(self, func, *args):
		"""
		"""
		self.callbackID = 0
		if self.ai is None: return
		if hasattr(self.ai, func):
			f = getattr(self.ai, func)
			f(*args)
