# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import KST
import csdefine
import csstatus
from CoreObject.MgrPersistentObject import MgrPersistentObject
from CampMoraleConfigLoader import g_campMoraleConfig
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()

class CampMgr(MgrPersistentObject):
	"""
	阵营管理器
	"""
	def __init__(self):
		MgrPersistentObject.__init__(self)
		self.register()

	def register( self ):
		"""
		注册
		"""
		# 活动事件绑定
		taskEvents = {
						"CampMorale_reset": "onMoraleReset",
						"CampKillerList_reset":"onKillerListReset",
						}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )
		self.onCompleteInit()

	def onMoraleReset( self, cmd ):
		"""
		define method.
		重置阵营士气
		"""
		self.setMoraleRewards()
		self.taoismMorale = 0
		self.demonMorale = 0
		self.taoismVenName = ""
		self.demonVenName = ""
		self.setMorale( csdefine.CAMP_TAOSIM, 0 )
		KST.g_baseAppEntity.resetCampData()

	def onKillerListReset(self, cmd):
		"""
		define method.
		重置击杀者列表
		"""
		def sqlcallback1(result, rows, insertid, errstr):
			if errstr != None:
				KBEDebug.ERROR_MSG("clear tbl_Role_camp_killerList  is Failed")
				return
		def sqlcallback2(result, rows, insertid, errstr):
			if errstr != None:
				KBEDebug.ERROR_MSG("clear sm_dayCampMorale  is Failed")
				return
		sql = " Delete table tbl_Role_camp_killerList"
		sql_role = "UPDATE tbl_Role SET sm_dayCampMorale = 0"
		KBEngine.executeRawDatabaseCommand(sql,sqlcallback1)
		KBEngine.executeRawDatabaseCommand(sql_role,sqlcallback2)
		KST.g_baseAppEntity.clearCampKillerList()


	def addMorale( self, camp, morale ):
		"""
		define method.
		添加阵营士气，morale：可为负数
		"""
		if not self.campSwitch:
			return
		if camp == csdefine.CAMP_TAOSIM:
			morale += self.taoismMorale
		elif camp == csdefine.CAMP_DEMON:
			morale += self.demonMorale
		if morale < 0:
			morale = 0
		self.setMorale( camp, morale )


	def setMorale( self, camp, morale ):
		"""
		define method.
		设置阵营士气值
		"""
		if camp == csdefine.CAMP_TAOSIM:
			oldMorale = self.taoismMorale
			self.taoismMorale = morale
			skillID = g_campMoraleConfig.getMoraleSkillID( morale - self.demonMorale )
			KST.g_baseAppEntity.globalRemoteCallCampMoraleCell( camp, self.taoismMorale, oldMorale, self.demonMorale, skillID )
			skillID = g_campMoraleConfig.getMoraleSkillID( self.demonMorale - morale )
			KST.g_baseAppEntity.globalRemoteCallCampMoraleCell( csdefine.CAMP_DEMON,  self.demonMorale, self.demonMorale, self.taoismMorale, skillID )
		elif camp == csdefine.CAMP_DEMON:
			oldMorale = self.demonMorale
			self.demonMorale = morale
			skillID = g_campMoraleConfig.getMoraleSkillID( morale - self.taoismMorale )
			KST.g_baseAppEntity.globalRemoteCallCampMoraleCell( camp, self.demonMorale, oldMorale, self.taoismMorale, skillID )
			skillID = g_campMoraleConfig.getMoraleSkillID( self.taoismMorale - morale )
			KST.g_baseAppEntity.globalRemoteCallCampMoraleCell( csdefine.CAMP_TAOSIM, self.taoismMorale, self.taoismMorale, self.demonMorale, skillID )

	def setCampVenName(self, camp, name ):
		"""
		define method.
		设置阵营尊者名字
		"""
		if camp == csdefine.CAMP_TAOSIM:
			self.taoismVenName = name
		elif camp == csdefine.CAMP_DEMON:
			self.demonVenName = name

	def queryCampMorale( self, roleBase, camp ):
		"""
		define method.
		玩家上线查询阵营气运值
		"""
		roleBase.cell.setClientCampSwitch( self.campSwitch )
		if camp == csdefine.CAMP_TAOSIM:
			roleBase.cell.onQueryCampMorale( self.taoismMorale, self.demonMorale )
		elif camp == csdefine.CAMP_DEMON:
			roleBase.cell.onQueryCampMorale( self.demonMorale, self.taoismMorale )

	def setMoraleRewards(self):
		"""
		结算奖励
		"""
		self.resetMoraleReward()
		self.taoismMoraleReward = g_campMoraleConfig.getRewardIDByMorale(self.taoismMorale)
		self.demonMoraleReward = g_campMoraleConfig.getRewardIDByMorale(self.demonMorale)

	def resetMoraleReward(self):
		"""
		重置奖励
		"""
		def sqlcallback(result, rows, insertid, errstr):
			if errstr != None:
				KBEDebug.ERROR_MSG("clear sm_isGetCampReward  is Failed")
				return
		sql_role = "UPDATE tbl_Role SET sm_isGetCampReward = 0"
		KBEngine.executeRawDatabaseCommand(sql_role,sqlcallback)

	def queryMoraleRewards(self, roleBase, camp):
		"""
		define method.
		获得奖励
		"""
		if camp == csdefine.CAMP_TAOSIM:
			roleBase.cell.onQueryMoraleRewards( self.taoismMoraleReward )
		elif camp == csdefine.CAMP_DEMON:
			roleBase.cell.onQueryMoraleRewards( self.demonMoraleReward)

	def queryCampUIData(self, roleBase, camp):
		"""
		define method.
		查询阵营界面数据
		"""
		roleBase.cell.onQueryCampUIData( self.taoismMorale, self.demonMorale, self.taoismVenName, self.demonVenName )

	def onCampVenOline(self, venName, title, camp ):
		"""
		define method.
		阵营尊者上线
		"""
		KST.g_baseAppEntity.globalRemoteCampVenOline(venName, title, camp)

	def setCampSwitch(self, campSwitch):
		"""
		define method.
		设置阵营开关
		"""
		if not campSwitch:
			self.onMoraleReset()
		self.campSwitch = campSwitch
		KST.g_baseAppEntity.globalOnSetCampSwitch(campSwitch)

	def onCampBeKilled(self, roleBase, killerID):
		"""
		define method.
		被敌对阵营玩家击杀
		"""		
		if not self.campSwitch:
			return
		roleBase.cell.onCampBeKilled(killerID)

