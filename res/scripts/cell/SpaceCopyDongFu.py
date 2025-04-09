# -*- coding: utf-8 -*-

from SpaceCopy import SpaceCopy
import KBEngine
import KBEDebug
import time
import csconst
import csdefine
import Math
import Const
import csstatus
from LunHuiMiJin.DFGuard import Datas as DFGuardDatas


class SpaceCopyDongFu( SpaceCopy ):
	"""
	洞府
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.belongDBID = self.createArgs.get( "belongDBID", 0 ) # 归宿玩家DBID
		self.isActivetyStart =  False
		self.buildLevel = {}							# 建筑等级
		self.isCapture = False							# 是否被攻陷
		self.battleFormationID = 0						# 阵图id
		self.trapList = []								# 陷阱符玉id
		self.ghostList = []								# 傀儡id
		self.destroyBuild = []							# 需要修复的建筑(建筑类型)
		self.isDestroyBuild = []						# 刚被破坏的建筑
		self.guardScriptIDList = []						# 守卫scriptID
		self.guardType = []								# 守卫类型
		self.batteryScriptIDList = []					# 火炮的scriptID
		self.monsterCorralMap = {}						# 兽栏 栅栏 格式如 { index : monsterID }
		self.petCorralMap = {}							# 兽栏 幻兽数据 格式如{ index : {"uid":uid, "scriptID":id, "bEvolution":bool}}
		self.protectDeadNum = 0							# 守方死亡次数
		self.attackDeadNum = 0							# 攻方死亡次数
		self.activetyBeginTime = 0						# 活动开始时间
		self.tempSign = False							# 临时标记
		
	def addEntityMailBoxRecord( self, scriptID, entityCell ):
		"""
		增加entityCell 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityCell )
		if scriptID in self.getScript().attackEntityScriptIDs:
			entityCell.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		else:
			entityCell.setBelongSide( csdefine.BELONG_SIDE_PROTECT )
		spaceObj = self.getScript()
		if scriptID in spaceObj.batteryScriptIDs:
			self.batteryScriptIDList.append( scriptID )
		
	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		SpaceCopy.delEntityMailBoxRecord( self, scriptID, entityMailBox )
		if scriptID in self.batteryScriptIDList:
			self.batteryScriptIDList.remove( scriptID )

	def registSpecialMonsterToSpace( self, type, entityID, scriptID ):
		"""
		AI触发将怪物注册到space
		使用这种方式，避免 addEntityMailBoxRecord中字符串比较
		"""
