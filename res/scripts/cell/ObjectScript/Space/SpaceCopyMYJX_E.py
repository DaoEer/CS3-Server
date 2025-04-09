# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KST
from MsgLogger import g_logger
import KBEDebug
import time
import csdefine
import csstatus

SPACE_PASS_LEVEL_RD = 1 #入道
SPACE_PASS_LEVEL_CC = 2 #出尘
SPACE_PASS_LEVEL_WD = 3 #问鼎
SPACE_PASS_LEVEL_CF = 4	#超凡

class SpaceCopyMYJX_E( SpaceCopy ):
	"""
	冥域缉凶
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		
	def onEnter( self, selfEntity, playerRole, packArgs ):
		if selfEntity.lifeTime <= 0:
			selfEntity.lifeTime = packArgs["lifeRemainTime"]
			selfEntity.setTemp("costTime",packArgs["costTime"])
		if not len(selfEntity.recordAddExp):
			selfEntity.recordAddExp = packArgs["recordAddExp"]
		if not len( selfEntity.recordAddPotential ):
			selfEntity.recordAddPotential = packArgs["recordAddPotential"]
		if selfEntity.recordPlayerDieNumber == 0:
			selfEntity.recordPlayerDieNumber = packArgs["recordPlayerDieNumber"]
		if selfEntity.leaveCloseTimer:
			selfEntity.popTimer( selfEntity.leaveCloseTimer )
			selfEntity.leaveCloseTimer = 0
		self.spaceStage_onPlayerEnter( selfEntity, playerRole )
		self.spaceSettlement_onPlayerEnter( selfEntity, playerRole.base )
		self.spaceBunch_onPlayerEnter( selfEntity, playerRole.base, packArgs["playerDBID"] )
		self.spaceStatistics_onPlayerEnter( selfEntity, playerRole )
		if self.spaceStrategyFile:
			self.spaceStrategy_onPlayerEnter( selfEntity, playerRole, self.spaceStrategyFile )
		if self.clientUseCharacterMovment:
			if playerRole.getClient():
				playerRole.client.ChangeMovementMode(self.clientUseCharacterMovment)
				
		#添加活动、副本参与日志
		g_logger.actCopyJoin(self.getSpaceType(), self.getSpaceName(), playerRole.playerDBID, playerRole.getName())

	def onTeleportCompleted( self, selfEntity, playerRole ):
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		selfEntity.lifeStartTime = time.time()
		self.showSpaceLifeTime( selfEntity, playerRole )
	
	def spaceSettlement_onSpaceSuccess6369( self, selfEntity ):
		"""
		副本通关 显示结算界面
		"""
		if selfEntity.getScript().getSpaceType() not in [csdefine.SPACE_TYPE_POTENTIAL,csdefine.SPACE_TYPE_CHUAN_CHENG]:
			return
		costTime = int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		if selfEntity.queryTemp("costTime",None) != None:
			costTime = selfEntity.queryTemp("costTime") + costTime
		time = selfEntity.lifeTime/4
		level = None
		if costTime > 0 and costTime <= time:
			level = SPACE_PASS_LEVEL_CF
		elif costTime > time and costTime <= (time * 2):
			level = SPACE_PASS_LEVEL_WD
		elif costTime > (time*2) and costTime <= (time*3):
			level = SPACE_PASS_LEVEL_CC
		else:
			level = SPACE_PASS_LEVEL_RD
		

		if selfEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_POTENTIAL:
			rewardValue = selfEntity.recordAddPotential
			rewardType = csdefine.SPACE_TYPE_POTENTIAL
		else:
			rewardValue = selfEntity.recordAddExp
			rewardType = csdefine.SPACE_TYPE_CHUAN_CHENG
		for role in selfEntity._spaceRoles:
			if role.playerDBID in rewardValue:
				value = rewardValue[role.playerDBID]
			else:
				value = 0
			if role.getClient():
				role.client.CLIENT_ShowSpaceSettlementWin(rewardType, value, int(costTime), selfEntity.recordPlayerDieNumber, level )




	