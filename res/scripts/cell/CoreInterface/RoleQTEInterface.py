# -*- coding: utf-8 -*-

import KBEngine
import csdefine


class RoleQTEInterface:
	"""
	QTE接口
	"""
	def __init__( self ):
		pass

	def onCompleteQTEBuffEvent( self, srcEntityID,isSucceed ):
		"""
		<Exposed Method>
		完成BuffQTE事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_QTE, self.id, {"isSucceed":int(isSucceed)} )

	def onCompleteBuffQTE( self, srcEntityID ):
		"""
		<Exposed Method>
		客户端完成整套QTE通知服务器移除QTEbuff
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_QTE, self.id, {} )

	def onCompleteQTEStoryEvent( self, srcEntityID, sceneID ):
		"""
		<Exposed Method>
		完成镜头QTE事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.client.StartPlayStory( sceneID, 1 )


	