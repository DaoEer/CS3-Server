# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from SmartImport import smartImport
from ObjectScript.SpellBox import SpellScriptBase
import csstatus

class SpellBox( SpellScriptBase.SpellScriptBase ):
	def __init__( self ):
		SpellScriptBase.SpellScriptBase.__init__( self )
		self.gossipConditions = []
		self.gossipResults = []
		self.listenEvents = 0	#需要监听的影响自身交互状态的事件，这是采用int64类型是因为all_clients属性不支持列表
		self.skillID = 0
		self.effectID = ""
		self.isInteractive = 0
		self.effectModelScale = -1.0
		self.slotName = ""
		self.canMountPetGossip = True		# 能否骑马交互
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""
		self.param4 = ""
		self.param5 = ""
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		SpellScriptBase.SpellScriptBase.initData( self, data )
			
		if 'Uname' in data:
			self.setEntityProperty( "uname", data["Uname"] )
		
		if 'gossipDistance' in data:
			tempList = data["gossipDistance"].split("|")
			self.setEntityProperty( "minGossipDis", float( tempList[0] ) )
			self.setEntityProperty( "maxGossipDis", float( tempList[1] ) )
		
		if 'lifeTime' in data:
			self.setEntityProperty( "lifeTime", data["lifeTime"] )
		
		if 'destroyTime' in data:
			self.setEntityProperty( "destroyTime", data["destroyTime"] )
		
		if 'reviveTime' in data:
			self.setEntityProperty( "reviveTime", data["reviveTime"] )
		
		if 'cooldownTime' in data:
			self.setEntityProperty( "cooldownTime", data["cooldownTime"] )
		
		if 'skillID' in data:
			self.skillID = int( data["skillID"] )

		if 'effectID' in data:
			self.effectID = data["effectID"]

		if 'IsInteractive' in data:
			self.isInteractive = data["IsInteractive"]

		if 'effectModelScale' in data:
			self.effectModelScale = data["effectModelScale"]
			
		if "canMountPet" in data:
			self.canMountPetGossip = bool( data["canMountPet"])

		if 'slotName' in data:
			self.slotName = data["slotName"]

		if 'curSorName' in data:
			self.setEntityProperty("curSorName",data["curSorName"])

		if 'InitActionId' in data:
			self.setEntityProperty("initActionId",data["InitActionId"])
			
		if 'DisplayOnClient' in data:
			self.setEntityProperty("displayOnClient",int(data["DisplayOnClient"]))

		if 'endActionID' in data:
			self.endActionID = data["endActionID"]

		if 'endEffectID' in data:
			self.endEffectID = data["endEffectID"]

		if 'startEffectID' in data:
			self.startEffectID = data["startEffectID"]

		if 'WalkSpeed' in data:
			self.setEntityProperty( "moveSpeed", float(data["WalkSpeed"]) )

		if 'onlifeTimeUseSkill' in data:
			self.setEntityProperty( "onlifeTimeUseSkill",data["onlifeTimeUseSkill"] )
				
		if "gossipCondition" in data:
			for conDict in data["gossipCondition"]:
				scriptName = conDict[ "scriptName" ]
				scriptObj = smartImport( "ConfigObject.SpellBoxGossip.SpellGossipCondition" + ":" + scriptName )()
				scriptObj.init( conDict )
				self.gossipConditions.append( scriptObj )
				
				if not self.hasListenEvent( scriptObj.eventType ):
					self.addListenEvent( scriptObj.eventType )
		
		if "gossipResult" in data:
			for conDict in data["gossipResult"]:
				scriptName = conDict[ "scriptName" ]
				scriptObj = smartImport( "ConfigObject.SpellBoxGossip.SpellGossipResult" + ":" + scriptName )()
				scriptObj.init( conDict )
				self.gossipResults.append( scriptObj )

		if "Param1" in data:
			self.param1 = data["Param1"]
				
		if "Param2" in data:
			self.param2 = data["Param2"]
				
		if "Param3" in data:
			self.param3 = data["Param3"]
				
		if "Param4" in data:
			self.param4 = data["Param4"]
				
		if "Param5" in data:
			self.param5 = data["Param5"]

	
	def hasListenEvent( self, eventType ):
		eventType = 1 << eventType
		return ( self.listenEvents & eventType ) == eventType
	
	def addListenEvent( self, eventType ):
		eventType = 1 << eventType
		self.listenEvents |= eventType

	def getGossipSkillID( self ):
		"""
		获得交互的技能ID
		"""
		return self.skillID
	
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化entity
		"""
		SpellScriptBase.SpellScriptBase.initEntity( self, selfEntity )
		selfEntity.listenEvents = self.listenEvents
		if selfEntity.lifeTime >= 0:
			selfEntity.lifeTimerID = selfEntity.addTimerCallBackForScript( selfEntity.lifeTime, "onLifeTimeCB", () )

	def onClientActorReady( self, selfEntity ):
		"""
		客户端Character Actor已经准备好
		"""
		pass
	
	def requestRefreshStatus( self, selfCell, playerEntity ):
		"""
		玩家请求更新箱子状态
		"""
		if selfCell.isDestroyHide:
			result = 0		#不可见
		elif selfCell.isCoolDowning or not self.__checkGossipCondition( selfCell, playerEntity ):
			result = 1		#不可交互
		else:
			result = 2		#可交互
		try:
			playerEntity.clientEntity( selfCell.id ).CLIENT_SetBoxStatus( result, self.effectID, self.effectModelScale, self.slotName )
		except:
			pass
	
	def gossipWith( self, selfEntity, srcEntityID ):
		"""
		玩家点击交互
		"""
		if selfEntity.id == srcEntityID:
			return
		
		playerCell = KBEngine.entities.get( srcEntityID, None )
		if playerCell is None:
			KBEDebug.ERROR_MSG( "SpellBox::gossipWith:Can't found gossip with player entity %i!" % srcEntityID )
			return
		
		#不在同一个space
		if playerCell.spaceID != selfEntity.spaceID:
			return
		
		if selfEntity.isCoolDowning or selfEntity.isDestroyHide:
			return
		
		self.gossipWithForwardCB( selfEntity, playerCell )
	
	def gossipWithForwardCB( self, selfCell, playerEntity ):
		"""
		玩家交互
		"""
		if not self.__checkGossipCondition( selfCell, playerEntity ):
			return
			
		if not self.canMountPetGossip and playerEntity.isMountOnPet():
			playerEntity.transformPet( playerEntity.id )
			
		if self.skillID==0:
			KBEDebug.ERROR_MSG( "SpellBox::gossipWith:Can't found skill by entity %i!" % self.id )
			return
		playerEntity.useSkillToEntityFC( playerEntity.id, self.skillID, selfCell.id )
	
	def onPlayerIntonateOver( self, selfEntity, playerCell ):
		"""
		virtual method
		玩家吟唱结束
		"""
		self.__handleGossipResult( selfEntity, playerCell )
		#这里延迟1秒,是由于可能该spellBox需要播放动作,而策划又不想在这个动作没有播完之前，通知其他人可以交互，故和策划商量延迟1秒
		selfEntity.addTimerCallBack( 1.0,"notify_OtherClientCanInteractive",(playerCell.id,) ) 
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onTriggerBox( selfEntity.id, selfEntity.scriptID )

		playerCell.spaceStrategy_onTriggerBox( selfEntity.scriptID )

		if selfEntity.cooldownTime >= 0:
			selfEntity.isCoolDowning = True
			selfEntity.allClients.CLIENT_RefreshBoxStatus()
			if selfEntity.cooldownTime != 999:	#配999则一直冷却
				selfEntity.addTimerCallBackForScript( selfEntity.cooldownTime, "onCooldownTimeOverCB", (playerCell.id,) )
		
		if selfEntity.destroyTime >= 0:
			selfEntity.addTimerCallBackForScript( selfEntity.destroyTime, "onDestroyTimeCB", (playerCell.id,) )
	
	def onCooldownTimeOverCB( self, selfEntity, srcEntityID ):
		"""
		冷却结束，恢复可交互状态
		"""
		selfEntity.isCoolDowning = False
		selfEntity.allClients.CLIENT_RefreshBoxStatus()
		selfEntity.spaceNotifyTempData = {}
	
	def onDestroyTimeCB( self, selfEntity, srcEntityID ):
		"""
		销毁timer到达
		"""
		if selfEntity.reviveTime >= 0:	#如果需要复活，销毁时不做真正销毁，只隐藏模型
			#隐藏
			selfEntity.isDestroyHide = True
			selfEntity.allClients.CLIENT_RefreshBoxStatus()
			selfEntity.addTimerCallBackForScript( selfEntity.reviveTime, "onReviveTimeCB", () )
		else:
			selfEntity.destroySelf()
	
	def onLifeTimeCB( self, selfEntity ):
		"""
		virtual method
		生存时间到达
		"""
		selfEntity.lifeTimerID = 0
		if selfEntity.reviveTime >= 0:	#如果需要复活，销毁时不做真正销毁，只隐藏模型
			#隐藏
			selfEntity.isDestroyHide = True
			selfEntity.allClients.CLIENT_RefreshBoxStatus()
			selfEntity.addTimerCallBackForScript( selfEntity.reviveTime, "onReviveTimeCB", () )
		else:
			selfEntity.destroySelf()
	
	def onReviveTimeCB( self, selfEntity, srcEntityID = 0 ):
		"""
		复活时间到，重新显示出来
		"""
		selfEntity.isDestroyHide = False
		selfEntity.allClients.CLIENT_RefreshBoxStatus()
	
	def __checkGossipCondition( self, selfCell, playerEntity ):
		"""
		检测交互条件
		"""
		for obj in self.gossipConditions:
			if not obj.check( selfCell, playerEntity ):
				return False
		return True
	
	def __handleGossipResult( self, selfEntity, playerCell ):
		"""
		执行交互效果脚本
		"""
		for obj in self.gossipResults:
			obj.do( selfEntity, playerCell )

	def delyGetResult( self, selfEntity, playerID, result, value ):
		"""
		延迟获得结果,并提示(主要满足策划在屏幕中央提示)
		"""
		player = KBEngine.entities.get(playerID,None)
		if player == None:
			KBEDebug.ERROR_MSG("role is destroy")
			return
		if result == csdefine.SPELL_BOX_RESULT_GETKEY:
			spaceEntity =  player.getCurrentSpace()
			if spaceEntity and player.isInSpaceCopy():
				spaceEntity.getScript().onConditionChange( spaceEntity, "SPELL_GOSSIP_RESULT", selfEntity.scriptID, value, player.getName() )
		elif result == csdefine.SPELL_BOX_RESULT_ADDEXP:
			player.addExp( value, csdefine.EXP_ADD_REASON_BY_SPELLBOX )
		elif result == csdefine.SPELL_BOX_RESULT_ADDBUFF:
			if player.addBuff( player,value ):
				player.client.ShowSpellBoxResultMessage( csdefine.SPELL_BOX_RESULT_ADDBUFF,value )
	