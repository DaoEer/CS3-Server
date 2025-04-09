# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import KBEDebug
import Monster
import csdefine
import Const
import time
import csstatus

class MonsterExtCover( Monster.Monster ):
	"""
	轮回秘境：保护罩
	用于 更新血量
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_COVER)

	def setPlayerMB(self, playerRole):
		self.ownerID = playerRole.id
		playerRole.updateLHMJCoverHP( self.HP )
	
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		玩家客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get( srcEntityID )
		if player and self.belongDBID and player.challengeDBID == self.belongDBID:
			player.client.NoticeMECEnter( self.id )		# 当挑战玩家靠近，需要提示使用 远程武器
	
	def noticeMECPEnter( self, playerID ):
		""""""
		playerCell = KBEngine.entities.get( playerID )
		if playerCell and playerCell.spaceID == self.spaceID and playerCell.position.distTo( self.position ) <= Const.DEFAULT_AOI_RADIUS:
			playerCell.client.NoticeMECEnter( self.id )
	
	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		Monster.Monster.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		if (time.time() - self.receiveDamageTime) > 60:
			self.receiveDamageTime = int(time.time())
			caster = KBEngine.entities.get(casterID)
			if caster:
				if self.ownerID:
					player = KBEngine.entities.get(self.ownerID, None)
					if player:
						player.statusMessage( csstatus.DONG_FU_COVER_BEING_ATTACK, caster.getName())
						return
				KBEngine.globalData["SpaceLunHuiMiJinMgr"].onMonsterCoverBeAttack( self.belongDBID, caster.getName() )
					
	
	def onHPChanged( self, oldValue ):
		"""
		血量改变回调
		"""
		Monster.Monster.onHPChanged(self, oldValue)
		if self.ownerID:
			player = KBEngine.entities.get(self.ownerID, None)
			if player:
				player.updateLHMJCoverHP( self.HP )						# 如果跟玩家同一个cell，直接获取entity！否则通过 baseMailBox 寻找
	
	def onBeKill( self, killerID, deadEffect, actForbid ):
		"""
		被击杀
		"""
		Monster.Monster.onBeKill( self, killerID, deadEffect, actForbid )
		killer = KBEngine.entities.get( killerID )
		result = 0
		if killer and killer.challengeDBID == self.belongDBID:
			killer.statusMessage( csstatus.DONG_FU_COVER_DESTROY_ATTACK, "" )
		else:
			result += 1						
		if self.ownerID:
			player = KBEngine.entities.get(self.ownerID, None)
			if player:
				player.statusMessage( csstatus.DONG_FU_COVER_DESTROY_PROTECT, killer.getName(), killer.getName() )
			else:
				result += 2
		else:
			result += 2
		# result为1，攻方没发msg;result为2，守方没发msg；result为3，双方都没发msg
		# 没发msg，就通过mgr发送
		if result and self.belongDBID:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onMonsterCoverBeKill( self.belongDBID, result )