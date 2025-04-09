# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
import csstatus
import csarithmetic
import ItemFactory
from KBEDebug import *
from ConfigObject.Talk.TalkBase import BaseNPCTalkAction
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
import Math
import KBEMath
import random
import Define
import Const
import Functions
import time
import csconst

class TATeleport(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:传送功能
	"""
	def __init__(self, actionData):
		"""
		"""
		self._spaceName = actionData["param1"]

		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		self._position = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
		self._direction = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.gotoSpaceUE4(self._spaceName, self._position, self._direction)
		player.sendGossipComplete( talkEntity.id )

class TATeleportWithTeamFollow(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:传送功能，比TATeleport多了组队跟随功能，用于地图传送NPC
	"""
	def __init__(self, actionData):
		"""
		"""
		self._spaceName = actionData["param1"]

		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		self._position = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
		self._direction = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.npcTeamFollowTransport( talkEntity, dlgKey )
		player.gotoSpaceUE4(self._spaceName, self._position, self._direction)
		player.sendGossipComplete( talkEntity.id )

class TAOpenShop(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开商店
	"""
	def __init__(self, actionData):
		"""
		"""
		self.shopID = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.requestShopItemList( talkEntity.id, self.shopID )
		player.sendGossipComplete( talkEntity.id )

class TAEnterBunchSpaceBase(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:进入副本串
	"""
	def __init__(self, actionData):
		"""
		"""
		self.bunchSpace = actionData["param1"]
		self.needLevel = int( actionData["param2"] )
		self.activityType = csdefine.ACTIVITY_TYPE_UNKNOWN
		if actionData["param3"]: 
			self.activityType = int( actionData["param3"] )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		from ConfigObject.BunchChildStrategy.StrategyLoader import g_bunchChildStrategyLoader
		
		bunchObj = g_objFactory.getBunchSpaceObject( self.bunchSpace )
		destSpace = g_bunchChildStrategyLoader.getFirstSpace( bunchObj, player )	#CST-1938 按策略随机第一个子副本
		bunchLevel = min( self.needLevel+19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
		
		#次数不够了
		if player.isExceedActivityDegree(self.activityType):
			player.statusMessage( csstatus.SPACE_ENTER_EXCEED_JOIN_DEGREE )
			player.sendGossipComplete( talkEntity.id )
			return
		
		if player.isInTeam():
			globalRecord = KBEngine.globalData["BunchSpaceGlobalRecord"]
			belongType = csdefine.SPACE_BELONG_TEAM
			spaceKey = str( player.teamMailbox.id )

			if ( self.bunchSpace in globalRecord ) and \
				( belongType in globalRecord[ self.bunchSpace ] ) and \
				( spaceKey in globalRecord[ self.bunchSpace ][ belongType ] ):	# 存在副本
				player.gotoBunchSpace( self.bunchSpace, { "packBelongType": belongType, "bunchLevel": bunchLevel, "destChildSpace": destSpace, "activityType" : self.activityType } )
			else:
				if not player.isTeamCaptain():	# 副本不存在的情况下，这里一定是队长对话
					ERROR_MSG("Gossip player is not captain!")
					return
				
				msgArgs = ""
				teammates = []
				for memMB in player.getAllTeamMemberMB():
					entity = KBEngine.entities.get(memMB.id)
					#有队伍成员距离过远
					if entity is None or player.position.distTo(entity.position) > 50:	
						player.statusMessage(csstatus.CAMP_RANDOM_FIT_FAR)
						player.sendGossipComplete( talkEntity.id )
						return
					
					#次数不够了
					if entity.isExceedActivityDegree(self.activityType):
						if msgArgs: msgArgs += "、"
						msgArgs += entity.playerName
						continue
					
					if memMB.id != player.id:
						teammates.append( memMB )
					
				if msgArgs:
					player.statusMessage(csstatus.ACTIVITY_COPY_SPACE_FAIL_SOMEONE_TIMES, msgArgs)
					player.sendGossipComplete( talkEntity.id )
					return
					
				player.gotoBunchSpace( self.bunchSpace, { "packBelongType": belongType, "bunchLevel": bunchLevel, "destChildSpace": destSpace, "teammates": teammates, "activityType" : self.activityType } )

		else:
			belongType = csdefine.SPACE_BELONG_PERSON
			player.gotoBunchSpace( self.bunchSpace, { "packBelongType": belongType, "bunchLevel": bunchLevel, "destChildSpace": destSpace, "activityType" : self.activityType } )

		player.sendGossipComplete( talkEntity.id )

class TAEnterPotentailBunchSpace( TAEnterBunchSpaceBase ):
	"""
	npc对话:进入潜能副本串
	"""
	def __init__(self, actionData):
		"""
		"""
		TAEnterBunchSpaceBase.__init__(self, actionData)

class TAEnterChuanChengBunchSpace( TAEnterBunchSpaceBase ):
	"""
	npc对话:进入传承副本串
	"""
	def __init__(self, actionData):
		"""
		"""
		TAEnterBunchSpaceBase.__init__(self, actionData)

class TAOpenSkillLearn(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开技能学习界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__( self, actionData )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.requestOpenSkillLearn( int(talkEntity.scriptID) )
		player.sendGossipComplete( talkEntity.id )
		
class TAEnterPlane(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:进入位面
	"""
	def __init__(self, actionData):
		"""
		"""
		self._spaceName = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.gotoSpacePlane( self._spaceName )
		player.sendGossipComplete( talkEntity.id )
		
class TALeavePlane(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:离开位面
	"""
	def __init__(self, actionData):
		"""
		"""
		self._spaceName = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.leaveSpacePlane( self._spaceName )
		player.sendGossipComplete( talkEntity.id )

class TAOpenStore(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开仓库
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.base.requestOpenStoreWindow( talkEntity.id )
		player.sendGossipComplete( talkEntity.id )
		

class TAPlayGossipVoice(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:播放对话语音
	"""
	def __init__(self, actionData):
		"""
		"""
		self._voiceID = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.client.onPlayGossipVoice(self._voiceID)

class TASetPlayerRevivePos( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：设置玩家复活点
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._spaceName = actionData["param1"]
		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		self._position = KBEMath.Unreal2KBEnginePosition((eval(position[0]), eval(position[1]), eval(position[2])))
		self._direction = KBEMath.Unreal2KBEngineDirection(Math.Vector3(eval(direction[0]), eval(direction[1]), eval(direction[2])))

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.setRevivePos( self._spaceName,self._position,self._direction )
		player.client.CLIENT_SetRevivePosStatus( csstatus.TALK_SET_REVIVE_POS, self._spaceName )
		player.sendGossipComplete( talkEntity.id )
		
class TASkill( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：对玩家释放技能
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._skillID = int(actionData["param1"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.useSkillToEntity( self._skillID, player.id )

class TAQuestTalk( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：触发对话任务目标完成
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._questID = int(actionData["param1"])
		self._taskID = int(actionData["param2"])
		
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.forceQuestTaskIncreaseState( self._questID, self._taskID )
		
class TAClose( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：关闭NPC自身对话聊天界面
	"""
	def __init__( self, actionData ):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__( self, actionData )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.sendGossipComplete( talkEntity.id )

class TADestroy( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：NPC销毁自身
	"""
	def __init__( self, actionData ):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__( self, actionData )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.sendGossipComplete( talkEntity.id )
		talkEntity.destroySelf( )

class TASummonEntity( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：刷1个entity
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._entityID = actionData["param1"]
		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		#配置中的是客户端的位置和朝向，需要转换成服务器的位置和朝向
		self._position = KBEMath.Unreal2KBEnginePosition((eval(position[0]), eval(position[1]), eval(position[2])))
		self._direction = KBEMath.Unreal2KBEngineDirection(Math.Vector3(eval(direction[0]), eval(direction[1]), eval(direction[2])))

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		level = 1
		objData = g_objFactory.getObject( self._entityID )
		if not objData:
			player.statusMessage( csstatus.GM_SCRIPTID_DONT_EXIST,"")
			return
		if hasattr( objData, "minLv" ) and hasattr( objData, "maxLv" ):
			minLevel = int(objData.minLv)
			maxLevel = int(objData.maxLv)
			level = random.randint(minLevel,maxLevel)
		
		if self._entityID.startswith("1"):
			Obj = player.createNPC(self._entityID, self._position, self._direction, { "spawnPos":tuple(Math.Vector3( self._position )), "level":level} )
		elif self._entityID.startswith("2"):
			Obj = player.createMonster(self._entityID, self._position, self._direction, { "spawnPos":tuple(Math.Vector3( self._position )), "spawnDir":tuple(Math.Vector3(self._direction)), "level":level} )	
		elif self._entityID.startswith("3"):
			Obj = player.createTrap(self._entityID, self._position, self._direction, { "spawnPos":tuple(Math.Vector3( self._position )), "level":level} )
		elif self._entityID.startswith("4"):
			Obj = player.createSpellBox(self._entityID, self._position, self._direction, {} )
	
class TAItem( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：玩家获得物品
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._itemID = int( actionData["param1"] )
		self._amount = int( actionData["param2"] )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( self._itemID, self._amount )
		player.addItem( itemInst, csdefine.ITEM_ADD_BY_QUESTACTION )
		
class TAPlayAction( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：NPC播放动作
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._actionID = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		talkEntity.allClients.CLIENT_OnPlayAction(self._actionID,-1.0)
		
class TAAcceptLoopQuest( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：接取环任务
	"""
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.randomLoopQuest():
			if player.loopQuest["loopQuestList"]:
				questID = player.loopQuest["loopQuestList"][0]
				player.sendApplyQuestDataByClick( questID, talkEntity.id )
			
		player.sendGossipComplete( talkEntity.id )

class TAGuessGame( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：开始猜大小游戏
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._questID = actionData["param1"]
		self._initMsg = actionData["param2"]
		self._winMsg = actionData["param3"]
		self._lostMsg = actionData["param4"]
		self._finishMsg = actionData["param5"]
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.startGuessGame( self._questID, self._initMsg, self._winMsg, self._lostMsg, self._finishMsg )
		player.sendGossipComplete( talkEntity.id )

class TAChangeBody( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：开始比赛变身
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._scriptID = actionData["param1"]
		
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.inquireMessage( csstatus.CHALLENGE_CHANGE_BODY, [], "isChallengeChangeBody", self._scriptID )

class TAOpenHLD( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：点开欢乐鼎
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._scriptID = actionData["param1"]		#刷出的怪物scriptID
		self.effectID= actionData["param2"].split("|")			#真光效ID|假光效ID
		self.countKeyList = actionData["param3"].split("|")		#增加计数事件|通知副本阶段Key值
		if actionData["param4"]:
			self._amount = int(actionData["param4"])  	#选中次数
		else:
			self._amount = -1
		self.soundIDList = actionData["param5"].split("|") #真音效ID|假音效ID
		
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		isTrue = talkEntity.queryIsTrue()
		spaceEntity= talkEntity.getCurrentSpace()
		if isTrue :
			spaceEntity.getScript().spaceEvent_addCount( spaceEntity, self.countKeyList[0], 1 )
			if spaceEntity.spaceEventCountInt[self.countKeyList[0]] != self._amount:
				dstPos = csarithmetic.getPositionByLink( talkEntity.position , 3 )
				talkEntity.addTimerCallBack( 1.0,"createEntityByScriptID",(talkEntity.scriptID,dstPos,talkEntity.direction,{"spawnPos":dstPos}) )
			if spaceEntity.spaceEventCountInt[self.countKeyList[0]] == 1: #只播放一次
				player.showMessagePlaySound(self.soundIDList[0])
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, self.countKeyList[1], "") #通知副本阶段条件改变
			talkEntity.allClients.CLIENT_OnPlayParticles( talkEntity.id, self.effectID[0],"",1.0,Math.Vector3(0,0,0) )
			player.client.HLDCanStart()
			#talkEntity.createEntityByScriptID( talkEntity.scriptID,dstPos,talkEntity.direction,{"spawnPos":dstPos} )
		else :
			talkEntity.createEntityByScriptID( self._scriptID, talkEntity.position, talkEntity.direction,{"spawnPos":talkEntity.position})
			if spaceEntity.queryTemp("ClickError") == None: #只播放一次
				player.showMessagePlaySound( self.soundIDList[1] )
				spaceEntity.setTemp("ClickError",True)
			talkEntity.allClients.CLIENT_OnPlayParticles( talkEntity.id, self.effectID[1],"",1.0,Math.Vector3(0,0,0) )
		
		# 让正确的鼎发光，并将所有鼎复原
		entitylist = spaceEntity.getEntityRecord( talkEntity.scriptID )
		for eid  in entitylist:
			HLDEntity = KBEngine.entities.get(eid)
			if not HLDEntity:
				continue
			HLDEntity.HLDReset()		

class TANone(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:无操作
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		pass
		#player.sendGossipComplete( talkEntity.id )

class TACreateEntity( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：在当前位置创建entity
	"""
	def __init__(self, actionData):
		"""
		"""
		self.scriptID = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		talkEntity.createEntityByScriptID( self.scriptID,talkEntity.position,talkEntity.direction, {"spawnPos":talkEntity.position} )

class TAOnNitySpaceCountAdd( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：通知副本计数改变
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""	
		spaceEntity = talkEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().spaceEvent_addCount(spaceEntity,talkEntity.scriptID,1)

class TAStoneTeleport(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:传送石传送功能
	"""
	def __init__(self, actionData):
		"""
		"""
		self._spaceName = actionData["param1"]

		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		self._position = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
		self._direction = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )
		self._teleportIndex = actionData["param4"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.gotoSpaceUE4(self._spaceName, self._position, self._direction)
		player.addTeleportPoint( self._teleportIndex )
		#player.sendGossipComplete( talkEntity.id )
		
class TAOnSpaceConditionChange(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:给副本发送事件
	"""
	def __init__(self, actionData):
		"""
		"""
		self._scriptID = actionData["param1"]
		self._key = actionData["param2"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		spaceEntity = talkEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "TALK", self._scriptID, self._key, "" )
		else:
			ERROR_MSG("NPC(%s) talk action fail!!in space(%s)"%(talkEntity.scriptID,spacee))

class TAOnDetermineDemon(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:妖魔化身判断
	"""
	def __init__(self, actionData):
		"""
		"""
		self._scriptID = actionData["param1"]
		self._key = actionData["param2"]
		self._msg = actionData["param3"]
		self._skillID = int( actionData["param4"] )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		spaceEntity = talkEntity.getCurrentSpace()
		try:
			headModel = spaceEntity.queryTemp( "demon_headModel", "" )
			cloakModel = spaceEntity.queryTemp( "demon_cloakModel", "" )
			bodyModel = spaceEntity.queryTemp( "demon_bodyModel", "" )
			coatModel = spaceEntity.queryTemp( "demon_coatModel", "" )
			handModel = spaceEntity.queryTemp( "demon_handModel", "" )
			waistModel = spaceEntity.queryTemp( "demon_waistModel", "" )
			
			if talkEntity.headModel == headModel and talkEntity.cloakModel == cloakModel and \
			talkEntity.bodyModel == bodyModel and talkEntity.coatModel == coatModel and \
			talkEntity.handModel == handModel and talkEntity.waistModel == waistModel:
				spaceEntity.getScript().onConditionChange( spaceEntity, "TALK", self._scriptID, self._key, "" )
			else:
				player.setGossipText( talkEntity.id, self._msg )
				player.useSkillToEntity( self._skillID, player.id )
		except:
			ERROR_MSG("NPC(%s) talk action fail!!in space(%s)"%(talkEntity.scriptID,spacee))

class TASparHunTingSignUp( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：晶石狩猎场报名
	"""
	def __init__(self, actionData):
		"""
		"""
		self.minLevel = int(actionData["param1"])
		self.maxLevel = int(actionData["param2"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.level < self.minLevel or player.level > self.maxLevel:
			player.statusMessage( csstatus.SPARHUNTING_ACTIVITY_SIGN_UP_LEVEL_ERROR,"" )
			return
		if player.isInTeam():
			player.statusMessage(csstatus.SHI_FANG_CHENG_LIMIT_TEAM)
			return
		KBEngine.globalData["SparHunTingManager"].activeSignUp( player, player.playerDBID, player.getLevel() ,player.getCamp() )

class TASparHunTingEnter( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入晶石狩猎场
	"""
	def __init__(self, actionData):
		"""
		"""
		xianEnterPos = actionData["param1"].split("|")
		moEnterPos = actionData["param2"].split("|")
		self._xianEnterPos = ( eval(xianEnterPos[0]), eval(xianEnterPos[1]), eval(xianEnterPos[2]) )
		self._moEnterPos = ( eval(moEnterPos[0]), eval(moEnterPos[1]), eval(moEnterPos[2]) )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		pos = Math.Vector3(0,0,0)
		if player.getCamp() == csdefine.CAMP_TAOSIM:
			pos = self._xianEnterPos
		else:
			pos = self._moEnterPos
		pos = KBEMath.Unreal2KBEnginePosition( pos )
		KBEngine.globalData["SparHunTingManager"].requestEnter( player ,Math.Vector3(pos),Math.Vector3(0,0,0),player.getLevel() )
		player.sendGossipComplete( talkEntity.id )

class TALeaveJail( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	传送出监狱（用于监狱传送员）
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		spaceObject = player.getCurrentSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( player )
		player.gotoSpaceUseArg( exitScriptID, Math.Vector3(exitPosition), exitDirection, {"isTalkLeave":True} )

class TATeleportLastMap(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:回到进来当前地图的上一个地图的位置
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.gotoExitSpacePos()

class TAActivityBunchSignUp(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:报名活动串
	"""
	def __init__(self, actionData):
		"""
		"""
		self.bunchName = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.actBunch_signUp( self.bunchName )
		player.sendGossipComplete( talkEntity.id )

class TAEnterMagicMazeSpace(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:进幻阵迷宫副本
	"""
	def __init__(self, actionData):
		"""
		"""
		self.mainSpaceDatas = actionData["param1"].split("|")
		self.needLevel = int( actionData["param2"] )
		self.activityType = csdefine.ACTIVITY_TYPE_UNKNOWN
		if actionData["param3"]:
			self.activityType = int(actionData["param3"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		spaceLevel = min( self.needLevel+19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
		mainSpaceData = random.choice(self.mainSpaceDatas)
		spaceData = mainSpaceData.split(":")
		
		#次数不够了
		if player.isExceedActivityDegree(self.activityType):
			player.statusMessage(csstatus.SPACE_ENTER_EXCEED_JOIN_DEGREE)
			player.sendGossipComplete( talkEntity.id )
			return
		pickArg = {}
		pickArg["mainScriptID"] = spaceData[1]
		if player.isInTeam():
			globalRecord = KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"]
			belongType = csdefine.SPACE_BELONG_TEAM
			spaceKey = str( player.teamMailbox.id )
			
			scriptID = ""
			for key,mainScriptID in globalRecord.items():
				if spaceKey == key[1]:
					scriptID = mainScriptID
					break

			if (belongType, spaceKey,scriptID) in globalRecord:	# 存在副本
				pickArg.update({ "packBelongType": belongType, "spaceKey":spaceKey, "activityType":self.activityType,"mainScriptID":scriptID, "players":{ player.playerDBID: player.base } })
				KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)
			else:
				if not player.isTeamCaptain():	# 副本不存在的情况下，这里一定是队长对话
					ERROR_MSG("Gossip player is not captain!")
					return
					
				msgArgs = ""
				teammates = {}
				for memMB in player.getAllTeamMemberMB():
					memPlayer = KBEngine.entities.get( memMB.id, None )
					if memPlayer is None or player.position.distTo(memPlayer.position) > 50:
						player.statusMessage(csstatus.CAMP_RANDOM_FIT_FAR)
						player.sendGossipComplete( talkEntity.id )
						return
						
					if memPlayer.isExceedActivityDegree(self.activityType):
						if msgArgs: msgArgs += "、"
						msgArgs += memPlayer.playerName
						continue
						
					teammates[ memPlayer.playerDBID ] = memMB
					
				if msgArgs:
					player.statusMessage(csstatus.ACTIVITY_COPY_SPACE_FAIL_SOMEONE_TIMES, msgArgs)
					player.sendGossipComplete( talkEntity.id )
					return
				
				pickArg.update({ "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "players": teammates, "mainSpace":spaceData[0], "activityType":self.activityType})
				KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)
		else:
			belongType = csdefine.SPACE_BELONG_PERSON
			spaceKey = str( player.playerDBID )
			pickArg.update({ "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "activityType":self.activityType, "players":{ player.playerDBID: player.base },"mainSpace":spaceData[0]})
			KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)	
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenTongStore(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开帮会仓库
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.tongMB:
			player.tongMB.enterTongStorage( player.playerDBID, talkEntity.id )
			player.sendGossipComplete( talkEntity.id )
		
class TAOpenTongShop(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开帮会商店
	"""
	def __init__(self, actionData):
		"""
		"""
		self.shopID = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.tongMB:
			player.requestTongShopItemList( player.id, talkEntity.id, self.shopID )
			player.sendGossipComplete( talkEntity.id )

class TAGotoTongSpaceCopy(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:进入帮会副本
	"""
	def __init__(self, actionData):
		"""
		"""
		self._delayTime = 0
		if actionData["param1"]:
			self._delayTime = float( actionData["param1"] )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		validSpace = []
		
		import ObjectScript.Space as space
		tongSpaceCopy = space.getTongSpaceCopyScriptIDs()
		for reqLevel, spaceList in tongSpaceCopy.items():
			if player.getLevel() >= reqLevel:
				validSpace.extend( spaceList )
		
		if validSpace:
			spaceScriptID = random.choice( validSpace )
			if self._delayTime:
				from ObjectScript.ObjectScriptFactory import g_objFactory
				spaceObject = g_objFactory.getSpaceObject( spaceScriptID )
				player.statusMessage( csstatus.TONG_SPACE_COPY_ENTER_DELAY, self._delayTime,  )
				player.addTimerCallBack( self._delayTime, "gotoSpaceEnterPos", ( spaceScriptID,{}) )
			else:
				player.gotoSpaceEnterPos( spaceScriptID, {} )
			player.sendGossipComplete( talkEntity.id )
		else:
			ERROR_MSG("Can not find valid Tong SpaceCopy!")

class TAActivityBunchJoin(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:参加活动串
	"""
	def __init__(self, actionData):
		"""
		"""
		self.bunchName = actionData["param1"]
		self.activityName = actionData["param2"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.isInTeam():
			player.statusMessage( csstatus.ZHIZUNZHENBA_ENTER_LIMIT_TEAM )
			return
		player.actBunch_join(self.bunchName,self.activityName,"" )
		player.sendGossipComplete( talkEntity.id )

class TAFlyToSubSpace(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:起飞到飞行路线的第一个点
	"""
	def __init__(self, actionData):
		"""
		"""
		self.patrolID = actionData["param1"]
		self.flySpeed = actionData["param2"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		enterPos = Math.Vector3( 0.0, 0.0, 0.0 )
		if player.isInTeam():	#玩家在队伍里
			inRangeMem = player.getInRangeTeammate( Define.TEAM_ITEM_PICKUP_RANGE )
			for inRangPlay in inRangeMem:
				inRangPlay.allClients.FlyToSubSpace( self.patrolID, "0", 0, 0, int(self.flySpeed), enterPos )
		else:
			player.allClients.FlyToSubSpace( self.patrolID, "0", 0, 0, int(self.flySpeed), enterPos )

class TAYXLMSignUp( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:报名英雄王座
	"""
	def __init__(self, actionData):
		"""
		"""
		self.diffLevel = int(actionData["param1"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""

		if player.isInTeam():
			if not player.isTeamCaptain():
				player.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_NOT_CAPTAIN_SIGNUP )
				return
			if player.getActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_YXLM ):
				player.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_ACTIVITY_IS_JOIN )
				return
			memberIsJoin = False
			for member in player.getAllTeamMemberMB():
				entity = KBEngine.entities.get(member.id,None)
				if entity and entity.id != player.id and entity.getActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_YXLM ):
					memberIsJoin = True	
					break
			if memberIsJoin:
				player.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_MEMBER_IS_JOIN )
				return
			minLevel = player.level
			maxLevel = player.level
			for member in player.getAllTeamMemberMB():
				entity = KBEngine.entities.get(member.id,None)
				if entity and entity.getLevel() > maxLevel:
					maxLevel = entity.getLevel()
				
				if entity and entity.getLevel() < minLevel:
					minLevel = entity.getLevel()

			if maxLevel - minLevel > self.diffLevel:
				player.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_MEMBER_LEVEL_NOTIN_DIFFLEVEL )
				return
			memberDataList = []
			for member in player.getAllTeamMemberMB():
				entity = KBEngine.entities.get(member.id,None)
				if not entity:
					continue
				tempDict = {}
				tempDict["playerMB"] = entity.base
				tempDict["playerDBID"] = entity.playerDBID
				tempDict["camp"] = entity.getCamp()
				tempDict["level"] = entity.getLevel()
				tempDict["name"] = entity.getName()
				memberDataList.append(tempDict)

			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_reqTeam( player.base, player.teamMailbox, memberDataList, player.getCamp(), player.getLevel() )

		else:
			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_reqPerson( player.base, player.playerDBID, player.getCamp(), player.getLevel(), player.getName() )
		player.sendGossipComplete( talkEntity.id )

class TAOpenTraviaShop(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开英雄王座商店
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.openTraviaShop( talkEntity.id )
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenLMNeuralShop(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开英雄王座 中立商店
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		scriptIDs = list(talkEntity.mScriptIDs)
		times = list(talkEntity.mScriptIDs.values())
		player.openLMNeuralShop( talkEntity.id, scriptIDs, times, talkEntity.level )
		player.sendGossipComplete( talkEntity.id )
		
class TAEnterLingMaiActivity(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:报名进入灵脉战场
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.base.signInLingMai()
		player.sendGossipComplete( talkEntity.id )

class TAShowTongMemberWin( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：显示帮会成员面板
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.client.CLIENT_ShowTongMemberWindow(Const.TONG_STARCRAFT_JOIN_MEMBER)
		player.sendGossipComplete( talkEntity.id )

class TAShowTongSignSuccessWin( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：查看帮会争霸报名成功面板
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_firstQuerySignUp( player.getCamp(),player.base )
		player.sendGossipComplete( talkEntity.id )

class TAGotoTongStarcraft( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入帮会争霸第一场
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_gotoFirstStarcraft( player.getCamp(), player.tongDBID,player.base,player.playerDBID,player.tongName  )
		player.sendGossipComplete( talkEntity.id )

class TAQueryPassFirstTongStarcraft( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：查看帮会争霸第一场通过的帮会
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_queryPassFirstTongStarcraft( player.getCamp(),player.base  )
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenForgeEquip( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：打开装备打造界面
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.client.OpenForgeEquip( talkEntity.id )


class TASubmitIceCrystalsFrozenFight(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话：cst-4056 冰雪之战活动 提交冰晶核心
	"""
	def __init__(self, actionData):
		""""""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		""""""
		spaceEntity = player.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.submitIceCrystals(player)


class TAEnterFrozenFightActivity(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:报名进入冰雪之战
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.base.signInFrozenFight()
		player.sendGossipComplete( talkEntity.id )


class TAOpenSecondTongStarcraftGroup( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话:打开帮会争霸第二场的分组
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager"].openSecondTongStarcraftGroup( player.getCamp(), player.base )
		player.sendGossipComplete( talkEntity.id )

class TAEnterSecondTongStarcraft( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话:打开帮会争霸第二场的分组
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_gotoSecondStarcraft( player.getCamp(), player.tongDBID,player.base,player.playerDBID,player.tongName )
		player.sendGossipComplete( talkEntity.id )


class TAAnswerTongQuestion( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话:继续帮会日常任务答题
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._questID = int(actionData["param1"])

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		player.selectNextTongQuestion(player.id, self._questID)
		

class TAOpenGameRank( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话:打开排行榜
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		KBEngine.globalData["GameRankingManager"].openGameRank( player, player.playerDBID, talkEntity.id )
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenMailWindow( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话:打开邮箱界面
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		player.client.CLIENT_OpenMailWindow()
		player.sendGossipComplete( talkEntity.id )

class TASignUpThirdStarcraftField(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	NPC对话:报名帮会争霸第三场内场
	"""
	def __init__( self, actionData ):
		"""
		"""
		self.signUpSuccSound = actionData["param1"]
		self.fullSound = actionData["param2"]

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			spaceEntity.signUpThirdStarcraftField(player.tongDBID,player.playerDBID,player,self.signUpSuccSound,self.fullSound)
		player.sendGossipComplete( talkEntity.id )

class TASYDXSubmitYueQi(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	NPC对话:神乐雕像 提交乐器
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass	

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			spaceEntity.submitYueQi(talkEntity)

class TASignUpShiFangCheng( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话: 报名十方城
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass	

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		activityKey = int(player.getLevel() / 10)
		KBEngine.globalData["PersonStarcraftMgr"].shiFangChengSignUp( activityKey, player.base, player.playerDBID, player.getName() )
		player.sendGossipComplete( talkEntity.id )

class TAGotoShiFangCheng( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话: 进入十方城
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass	

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		if player.isInTeam():
			player.base.leaveTeamFB( player.id )
		activityKey = int(player.getLevel() / 10)
		KBEngine.globalData["PersonStarcraftMgr"].gotoShiFangCheng( player.base,activityKey, player.playerDBID )
		player.sendGossipComplete( talkEntity.id )

class TAGotoYeZhanFengQi( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话: 进入血斗凤栖镇
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass	

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		activityKey = int(player.getLevel() / 10)
		KBEngine.globalData["PersonStarcraftMgr"].gotoYeZhanFengQi( player.base,activityKey,player.playerDBID )
		player.sendGossipComplete( talkEntity.id )

class TASpaceCopyMagicMazeFlyToSubSpace(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	NPC对话:幻阵迷宫 飞行
	"""
	def __init__( self, actionData ):
		"""
		"""
		self.flySpeed = actionData["param1"]

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		spaceEntity = player.getCurrentSpace()
		if spaceEntity and spaceEntity.progress==0 and not spaceEntity.copyIsComplet:
			if player.isInTeam():	#玩家在队伍里
				if player.isTeamCaptain():#必须是队长才能对话
					spaceEntity.onClientStartMove( player, self.flySpeed )
				else:
					player.statusMessage(csstatus.SPACE_ENTER_NOT_CAPTAIN, "")
			else:
				spaceEntity.onClientStartMove( player, self.flySpeed )
				
			player.sendGossipComplete( talkEntity.id )

class TAGetRewardItem(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	领取奖励（每个玩家只能领取一次）
	"""
	def __init__( self, actionData ):
		"""
		"""
		self._itemID = actionData["param1"]

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		spaceEntity = talkEntity.getCurrentSpace()
		if not spaceEntity:
			return

		if player.id not in spaceEntity.advanceAwardList:
			result, _ = player.addItemByID( self._itemID )
			if result != csstatus.ITEM_GO_ON:
				player.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH, "")
				return
			else:
				spaceEntity.advanceAwardList.append( player.id )
				player.sendGossipComplete( talkEntity.id )
				return
		else:
			player.statusMessage( csstatus.TALK_GET_REWARD_ITEM, "" )
			player.sendGossipComplete( talkEntity.id )

class TATestEnterThirdTongStarcraft( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话, 测试进入帮会争霸 第三场
	"""
	def __init__( self, actionData ):
		"""
		"""
		self.side = int(actionData["param1"]) # 红方:0 or蓝方:1
		self.spaceName = actionData["param2"] #副本scriptID
		self.enterPos = Math.Vector3(0,0,0)
		self.enterDir = Math.Vector3(0,0,0)
		enterPosStr = actionData["param3"]  #进入坐标
		enterDirStr = actionData["param4"]  #进入朝向
		if enterPosStr:
			enterPos = Functions.vector3TypeConvert(enterPosStr)
			self.enterPos = Math.Vector3(KBEMath.Unreal2KBEnginePosition(tuple(enterPos)))
		if enterDirStr:
			enterDir = Functions.vector3TypeConvert(enterDirStr)
			self.enterDir = Math.Vector3(KBEMath.Unreal2KBEngineDirection(tuple(enterDir)))

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		if player.tongMB and player.isTongLeader():
			player.tongMB.testEnterThirdTongStarcraft( self.side, self.spaceName, self.enterPos,self.enterDir )
		player.sendGossipComplete( talkEntity.id )

class TATestSignThirdTongStarcraft( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	NPC对话, 测试报名帮会争霸 第三场
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do( self, dlgKey, player, talkEntity, args ):
		"""
		"""
		if player.tongMB and player.isTongLeader():
			KBEngine.globalData["TongStarcraftManager"].tongStarcraft_ThirdSignUp(player.getCamp(),player.tongDBID,player.tongName )

class TAOpenSkillShenTongComminution(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开神通技能精研
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__( self, actionData )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.client:
			player.client.CLIENT_rquestComminution( talkEntity.id )
		player.sendGossipComplete( talkEntity.id )

class TAJSZZCreateEntity(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:金树种子创建友方怪物
	"""
	def __init__( self, actionData ):
		"""
		"""
		self.scriptID = actionData["param1"] #怪物ID

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		monster = talkEntity.createEntityByScriptID( self.scriptID, talkEntity.position, talkEntity.direction,{"spawnPos":talkEntity.position,"spawnDir":talkEntity.direction} )
		if monster:
			monster.setTemp("RecordNPCScriptID",talkEntity.scriptID)
			talkEntity.destroySelf()
		player.sendGossipComplete( talkEntity.id )

class TAOpenTongNagualUI(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开神兽界面
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.client.OpenTongNagualUI()


class TAShowTongStarcraftSignUpWin( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：JIRA-7904 帮会争霸显示报名成功帮会
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager7904"].tongStarcraft_firstQuerySignUp(player.getCamp(),player.base)
		player.sendGossipComplete( talkEntity.id )


class TAGotoFirstTongStarcraft( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：JIRA-7904 帮会争霸进入第一场
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongStarcraftManager7904"].gotoFirstTongStarcraft(player.getCamp(),player.tongDBID, player.base, player.playerDBID)
		player.sendGossipComplete( talkEntity.id )

class TAEnterLoopQuestSpace( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入环任务秘境
	"""
	def __init__(self, actionData):
		"""
		"""
		self.mainSpaceList = actionData["param1"].split("|")

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		belongType = csdefine.SPACE_BELONG_PERSON
		spaceKey = str( player.playerDBID )
		pickArg = { "packBelongType": belongType, "spaceKey":spaceKey }
		if player.loopQuest["loopQuestList"]:
			KBEngine.globalData["RingTaskSpaceMgr"].setRingTaskItem( spaceKey )
			questID = player.loopQuest["loopQuestList"][0]
			KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( player.base, spaceKey, str(questID), 0 )
			KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( spaceKey, player.loopQuestProgress )
			if player.loopQuestProgress in range( 0, 6 ):
				player.gotoRingTaskSpace( self.mainSpaceList[0], str(questID), pickArg, player.hasQuest(questID) )
			elif player.loopQuestProgress in range( 6, 13 ):
				player.gotoRingTaskSpace( self.mainSpaceList[1], str(questID), pickArg, player.hasQuest(questID) )
			else:
				player.gotoRingTaskSpace( self.mainSpaceList[2], str(questID), pickArg, player.hasQuest(questID) )
		else:
			if player.randomLoopQuest():
				questID = str(player.loopQuest["loopQuestList"][0])
				KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( spaceKey, player.loopQuestProgress )
				KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( player.base, spaceKey, questID, 0 )
				player.gotoRingTaskSpace( self.mainSpaceList[0], questID, pickArg, True )
		player.sendGossipComplete( talkEntity.id )

class TAOpenLingLongBaoZhuUI(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:开启玲珑宝珠小游戏 CST-8117
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		spaceEntity = player.getCurrentSpace()
		spaceEntity.StartLLBZGame(player, talkEntity.scriptID)
		player.sendGossipComplete( talkEntity.id )

class TASGMZSignUp( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:报名上古密阵
	"""
	def __init__(self, actionData):
		"""
		"""
		self.diffLevel = int(actionData["param1"])
		self.teamNum = int(actionData["param2"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.isInTeam():
			player.teamMailbox.signUpSGMZ( player.base, player.getCamp(), player.getLevel(), player.getProfession() )
			player.sendGossipComplete( talkEntity.id )
			return
			if not player.isTeamCaptain():		# 必须由队长对话
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_CAPTAIN )
				return
			if player.getActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_SGMZ ):
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_DEGREE )	# 参与该活动的次数用完了
				return
			if len( player.getAllTeamMemberMB() ) != self.teamNum:	#队伍人数不匹配
				player.statusMessage( csstatus.DEFAULT_STATUS_MESSAGE,"unused" )
				return
			memberIsJoin = False
			for member in player.getAllTeamMemberMB():
				entity = KBEngine.entities.get( member.id, None )
				if entity and entity.id != player.id and entity.getActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_SGMZ ):
					memberIsJoin = True	
					break
			if memberIsJoin:		# 队伍中有人参与该活动的次数用完了
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_DIFF_DEGREE )
				return
			# 判断队伍中所有的玩家是否满足等级要求
			if player.level < self.diffLevel:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_LEVEL )
				return
			for member in player.getAllTeamMemberMB():
				entity = KBEngine.entities.get( member.id, None )
				if entity and entity.getLevel() < self.diffLevel:
					player.statusMessage( csstatus.CAMP_RANDOM_FIT_LEVEL )
					return
			#开始请求匹配
			player.teamMailbox.signUpSGMZ( player.base, player.getCamp(), player.getLevel(), player.getProfession() )
		else:	#必须组队参加
			player.statusMessage( csstatus.DEFAULT_STATUS_MESSAGE,"unused")
		player.sendGossipComplete( talkEntity.id )


class TAOpenTongSignUpUI(BaseNPCTalkAction.BaseNPCTalkAction):
	"""
	npc对话:打开帮会报名界面
	"""
	def __init__( self, actionData ):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongCampWarManager"].queryTongSignUpData( player.getCamp(), player.tongDBID, player.base )

class TAFHLTSignUp( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:报名烽火连天
	"""
	def __init__(self, actionData):
		"""
		"""
		self.diffLevel = int( actionData["param1"] )  	#最低要求等级
		self.punishBuff = int( actionData["param2"] )	#处于惩罚时间

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		# 判断玩家是否满足等级要求
		if player.level < self.diffLevel:
			player.statusMessage( csstatus.ACTIVITY_CAMP_FHLT_LEVEL_NOTIN_DIFFLEVEL )
			return
		# 判断玩家是否处于战场时间
		if len( player.findBuffsByBuffID( self.punishBuff ) ):
			player.statusMessage( csstatus.ACTIVITY_CAMP_FHLT_PUNISH_TIME )
			return
		# 开始请求匹配
		player.base.signUpFHLT()
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenWorkShopUI( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:打开工坊打造界面
	"""
	def __init__(self, actionData):
		"""
		"""
		if actionData["param1"] == "1":
			self._composeType = csdefine.COMPOSE_TOOL_NORMAL
		else:
			self._composeType = csdefine.COMPOSE_TOOL_TRIPOD

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.requestComposetDatas(self._composeType, talkEntity.id)
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenQuenchingEquipUI( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:打开淬炼界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__( self, actionData )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.client.CLIENT_OpenQuenchingEquip(talkEntity.id)
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenOriginPetUI( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:打开原兽界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.client.CLIENT_openOriginPetUI(talkEntity.id)
		player.sendGossipComplete( talkEntity.id )
		
class TAUpGradeJadeItem( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:升级玲珑玉令
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.upgradeJadeItem()

class TAEnterTongTianDaFirst( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:第一次进入通天塔试炼
	"""
	def __init__(self, actionData):
		"""
		"""
		self.needLevel = int( actionData[ "param1" ] )			#需要等级
		self.startLayer = int( actionData[ "param2" ] )			#起始层数
		self.jumpLayer = int( actionData[ "param3" ] )			#跳层数
		self.questID = int( actionData[ "param4" ] )			#试炼阶段任务ID

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		#等级限制
		if player.getLevel() < self.needLevel:
			player.statusMessage(csstatus.TTE_NEED_PLAYER_LEVEL,self.needLevel)
			return
		# 次数显示
		if player.isChallenge:
			player.statusMessage( csstatus.TTT_HAS_CHALLENGE_TODAY )
			return
		#队伍限制
		if player.isInTeam():
			player.statusMessage( csstatus.TTD_PLAYER_IS_IN_TEAM )
			return
		#选择试炼层数
		if player.getLevel() - self.jumpLayer <= self.startLayer:
			player.layerNumber = self.startLayer
		else:
			player.layerNumber = player.getLevel() - self.jumpLayer
		player.acceptQuest( self.questID )
		KBEngine.globalData["SpaceTongTianDaMgr"].onEnterTongTianDa( player.base, player.layerNumber )
		player.sendGossipComplete( talkEntity.id )
		
class TAEnterTongTianDa( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:继续进入通天塔试炼
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["SpaceTongTianDaMgr"].onEnterTongTianDa( player.base, player.layerNumber )
		player.sendGossipComplete( talkEntity.id )

class TAGetSalaryLN( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:领取俸禄（灵能）
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.getSalary()

class TACampActivityRandomFit( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:阵营战场随机匹配
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self._activityTypeList = [ int(i) for i in actionData["param1"].split("|") ]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		#战场匹配中，请勿重复报名
		if player.isHasMatchCampRandomFit():
			player.statusMessage( csstatus.ACTIVITY_CAMP_CANNOT_SIGNIN_AFTER_MATCHING )
			return

		randomTypeList = []
		# 单人匹配
		if not player.isInTeam():
			for i in  self._activityTypeList:
				if not player.isExceedActivityDegree( i ):
					randomTypeList.append(i)
			if not randomTypeList:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_DEGREE )
				return
			random.shuffle(randomTypeList)
			KBEngine.globalData["CampActivityRandomFitMgr"].randomFit_reqPerson( randomTypeList[0], player.base, player.playerDBID, player.getCamp(), player.getLevel(), player.getName() )
			player.sendGossipComplete( talkEntity.id )
			return

		# 队伍匹配
		TeamEntities = []
		memberDataList = []
		captain =  KBEngine.entities.get( player.captainID, None )
		for member in player.getAllTeamMemberMB():
			entity = KBEngine.entities.get( member.id, None )
			if not entity:
				continue
			TeamEntities.append(entity)
			tempDict = {}
			tempDict["playerMB"] = entity.base
			tempDict["playerDBID"] = entity.playerDBID
			tempDict["camp"] = entity.getCamp()
			tempDict["level"] = entity.getLevel()
			tempDict["name"] = entity.getName()
			memberDataList.append(tempDict)

		# 队长才能开启匹配
		if not player.isTeamCaptain():
			player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_CAPTAIN )
			return

		# 有离线队友，无法匹配
		for e in player.teamMembers:
			if e["mailbox"] == None:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_OFFLINE )
				return

		# 有死亡队友，无法匹配
		for entity in TeamEntities:
			if entity.isState(csdefine.ENTITY_STATE_DEAD):
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_DIE )
				return

		# 有非本阵营玩家，无法匹配
		for entity in TeamEntities:
			if captain.camp != entity.camp:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_CAMP )
				return

		# 有距离过远队友，无法匹配
		for entity in TeamEntities:
			if captain.position.distTo( entity.position ) > 50:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_FAR )
				return

		# 队伍成员不在同一等级，无法匹配
		for entity in TeamEntities:
			if int(captain.level/10) != int(entity.level/10):
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_LEVEL )
				return

		# 队长没有活动次数，无法匹配
		noDegree = True
		for i in  self._activityTypeList:
			if not player.isExceedActivityDegree( i ):
				noDegree = False
				break
		if noDegree:
			player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_DEGREE )
			return			

		# 队伍没有相同活动次数，无法匹配
		for i in  self._activityTypeList:
			flag = True
			for entity in TeamEntities:
				if entity.isExceedActivityDegree( i ):
					flag = False
					break
			if flag:
				randomTypeList.append(i)
		if not randomTypeList:
			player.statusMessage( csstatus.CAMP_RANDOM_FIT_DIFF_DEGREE )
			return

		random.shuffle(randomTypeList)
		KBEngine.globalData["CampActivityRandomFitMgr"].randomFit_reqTeam( randomTypeList[0], player.base, player.teamMailbox, memberDataList, player.getCamp(), player.getLevel() )		
		player.sendGossipComplete( talkEntity.id )

class TAQueryPublicActRecord( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:选择查看剩余活动次数选项弹出界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self._activityTypeList = [ int(i) for i in actionData["param1"].split("|") ]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		maxDegreeList = []
		degreeList = []
		for i in self._activityTypeList:
			maxDegreeList.append(player.getMaxDegree(i))
			degreeList.append(player.getActivityDegree(i))
		player.client.ShowPublicActRecordUI(self._activityTypeList, maxDegreeList, degreeList)
		player.sendGossipComplete( talkEntity.id )

class TAGetJade( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:消耗金钱和潜能，获取玲珑玉令
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.itemID = int( actionData["param1"])
		self.money = int( actionData["param2"])
		self.potential = int(actionData["param3"])
		
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.addJadeItem(self.itemID, self.money, self.potential)
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenLHMJShop( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:打开轮回秘境商店
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.shopID = actionData["param1"]
		
	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.requestLHMJShop(talkEntity.id, self.shopID)
		player.sendGossipComplete( talkEntity.id )

class TABHZBSignUp( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：帮会争霸报名
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.tongLevel = int( actionData["param1"] )
		self.costMoney = int( actionData["param2"] )
		self.needTongMemAmount = int( actionData["param3"] )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.tongMB:
			player.tongMB.signUPBHZB( self.tongLevel, csconst.BHZB_SIGN_UP_COST_MONEY, player.base, player.playerDBID, self.needTongMemAmount)
		player.sendGossipComplete( talkEntity.id )

class TAEnterStandMapSpace( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入沙盘大地图
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

		self._spaceName = actionData["param1"]
		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		self._position = KBEMath.Unreal2KBEnginePosition((eval(position[0]), eval(position[1]), eval(position[2])))
		self._direction = KBEMath.Unreal2KBEngineDirection(Math.Vector3(eval(direction[0]), eval(direction[1]), eval(direction[2])))

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		spaceObject = g_objFactory.getSpaceObject(self._spaceName)
		gotoArgs = spaceObject.getPackDomainData( player, {} )
		KBEngine.globalData["TrainSoldierGroundManager"].enterStandMap( player.base, self._position, self._direction, gotoArgs )
		player.sendGossipComplete( talkEntity.id )

class TALeaveDongFuSpace( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：回到洞府入口
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

		self._spaceName = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		for key, posStr in player.groundPosDict.items():
			player.gotoSpace( self._spaceName, posStr, Math.Vector3(0.0, 0.0, 0.0) )
			break
		player.sendGossipComplete( talkEntity.id )

class TAOpenLingQuanUI( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：打开灵泉建筑界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.requestLHMJLinqQuanUI(talkEntity.id)
		player.sendGossipComplete( talkEntity.id )

class TAOpenTrainSoldierGroundDetails( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc 对话: 打开练兵场信息界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		talkEntity.openTrainSoldierGroundDetails( player )
		player.sendGossipComplete( talkEntity.id )

class TAEnterTrainSoldierGround( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc 对话: 进入练兵场大本营
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TrainSoldierGroundManager"].enterHomeBarracks( player.base, player.playerDBID )
		player.sendGossipComplete( talkEntity.id )
		
class TAOpenTrainSoldierGroundQuestDetails( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc 对话: 打开练兵场任务界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.openLbcTaskUI(talkEntity.id)
		player.sendGossipComplete( talkEntity.id )

class TAEnterBHZBHomeBarracks( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入帮会争霸大本营
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player.tongMB:
			KBEngine.globalData["BHZBManager"].enterBHZBHomeBarracks( player.getCamp(),player.tongDBID,player.playerDBID,player.base )
		player.sendGossipComplete( talkEntity.id )

class TAEnterBHZBStandMapSpace( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入帮会争霸沙盘大地图
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

		self._spaceName = actionData["param1"]
		position = actionData["param2"].split(" ")
		direction = actionData["param3"].split(" ")
		self._position = KBEMath.Unreal2KBEnginePosition((eval(position[0]), eval(position[1]), eval(position[2])))
		self._direction = KBEMath.Unreal2KBEngineDirection(Math.Vector3(eval(direction[0]), eval(direction[1]), eval(direction[2])))

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		spaceObject = g_objFactory.getSpaceObject(self._spaceName)
		gotoArgs = spaceObject.getPackDomainData( player, {} )
		KBEngine.globalData["BHZBManager"].enterBHZBStandMap( player.getCamp(),player.tongDBID,player.playerDBID,player.base , self._position, self._direction, gotoArgs )
		player.sendGossipComplete( talkEntity.id )

class TAOpenNPCExtPointDetails( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc 对话: 打开帮会争霸据点信息界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		talkEntity.openNPCExtPointDetails( player )
		player.sendGossipComplete( talkEntity.id )
		
class TATrainSoldierGroundSave( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc 对话: 进入布防副本
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		
		self._spaceNameList = actionData["param1"].split("|")
		self._positionList = []
		self._directionList = []
		positionList = actionData["param2"].split("|")
		for position in positionList:
			posStr = position.split(" ")
			self._positionList.append( KBEMath.Unreal2KBEnginePosition((float(posStr[0]), float(posStr[1]), float(posStr[2]))) )
		directionList = actionData["param3"].split("|")
		for direction in directionList:
			dirStr = direction.split(" ")
			self._directionList.append( KBEMath.Unreal2KBEngineDirection((float(dirStr[0]), float(dirStr[1]), float(dirStr[2]))) )

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if talkEntity.occupyPlayerDBID == 0:
			player.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_NO_OCCUPY, "" )
		elif talkEntity.occupyPlayerDBID != player.playerDBID:
			player.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_NO_BELONGTO, "" )
		else:
			type = talkEntity.trainGroundType - 1
			player.gotoSpace( self._spaceNameList[type], self._positionList[type], self._directionList[type] )
		player.sendGossipComplete( talkEntity.id )
		
class TATrainSoldierGroundGetItem( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc 对话: 中 高级练兵场获取物品
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		
		self._midItemID = int( actionData["param1"])
		self._highItemID = int( actionData["param2"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		itemID = 0
		if talkEntity.occupyPlayerDBID == 0:
			player.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_NO_OCCUPY, "" )
		elif talkEntity.occupyPlayerDBID != player.playerDBID:
			player.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_NO_BELONGTO, "" )
		elif talkEntity.trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:
			player.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_NO_LOWER, "" )
			
		gainLocalTime = time.localtime( player.gainTSGItemTime )
		curLocalTime = time.localtime()
		if curLocalTime.tm_year == gainLocalTime.tm_year and curLocalTime.tm_mon == gainLocalTime.tm_mon and curLocalTime.tm_mdy == gainLocalTime.tm_mdy:
			player.statusMessage(csstatus.TRAIN_SOLDIER_GROUND_NO_LOWER, "" )
		
		elif talkEntity.trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL:
			itemID = self._midItemID
		elif talkEntity.trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL:
			itemID = self._highItemID
		
		if itemID:
			result,itemInst = player.addItemByID( itemID, 1, csdefine.ITEM_ADD_BY_TALKING )
			if result == csstatus.ITEM_GO_ON:
				player.gainTSGItemTime = time.time()
		player.sendGossipComplete( talkEntity.id )

class TAEnterDongFuSpace( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入洞府（要和是否阔以进入洞府的可见性搭配使用）
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

		self._spaceName = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		packArgs = {}
		packArgs["belongDBID"] = player.playerDBID
		player.gotoSpaceEnterPos( self._spaceName, packArgs )
		player.sendGossipComplete( talkEntity.id )

class TAOpenBHZBIntegralRank( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:打开帮会争霸积分
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["BHZBManager"].openBHZBIntegralRank( player.getCamp(), player.base )
		player.sendGossipComplete( talkEntity.id )

class TAOpenAllTrainGroundDetail( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：打开所有练兵场信息
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		lineNumber, index = player.getRoleOccupyTrainData()
		KBEngine.globalData["TrainSoldierGroundManager"].openAllGroundDetail( lineNumber, index, player, 1,talkEntity.id ) #默认打开1线所有练兵场信息
		player.sendGossipComplete( talkEntity.id )
		
class TAAcceptQiYuanQuest( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:接受奇缘任务
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.questID = int(actionData["param1"])

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if not player.acceptQuest(self.questID):
			ERROR_MSG("accept QiYuanQuest fail")
		
class TAEnterActivitySpaceCopy( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:进入活动副本（近战、远程吃鸡、攻城战）
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self._verifyData = actionData["param1"].split("|")		#对应visible中的条件，防止打开对话界面后，长时间等待后点击界面进入
		tempData = actionData["param2"].split("|")
		self._activityType = int(tempData[0])
		self._spaceTimes = int(tempData[1])
		self._spaceName = actionData["param3"]
		position = actionData["param4"].split(" ")
		direction = actionData["param5"].split(" ")
		self._position = KBEMath.Unreal2KBEnginePosition((eval(position[0]), eval(position[1]), eval(position[2])))
		self._direction = KBEMath.Unreal2KBEngineDirection(Math.Vector3(eval(direction[0]), eval(direction[1]), eval(direction[2])))

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if len(self._verifyData) >= 2 and KBEngine.globalData.get(self._verifyData[0], None) == self._verifyData[1]:
			if not player.isInTeam():
				if player.getActivityDegree(self._activityType) >= self._spaceTimes:
					player.statusMessage(csstatus.ACTIVITY_COPY_SPACE_FAIL_TIMES)
					player.sendGossipComplete( talkEntity.id )
					return
				
				player.gotoSpace( self._spaceName, self._position, self._direction )
				player.sendGossipComplete( talkEntity.id )
				return
			
			if not player.isTeamCaptain():
				player.statusMessage( csstatus.TEAM_NOT_CAPTAIN )
				player.sendGossipComplete( talkEntity.id )
				return
			
			members = []
			message = ""
			noCanEnterMembers = []
			for member in player.teamMembers:
				if member["mailbox"] == None:
					continue
					
				entity = KBEngine.entities.get(member["mailbox"].id, None)
				if entity is None or entity.spaceID != player.spaceID:
					continue
					
				if player.position.flatDistTo( entity.position ) > 50:
					continue
					
				if entity.getActivityDegree(self._activityType) >= self._spaceTimes:
					if message: message += "、"
					message += entity.getName()
					noCanEnterMembers.append(entity)
					continue
				
				members.append(entity)
			
			if len(noCanEnterMembers):
				noCanEnterMembers.extend(members)
				for member in noCanEnterMembers:
					member.statusMessage(csstatus.ACTIVITY_COPY_SPACE_FAIL_SOMEONE_TIMES, message)
					player.sendGossipComplete( talkEntity.id )
				return
			
			for entity in members:
				entity.gotoSpace( self._spaceName, self._position, self._direction )
				player.sendGossipComplete( talkEntity.id )
			return
		
		player.statusMessage(csstatus.ACTIVITY_COPY_SPACE_CLOSE)
		player.sendGossipComplete( talkEntity.id )
				
class TAOpenSignUpBHZBRankWin( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：打开帮会争霸报名排名界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["BHZBManager"].openSignUpBHZBRankWin( player.getCamp(),player.base )
		player.sendGossipComplete( talkEntity.id )	


class TAEnterSmallMiJing( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：进入小秘境
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.spaceScriptID = actionData["param1"]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		player.gotoSpaceEnterPos(self.spaceScriptID,{})
		talkEntity.destroySelf()
	
class TAEnterTongLueDuo( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	CST-11602 程序功能需求——帮会掠夺测试功能支持
	npc对话：进入帮会掠夺
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["TongPlunderManager"].enterTongPlunderSpace(player.base, player.playerDBID, player.tongDBID)
		
class TAOpenTongLueDuoSignUpWidget( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	CST-11602 程序功能需求——帮会掠夺测试功能支持
	npc对话：打开帮会掠夺战报名界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player:
			KBEngine.globalData["TongMgr"].openTongPlunderSignUpWnd(player.base, player.tongDBID)

class TAOpenRepairBuildUI( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：打开洞府建筑修复界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.buildType = int(actionData["param1"])		# 1:灵泉，2:工坊，3:乾坤鼎，4:兽栏，5:灵田

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if self.buildType in player.destroyBuilds:
			player.client.OpenRepairBuildUI( self.buildType, player.destroyBuilds[self.buildType] )
		else:
			ERROR_MSG("Can not repair build!as build is not destroy!!")

class TAOpenRepairBuildUI( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话：打开洞府正在修复建筑界面		
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.buildType = int(actionData["param1"])		# 1:灵泉，2:工坊，3:乾坤鼎，4:兽栏，5:灵田

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		self.repairBuildTime[buildType] = endTime
		player.client.OnBeginRepairDFBuild( buildType, player.repairBuildTime[self.buildType] )
		
class TAGetRewardByLevel( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	CST-11294 程序功能需求（23级）——潜能副本奖励规则
	npc对话：根据获取的等级发放奖励
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self.winTimes = int(actionData["param1"].strip())
		self.itemIDList = actionData["param2"].split("|")
		self.levelList = actionData["param3"].split("|")

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if player is None: 
			return
		
		if player.qianNengData.get("WinTimes", 0) < self.winTimes:
			return
		
		for index, temp in enumerate(self.levelList):
			lst = temp.split(":")
			level = player.level
			if player.isInTeam():
				entity = KBEngine.entities.get(player.captainID)
				level = entity.level if entity else player.level
			
			if int(lst[0]) <= level and level <= int(lst[1]):
				if index < len(self.itemIDList):
					result,itemInst = player.addItemByID( int(self.itemIDList[index]), 1, csdefine.ITEM_ADD_BY_TALKING )
					if result != csstatus.ITEM_GO_ON:
						player.statusMessage(result)
						return
		
		player.qianNengData["WinTimes"] = 0
		
class TAOpenMysteriousShop( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	打开神秘商人界面
	"""
	def __init__(self, actionData):
		"""
		"""
		pass

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		talkEntity.requestShopData(player.id)
		player.sendGossipComplete( talkEntity.id )	
		

class TAOpenJoinGCZWin( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	打开参加攻城战界面
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_SIGNUP in KBEngine.globalData.get( "GCZStatus",[] ):
			KBEngine.globalData["GCZManager"].openJoinGCZWin( talkEntity.getScript().getNumberGCZs(), talkEntity.getScript().getGCZStartTimes(), talkEntity.getScript().getGCZMaxJoinNums(), player.base, talkEntity.id )

		player.sendGossipComplete( talkEntity.id )

class TAMatchGCZ( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	进行匹配攻城战
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_MATCH in KBEngine.globalData.get( "GCZStatus",[] ):
			KBEngine.globalData["GCZManager"].reStartToMathGCZ( player.base, player.playerDBID )
		player.sendGossipComplete( talkEntity.id )

class TAEnterGCZ( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	进入攻城战
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_ENTER in KBEngine.globalData.get( "GCZStatus",[] ):
			teamID = 0
			if player.teamMailbox:
				teamID = player.teamMailbox.id
			KBEngine.globalData["GCZManager"].enterGCZ( player.base, player.playerDBID, teamID )
		player.sendGossipComplete( talkEntity.id )

class TAQueryAllBHZBIntegralData( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	查询帮会争霸历史战报
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		KBEngine.globalData["BHZBManager"].queryAllBHZBIntegralData( player.base, talkEntity.id )
		player.sendGossipComplete( talkEntity.id )



class TABattleActivitySignUp( BaseNPCTalkAction.BaseNPCTalkAction ):
	"""
	npc对话:团队竞技随机匹配
	"""
	def __init__(self, actionData):
		"""
		"""
		BaseNPCTalkAction.BaseNPCTalkAction.__init__(self, actionData)
		self._activityTypeList = [ int(i) for i in actionData["param1"].split("|") ]

	def do(self, dlgKey, player, talkEntity, args):
		"""
		"""
		#战场匹配中，请勿重复报名
		if player.isHasMatchBattleActivity():
			player.statusMessage( csstatus.ACTIVITY_CAMP_CANNOT_SIGNIN_AFTER_MATCHING )
			return

		randomTypeList = []
		# 单人匹配
		if not player.isInTeam():
			for i in  self._activityTypeList:
				if not player.isExceedActivityDegree( i ):
					randomTypeList.append(i)
			if not randomTypeList:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_DEGREE )
				return
			random.shuffle(randomTypeList)
			KBEngine.globalData["BattleActivityMgr"].signUpSingle( randomTypeList[0], player.base, player.playerDBID, player.getLevel()//10*10)
			player.sendGossipComplete( talkEntity.id )
			return

		# 队伍匹配
		TeamEntities = []
		memberDataList = []
		captain =  KBEngine.entities.get( player.captainID, None )
		for member in player.getAllTeamMemberMB():
			entity = KBEngine.entities.get( member.id, None )
			if not entity:
				continue
			TeamEntities.append(entity)
			tempDict = {}
			tempDict["playerBase"] = entity.base
			tempDict["playerDBID"] = entity.playerDBID
			memberDataList.append(tempDict)

		# 队长才能开启匹配
		if not player.isTeamCaptain():
			player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_CAPTAIN )
			return

		# 有离线队友，无法匹配
		for e in player.teamMembers:
			if e["mailbox"] == None:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_OFFLINE )
				return

		# 有死亡队友，无法匹配
		for entity in TeamEntities:
			if entity.isState(csdefine.ENTITY_STATE_DEAD):
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_DIE )
				return

		# 有距离过远队友，无法匹配
		for entity in TeamEntities:
			if captain.position.distTo( entity.position ) > 50:
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_FAR )
				return

		# 队伍成员不在同一等级，无法匹配
		for entity in TeamEntities:
			if int(captain.level/10) != int(entity.level/10):
				player.statusMessage( csstatus.CAMP_RANDOM_FIT_LEVEL )
				return

		# 队长没有活动次数，无法匹配
		noDegree = True
		for i in  self._activityTypeList:
			if not player.isExceedActivityDegree( i ):
				noDegree = False
				break
		if noDegree:
			player.statusMessage( csstatus.CAMP_RANDOM_FIT_NOT_DEGREE )
			return			

		# 队伍没有相同活动次数，无法匹配
		for i in  self._activityTypeList:
			flag = True
			for entity in TeamEntities:
				if entity.isExceedActivityDegree( i ):
					flag = False
					break
			if flag:
				randomTypeList.append(i)
		if not randomTypeList:
			player.statusMessage( csstatus.CAMP_RANDOM_FIT_DIFF_DEGREE )
			return

		random.shuffle(randomTypeList)
		KBEngine.globalData["BattleActivityMgr"].signUpTeam( randomTypeList[0], player.base, player.teamMailbox, memberDataList, player.getLevel()//10*10 )		
		player.sendGossipComplete( talkEntity.id )
