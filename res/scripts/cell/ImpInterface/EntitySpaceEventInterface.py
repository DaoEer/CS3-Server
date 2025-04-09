# -*- coding: utf-8 -*-

import Define
import csdefine
import Functions
import KBEDebug
from SpaceEvent.SpaceEvents import Datas as g_spaceEventDatas
from ObjectScript.ObjectScriptFactory import g_objFactory

class EntitySpaceEventInterface:
	"""
	怪物和玩家副本事件接口
	"""
	def addListenSpaceEvents( self, spaceScriptID, eventType, eventID, conditions ):
		"""
		绑定感兴趣的副本事件
		"""
		info = {}
		info[ "eventType" ] = eventType
		info[ "eventID" ] = eventID
		info[ "conditions" ] = conditions
		self.listenSpaceEvents.append( info )
		
		if g_spaceEventDatas[ eventType][ "clientTrigger" ]:		# 客户端触发的事件才发给客户端
			if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:	# 目前只监听由role触发的事件
				conInfo = []
				for con in conditions:
					if not con.isClientCon:		# 客户端检测的条件才发往客户端
						continue
					conDict = { "scriptName" : con.__class__.__name__, "param1" : str(con.param1), "param2" : str(con.param2), "param3" : str(con.param3), "param4" : str(con.param4) }
					conInfo.append( conDict )
				self.client.CLIENT_AddListenSpaceEvents( spaceScriptID, eventType, eventID, Functions.toJsonString( conInfo ) )

	def clearListenSpaceEvents( self ):
		"""
		清除绑定的副本事件
		"""
		self.listenSpaceEvents = []
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if self.getClient():
				self.client.CLIENT_ClearListenSpaceEvents()

	def __checkEventConditions( self, conditions, eventParams ):
		"""
		"""
		for cond in conditions:
			if not cond.check( self, eventParams ):
				return False
		return True

	def triggerSpaceEvent( self, eventType, eventParams ):
		"""
		触发副本事件
		"""
		eventIDs = []
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] != eventType:
				continue
			if not self.__checkEventConditions( event[ "conditions" ], eventParams ):
				continue
			eventIDs.append( event[ "eventID" ] )
		
		if eventIDs:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				spaceEntity.remoteScriptCall( "triggerEvent", ( eventType, eventIDs, self.id, eventParams ) )
				KBEDebug.DEBUG_MSG("Entity trigger space event! entityID:%s. "%self.id, eventType, eventIDs, eventParams)

	def CELL_triggerSpaceEventByClient( self, srcEntityID, eventType, eventIDs, eventParamsStr ):
		"""
		<Exposed method>
		客户端触发副本事件
		"""
		KBEDebug.DEBUG_MSG( "client trigger!!!!!!!!!%s,%s,%s"%(eventType, eventIDs, eventParamsStr) )
		if self.id != srcEntityID:
			return
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] != eventType:
				continue
			if event[ "eventID" ] in eventIDs and not self.__checkEventConditions( event[ "conditions" ], eval( eventParamsStr ) ):
				eventIDs.remove( event[ "eventID" ] )
		if eventIDs:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(spaceEntity, 0, "客户端触发副本事件, eventType:%s" %(eventType))
				spaceEntity.remoteScriptCall( "triggerEvent", ( eventType, eventIDs, self.id, eval( eventParamsStr ) ) )

