# -*- coding: utf-8 -*-

"""
用于技能对象受术者的基类
"""


import KBEngine
#script
import CoreInterface.SkillInterface as SkillInterface
from CoreInterface.ActionFlagInterface import ActionFlagInterface
import CoreObject.GameObject as GameObject
import KST
import csdefine


class GhostReceiverObject(GameObject.GameObject, SkillInterface.SkillInterface, ActionFlagInterface ):
	"""
	技能对象受术者
	"""
	def __init__(self):
		GameObject.GameObject.__init__(self)
		ActionFlagInterface.__init__(self)
		SkillInterface.SkillInterface.__init__( self )
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_GHOST_RECEIVER )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt( csdefine.ENTITY_FLAG_EXT_GHOST_RECEIVER )

	def getScript( self ):
		return None
	
	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		SkillInterface.SkillInterface.beforeDestroy( self )
		GameObject.GameObject.beforeDestroy(self)
		
	def stopMoving( self, moveScriptID ):
		pass

	def onActWordChangedTrigger(self, params):
		"""
		"""
		ActionFlagInterface.onActWordChangedTrigger(self, params)
		act, disabled =  params
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, self.id, {"actWord":act, "disabled": disabled})

	def changeDirection(self, direction, reason= csdefine.REASON_CHANGE_DIR_FORCE):
		"""
		改变朝向 需要判断是主动设置还是被动设置 事务见:CST-7630 程序功能需求（0级）—— "禁止转向"设定优化
		"""
		#主动改变朝向
		if reason == csdefine.REASON_CHANGE_DIR_VOLUNTARY:
			if self.actionForbidSign(csdefine.ACTION_FORBID_TRANSLATE_DIRECTION):
				return

		self.setDirection(direction)
		
	def setAttrBuffsForClient( self, clientBuffs):
		pass