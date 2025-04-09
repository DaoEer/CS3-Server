# -*- coding: utf-8 -*-
#############
# 九字真言副本(真言)
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtJiuZiZhenYan( Monster.Monster ):
	"""
	真言（墙壁）
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.zhenYanType = 0
		self.buffInfo = None
		
	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		self.zhenYanType = int(configData["Param1"])
		if not configData["Param2"]: return
		tempLst = configData["Param2"].split("|")
		if len(tempLst) <= 0: return
		self.buffInfo = (int(tempLst[0]), int(tempLst[1]), int(tempLst[2]))
		
	def getBuffInfo(self):
		return self.buffInfo