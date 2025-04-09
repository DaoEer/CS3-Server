# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyTong import SpaceCopyTong
import KBEDebug
import Math


class SpaceCopyLingHunZhiShi( SpaceCopyTong ):
	"""
	灵魂之誓(CST-3704 程序功能需求（35级）——环任务【灵魂之誓】玩法功能)
	"""
	def __init__( self ):
		SpaceCopyTong.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopyTong.initData( self, configData )
		#怪物数据
		self.monsterData = configData["SpaceData"].get("monsterData",None)
		self.weakBuffID = int(configData["SpaceData"].get("weakBuffID",None))


		




