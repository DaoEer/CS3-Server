# -*- coding: utf-8 -*-
#


class QuestRequirementBase:

	def __init__(self):
		pass

	def init(self, data):
		"""
		@param data:初始化参数，参数格式由每个实例自己决定
		@type  data:pyDataSection
		@return: None
		"""
		pass

	def query(self, player):
		"""
		判断player是否符合要求
		@param player:玩家的entity实例
		@type  player:Entity
		@return: BOOL
		@rtype:BOOL
		"""
		pass

	def getDetail(self):
		"""
		返回要求相关的描述

		@return: String
		@rtype: String
		"""
		pass