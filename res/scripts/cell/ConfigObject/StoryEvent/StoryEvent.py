# -*- coding: utf-8 -*-

# 过场动画事件脚本
import KST
import csdefine
import KBEDebug
import KBEMath
import Math
import random
import csstatus
from ConfigObject.JiYuanCfgLoader import g_jiYuanCfgLoader

class SEBase:
	def __init__( self, storyID, orderIndex ):
		self.storyID = storyID
		self.orderIndex = orderIndex
	
	def init( self, config ):
		pass
	
	def do( self, player ):
		pass

class SETeleportPlayerByClass( SEBase ):
	"""
	根据玩家职业传送到对应的地图
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.scriptIDList = []	# 战士|剑客|射手|法师
		self.posList = []
		self.dirList = []
	
	def init( self, config ):
		_scriptIDList = config["param1"].split("|")
		_posStrList = config["param2"].split("|")
		_dirStrList = config["param3"].split("|")
		
		if len( _scriptIDList ) == 4 and len( _posStrList ) == 4 and len( _dirStrList ) == 4:
			self.scriptIDList = _scriptIDList
			for posStr in _posStrList:
				tempList = posStr.split()
				kbePos = KBEMath.Unreal2KBEnginePosition( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
				self.posList.append( kbePos )
			
			for dirStr in _dirStrList:
				tempList = dirStr.split()
				kbeDir = KBEMath.Unreal2KBEngineDirection( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
				self.dirList.append( kbeDir )
		else:
			KBEDebug.ERROR_MSG( "StoryEvent config error:scriptID or pos or dir num error!(%s,%s)."%(self.storyID, self.orderIndex) )
	
	def do( self, player ):
		position = (0,0,0)
		direction = (0,0,0)
		if player.profession == csdefine.CLASS_FIGHTER:
			scriptID = self.scriptIDList[0]
			position = self.posList[0]
			direction = self.dirList[0]
		elif player.profession == csdefine.CLASS_SWORDMAN:
			scriptID = self.scriptIDList[1]
			position = self.posList[1]
			direction = self.dirList[1]
		elif player.profession == csdefine.CLASS_ARCHER:
			scriptID = self.scriptIDList[2]
			position = self.posList[2]
			direction = self.dirList[2]
		elif player.profession == csdefine.CLASS_MAGE:
			scriptID = self.scriptIDList[3]
			position = self.posList[3]
			direction = self.dirList[3]
		
		player.gotoSpace( scriptID, Math.Vector3(position), direction )

class SETeleportPlanesPlayerByClass( SEBase ):
	"""
	根据玩家职业传送到对应的位面
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.scriptIDList = []	# 战士|剑客|射手|法师
		self.posList = []
		self.dirList = []
	
	def init( self, config ):
		_scriptIDList = config["param1"].split("|")
		_posStrList = config["param2"].split("|")
		_dirStrList = config["param3"].split("|")
		
		if len( _scriptIDList ) == 4 and len( _posStrList ) == 4 and len( _dirStrList ) == 4:
			self.scriptIDList = _scriptIDList
			for posStr in _posStrList:
				tempList = posStr.split()
				kbePos =  ( float(tempList[0]), float(tempList[1]), float(tempList[2]) )
				self.posList.append( kbePos )
			
			for dirStr in _dirStrList:
				tempList = dirStr.split()
				kbeDir =  ( float(tempList[0]), float(tempList[1]), float(tempList[2]) )
				self.dirList.append( kbeDir )
		else:
			KBEDebug.ERROR_MSG( "StoryEvent config error:scriptID or pos or dir num error!(%s,%s)."%(self.storyID, self.orderIndex) )
	
	def do( self, player ):
		position = (0,0,0)
		direction = (0,0,0)
		if player.profession == csdefine.CLASS_FIGHTER:
			scriptID = self.scriptIDList[0]
			position = self.posList[0]
			direction = self.dirList[0]
		elif player.profession == csdefine.CLASS_SWORDMAN:
			scriptID = self.scriptIDList[1]
			position = self.posList[1]
			direction = self.dirList[1]
		elif player.profession == csdefine.CLASS_ARCHER:
			scriptID = self.scriptIDList[2]
			position = self.posList[2]
			direction = self.dirList[2]
		elif player.profession == csdefine.CLASS_MAGE:
			scriptID = self.scriptIDList[3]
			position = self.posList[3]
			direction = self.dirList[3]
		
		player.requestGotoSpacePlane( player.id, scriptID, Math.Vector3(position), direction )

