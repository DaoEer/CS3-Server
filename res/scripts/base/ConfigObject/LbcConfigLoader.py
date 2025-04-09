# -*- coding: utf-8 -*-
import KBEDebug
from Singleton import Singleton
import csconst


class LbcConfigLoader( Singleton ):
	"""
	活动奖励管理类
	"""
	def __init__( self ):
		self.lbcConfig = {}

	def init( self, configData ):
		"""
		"""
		self.lbcConfig.clear()
		#分线数量，每个分线的配置是一样的
		lineNumber = csconst.LBC_LINE_NUM
		for line in range(1,lineNumber+1):
			self.lbcConfig[line] ={}
			for data in configData:
				index = data['index']
				level = data['level']
				lbcName = data['lbcName']
				temp = {'index':index, 'level':level, 'line':line, 'lbcName':lbcName}
				self.lbcConfig[line].update({index:temp})

g_lbcConfigData = LbcConfigLoader()