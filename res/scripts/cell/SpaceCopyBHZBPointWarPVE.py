# -*- coding: utf-8 -*-

from SpaceCopyAttackCityWar import SpaceCopyAttackCityWar
import csdefine
import csarithmetic
from SpaceCopy import SpaceCopy
import KBEngine
import csstatus
import KBEMath
from CoreInterface.SpaceBHZBWarDetailInterface import SpaceBHZBWarDetailInterface
import cschannel_msgs

class SpaceCopyBHZBPointWarPVE( SpaceCopyAttackCityWar,SpaceBHZBWarDetailInterface ):
	"""
	帮会争霸 据点争夺战 PVE
	"""
	def __init__( self ) :
		SpaceCopyAttackCityWar.__init__( self )
		SpaceBHZBWarDetailInterface.__init__( self )
		declareTongDBID = self.createArgs.get("declareTongDBID",0)
		attackWarDetail = self.createArgs.get("attackWarDetailData",None)
		if attackWarDetail != None:
			self.warDetailMgr[declareTongDBID] = attackWarDetail
		else:
			self.addBHZBWarDetailData( declareTongDBID )
		self.barrackInfo= {}							# 兵营据点等信息{ belongSide : { scriptID : pos},}
		self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_ATTACK] = {}
		self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_PROTECT] = {}
		self.isShowSettlementWnd = False

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		self.getScript().addEntityMailBoxRecord( self,scriptID, entityMailBox )

		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongAttackScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_ATTACK )
				self.changeRviverPosition( entityMailBox.id, csdefine.TRAP_BARRACKS_BELONG_ATTACK,entityMailBox.position,csdefine.TRAP_BARRACKS_BELONG_ATTACK )
				self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_ATTACK].update( { str(entityMailBox.id) : KBEMath.KBEngine2UnrealPosition( entityMailBox.position) } )
			else:
				entityMailBox.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongProtectScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )
				self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_PROTECT].update( { str(entityMailBox.id) : KBEMath.KBEngine2UnrealPosition( entityMailBox.position )} )
			else:
				entityMailBox.setBelongSide( csdefine.BELONG_SIDE_PROTECT )

		if scriptID in self.getScript().getNotReviveBossScriptID():
			if entityMailBox.getUname() not in self.recordBossCmdSoldierIDs:
				self.recordBossCmdSoldierIDs[entityMailBox.getUname()] = []

		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER:
			cmder =entityMailBox.getCmder()
			if not cmder:
				return
			if cmder.getUname() in self.recordBossCmdSoldierIDs:
				self.recordBossCmdSoldierIDs[cmder.getUname()].append( entityMailBox.id )

	def setGCZIsWin( self, isWin ):
		"""
		设置攻城战是否胜利
		"""
		if self.isShowSettlementWnd:
			return
		self.isShowSettlementWnd = True
		self.isWin = isWin
		self.showGCZSettlementWnd()
		time = self.getScript().delyCloseTime - 1.0
		self.addTimerCallBack( time,"bhzbPointWarEnd",() )
		self.addTimerCallBack( self.getScript().delyCloseTime,"closeSpace",() )

	def showGCZSettlementWnd( self ):
		"""
		"""
		SpaceCopyAttackCityWar.showGCZSettlementWnd( self )

	def bhzbPointWarEnd( self ):
		"""
		"""
		camp = self.createArgs.get("camp",0)
		pointIndex = self.createArgs.get("pointIndex",0)
		groupID = self.createArgs.get("declarePlayerDBID",0) #后一个版本修改为队伍编号
		if self.isWin:
			KBEngine.globalData["BHZBManager"].onBHZBPointWarSuccess( camp, pointIndex, groupID )
			KBEngine.globalData["BHZBManager"].occupyPointAddIntergral( camp, pointIndex, self.getScript().getRewardIntegral(),self.getScript().getRewardRepeatIntegral(),self.getScript().getRewardRepeatTime() )
		else:
			KBEngine.globalData["BHZBManager"].onBHZBPointWarFail( camp, pointIndex,groupID )
		self.statusEndMsg()

	def statusEndMsg( self ):
		"""
		播放结束消息
		"""
		if self.isWin:
			for role in self._spaceRoles:
				role.statusMessage( csstatus.BHZB_ATTACK_PVEPOINT_SUCCESS, self.createArgs.get("declareTongName",""),self.createArgs.get("pointName","") )
				role.addExp(self.getScript().getAddRewardExp(), csdefine.EXP_ADD_REASON_BHZB_POINT_WAR)
		else:
			for role in self._spaceRoles:
				role.statusMessage( csstatus.BHZB_ATTACK_PVEPOINT_FAIL, self.createArgs.get("pointName","") )

	def statusMsgToMember( self, msgID, msgArgs ):
		"""
		"""
		for role in self._spaceRoles:
			if role.getClient():
				role.client.statusMessage( msgID, msgArgs )

	def statusMsgToTongMember( self, msgID, msgArgs, tongDBID ):
		"""
		"""
		self.statusMsgToMember(msgID, msgArgs)

	def delayTransferDataToClient( self, roleCell ):
		"""延迟传送时间，因为怪物还没创建好"""
		self.addTimerCallBack(2, "transferDataToClient", (roleCell,))
		
	def transferDataToClient( self, roleCell ):
		"""
		传输数据到客户端
		"""
		if not roleCell or not roleCell.client:return
		barrackDict = {}
		barrackDict["dictDatas"] = []
		for side, datas in self.barrackInfo.items():
			temp = {}
			temp["belongSide"] = side
			temp["datas"] = []
			for key, value in datas.items():
				_dict = {}
				_dict["key"] = key
				_dict["value"] = value
				temp["datas"].append( _dict )
			barrackDict["dictDatas"].append( temp )
		if roleCell.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			roleCell.client.InitGTAttackDatas( barrackDict )
		else:
			batteryDict = {}
			batteryDict["dictDatas"] = []
			roleCell.client.InitGTProtectDatas( barrackDict, batteryDict, [], 0 )


	def changeRviverPosition( self, entityID, belongType, position, oldBelongType ):
		"""
		增加复活信息
		"""
		if belongType == csdefine.TRAP_BARRACKS_BELONG_ATTACK:
			self.revivePosInfos.append(position)

		battackEntity = KBEngine.entities.get( entityID )
		if battackEntity and oldBelongType in self.barrackInfo and str(battackEntity.id) in self.barrackInfo[oldBelongType]:
			pos = self.barrackInfo[oldBelongType].pop( str(battackEntity.id) )
			self.barrackInfo[belongType] = { str(battackEntity.id) : pos } 
			for roleCell in self._spaceRoles:
				roleCell.client.occupyGTBarrack( belongType, str(battackEntity.id) )
	
	def onTeleportCompleted( self, playerRole ):
		SpaceCopy.onTeleportCompleted( self, playerRole )
		SpaceBHZBWarDetailInterface.onTeleportCompleted( self, playerRole )