class SESendAICommand( SEBase ):
	"""
	给周围某些scriptID的entity发送AI指令
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.radius = 0
		self.scriptIDs = []
		self.commandID = ""
	
	def init( self, config ):
		self.radius = int( config["param1"] )
		self.scriptIDs = config["param2"].split("|")
		self.commandID = config["param3"]
	
	def do( self, player ):
		entitys = player.entitiesInRangeExt( self.radius )
		for e in entitys:
			if not e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				if e.scriptID in self.scriptIDs:
					e.monsterAIOnCommand( player.id, "Role", self.commandID )
					
class SETeleportPlayer( SEBase ):
	"""
	传送玩家
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.scriptID = ""
		self.position = None
		self.direction = None
	
	def init( self, config ):
		self.scriptID = config["param1"]
		_pos = config["param2"].split()
		self.position = KBEMath.Unreal2KBEnginePosition( ( float(_pos[0]), float(_pos[1]), float(_pos[2]) ) )
		
		_dir = config["param3"].split()
		self.direction = KBEMath.Unreal2KBEngineDirection( ( float(_dir[0]), float(_dir[1]), float(_dir[2]) ) )
	
	def do( self, player ):
		player.gotoSpace( self.scriptID, Math.Vector3(self.position), self.direction )
		
class SETeleportPlanesPlayer( SEBase ):
	"""
	传送玩家进入位面
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.scriptID = ""
		self.position = None
		self.direction = None
	
	def init( self, config ):
		self.scriptID = config["param1"]
		_pos = config["param2"].split()
		self.position =  ( float(_pos[0]), float(_pos[1]), float(_pos[2]) )
		
		_dir = config["param3"].split()
		self.direction =  ( float(_dir[0]), float(_dir[1]), float(_dir[2]) )
	
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity and spaceEntity.scriptID == self.scriptID:
			player.position = Math.Vector3(KBEMath.Unreal2KBEnginePosition(self.position))
			player.direction = Math.Vector3(KBEMath.Unreal2KBEngineDirection(self.direction))
		else:
			player.requestGotoSpacePlane( player.id, self.scriptID, Math.Vector3(self.position), self.direction )

class SESpaceConditionChange( SEBase ):
	"""
	给副本发送通知
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.key = ""
	
	def init( self, config ):
		self.key = config["param1"]
	
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "STORY", self.storyID, self.key, "" )
			KBEDebug.DEBUG_MSG("Story notify space condition change. storyID id:%s. "%self.storyID, spaceEntity.id, self.key )

class SESpaceConditionChangeByClass( SEBase ):
	"""
	通过职业给副本发送通知
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.key = []

	def init( self, config ):
		_key = config["param1"].split("|")
		if len(_key) == 4:
			self.key = _key
		else:
			KBEDebug.ERROR_MSG( "StoryEvent config error:key is error!(%s,%s)."%(self.storyID, self.orderIndex))

	def do( self, player ):
		key = ""
		if player.profession == csdefine.CLASS_FIGHTER:
			key = self.key[0]
		elif player.profession == csdefine.CLASS_SWORDMAN:
			key = self.key[1]
		elif player.profession == csdefine.CLASS_ARCHER:
			key = self.key[2]
		elif player.profession == csdefine.CLASS_MAGE:
			key = self.key[3]
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "STORY", self.storyID, key, "" )
			KBEDebug.DEBUG_MSG("Story notify space condition change. storyID id:%s. "%self.storyID, spaceEntity.id, key )

class SEPlayerGetItem( SEBase ):
	"""
	播放镜头的玩家获得物品
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self._itemList = {}
	
	def init( self, config ):
		itemList = config["param1"].split("|")
		for i in itemList:
			_item = i.split(":")
			self._itemList[int(_item[0])] = int(_item[1])
	
	def do( self, player ):
		for itemID, amount in self._itemList.items():
			player.addItemByID( itemID, amount )


