# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import json
import Functions
import KBEMath
import Math
import KBEDebug
import csdefine
import Define
import time
import Const
import csstatus
import csconst

class SpaceCopyLQMG( SpaceCopyRingTaskChild ):
	"""
	环任务【灵气迷宫】
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond, "notCloseSpace", () )
		if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		else:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))
			
	def changeSpaceLife( self, selfEntity, dynamicTime ):
		"""
		改变计时
		"""
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		selfEntity.popTimer( selfEntity.lifeNotifyTimer )
		selfEntity.lifeNotifyTimer = 0
		
		selfEntity.dynamicTime += dynamicTime
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		if remainTime >= 0:
			selfEntity.lifeTimer = selfEntity.addTimerCallBackForScript( remainTime, "notCloseSpace", () )
			if remainTime - Const.SPACE_LIFE_NOTIFY_TIME >= 0:
				if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( remainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
				else:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( remainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )
		else:
			selfEntity.getScript().onConditionChange( selfEntity, "", selfEntity.id, "closeSpace", "" )

	def notCloseSpace(self, selfEntity):
		"""
		"""
		selfEntity.getScript().onConditionChange( selfEntity, "", selfEntity.id, "closeSpace", "" )
