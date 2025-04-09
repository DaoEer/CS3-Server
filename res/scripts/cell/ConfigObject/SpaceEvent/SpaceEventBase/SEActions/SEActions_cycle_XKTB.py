# -*- coding: utf-8 -*-

# 虚空探宝 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import random

class SEAction343( SEActionBase ):
	"""
	虚空探宝 归元盾充能
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self.amount = int( section["param1"] ) #充能次数
		if section["param2"]:
			self.itemID = int( section["param2"] ) #物品ID
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			itemInstList = player.getItemInstsByID( self.itemID )
			for itemInst in itemInstList:
				itemInst.addUseNumber( self.amount, player )
			player.client.NotifyRechargeableValue( float(itemInst.amount) )

class SEAction344( SEActionBase ):
	"""
	虚空探宝 归元盾消耗能
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self.amount = int( section["param1"] ) #充能次数
		if section["param2"]:
			self.itemID = int( section["param2"] ) #物品ID
		if section["param3"]:
			self._skillID = int(section["param3"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for player in spaceEntity._spaceRoles:
			itemInstList = player.getItemInstsByID( self.itemID )
			for itemInst in itemInstList:
				itemInst.amount -= self.amount
				if itemInst.amount <= 0:
					itemInst.amount = 0
					spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "dend", "")
					player.useSkillToEntity( self._skillID, player.id )
				player.updateOneDataToClient( "amount", itemInst.amount, itemInst )
				player.client.NotifyRechargeableValue( float(itemInst.amount) )

class SEAction345( SEActionBase ):
	"""
	虚空探宝 随机时间后，探灵石开始探测
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.probeTime = [ int(i) for i in section["param1"].split("|") ]
		self.extcavateTime = [ int(i) for i in section["param2"].split("|") ]
		self.scriptID = section["param3"]
		self.currentText = section["param4"].split("|")
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		entityList = spaceEntity.getEntityMailBoxRecord(self.scriptID)
		if not len(entityList):
			return
		entityList[0].allClients.DisplyCurrentText( self.currentText[0], 0 )			# 显示探测中
		spaceEntity.probeTimerID = spaceEntity.addTimerCallBack( random.randint( self.probeTime[0], self.probeTime[1] ),"onStartProbeItem",(entityList[0], self.extcavateTime, self.currentText[1],))

class SEAction413( SEActionBase ):
	"""
	虚空探宝 统计探宝次数
	"""	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		#统计探宝次数
		probeTimes = spaceEntity.queryTemp("PROBETIMES", 0) + 1
		spaceEntity.setTemp("PROBETIMES", probeTimes)
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.CLIENT_notifyProbeTimes(probeTimes)
				
class SEAction424( SEActionBase ):
	"""
	CST-11308 晶石狩猎场机缘玩法 虚空探宝，根据探宝次数奖励金精
	@param1: 探宝次数（大于或等于）:奖励金精数|探宝次数:奖励金精数
	"""	
	def init ( self, section ):
		SEActionBase.init( self, section )
		self._integralRewardInfo = {}
		for rewardInfo in section["param1"].split("|"):
			times, value = rewardInfo.split(":")
			self._integralRewardInfo[int(times)] = int(value)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		value = 0
		probeTimes = spaceEntity.queryTemp("PROBETIMES", 0)
		
		timesKeys = list(self._integralRewardInfo.keys())
		timesKeys.sort(reverse = True)
		for key in timesKeys:
			if probeTimes >= key:
				value = self._integralRewardInfo[key]
				break
		if value > 0:
			for player in spaceEntity._spaceRoles:
				player.addSparHunTingIntegral(value)
								
		
SEActionBase.setActionClass("SEAction343", SEAction343)
SEActionBase.setActionClass("SEAction344", SEAction344)
SEActionBase.setActionClass("SEAction345", SEAction345)
SEActionBase.setActionClass("SEAction413", SEAction413)
SEActionBase.setActionClass("SEAction424", SEAction424)