class SEUseSkillToPlayer( SEBase ):
	"""
	对播放镜头的玩家使用技能
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.skillID = 0
	
	def init( self, config ):
		self.skillID = int( config["param1"] )
	
	def do( self, player ):
		if self.skillID:
			player.useSkillToEntity( self.skillID, player.id )

class SERandomTeleportPlayer( SEBase ):
	"""
	随机一个副本传送玩家
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.scriptIDList = []	# 多个副本随机
		self.posList = []
		self.dirList = []
	
	def init( self, config ):
		_scriptIDList = config["param1"].split("|")
		_posStrList = config["param2"].split("|")
		_dirStrList = config["param3"].split("|")
		
		if len( _scriptIDList ) == len( _posStrList ) and len( _posStrList ) == len( _dirStrList ):
			self.scriptIDList = _scriptIDList
			for posStr in _posStrList:
				tempList = posStr.split()
				kbePos = KBEMath.Unreal2KBEnginePosition( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
				self.posList.append( kbePos )
			
			for dirStr in _dirStrList:
				tempList = dirStr.split()
				kbeDir = KBEMath.Unreal2KBEngineDirection( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
				self.dirList.append( kbeDir )
		else:
			KBEDebug.ERROR_MSG( "StoryEvent config error:scriptID or pos or dir num error!(%s,%s)."%(self.storyID, self.orderIndex) )
	
	def do( self, player ):
		position = (0,0,0)
		direction = (0,0,0)
		index = random.randint(0, len(self.scriptIDList) - 1)
		scriptID = self.scriptIDList[index]
		position = self.posList[index]
		direction = self.dirList[index]
		
		player.gotoSpace( scriptID, Math.Vector3(position), direction )

class SETriggerSpaceEffect( SEBase ):
	"""
	播放镜头触发空间效果
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.effectList = []
		self.IsDeleteList = []
	
	def init( self, config ):
		if config["param1"]:
			self.effectList = [ int(i) for i in config["param1"].split("|")]
		if config["param2"]:
			self.IsDeleteList = [ int(i) for i in config["param2"].split("|")]
	
	def do( self, player ):
		player.replaceSpaceEffect( self.IsDeleteList, self.effectList )

class SEMagicMazeEnterChildSpace( SEBase ):
	"""
	幻阵迷宫 进入子副本
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			if player.isInTeam():	#玩家在队伍里
				if player.isTeamCaptain():#必须是队长才能对话
					spaceEntity.getScript().onStartTeleportToChild( spaceEntity,player,csdefine.SPACE_BELONG_TEAM )
					spaceEntity.getScript().onStopOtherPlayerFly( spaceEntity )
			else:
				spaceEntity.getScript().onStartTeleportToChild( spaceEntity,player,csdefine.SPACE_BELONG_PERSON )

class SEMagicMazeEnterParentSpace( SEBase ):
	"""
	幻阵迷宫 进入父副本
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.spaceScriptID = ""
	
	def init( self, config ):
		if config["param1"]:
			self.spaceScriptID = config["param1"]
		
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity.scriptID == self.spaceScriptID:
			spaceEntity.getScript().onStartTeleportToParent( spaceEntity )
		else:
			#player.client.AgainNotifySpaceData(spaceEntity.scriptID)
			pass

class SESelectOperationMode( SEBase ):
	"""
	玩家新建角色首次进入游戏时，通知弹出操作模式引导界面
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		
	def do( self, player ):
		player.client.FirstEnterGameNotify()

class SEAddBuffToPlayer( SEBase ):
	"""
	给玩家加上若干Buff
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )

	def init( self, config ):
		self.buffIDs = [ int(i) for i in config["param1"].split("|") ]
		
	def do( self, player ):
		for buffID in self.buffIDs:
			player.addBuff( player, buffID )

class SERingTaskEnterChildScene( SEBase ):
	"""
	环任务秘境 进入子副本
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onStartTeleportChildScene( spaceEntity, player )

class SERingTaskEnterParentScene( SEBase ):
	"""
	环任务秘境 进入父副本
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onStartTeleportParentScene( spaceEntity, player )

class SERingTaskTeleportPlayer( SEBase ):
	"""
	环任务秘境,主场景与主场景之间的切换
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.scriptID = ""
		self.position = None
		self.direction = None
	
	def init( self, config ):
		self.scriptID = config["param1"]
		_pos = config["param2"].split()
		self.position = KBEMath.Unreal2KBEnginePosition( ( float(_pos[0]), float(_pos[1]), float(_pos[2]) ) )
		
		_dir = config["param3"].split()
		self.direction = KBEMath.Unreal2KBEngineDirection( ( float(_dir[0]), float(_dir[1]), float(_dir[2]) ) )
	
	def do( self, player ):
		player.client.OnNotifyPreloadSpace( self.scriptID, 0 )
		player.gotoSpace( self.scriptID, Math.Vector3(self.position), self.direction )

class SERingTaskQusetIDTeleportPlayer( SEBase ):
	"""
	环任务秘境 按玩家身上环任务ID去选择传送点
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self.questIDList = []
		self.scriptIDList = []	
		self.posList = []
		self.dirList = []

	def init( self, config ):
		_questIDList = config["param1"].split("|")
		_scriptIDList = config["param2"].split("|")
		_posStrList = config["param3"].split("|")
		_dirStrList = config["param4"].split("|")

		if len( _scriptIDList ) == len( _posStrList ) and len( _posStrList ) == len( _dirStrList ) and len( _dirStrList ) == len(_questIDList):
			self.scriptIDList = _scriptIDList
			self.questIDList = _questIDList
			for posStr in _posStrList:
				tempList = posStr.split()
				kbePos = KBEMath.Unreal2KBEnginePosition( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
				self.posList.append( kbePos )
			
			for dirStr in _dirStrList:
				tempList = dirStr.split()
				kbeDir = KBEMath.Unreal2KBEngineDirection( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
				self.dirList.append( kbeDir )	

	def do( self, player ):
		questID = player.loopQuest["loopQuestList"][0]
		if str(questID) in self.questIDList:
			index = self.questIDList.index(questID)
			player.gotoSpace( self.scriptIDList[index], Math.Vector3(self.posList[index]), self.dirList[index] )
		else:
			KBEDebug.ERROR_MSG( "StoryEvent config error:player questID not in questIDList ")

class SEOnEnterTrainSoldierMode( SEBase ):
	"""
	练兵场沙盘大地图 重新进入练兵场模式
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		
	def do( self, player ):
		currentSpace = player.getCurrentSpace()
		if currentSpace and currentSpace.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			armLength, cameraRotation = currentSpace.getScript().getEnterTrainGrounModeData()
			if player.getClient():
				player.getClient().CLIENT_OnEnterTrainSoldierGround( armLength, cameraRotation )

class SEOnLbcTaskStoryEnd( SEBase ):
	"""
	练兵场任务 镜头结束恢复练兵场任务操作模式
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		
	def do( self, player ):
		currentSpace = player.getCurrentSpace()
		armLength = currentSpace.getScript().armLength
		cameraRotation = currentSpace.getScript().cameraRotation
		if player.getClient():
			player.getClient().StartRoleLbcTaskOperation(armLength, cameraRotation)
			
class SESelectJiYuanSpaceAndPlaySound( SEBase ):
	"""
	CST-12205 机缘玩法
	选择地图并播放相应的语音
	"""
	def __init__( self, storyID, orderIndex ):
		SEBase.__init__( self, storyID, orderIndex )
		self._groupID = 0
		
	def init( self, config ):
		self._groupID = int(config["param1"])
		
	def do( self, player ):
		currID = player.queryTemp("JiYuanXinXi",None)
		currData = g_jiYuanCfgLoader.getCfgByID(currID)
		if currData is None or currData["groupID"] != self._groupID: #数据不存在或者数据不匹配天机秘图
			probability = 0
			_probability = random.uniform(0, 100)
			datas = g_jiYuanCfgLoader.getAllData()
			for id, data in datas.items():
				if data["groupID"] != self._groupID:
					continue
				probability += data["ratio"]
				if probability >= _probability:
					player.setTemp("JiYuanXinXi",id)
					currID = id
					currData = data
					break
		if currData["groupID"] == self._groupID:
			player.showMessagePlaySound(currData["sound"])
			isGossipEnter = player.queryTemp("JIYUANDATA", {}).get("GossipEnter", False)
			if not isGossipEnter:
				return
			spaceObject = KST.g_objFactory.getSpaceObject( currData["scriptID"] )
			if not spaceObject:
				return
			curSpace = player.getCurrentSpace()
			for role in curSpace._spaceRoles:
				role.statusMessage(csstatus.LHMJ_JYWF_NOTICE_ALL, player.playerName, curSpace.getScript().getSpaceName(), spaceObject.getSpaceName())
			return

class SEPlayVideoWithEnterJiYuanSpace( SEBase ):
	"""
	CST-12205 机缘玩法(进入)
	播放相应的视频（替换loading界面）
	"""
	def do( self, player ):
		id = player.queryTemp("JiYuanXinXi", None)
		if id is None:
			KBEDebug.ERROR_MSG("JiYuanXinXi is None %s" %(player.id))
			return
		
		data = g_jiYuanCfgLoader.getCfgByID(id)
		if data is None:
			KBEDebug.ERROR_MSG("not found config %s" %(id))
			return
		
		player.client.OnPlayVideo(data["enterVideo"])
	
class SEPlayVideoWithLeaveJiYuanSpace( SEBase ):
	"""
	CST-12205 机缘玩法(离开)
	播放相应的视频（替换loading界面）
	"""
	def do( self, player ):
		spaceEntity = player.getCurrentSpace()
		if spaceEntity is None:
			return
		
		id = spaceEntity.createArgs.get("JiYuanXinXi", 0)
		if id is None:
			KBEDebug.ERROR_MSG("JiYuanXinXi is None %s" %(player.id))
			return
		
		data = g_jiYuanCfgLoader.getCfgByID(id)
		if data is None:
			KBEDebug.ERROR_MSG("not found config %s" %(id))
			return
		
		player.client.OnPlayVideo(data["leaveVideo"])