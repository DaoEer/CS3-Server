import KBEngine
#common
import Singleton
import KBEDebug
import LoadModule
import SmartImport
import csconst
import json
import csdefine

ANTIWALLOW_CONFIG = "res/volatile_data/AntiWallow.json"

class AntiWallowLoader(Singleton.Singleton):
	"""
	防沉迷配置读取，写入
	"""
	def __init__( self ):
		self.datas = {}

	def loadAllData( self ):
		try:
			self.datas = LoadModule.openFile(ANTIWALLOW_CONFIG)
		except IOError:
			KBEDebug.WARNING_MSG("----AntiWallow.json---- open error")

	def writeRoleData(self, newData):
		try:
			ConfigData = LoadModule.openFile(ANTIWALLOW_CONFIG)
			oldData = ConfigData["role"]
			oldData.update(newData)
			self.datas = ConfigData

			strfile = ANTIWALLOW_CONFIG
			wf = open( strfile, "w" )
			json.dump( ConfigData, wf, indent=4 )
			wf.close()
		except IOError:
			KBEDebug.WARNING_MSG("The failed that write config to AntiWallow.json !!! write again next times!!")

	def getAllData(self):
		return self.datas

	def getData(self, key, default = None):
		try:
			return self.datas[key]
		except KeyError:
			return default

	def getRoleData(self, key, default = None):
		try:
			return self.datas["role"][key]
		except KeyError:
			return default

g_antiWallow = AntiWallowLoader()
g_antiWallow.loadAllData()