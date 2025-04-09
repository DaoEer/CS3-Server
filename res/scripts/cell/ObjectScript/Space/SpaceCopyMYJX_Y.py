# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KST
import KBEDebug
import time

class SpaceCopyMYJX_Y( SpaceCopy ):
	"""
	冥域缉凶
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.delayToNextSpaceTime = 0.0

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.delayToNextSpaceTime = configData["SpaceData"].get("delayToNextSpaceTime",0.0)
		
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceSuccess( selfEntity )
		self.spaceBunch_onSpaceSuccess( selfEntity )

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
				selfEntity.addTimerCallBackForScript( self.delayToNextSpaceTime,"gotoNextChildSpace",() )

	def gotoNextChildSpace( self, selfEntity ):
		"""
		传送进下一个
		"""
		curChildNextSpace = self.getBunchSpaceObj().getChildNextSpace( selfEntity.bunchChildSpaceIndex, self.scriptID )
		_completeList = list( selfEntity.createArgs["completeList"] )
		remainTime = selfEntity.lifeTime - int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		costTime = int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		packArgs = { "packBelongType": selfEntity.belongType, "packSpaceLevel": self.getNextSpaceLevel(selfEntity), "completeList": _completeList,"lifeRemainTime":remainTime,"lifeStartTime":selfEntity.lifeStartTime,"recordAddExp":selfEntity.recordAddExp,"recordAddPotential":selfEntity.recordAddPotential,"recordPlayerDieNumber":selfEntity.recordPlayerDieNumber,"costTime":costTime }
		for e in selfEntity._spaceRoles:
			e.gotoSpaceEnterPos( curChildNextSpace,packArgs )

	def onLogin( self, selfEntity, playerRole ):
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		if self.isBunchChildSpace():
			if  self.spaceBunch_isChildSpaceComplete(selfEntity):
				self.gotoNextChildSpace( selfEntity )
	