#		if type == 1:
#			self.guardScriptIDList.append( scriptID )				暂时不用这种方式，因为ai那边通知过来，有点晚了！
		if type == 3:
			if not entityID in self.ghostList:
				self.ghostList.append( entityID )
		
	def unRegistSpecialMonsterToSpace( self, type, entityID, scriptID ):
		"""
		取消注册
		"""
		if type == 1:
			if scriptID in self.guardScriptIDList:
				self.guardScriptIDList.remove( scriptID )
				KBEngine.globalData["SpaceLunHuiMiJinMgr"].onGuardDead( self.belongDBID )
		elif type == 3:
			if entityID in self.ghostList:
				self.ghostList.remove( entityID )
		
	def registTrapToSpace( self, trapID ):
		""""""
		self.trapList.append( trapID )
		
	def unRegistTrapToSpace( self, trapID ):
		""""""
		self.trapList.remove( trapID )
		
	def getTrapNum( self ):
		""""""
		return len( self.trapList )
		
	def createBattleformation( self, scriptID, insPos, insDir ):
		"""
		define method
		创建阵图entity
		"""
		param = {}
		param["belongDBID"] = self.belongDBID
		param["spawnPos"] = insPos
		param["spawnDir"] = insDir
		entity = self.createEntityByScriptID(scriptID, insPos, insDir, param)
		if entity:
			self.battleFormationID = entity.id
			
	def destroyBattleformation( self ):
		"""
		define method
		销毁阵图
		"""
		entityObject = KBEngine.entities.get( self.battleFormationID )
		if entityObject:
			entityObject.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (entityObject.id, entityObject.scriptID, "destroySelf"), entityObject)
		
	def onRequestSpaceNPCInfo( self, spaceData ):
		"""
		<define method>
		请求保存的数据回调
		"""
		scriptIDList = self.getScript().batteryScriptIDs
		for data in spaceData:
			if "lifeTime" in data["createArgs"] and time.time() >= data["createArgs"]["lifeTime"]:
				continue
			data["createArgs"].update( {"belongDBID" : self.belongDBID} )
			data["createArgs"].update( {"spawnPos" : data["position"]} )
			data["createArgs"].update( {"spawnDir" : data["direction"]} )
			monster = self.createEntityByScriptID( data["scriptID"], data["position"], data["direction"], data["createArgs"])
			if monster.isEntityFlagExt( csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_MENU ):
				self.guardScriptIDList.append( monster.scriptID )
		self.delayInitEnityObject()
			
	def onRequestDFDatas( self, buildLevel, ltDatas, destroyBuild, guardType, petDatas, hasGuardRTime ):
		"""
		<define method>
		请求数据回调
		"""
		self.buildLevel = buildLevel
		self.destroyBuild = destroyBuild
		self.guardType = guardType
		self.onInitLingTianData( ltDatas )
		self.onInitPetCorral( petDatas )
		self.addTimerCallBack(3.0, "onInitDetroyBuild", ())				#因为怪物的状态还没变为自由状态
		if not hasGuardRTime:
			self.onGuardRevive()
		self.delayInitEnityObject()
		
	def onInitLingTianData( self, ltDatas = [] ):
		"""灵田初始化"""
		level = self.buildLevel[csdefine.LHMJ_BUIILD_LING_TIAN]
		num = csconst.LHMJ_LING_TIAN_LEVEL_NUM_MAP[level]
		for index in range(num):
			scriptID = csconst.LHMJ_LING_TIAN_SCRIPTS[index]
			ltSpellBoxs = self.getEntityMailBoxRecord( scriptID )
			for spellBox in ltSpellBoxs:
				if index > csconst.LHMJ_LING_TIAN_LEVEL_NUM_MAP[1] - 1:				# 初始灵田不添加标记位
					spellBox.removeFlag( csdefine.FLAG_UNVISIBLE )
				for data in ltDatas:
					if data.scriptID == scriptID:
						spellBox.initLTData( data )
						
	def delayInitEnityObject( self ):
		"""延迟初始化 entity"""
		if self.tempSign:
			del self.tempSign
		else:
			self.tempSign = True
			return
		self.onInitBatteryData()
		
	def onInitBatteryData( self ):
		"""初始化火炮"""
		spaceObj = self.getScript()
		if len( spaceObj.batteryPosList ) > len( self.batteryScriptIDList ):
			isValid = False if self.batteryScriptIDList else True
			for i in range( len(spaceObj.batteryPosList) - len(self.batteryScriptIDList) ):
				pos = spaceObj.batteryPosList[i]
				dir = spaceObj.batteryDirList[i]
				if isValid or self.isValidBatteryPos( pos ):
					param = {}
					param["belongDBID"] = self.belongDBID
					param["spawnPos"] = pos
					param["spawnDir"] = dir
					self.createEntityByScriptID( spaceObj.batteryScriptID, pos, dir, param)
					
	def isValidBatteryPos( self, pos ):
		"""
		刷新位置是否有效，
		防止在同一位置重复刷
		"""
		for sID in self.batteryScriptIDList:
			for entityCell in self.getEntityMailBoxRecord( sID ):
				if entityCell.position.distTo( pos ) <= 1:
					return False
		return True
		
	def onGuardRevive( self ):
		"""守卫复活"""
		typeLen = len( self.guardType )
		scriptIDLen = len( self.guardScriptIDList )
		if typeLen == scriptIDLen:
			return
		if typeLen < scriptIDLen:
			KBEDebug.ERROR_MSG("onInitGuard err!! guardType(%d） is smaller than guardScriptIDList(%d)"%(typeLen, scriptIDLen))
			return
		
		level = self.buildLevel[csdefine.LHMJ_BUIILD_LING_QUAN]
		data = DFGuardDatas[level]
		temp = list( self.guardScriptIDList )
		spaceObj = self.getScript()
		for type in self.guardType:
			scriptID = data[Const.DONG_FU_GUARD_TYPE[type]]
			if scriptID in temp:
				temp.remove( scriptID )
				continue
			pos = spaceObj.getGuardPos()
			dir = Math.Vector3()
			param = {}
			param["belongDBID"] = self.belongDBID
			param["spawnPos"] = pos
			param["spawnDir"] = dir
			self.createEntityByScriptID( scriptID, pos, dir, param )
			self.guardScriptIDList.append( scriptID )
	
	def changeGuardType( self, oldType, newType, entityID, scriptID ):
		"""改变守卫类型"""
		self.guardType.remove( oldType )
		self.guardType.append( newType )
		# 需要手动取消注册，因为是程序这边销毁了，策划ai那边无法走这里
		if scriptID in self.guardScriptIDList:
			self.guardScriptIDList.remove( scriptID )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].changeGuardType( self.belongDBID, oldType, newType )
	
	def getGuardIDList( self ):
		""""""
		temp = []
		for scriptID in self.guardScriptIDList:
			for ent in self.getEntityMailBoxRecord(scriptID):
				temp.append(ent.id)
		return temp
	
	def updateGuardObject( self, level ):
		"""建筑升级，更新守卫"""
		spaceObj = self.getScript()
		for scriptID in self.guardScriptIDList:
			for guardObj in self.getEntityMailBoxRecord( scriptID ):
				guardObj.destroySelf()
		self.guardScriptIDList = []
		
		if level in csconst.ADD_GUARD_LEVEL:
			self.guardType.append( csdefine.DONG_FU_GUARD_TYPE_DEFAULT )
		data = DFGuardDatas[level]
		for type in self.guardType:
			scriptID = data[Const.DONG_FU_GUARD_TYPE[type]]
			pos = spaceObj.getGuardPos()
			dir = Math.Vector3()
			param = {}
			param["belongDBID"] = self.belongDBID
			param["spawnPos"] = pos
			param["spawnDir"] = dir
			self.createEntityByScriptID( scriptID, pos, dir, param )
			self.guardScriptIDList.append( scriptID )
	
	def onInitDetroyBuild( self ):
		"""初始化 被破坏的建筑"""
		for buildType in self.destroyBuild:
			if not buildType in Const.DONG_FU_BUILD_MAP_MONSTER:
				continue
			scriptID = Const.DONG_FU_BUILD_MAP_MONSTER[buildType]
			for monsterEnt in self.getEntityMailBoxRecord( scriptID ):
				monsterEnt.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (monsterEnt.id, monsterEnt.scriptID, "destroyBuild"), monsterEnt)
	
	def onInitPetCorral( self, petDatas ):
		"""初始化兽栏"""
		spaceObj = self.getScript()
		posList = spaceObj.petCorralPosList
		dir = spaceObj.petCorralDir
		for index, data in enumerate( petDatas ):
			if len(posList) <= index:
				KBEDebug.ERROR_MSG("pet corral err!!as pos len(%d) less than index(%d)"%(len(posList), index))
				return
			if not data["quality"] in spaceObj.petCorralScriptIDs:
				KBEDebug.ERROR_MSG("Can not find scriptID in space::petCorralScriptIDs by pet quality(%d)"%data["quality"], spaceObj.petCorralScriptIDs)
				break
			monsterScriptID = spaceObj.petCorralScriptIDs[data["quality"]]
			param = {}
			param["belongDBID"] = self.belongDBID
			param["spawnPos"] = posList[index]
			param["spawnDir"] = dir
			monster = self.createEntityByScriptID( monsterScriptID, posList[index], dir, param)
			self.monsterCorralMap[index] = monster.id
			self.petCorralMap[index] = data
			
		# 因为玩家onEnter，进入副本 太早了！导致 通知客户端数据为空
		petData = self.getPetCorralData()
		if petData:
			for playerRole in self._spaceRoles:
				playerRole.client.CLIENT_showOriginPetModel( petData )
	
	def getPetCorralData( self ):
		""""""
		temp = []
		for index, datas in self.petCorralMap.items():
			tempDict = dict(datas)
			tempDict.pop("quality")
			tempDict["index"] = index
			temp.append(tempDict)
		return temp
		
	def onAddOriginPet( self, petData ):
		"""
		define method
		兽栏 添加幻兽
		"""
		for index in range(6):
			if index in self.petCorralMap:
				continue
			spaceObj = self.getScript()
			if not petData["quality"] in spaceObj.petCorralScriptIDs:
				KBEDebug.ERROR_MSG("Can not find scriptID in space::petCorralScriptIDs by pet quality(%d)"%petData["quality"], spaceObj.petCorralScriptIDs)
				return
			monsterScriptID = spaceObj.petCorralScriptIDs[petData["quality"]]
			posList = spaceObj.petCorralPosList
			dir = spaceObj.petCorralDir
			param = {}
			param["belongDBID"] = self.belongDBID
			param["spawnPos"] = posList[index]
			param["spawnDir"] = dir
			monster = self.createEntityByScriptID( monsterScriptID, posList[index], dir, param)
			self.monsterCorralMap[index] = monster.id
			self.petCorralMap[index] = petData
			tempDict = dict(petData)
			tempDict.pop("quality")
			tempDict["index"] = index
			for playerCell in self._spaceRoles:
				playerCell.client.CLIENT_OnAddOriginPetModel( tempDict )
			return
		
	def onRemoveOriginPet( self, uid, directDel ):
		"""
		define method
		兽栏 移除幻兽
		"""
		for index, petData in self.petCorralMap.items():
			if petData["uid"] != uid:
				continue
			self.petCorralMap.pop( index )
			monster = KBEngine.entities.get( self.monsterCorralMap.pop(index) )
			if monster:
				monster.destroySelf()
			for playerCell in self._spaceRoles:
				playerCell.client.CLIENT_OnRemoveOriginPetModel( index, directDel )
			return
	
	def onExChangeOriginPet( self, petData, uid ):
		"""
		define method
		兽栏 交换幻兽
		"""
		index = None
		for index, data in self.petCorralMap.items():
			if data["uid"] != uid:
				continue
			self.petCorralMap[index] = data
			tempDict = dict(data)
			tempDict["index"] = index
			for playerCell in self._spaceRoles:
				playerCell.client.CLIENT_OnExChangeOriginPetModel( tempDict, index )
			return
	
	def onPetCorralDestroy( self, playerRole, monsterID, dropPro ):
		"""兽栏被玩家击毁"""
		petIndex = None
		for index, id in self.monsterCorralMap.items():
			if id == monsterID:
				petIndex = index
				break
		if petIndex == None:
			KBEDebug.ERROR_MSG("onPetCorralDestroy  can not find monster(%d)"%monsterID)
			return
		uid = self.petCorralMap[petIndex]["uid"]
		srcPlayer = None
		for player in self._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
				srcPlayer = player
				break
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].onPetCorralDestroy( srcPlayer, self.belongDBID, uid, playerRole, dropPro )
	
	def onPlayerUngradeBuild( self, rolePlayer, buildType, level ):
		"""玩家升级建筑"""
		self.buildLevel[buildType] = level
		if buildType == csdefine.LHMJ_BUIILD_LING_TIAN:
			self.onInitLingTianData()
		elif buildType == csdefine.LHMJ_BUIILD_SHOU_LAN:
			pass
		elif buildType == csdefine.LHMJ_BUIILD_LING_QUAN:
			self.updateGuardObject( level )
	
	def onBuildRepair( self, buildType ):
		"""
		define method
		某建筑修复完成
		"""
		if not buildType in self.destroyBuild:
			return
		if not buildType in Const.DONG_FU_BUILD_MAP_MONSTER:
			return
		scriptID = Const.DONG_FU_BUILD_MAP_MONSTER[buildType]
		for monsterEnt in self.getEntityMailBoxRecord( scriptID ):
			monsterEnt.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (monsterEnt.id, monsterEnt.scriptID, "repairedBuild"), monsterEnt)
	
	def onChallengeActiveStart( self ):
		"""
		define method
		争夺(掠夺战)活动开启
		"""
		self.isActivetyStart = True
		self.activetyBeginTime = int(time.time())
		self.getScript().onChallengeActiveStart( self )
		
	def onChallengeCheckStage( self ):
		"""
		define method
		检测副本阶段（废弃，暂留）
		"""
		pass
		
	def onChallengeActiveEnd( self, isChallengeActive ):
		"""
		define method
		争夺活动结束
		"""
		self.isActivetyStart = False
		if len( self._spaceRoles ) == 0:
			self.closeSpace()
	
	def onActiveResult( self, isChallengeActive, result ):
		"""活动结果"""
		self.isActivetyStart = False
		if isChallengeActive and result:
			self.isCapture = True
		self.getScript().onActiveResult( self, isChallengeActive, result )
	
	def onOccupyPlayerDFCallBack( self ):
		"""
		占领回调
		"""
		for role in self._spaceRoles:
			role.gotoExitSpacePos()
	
	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		if self.isActivetyStart:				# 活动期间，副本不关闭
			return
			
		if self.belongDBID:
			spaceNPCInfo = {}
			spaceNPCInfo["belongDBID"] = self.belongDBID
			spaceNPCInfo["spaceScriptID"] = self.scriptID
			spaceNPCInfo["spaceDatas"] = []
			for id in self.trapList:
				entityObject = KBEngine.entities.get( id, None )
				if entityObject and entityObject.lifeTime - time.time() >= Const.SAVE_TRAP_MORE_TIME:
					temp = {}
					temp["scriptID"] = entityObject.scriptID
					temp["position"] = entityObject.position
					temp["direction"] = entityObject.direction
					temp["createArgs"] = { "lifeTime" : entityObject.lifeTime }
					spaceNPCInfo["spaceDatas"].append(temp)
					
			scriptIDList = self.batteryScriptIDList
			scriptIDList.extend( self.guardScriptIDList )
			recordList = []
			for sID in scriptIDList:
				if sID in recordList:
					continue
				else:
					recordList.append( sID )
				if sID in self.entityMailBoxRecord:
					for entityCell in self.entityMailBoxRecord[sID]:
						temp = {}
						temp["scriptID"] = sID
						temp["position"] = entityCell.position
						temp["direction"] = entityCell.direction
						temp["createArgs"] = {  }
						spaceNPCInfo["spaceDatas"].append(temp)
			KBEngine.globalData["TrainSoldierGroundManager"].saveSpaceNPCInfo( spaceNPCInfo )
		
		SpaceCopy.closeSpace( self )
		
	def onDFBuildHPChange( self, buildName ):
		"""洞府建筑血量改变"""
		for player in self._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
				player.statusMessage( csstatus.DONG_FU_BUILD_BEING_ATTACK, buildName)
				return
				
	def onDFBuildDestroy( self, buildType ):
		"""洞府建筑被打坏"""
		self.isDestroyBuild.append( buildType )
		
