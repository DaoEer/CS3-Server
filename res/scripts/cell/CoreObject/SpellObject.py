# -*- coding: utf-8 -*-

"""
用于施法箱子类型的基本类型
"""


import KBEngine
import KST
#script
import CoreObject.NPCBaseObject as NPCBaseObject
import CoreInterface.SkillInterface as SkillInterface
import csdefine


class SpellObject( NPCBaseObject.NPCBaseObject, 
			SkillInterface.SkillInterface,
			 ):
	"""
	NPC对象基类
	"""
	def __init__(self):
		NPCBaseObject.NPCBaseObject.__init__(self)
		SkillInterface.SkillInterface.__init__( self )
		self.__scriptObject = None
		self.getScript().initEntity( self )

	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_SPELL )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_SPELL)

	def getScript( self ):
		if not self._scriptObject:
			self._scriptObject = KST.g_objFactory.getSpellBoxObject( self.scriptID )
		return self._scriptObject
	
	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		SkillInterface.SkillInterface.beforeDestroy( self )
		NPCBaseObject.NPCBaseObject.beforeDestroy(self)

	def actionForbidSign( self, signWord ):
		"""
		是否存在标记。
			@return	:	标记字
			@rtype	:	bool
		"""
		return False

	def requestRefreshCondition( self, selfEntity, playerEntity ):
		"""
		请求更新可交互条件是否已满足
		"""
		pass