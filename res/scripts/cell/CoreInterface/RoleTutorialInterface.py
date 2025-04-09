# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
import cschannel_msgs
import Functions
from KBEDebug import *
import Math

from LoadJsonData import g_JsonData

class RoleTutorialInterface:
	"""
	指引提示
	"""
	def __init__(self):
		pass


	def AddTrigger(self, srcEntityID, Index):
		"""
		Exposed method
		添加一次触发索引
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.RecordTutorialIndexs == "":
			self.RecordTutorialIndexs = Index
		else:
			self.RecordTutorialIndexs += ("|" + Index)

