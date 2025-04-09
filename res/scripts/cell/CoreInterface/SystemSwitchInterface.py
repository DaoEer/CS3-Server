# -*- coding: utf-8 -*-

import KBEDebug
from ConfigObject.SystemSwitch.SystemSwitchLoader import g_systemSwitchLoader

class SystemSwitchInterface:
	"""
	系统开关接口
	"""
	def __init__( self ):
		pass

	def checkSystemSwitchCnd( self, systemID, player ):
		"""
		检测系统是否开启
		"""
		return g_systemSwitchLoader.check( str(systemID), player )
