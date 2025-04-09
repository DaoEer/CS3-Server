# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from ObjectScript.SpellBox import SpellBox
import csstatus
import Const

class SpellBoxSpecial( SpellBox.SpellBox ):
	"""
	大地图特殊场景物件
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		SpellBox.SpellBox.initData( self, data )

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
		
		selfEntity.playerCoolList[srcEntityID] = selfEntity.cooldownTime
		selfEntity.playerDestroyTimeList[srcEntityID] = selfEntity.destroyTime
		if playerCell.playerDBID not in selfEntity.playerIsCoolList.keys():
			selfEntity.playerIsCoolList[playerCell.playerDBID] = selfEntity.isCoolDowning
		if selfEntity.playerIsCoolList[playerCell.playerDBID] or selfEntity.isDestroyHide:
			return
		
		self.gossipWithForwardCB( selfEntity, playerCell )

	def requestRefreshStatus( self, selfCell, playerEntity ):
		"""
		玩家请求更新箱子状态
		"""
		if selfCell.isDestroyHide:
			result = 0		#不可见
		elif (selfCell.playerIsCoolList and playerEntity.playerDBID in selfCell.playerIsCoolList\
		and selfCell.playerIsCoolList[playerEntity.playerDBID]) or not self.__checkGossipCondition( selfCell, playerEntity ):
			result = 1		#不可交互
		else:
			result = 2		#可交互
		if playerEntity.isEntityInView(selfCell):
			playerEntity.clientEntity( selfCell.id ).CLIENT_SetBoxStatus( result, self.effectID, self.effectModelScale, self.slotName )

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

		if playerCell.id in selfEntity.playerCoolList and selfEntity.playerCoolList[playerCell.id] >= 0:
			selfEntity.playerIsCoolList[playerCell.playerDBID] = True
			playerCell.clientEntity( selfEntity.id ).CLIENT_RefreshBoxStatus()
			if selfEntity.cooldownTime != 999:	#配999则一直冷却
				selfEntity.addTimerCallBackForScript( selfEntity.playerCoolList[playerCell.id], "onCooldownTimeOverCB", (playerCell.id,) )
		
		if playerCell.id in selfEntity.playerDestroyTimeList and selfEntity.playerDestroyTimeList[playerCell.id] >= 0:
			selfEntity.addTimerCallBackForScript( selfEntity.playerDestroyTimeList[playerCell.id], "onDestroyTimeCB", (playerCell.id,) )

	def onReviveTimeCB( self, selfEntity, srcEntityID = 0 ):
		"""
		复活时间到，重新显示出来
		"""
		player = KBEngine.entities.get( srcEntityID )
		selfEntity.isDestroyHide = False
		if player and player.isEntityInView(selfEntity):
			player.clientEntity( selfEntity.id ).CLIENT_RefreshBoxStatus()
			selfEntity.specialStopParticles( selfEntity.getScript().endEffectID, srcEntityID )
			player.clientEntity( selfEntity.id ).CLIENT_StopAction()
			selfEntity.specialPlayParticles( selfEntity.getScript().startEffectID, srcEntityID )

	def onCooldownTimeOverCB( self, selfEntity, srcEntityID ):
		"""
		冷却结束，恢复可交互状态
		"""
		player = KBEngine.entities.get( srcEntityID )
		if player and player.isEntityInView(selfEntity):
			selfEntity.playerIsCoolList[player.playerDBID] = False
			player.clientEntity( selfEntity.id ).CLIENT_RefreshBoxStatus()
			if player.playerDBID in selfEntity.spaceNotifyTempData:
				selfEntity.spaceNotifyTempData.pop(player.playerDBID)
			selfEntity.specialStopParticles( selfEntity.getScript().endEffectID, srcEntityID )
			player.clientEntity( selfEntity.id ).CLIENT_StopAction()
			selfEntity.specialPlayParticles( selfEntity.getScript().startEffectID, srcEntityID )

	def onDestroyTimeCB( self, selfEntity, srcEntityID ):
		"""
		销毁timer到达
		"""
		if selfEntity.reviveTime >= 0:	#如果需要复活，销毁时不做真正销毁，只隐藏模型
			#隐藏
			player = KBEngine.entities.get( srcEntityID )
			if player and player.isEntityInView(selfEntity):
				player.clientEntity( selfEntity.id ).CLIENT_RefreshBoxStatus()
			selfEntity.isDestroyHide = True
			selfEntity.addTimerCallBackForScript( selfEntity.reviveTime, "onReviveTimeCB", ( srcEntityID, ) )
		else:
			selfEntity.destroySelf()

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