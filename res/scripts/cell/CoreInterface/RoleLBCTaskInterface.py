#-*-coding:utf-8 -*-

import KBEMath
import Functions
import csconst
import KBEDebug
import KST
import random
import csdefine
import Const
import csstatus
class RoleLBCTaskInterface:
	"""
	练兵场练兵任务
	"""
	def __init__(self):
		pass



	def onFixedTimeZero(self):
		#零点重置剩余练兵次数
		self.setLbcTaskProcesses(csconst.LBC_TASK_PROCESSES)

	def setLbcTaskProcesses(self, processes):
		"""
		设置剩余练兵次数
		"""
		self.lbcTaskProcesses = processes

	def decLbcTaskProcesses(self):
		"""
		"""
		self.lbcTaskProcesses-=1

	def getLbcTaskProcesses(self):
		"""
		"""
		return self.lbcTaskProcesses

	def openLbcTaskUI(self, npcID):
		"""
		打开任务面板
		"""
		self.client.OpenLbcTaskUI(self.self.getLbcOccupyItem().level, npcID)


	def acceptLbcTask(self, exposed):
		"""
		接受任务
		"""
		if self.lbcTaskProcesses<=0:
			self.statusMessage(csstatus.LBC_TASK_PROCESS_LIMITED)
			return
		payItems ={}
		payItems[ csdefine.TRADE_PAY_ITEM_GOODS_BY_ID ] = {Const.TRAIN_GROUND_QUEST_UST_ITEM : 1}
		self.requestPay( csdefine.TRADE_TYPE_ACCEPT_LBC_TASK, 0, payItems)

	def onAcceptLbcTaskSuccessed(self):
		
		self.decLbcTaskProcesses()
		self.gotoLbcTaskSpace()


	def gotoLbcTaskSpace(self):
		"""
		进入任务地图
		"""
		spaceScriptID = self.getLbcTaskSpaceScriptID()
		if not spaceScriptID:
			KBEDebug.ERROR_MSG("spaceScriptID is \"\" ")
			return 

		spaceObj = KST.g_objFactory.getSpaceObject(spaceScriptID)
		if spaceObj is None:
			KBEDebug.ERROR_MSG("not found space[%s] object" %(spaceScriptID))
			return

		packArgs={
			"lastPos": self.position,
			"lastDir":self.direction,
			"lastSpaceScriptID":self.getCurrentSpace().scriptID
		}

		enterPos, enterDir =  spaceObj.getEnterPosInfo()
		self.gotoSpaceUseArg(spaceScriptID, enterPos, enterDir, packArgs)


	def leaveLbcTaskSpace(self, spaceEntity):
		"""
		离开任务地图
		"""
		lastPos = spaceEntity.createArgs.get("lastPos")
		lastDir = spaceEntity.createArgs.get("lastDir")
		lastSpaceScriptID = spaceEntity.createArgs.get("lastSpaceScriptID")
		
		self.gotoSpace(lastSpaceScriptID, lastPos, lastDir)


	def getLbcTaskSpaceScriptID(self):
		"""
		获取任务地图名
		"""		
		level = self.occupyInfo.level
		return random.choice(csconst.LBC_TASK_SPACE[level]) \
			if level in csconst.LBC_TASK_SPACE else ""


	def lbcTaskStartPlay(self, exposed):
		"""
		开始游戏
		"""
		if not self.validateClientCall(exposed):
			return
		space = self.getCurrentSpace()
		space.startPlay()



	def roleMoveToLocationOver(self, exposed):
		"""
		玩家移动结束回调
		"""
		if not self.validateClientCall(exposed):
			return
		space = self.getCurrentSpace()
		space.beginFight()

