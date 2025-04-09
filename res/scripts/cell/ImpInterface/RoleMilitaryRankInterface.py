# -*- coding: utf-8 -*-



import KBEDebug
import csdefine
import time
import Const
import csstatus
from ExploitLoader import g_exploitMgr

class RoleMilitaryRankInterface:
	"""
	玩家称号接口
	"""
	def __init__( self ):
		self.updateMilitaryRank()

	def addExploit(self , addValue):
		"""
		添加军功
		"""
		addValue = int(addValue)
		oldValue = self.exploit
		self.exploit  = oldValue + addValue
		self.statusMessage( csstatus.ADD_EXPLOIT_SUCCESS,addValue )
		if self.exploit < 0:
			self.exploit = 0
		self.onExploitChange()

	def onExploitChange( self ):
		"""
		军功改变
		"""
		self.updateMilitaryRank()
		self.updataExploit()

	def getExploit(self):
		"""
		获取军功
		"""
		return self.exploit

	def getMilitaryRank( self ):
		"""
		获取军衔等级
		"""
		return self.militaryRank

	def updateMilitaryRank(self):

		militaryRank = g_exploitMgr.getRoleMilitaryRank( self )
		if self.militaryRank != militaryRank:
			self.militaryRank = militaryRank
			self.onMilitaryRankChange()

	def onMilitaryRankChange( self ):
		data = g_exploitMgr.getRoleExploitData( self.getMilitaryRank() )
		if self.militaryRank > self.maxMilitaryRank:
			self.addBarracksExp( data["exp"] )
			self.maxMilitaryRank = self.militaryRank
		if self.barracksExpRate != data["expRate"]:
			self.barracksExpRate = data["expRate"]					#唯一改变barracksExpRate的地方

		if self.tongMB:
			self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID, self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())

	def exploitReduce( self , reduceNum):
		"""
		衰减军功
		"""
		oldExploit = self.exploit
		for n in range(reduceNum):
			oldExploit = oldExploit - oldExploit * 0.05
		self.exploit = int( oldExploit )
		self.onExploitChange()

#----------------------Client----------------------------------------------

	def updataExploit( self ):
		"""
		更新界面信息
		<Exposed method>
		"""
		self.client.onUpdataExploit( self.exploit , self.militaryRank)

#--------------------- GM命令 ------------------------------------------------
	def setMaxMilitaryRank( self, Value ):
		"""
		设置历史最大的军衔
		"""
		if Value > 0 and Value <= 16:
			self.maxMilitaryRank = Value
