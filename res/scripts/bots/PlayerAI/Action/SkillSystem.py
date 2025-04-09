# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

from PlayerAI.Action.ActionBase import ActionBase

		
class UseSkill(ActionBase):
	"""
	使用指定技能
	"""
	def doAction(self, role, param):
		"""
		"""
		try:
			skillID = int(param)
		except:
			return
		
		ActionBase.doAction(self, role, param)
		role.GMCommand(role, "addSkill", str(param))
		role.firstUseSkillID = skillID
		
class Attack(ActionBase):
	"""
	设置使用技能开始攻击
	"""
	def doAction(self, role, param):
		"""
		"""
		try:
			skillID = int(param)
		except:
			return
		
		role.GMCommand(role, "addSkill", str(param))
		role.firstUseSkillID = skillID
		ActionBase.doAction(self, role, param)
		
ActionBase.setClass("UseSkill", UseSkill)
ActionBase.setClass("Attack", Attack)		