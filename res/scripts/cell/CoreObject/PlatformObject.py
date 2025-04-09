# -*- coding: utf-8 -*-

"""
用于移动平台类型的基本类型
"""

import KBEngine
#script
import CoreObject.SceneObject as SceneObject
import KST
import csdefine


class PlatformObject(SceneObject.SceneObject):
	"""
	移动平台对象基类
	"""
	def __init__(self):
		SceneObject.SceneObject.__init__(self)
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_PLATFORM )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_PLATFORM)
	
	def behIsOptimize(self, bedType, behDescribe):
		"""
		是否采用优化的方案，目前暂时没有确定是判断逻辑
		:return: bool
		"""
		return False