# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csstatus
import csdefine
import KBEDebug
import cschannel_msgs

NAME_TAOSIM = cschannel_msgs.CAMP_TAOSIM		#仙道
NAME_DEMON = cschannel_msgs.CAMP_DEMON		#魔道
		
class MonsterExtSGMZ( Monster.Monster ):
	"""
	上古密阵BOSS
	"""
	def __init__( self ):
		"""
		"""
		Monster.Monster.__init__( self )
		self.timeID = 0
		self.campDamageDict={csdefine.CAMP_TAOSIM: 0 ,csdefine.CAMP_DEMON: 0 }
	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		spaceEntity = self.getCurrentSpace()
		caster = KBEngine.entities.get( casterID )
		if not spaceEntity or not caster:
			return
		self.campDamageDict[ caster.getCamp() ] += damage
		spaceEntity.addCampScore( caster.getCamp(), damage )
		
		if self.timeID==0:
			self.timeID = self.addTimerRepeatExt(int(self.getScript().param1), int(self.getScript().param1), "SendReceiveDamageInfo",())
		Monster.Monster.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )

	def SendReceiveDamageInfo(self):
		#每分钟刷一次的公告
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		damageTAOSIM= self.campDamageDict[csdefine.CAMP_TAOSIM]
		damageDEMON = self.campDamageDict[csdefine.CAMP_DEMON]
			
		for roleCell in spaceEntity._spaceRoles:
			roleCell.statusMessage( csstatus.MI_ZHEN_LAST_BOSS_BE_DAMAGE, NAME_TAOSIM, damageTAOSIM, NAME_DEMON, damageDEMON )

	def onEnterReset( self ):
		"""
		virtual method
		进入重置状态
		"""
		Monster.Monster.onEnterReset( self )
		
	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		Monster.Monster.onEnterDead( self )
		if self.timeID:
			self.popTimer( self.timeID )
			self.timeID = 0