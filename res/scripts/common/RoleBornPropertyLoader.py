# -*- coding: utf-8 -*-

import Singleton
import RoleBornPropertyConfig

class RoleBornPropertyLoader( Singleton.Singleton ):
	"""
	出生属性加载模块
	"""
	def __init__(self):
		self._datas = RoleBornPropertyConfig.Datas

	def getQuest( self, camp, profession, gender ):
		#任务
		strcamp = str(camp)		
		strgender = str(gender)
		strprofession = str(profession)
		
		return self._datas[strcamp][strgender][strprofession]["questID"]

	def getSkills( self, camp, profession, gender ):
		#技能
		strcamp = str(camp)		
		strgender = str(gender)
		strprofession = str(profession)
		
		return self._datas[strcamp][strgender][strprofession]["skills"]

	def getQuickBarSkills( self, camp, profession, gender ):
		#快捷栏技能
		strcamp = str(camp)		
		strgender = str(gender)
		strprofession = str(profession)
		
		return self._datas[strcamp][strgender][strprofession]["quickBarSkills"]

	def getItems( self, camp, profession, gender ):
		#物品
		strcamp = str(camp)		
		strgender = str(gender)
		strprofession = str(profession)
		
		return self._datas[strcamp][strgender][strprofession]["items"]

g_roleBornProLoader = RoleBornPropertyLoader()