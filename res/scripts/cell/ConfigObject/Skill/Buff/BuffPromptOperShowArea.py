# -*- coding: utf-8 -*-
from ConfigObject.Skill.Buff.BuffPromptOper import BuffPromptOper


class BuffPromptOperShowArea( BuffPromptOper ):
	"""
	操作提示(会在大地图显示目标区域)
	"""
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffPromptOper.init( self, receiver, buffData )
		receiver.client.CLIENT_ShowAreaInBigMapUI(self._spaceScriptID, self._spacePos, self._radius)
		
