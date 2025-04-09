# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csstatus
import csdefine

class MonsterExtLingMai( Monster.Monster ):
	"""
	灵脉战场BOSS
	"""
	def __init__( self ):
		"""
		"""
		Monster.Monster.__init__( self )
		self.damageObj = {}
		self.damageObj[csdefine.CAMP_TAOSIM] = []
		self.damageObj[csdefine.CAMP_DEMON] = []
		
	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		Monster.Monster.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		caster = KBEngine.entities.get( casterID )
		if caster:
			if not casterID in self.damageObj[caster.tempCamp]:
				self.damageObj[caster.tempCamp].append( casterID )
			if caster.tempCamp == csdefine.CAMP_TAOSIM:
				self.xianDamage += finalDamage
			elif caster.tempCamp == csdefine.CAMP_DEMON:
				self.moDamage += finalDamage
				
	def resetBoss( self ):
		"""
		重置Boss
		"""
		if self.tempCamp == csdefine.CMAP_NONE:					# 如果还没有改变临时阵营
			if self.xianDamage > self.moDamage:
				self.setTempCamp( csdefine.CAMP_TAOSIM )
			else:
				self.setTempCamp( csdefine.CAMP_DEMON )
		else:
			if self.tempCamp == csdefine.CAMP_TAOSIM:
				self.setTempCamp( csdefine.CAMP_DEMON )
			else:
				self.setTempCamp( csdefine.CAMP_TAOSIM )
		self.getCurrentSpace().occupyLingMai( self.scriptID, self.tempCamp, self.damageObj[self.tempCamp] )
		if self.xianDamage != 0:
			self.xianDamage = 0
		if self.moDamage != 0:
			self.moDamage = 0
		self.setHP( self.HP_Max )
		self.setMP( self.MP_Max )
		self.damageObj[csdefine.CAMP_TAOSIM] = []
		self.damageObj[csdefine.CAMP_DEMON] = []
		self.changeState( csdefine.ENTITY_STATE_FREE )
		
	def onEnterReset( self ):
		"""
		virtual method
		进入重置状态
		"""
		Monster.Monster.onEnterReset( self )
		self.moDamage = 0
		self.xianDamage = 0
		self.damageObj[csdefine.CAMP_TAOSIM] = []
		self.damageObj[csdefine.CAMP_DEMON] = []