#---------------------- 副本事件玩家相关接口 ------------------------------
	def spaceEvent_roleEnterSpace( self ):
		"""
		玩家进副本
		"""
		#执行上一个副本或位面的“玩家登陆其他地图事件”
		if self.spaceEventLastSpace != self.getCurrentSpaceScriptID():
			recordSpaceObj = g_objFactory.getSpaceObject( self.spaceEventLastSpace )
			if recordSpaceObj:
				from ObjectScript.Space.SpaceCopy import SpaceCopy
				from ObjectScript.Space.SpacePlane import SpacePlane
				
				if isinstance( recordSpaceObj, SpaceCopy ) or isinstance( recordSpaceObj, SpacePlane ):
					recordSpaceObj.spaceEvent_onLoginDiffSpace( self )
		
			self.spaceEventLastSpace = self.getCurrentSpaceScriptID()	#记录最后进入的地图
			#self.writeToDB()
		
		self.clearListenSpaceEvents()	#这里再清空一下绑定的副本事件，因为下线的情况下离开地图，spaceEvent_roleLeaveSpace中的清空操作未必有效（如果client已经lost的话会通知不到）
		if self.isInSpaceCopy() or self.isInSpacePlane():
			self.getCurrentSpaceObject().roleBindSpaceEvent( self )	# 绑定副本事件
			for event in self.listenSpaceEvents:
				if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_ENTER_SPACE:
					KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家进副本 eventType:%s" %(event["eventType"]))
					self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_ENTER_SPACE, { "playerID" : self.id} )
					break
	
	def spaceEvent_roleTelCompleted( self ):
		"""
		玩家完全进入副本（场景已加载完毕）
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_ENTER_SPACE_COM:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家完全进入副本 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_ENTER_SPACE_COM, {} )
				break
	
	def spaceEvent_roleLeaveSpace( self ):
		"""
		玩家出副本（出副本之前）
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_LEAVE_SPACE:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家出副本 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_LEAVE_SPACE, {} )
				break
		
		self.clearListenSpaceEvents()

	def spaceEvent_roleADDItem( self, itemID ):
		"""
		玩家获得物品
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return

		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_ADD_ITEM:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家获得物品 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_ADD_ITEM, {"itemID":itemID} )
				break

	def spaceEvent_roleDie( self ):
		"""
		玩家死亡
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_DIE:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家死亡 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_DIE, {} )
				break

	def spaceEvent_OnRoleBeKill( self, killerID ):
		"""
		玩家被击杀
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ON_ROLE_BEKILL:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家被击杀 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ON_ROLE_BEKILL,{"killerID":killerID} )
				break

	def spaceEvent_OnRoleStateChange( self ):
		"""
		玩家状态改变
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ON_STATE_CHANGE:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家状态改变 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ON_STATE_CHANGE, {} )
				break

	def spaceEvent_roleRemoveItem( self, itemID ):
		"""
		玩家获得物品
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return

		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_REMOVE_ITEM:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家获得物品 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_REMOVE_ITEM, {"itemID":itemID} )
				break

	def spaceEvent_roleChangeHP( self ):
		"""
		玩家HP改变
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_ROLE_CHANGE_HP:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家HP改变 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ROLE_CHANGE_HP, {} )
				break

	def spaceEvent_stopPlaySound(self, soundID):
		"""
		停止语音事件
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return

		for event in self.listenSpaceEvents:
			if event["eventType"] == Define.SPACE_EVENT_STOP_PLAY_SOUND:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "停止语音事件 eventType:%s" %(event["eventType"]))
				self.triggerSpaceEvent(Define.SPACE_EVENT_STOP_PLAY_SOUND, {"soundID":soundID})


#---------------------- 副本事件怪物相关接口 ------------------------------
	def spaceEvent_npcObjectCreate( self ):
		"""
		怪物或NPC创建
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		self.getCurrentSpaceObject().npcObjectBindSpaceEvent( self )	# 绑定副本事件
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_MONSTER_CREATE:
				scriptID = self.scriptID if hasattr( self, "scriptID" ) else ""
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "怪物或NPC创建 eventType:%s, scriptID:%s" %(event["eventType"], scriptID))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_MONSTER_CREATE, { "entityID": self.id, "scriptID": scriptID, "group": self.group } )
				break

	def spaceEvent_monsterDie( self ):
		"""
		怪物死亡
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_MONSTER_DIE:
				scriptID = self.scriptID if hasattr( self, "scriptID" ) else ""
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "怪物死亡 eventType:%s, scriptID:%s" %(event["eventType"], scriptID))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_MONSTER_DIE, { "entityID": self.id, "scriptID": scriptID, "group": self.group } )
				break

	def spaceEvent_npcObjectDestroy( self ):
		"""
		怪物或NPC销毁
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_MONSTER_DESTROY:
				scriptID = self.scriptID if hasattr( self, "scriptID" ) else ""
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "怪物或NPC销毁 eventType:%s, scriptID:%s" %(event["eventType"], scriptID))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_MONSTER_DESTROY, { "entityID": self.id, "scriptID": scriptID, "group": self.group } )
				break

	def spaceEvent_monsterChangeHP( self ):
		"""
		怪物HP改变
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event[ "eventType" ] == Define.SPACE_EVENT_TYPE_MONSTER_CHANGE_HP:
				scriptID = self.scriptID if hasattr( self, "scriptID" ) else ""
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "怪物HP改变 eventType:%s, scriptID:%s" %(event["eventType"], scriptID))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_MONSTER_CHANGE_HP, { "entityID": self.id, "scriptID": scriptID, "group": self.group, "HP_Max": self.HP_Max, "newValue": self.HP } )
				break

	def spaceEvent_onMonsterBeKill( self, killerID ):
		"""
		怪物被击杀的事件
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		
		for event in self.listenSpaceEvents:
			if event["eventType"] == Define.SPACE_EVENT_TYPE_ON_MONSTER_BEKILL:
				scriptID = self.scriptID if hasattr( self, "scriptID" ) else ""
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "怪物被击杀的事件 eventType:%s, scriptID:%s" %(event["eventType"], scriptID))
				self.triggerSpaceEvent( Define.SPACE_EVENT_TYPE_ON_MONSTER_BEKILL, { "entityID": self.id, "scriptID": scriptID,"killerID":killerID } )
				break

	def spaceEvent_onPlayerParachutingOver(self, playerID):
		"""
		玩家跳伞结束事件
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		for event in self.listenSpaceEvents:
			if event["eventType"] == Define.SPACE_EVENT_TYPE_PARACHUTING_OVER:
				KBEDebug.DEBUG_MSG_FOR_SPACECOPY_PLOT(self.getCurrentSpace(), 0, "玩家跳伞结束事件 eventType:%s, playerID:%s" %(event["eventType"], playerID))
				self.triggerSpaceEvent(Define.SPACE_EVENT_TYPE_PARACHUTING_OVER, {"playerID": playerID})
				break