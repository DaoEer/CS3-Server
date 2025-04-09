# -*- coding: utf-8 -*-
#
import KBEDebug
from ConfigObject.Quest.QuestBase.Quest import Quest
import Functions
import time
import csconst

class QuestJSZZ( Quest ):
	"""
	金树种任务
	第一阶段：QuestTaskJSZZFirstStage
	第二阶段：QuestTaskJSZZSecondStage
	第三阶段：QuestTaskJSZZThirdStage
	"""
	def __init__(self):
		Quest.__init__(self)

	def initFromConfig(self, id, tasks, data):
		Quest.initFromConfig(self, id, tasks, data)
		self._tasks[2].setPlantData(self._tasks[1].spaceScriptID,self._tasks[1].number)
		self._tasks[3].setPlaneData( self._tasks[1].spaceScriptID )

	def initFromStream(self, data):
		Quest.initFromStream(self, data)
		self._tasks[2].setPlantData(self._tasks[1].spaceScriptID,self._tasks[1].number)
		self._tasks[3].setPlaneData( self._tasks[1].spaceScriptID )		

	def getRemainTime( self ):
		"""
		获得剩余时间
		"""
		return int(25*60 - (time.time() - self._tasks[1].startTime)) #暂时写定任务时长为25分钟

	def showFirstTaskToClient( self, player ):
		"""
		通知客户端显示第一阶段数据
		"""
		if player.getClient() and self._tasks[1].spaceScriptID != "" and self._tasks[1].pos != None:
			player.client.CLIENT_showJSZZFirstTaskData( self._tasks[1].spaceScriptID,Functions.vector3TypeConvert(self._tasks[1].pos), self._tasks[1].radius )
			player.client.CLIENT_showJSZZQuestTime( str(int((self._tasks[1].startTime + 25*60) * csconst.TIME_ENLARGE_MULTIPLE)) )

	def showSecondTaskToClient( self, player ):
		"""
		通知客户端显示第二阶段数据
		"""
		if player.getClient() and self._tasks[2].plantCenterPos != None and self._tasks[2].plantRadius !=0.0:
			player.client.CLIENT_showJSZZSecondTaskData( self._tasks[2].plantCenterPos,self._tasks[2].plantRadius )
		if self._tasks[1].isDone() and not self._tasks[2].isDone():
			self.addSecondTaskArea(player)
			self.notifyClientSecondTaskCanSearch( player )

	def addSecondTaskArea( self, player ):
		"""
		"""
		if player.getClient():
			player.client.CLIENT_AddJSZZCircleArea( self._tasks[1].spaceScriptID, self._tasks[2].plantCenterPos,self._tasks[2].plantRadius )

	def clearSecondTaskArea( self, player ):
		"""
		"""
		if player.getClient():
			player.client.CLIENT_ClearJSZZCircleArea()

	def notifyClientSecondTaskCanSearch( self, player ):
		"""
		"""
		if player.getClient():
			player.client.CLIENT_NotifyClientSecondTaskCanSearch()

	def requestGotoJSZZPlane( self, player ):
		"""
		请求进入第三阶段的位面
		"""
		player.gotoSpacePlane( self._tasks[3].planeScriptID )

	def onTaskCompleted( self, taskID, player ):
		"""
		某个任务目标完成
		"""
		if taskID == 1:
			self.notifyClientSecondTaskCanSearch( player )
			self.addSecondTaskArea(player)
		if taskID == 2:
			self.clearSecondTaskArea(player)
			self.requestGotoJSZZPlane(player)

	def checkQuestIsTimeOut( self ):
		"""
		检查该任务是否超时
		"""
		if self.getRemainTime() <= 0 :
			return True
		return False

	def getFirstTaskData( self ):
		"""
		"""
		return ( self._tasks[1].spaceScriptID,self._tasks[1].pos,self._tasks[1].radius )

	def getFirstTaskNumber( self ):
		"""
		"""
		return self._tasks[1].number

	def getSecondTaskData( self ):
		"""
		"""
		return ( self._tasks[1].spaceScriptID,self._tasks[2].plantCenterPos,self._tasks[2].plantRadius )

	def getSecondTaskSearchSkillID( self ):
		"""
		获得第二阶段的搜索的技能ID
		"""
		return self._tasks[2].searchSkillID

	def getSecondTaskPlantSkillID( self ):
		"""
		获得第二阶段的种植的技能ID
		"""
		return self._tasks[2].plantSkillID

	def getThirdTaskPlaneRadius( self ):
		"""
		获得第三阶段的位面范围
		"""
		return self._tasks[3].planeRadius
