import KBEngine

#common
import Singleton
import KBEDebug
import csconst
import json
from LoadModule import *
from ConfigObject.SystemSwitch import SystemSwitchCondition


class SystemSwitchLoader(Singleton.Singleton):
	"""
	系统开关配置加载
	"""
	def __init__( self ):
		self._systemDict = {}
		self.sysyemObjDict = {}

	def init( self, configData ):
		"""
		读取配置
		"""
		for systemID, datas in configData.items():
			self.sysyemObjDict[systemID] = []
			for cndCfg in datas[ "systemCondition" ]:
				cndObj = SystemSwitchCondition.SystemSwitchConditionBase.getConditionClassObj( cndCfg )
				self.sysyemObjDict[systemID].append(cndObj)

	def check( self, systemID, player ):
		"""
		"""
		if systemID in self.sysyemObjDict:
			for cndObj in self.sysyemObjDict[systemID]:
				if not cndObj.check( player ):
					return False
		return True
	
	def reloadConfig( self ):
		"""
		配置热更新
		"""
		pass

g_systemSwitchLoader = SystemSwitchLoader()