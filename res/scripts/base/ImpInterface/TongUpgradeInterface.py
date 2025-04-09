# -*- coding: utf-8 -*-

import Const
import csstatus
import csdefine
import KBEDebug
import TongLoader

class TongUpgradeInterface( object ):
	
	def addActivity( self, activity ):
		oldValue = self.activity
		self.activity += activity
		self.onActivityChange( oldValue )
		
	def subActivity( self, activity ):
		if self.hasEnoughActivity( activity ):
			oldValue = self.activity
			self.activity -= activity
			self.onActivityChange( oldValue )
			return True
		else:
			return False
			
	def subActivityUntillZero( self, activity ):
		"""
		扣除活跃度
		活跃度不够直接扣到0
		"""
		if self.hasEnoughActivity( activity ):
			oldValue = self.activity
			self.activity -= activity
			self.onActivityChange( oldValue )
			return activity
		else:
			if self.activity <= 0:
				return self.activity
			
			oldValue = self.activity
			self.activity = 0
			self.onActivityChange( oldValue )
			return oldValue

	def getActivity( self ):
		return self.activity
		
	def hasEnoughActivity( self, activity ):
		return self.activity >= activity
		
	def onActivityChange( self, oldValue ):
		for member in self.members.values():
			if member.baseMailBox and hasattr(member.baseMailBox, "client") and member.baseMailBox.client:
				member.baseMailBox.client.OnActivityChange( self.activity )
		if not self.protectDay and not self.safeTime:
			# 帮会最低活跃度
			if self.activity < TongLoader.getMinActivity( self.level ):
				if self.level > 1:
					self.protectDay = Const.TONG_LEVEL_PROTECTTIME
				else:
					self.protectDay = Const.TONG_DISMISS_PROTECTIME
	
	def tongUpGrade( self, playerMB, playerDBID ):
		"""
		define method
		帮会升级
		"""
		if self.level >= TongLoader.getMaxTongLevel():return
		needMoney = TongLoader.getUpgradeUseMoney( self.level )
		needActivity = TongLoader.getUpgradeUseActivity( self.level )
		if not self.hasEnoughMoney( needMoney ):
			playerMB.client.statusMessage( csstatus.TONG_CANNOT_UPGRADE_NOT_ENOUGH_MONEY, "" )
			return
		if not self.hasEnoughActivity( needActivity ):
			playerMB.client.statusMessage( csstatus.TONG_CANNOT_UPGRADE_NOT_ENOUGH_ACTIVITY, "" )
			return
		if self.subTongMoney( needMoney ) and self.subActivity( needActivity ):
			self.level += 1
			if self.safeTime:
				self.addRecord( csdefine.TONG_EVENT_PROTECT_DAY_OVER_ADVAN )
			self.safeTime = Const.TONG_UPGRADE_SAFETIME
			self.onLevelChange( self.level - 1, playerDBID )
			
	def tongDownGrade( self ):
		"""帮会降级"""
		self.level -= 1
		self.onLevelChange( self.level + 1 )
		
	def onLevelChange( self, oldValue, playerDBID = None ):
		"""等级发生改变时"""
		if self.level > oldValue:
			name = ""
			if playerDBID and playerDBID in self.members:
				name = self.members[playerDBID].name
			self.addRecord( csdefine.TONG_EVENT_UP_GRADE, name, self.level )
		else:
			self.addRecord( csdefine.TONG_EVENT_DOWN_GRADE, self.level )
			self.builds.onTongLevelDown( self )
		for member in self.members.values():
			member.onTongLevelChange( self.level )
		
	#--------------------帮会建筑--------------------------------------------
	def addGrow( self, grow ):
		oldValue = self.grow
		maxGrow = self.builds[csdefine.TONG_BUILDING_TYPE_YSDT].getTongLimitGrow(self)
		self.grow = min( self.grow + grow, maxGrow )
		if oldValue != self.grow:
			self.onGrowChange( oldValue )
		
	def subGrow( self, grow ):
		if self.hasEnoughGrow( grow ):
			oldValue = self.grow
			self.grow -= grow
			self.onGrowChange( oldValue )
			return True
		else:
			KBEDebug.ERROR_MSG("Sub grow err!!has not enough money")
			return False
		
	def hasEnoughGrow( self, grow ):
		return self.grow >= grow
		
	def onGrowChange( self, oldValue ):
		for member in self.members.values():
			if member.baseMailBox and hasattr(member.baseMailBox, "client") and member.baseMailBox.client:
				member.baseMailBox.client.OnGrowChange( self.grow )
		
	def buildUpgrade( self, playerMB, buildType ):
		"""
		define method
		建筑升级
		"""
		level = self.builds[buildType].buildLevel + 1
		if level > TongLoader.getMaxTongBuildLevel():
			KBEDebug.ERROR_MSG( "Tong build level(%d) is max!"%level )
			return
		if self.level < TongLoader.getUpgrowNeedTongLevel( level, buildType ):
			playerMB.client.statusMessage( csstatus.TONG_UPGROW_FAIL_NOT_EMOUGH_LEVEL, "" )
			return
		needMoney = TongLoader.getUpgradeBuildUseMoney( level -1, buildType )
		needGrow = TongLoader.getUpgradeBuildUseGrow( level - 1, buildType )
		if not self.hasEnoughMoney( needMoney ):
			playerMB.client.statusMessage( csstatus.TONG_UPGROW_FAIL_NOT_EMOUGH_MONEY, "" )
			return
		if not self.hasEnoughGrow( needGrow ):
			playerMB.client.statusMessage( csstatus.TONG_UPGROW_FAIL_NOT_EMOUGH_GROW, "" )
			return
			
		if self.subTongMoney( needMoney ) and self.subGrow( needGrow ):
			self.builds.setLevel( self, buildType, level )
	
	def notifyClientTongBuild( self ):
		return self.builds.getBuildLevel()
