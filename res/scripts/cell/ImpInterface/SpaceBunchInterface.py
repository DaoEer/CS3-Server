# -*- coding: utf-8 -*-

import Const
import csstatus
import csdefine
import KBEngine
from KBEDebug import *

class SpaceBunchInterface:
	"""
	副本串功能接口
	"""
	def __init__( self ):
		self.bunchSpaceScriptID = ""

	def initData( self, configData ):
		self.bunchSpaceScriptID = configData.get( "bunchSpaceScriptID", "" )
	
	def isBunchChildSpace( self ):
		"""
		此副本是副本串中的子副本？
		"""
		return self.bunchSpaceScriptID != ""
	
	def getBunchSpaceObj( self ):
		from ObjectScript.ObjectScriptFactory import g_objFactory	#防止交叉引用，必须在这里import
		return g_objFactory.getBunchSpaceObject( self.bunchSpaceScriptID )

	def spaceBunch_isChildSpaceComplete( self, selfEntity ):
		"""
		当前的副本子串是否完成
		"""
		return self.getBunchSpaceObj().isChildSpaceComplete( selfEntity.bunchChildSpaceIndex,self.scriptID )
	
	def spaceBunch_onSpaceInit( self, selfEntity ):
		"""
		副本初始化
		"""
		if self.isBunchChildSpace():
			selfEntity.bunchChildSpaceIndex = self.getBunchSpaceObj().getChildIndexBySpaceScriptID(self.scriptID)
			KBEngine.globalData["BunchSpaceManager"].onSpaceCreateCell( self.bunchSpaceScriptID, selfEntity.belongType, selfEntity.spaceKey, self.scriptID )
			_stage = len( selfEntity.createArgs["completeList"] ) + 1	#完成0个副本(包括当前副本)则当前副本是第一层，完成1个是第二层，以此类推
			selfEntity.bunchStage = _stage
	
	def spaceBunch_onSpaceDestroy( self, selfEntity ):
		"""
		副本销毁
		"""
		if self.isBunchChildSpace():
			KBEngine.globalData["BunchSpaceManager"].onSpaceLoseCell( self.bunchSpaceScriptID, selfEntity.belongType, selfEntity.spaceKey, self.scriptID )
	
	def spaceBunch_onPlayerEnter( self, selfEntity, roleMB, roleDBID ):
		"""
		玩家进副本
		"""
		if self.isBunchChildSpace():
			activityType = selfEntity.createArgs.get("activityType", csdefine.ACTIVITY_TYPE_UNKNOWN)
			KBEngine.globalData["BunchSpaceManager"].onEnterSpace( self.bunchSpaceScriptID, selfEntity.belongType, selfEntity.spaceKey, activityType, roleMB, roleDBID )
	
	def spaceBunch_onSpaceSuccess( self, selfEntity ):
		"""
		副本通关
		"""
		if self.isBunchChildSpace():
			if self.spaceBunch_isChildSpaceComplete(selfEntity):
				KBEngine.globalData["BunchSpaceManager"].onSpaceSuccess( self.bunchSpaceScriptID, selfEntity.belongType, selfEntity.spaceKey, selfEntity.bunchChildSpaceIndex )
				_time = self.getBunchSpaceObj().getChildCreateDoorDelay( selfEntity.bunchChildSpaceIndex )
				selfEntity.addTimerCallBackForScript( _time, "spaceBunch_createDoor", () )
			else:
				curChildNextSpace = self.getBunchSpaceObj().getChildNextSpace( selfEntity.bunchChildSpaceIndex, self.scriptID )
				_completeList = list( selfEntity.createArgs["completeList"] )
				for e in selfEntity._spaceRoles:
					e.gotoSpaceEnterPos( curChildNextSpace, { "packBelongType": selfEntity.belongType, "packSpaceLevel": self.getNextSpaceLevel(selfEntity), "completeList": _completeList } )
	
	def spaceBunch_createDoor( self, selfEntity ):
		"""
		刷门
		"""
		self.getBunchSpaceObj().createDoor( self, selfEntity )
	
	def spaceBunch_setNextSpace( self, selfEntity, spaceScriptID ):
		"""
		设置下一个子副本
		"""
		selfEntity.nextBunchSpace = spaceScriptID
		DEBUG_MSG("Set next child space to %s. (space id:%s)"%( spaceScriptID, selfEntity.id ))
	
	def spaceBunch_setNextSpaceGM( self, selfEntity, spaceScriptID ):
		"""
		GM指令设置下一个子副本
		"""
		if not self.isBunchChildSpace():
			DEBUG_MSG("Current space(%s:%s) is not bunch child space."%( self.scriptID, selfEntity.id ))
			return
		
		if spaceScriptID not in self.getBunchSpaceObj().getAllChildScriptID():
			DEBUG_MSG("Bunch child space(%s) is invalid." % spaceScriptID )
			return
		
		index = self.getBunchSpaceObj().getChildIndexBySpaceScriptID( spaceScriptID )
		if spaceScriptID == self.scriptID or index in selfEntity.createArgs["completeList"]:
			DEBUG_MSG("Child space(%s) has created." % spaceScriptID )
			return
		
		INFO_MSG("GM set next child space to %s, current value is %s. (space id:%s)."%( spaceScriptID, selfEntity.nextBunchSpace, selfEntity.id ))
		selfEntity.nextBunchSpace = spaceScriptID
	
	def spaceBunch_isCompleted( self, selfEntity ):
		"""
		是否打完所有子副本
		"""
		_completeList = list( selfEntity.createArgs["completeList"] )
		_completeList.append( selfEntity.bunchChildSpaceIndex )
		_remainSpaces = set( _completeList ) ^ set( self.getBunchSpaceObj().getAllChildIndex() )
		return len(_remainSpaces) == 0
	
	def spaceBunch_doorTeleport( self, selfEntity ):
		"""
		传送门对话完传送
		"""
		if selfEntity.nextBunchSpace == Const.BUNCH_RECORD_SPACE_STR:
			for e in selfEntity._spaceRoles:
				if not self.spaceBunch_isCompleted( selfEntity ):	#未完成就出去，出去后给个提示信息
					e.setTemp( "spaceBunchFailureOutRcd", self.bunchSpaceScriptID )
				e.gotoExitSpacePos()
		else:
			_completeList = list( selfEntity.createArgs["completeList"] )
			_completeList.append( selfEntity.bunchChildSpaceIndex )
			for e in selfEntity._spaceRoles:
				e.gotoSpaceEnterPos( selfEntity.nextBunchSpace, { "packBelongType": selfEntity.belongType, "packSpaceLevel": self.getNextSpaceLevel(selfEntity), "completeList": _completeList } )
				
	def getNextSpaceLevel( self, selfEntity ):
		"""
		获取下一副本的等级
		"""
		return selfEntity.queryTemp("NextBunchSpaceLevel", selfEntity.spaceLevel)

		