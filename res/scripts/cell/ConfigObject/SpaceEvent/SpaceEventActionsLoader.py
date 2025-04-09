# -*- coding: utf-8 -*-

import os
import json
import HotUpdate
from KBEDebug import *
from LoadModule import *
from Singleton import Singleton
from SmartImport import smartImport
import SpaceEvent.SpaceEventActions
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

SEACTION_PATCH = "res/scripts/cell/ConfigObject/SpaceEvent/SpaceEventBase/SEActions"
def getSEActionsPathFiles():	#获得SEActions文件夹下的所有文件名
	tempList = []
	if os.path.isdir(SEACTION_PATCH):
		for file in os.listdir( SEACTION_PATCH ):
			filePath = SEACTION_PATCH + "/" + file
			if os.path.isfile( filePath ) and os.path.splitext(filePath)[1] in [".py", ".pyc"]:
				tempList.append(file.rsplit("/")[-1].rsplit(".")[0])
	return tempList

class SpaceEventActionsLoader( Singleton ):
	"""
	副本事件行为加载类
	"""
	def __init__( self ):
		self._datas = {}

	def init( self ):
		"""
		加载AI配置
		"""
		for SEActionsPath in getSEActionsPathFiles():
			__import__("ConfigObject.SpaceEvent.SpaceEventBase.SEActions" +"."+ SEActionsPath )	#动态导入SEActions文件夹下模块
		for id, data in SpaceEvent.SpaceEventActions.Datas.items():
			scriptName = data["scriptName"]
			action = SEActionBase.getActionClassObj(scriptName)
			if action == None:
				ERROR_MSG( "SpaceEventAction import scriptName = %s! id: %i.,Maybe not do SEActionBase.setActionClass"%(scriptName,id) )
				continue
			self._datas[id] = action
			
	def reloadConfig( self ):
		"""
		热加载配置
		"""
		module = HotUpdate.reloadByModule( SpaceEvent.SpaceEventActions )
		for SEActionsPath in getSEActionsPathFiles():
			__import__("ConfigObject.SpaceEvent.SpaceEventBase.SEActions" +"."+ SEActionsPath )	#动态导入SEActions文件夹下模块
		self._datas.clear()
		for id, data in module.Datas.items():
			scriptName = data["scriptName"]
			action = SEActionBase.getActionClassObj(scriptName)
			if action == None:
				ERROR_MSG( "SpaceEventAction import scriptName = %s! id: %i.,Maybe not do SEActionBase.setActionClass"%(id,scriptName) )
				continue
			self._datas[id] = action
		
	def __getitem__( self, key ):
		"""
		取得AI实例
		"""
		assert key in self._datas, "Space event action %i not find!" % key
			
		return self._datas[key]


g_SEActionsLoader = SpaceEventActionsLoader()