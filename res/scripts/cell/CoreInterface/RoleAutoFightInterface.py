# -*- coding- : utf-8 -*-

import KBEngine
import KBEDebug


class RoleAutoFightInterface:
	"""
	"""
	def __init__(self):
		pass
	
	def CELL_addSkillOnList(self, srcEntityID, skillKey, skillID):
		"""
		expose method
		添加技能到快捷栏
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if skillID not in self.attrSkills:
			return
		
		self.quick_attrSkills[skillKey] = skillID
		
	def CELL_removeSkillOnList(self, srcEntityID, skillKey):
		"""
		Exposed method
		从快捷栏移除技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if skillKey in self.quick_attrSkills:
			self.quick_attrSkills.pop(skillKey)
		