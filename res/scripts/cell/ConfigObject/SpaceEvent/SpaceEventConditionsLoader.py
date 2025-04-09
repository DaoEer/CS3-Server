# -*- coding: utf-8 -*-

import json
import HotUpdate
from KBEDebug import *
from LoadModule import *
from Singleton import Singleton
from SmartImport import smartImport
import SpaceEvent.SpaceEventConditions
from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase

SECONDITION_PATCH = "res/scripts/cell/ConfigObject/SpaceEvent/SpaceEventBase/SEConditions"
def getSEConditionsPathFiles():	#获得SEConditions文件夹下的所有文件名
	tempList = []
	if os.path.isdir(SECONDITION_PATCH):
		for file in os.listdir( SECONDITION_PATCH ):
			filePath = SECONDITION_PATCH + "/" + file
			if os.path.isfile( filePath ) and os.path.splitext(filePath)[1] in [".py", ".pyc"]:
				tempList.append(file.rsplit("/")[-1].rsplit(".")[0])
	return tempList

class SpaceEventConditionsLoader( Singleton ):
	"""
	副本事件条件加载类
	"""
	def __init__( self ):
		self._datas = {}

	def init( self ):
		"""
		加载AI配置
		"""
		for SEConditionsPath in getSEConditionsPathFiles():
			__import__("ConfigObject.SpaceEvent.SpaceEventBase.SEConditions" +"."+ SEConditionsPath )	#动态导入SEActions文件夹下模块
		for id, data in SpaceEvent.SpaceEventConditions.Datas.items():
			scriptName = data["scriptName"]
			condition = SEConditionBase.getConditionClassObj(scriptName)
			if condition == None:
				ERROR_MSG( "SpaceEventConditions import scriptName = %s! id: %i.,Maybe not do SEConditionBase.setConditionClass"%(scriptName,id) )
				continue
			self._datas[id] = condition
			
	def reloadConfig( self ):
		"""
		热加载配置
		"""
		module = HotUpdate.reloadByModule( SpaceEvent.SpaceEventConditions )
		for SEConditionsPath in getSEConditionsPathFiles():
			__import__("ConfigObject.SpaceEvent.SpaceEventBase.SEConditions" +"."+ SEConditionsPath )	#动态导入SEActions文件夹下模块
		self._datas.clear()
		for id, data in module.Datas.items():
			scriptName = data["scriptName"]
			condition = SEConditionBase.getConditionClassObj(scriptName)
			if condition == None:
				ERROR_MSG( "SpaceEventConditions import scriptName = %s! id: %i.,Maybe not do SEConditionBase.setConditionClass"%(scriptName,id) )
				continue
			self._datas[id] = condition
				
	def __getitem__( self, key ):
		"""
		取得AI实例
		"""
		assert key in self._datas, "Space event condition %i not find!" % key
			
		return self._datas[key]

	def createConditionObj( self, id, dict ):
		if id not in self._datas:
			return None
		return self._datas[ id ]( dict )


g_SEConditionsLoader = SpaceEventConditionsLoader()