# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
from ConfigObject.StoryEvent.StoryEventLoader import g_storyEventLoader

class RoleStoryInterface:
	def __init__( self ):
		pass
	
	def onNotifyDoStoryEvent( self, srcEntityID, storyID, orderIndex ):
		"""
		<Exposed method>
		客户端通知服务器执行剧情事件
		"""
		KBEDebug.DEBUG_MSG("Client notify story event(%s,%s,%s)."%(srcEntityID, storyID, orderIndex))
		if not self.validateClientCall( srcEntityID ):
			return
		
		events = g_storyEventLoader.getEvents( storyID, orderIndex )
		if not events:
			KBEDebug.ERROR_MSG( "Story event wrong! (%s, %s)"%( storyID, orderIndex ) )
			return
		for event in events:
			event.do( self )
	
	def onStopPlayStory( self, srcEntityID, buffIndex, storyID ):
		"""
		<Exposed method>
		剧情结束
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_STORY_END, self.id, {"storyID":storyID, "buffIndex":buffIndex} )


	def onNotifyAddEffectList( self, srcEntityID, storyID, holdEffectList ):
		"""
		添加镜头持有
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		indexList = self.storyEffectIndex.get(storyID, [])
		for holdEffectID in holdEffectList:
			index = self.addFixIDHoldEffect( holdEffectID, self )
			indexList.append(index)
		self.storyEffectIndex[storyID] = indexList	

	def onNotifyRemoveEffectList( self, srcEntityID, storyID ):
		"""
		移除镜头持有
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		for index in self.storyEffectIndex.pop(storyID, []):
			self.removeFixIDHoldEffect(index)
