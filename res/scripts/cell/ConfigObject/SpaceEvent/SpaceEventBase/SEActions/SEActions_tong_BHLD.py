# -*- coding: utf-8 -*-

# 帮会掠夺 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

class SEAction466( SEActionBase ):
	"""
	帮会掠夺胜利/失败给邮件奖励
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.winMailIDList = section["param1"].split("|")
		self.loseMailIDList = section["param2"].split("|")
		
		self.levelsegment = []
		segmentList = section["param3"].split("|")
		for segment in segmentList:
			temp = segment.split("-")
			self.levelsegment.append([int(temp[0]), int(temp[1])])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		if len(self.levelsegment) != len(self.winMailIDList):
			KBEDebug.ERROR_MSG("win config error, %s, %s" %(self.levelsegment, self.winMailIDList))
			return
			
		if len(self.levelsegment) != len(self.loseMailIDList):
			KBEDebug.ERROR_MSG("lose config error, %s, %s" %(self.levelsegment, self.loseMailIDList))
			return
			
		winMailID = self.getMailByLevel(spaceEntity.getWinnerTongLevel(), self.winMailIDList)
		if winMailID is None:
			KBEDebug.ERROR_MSG("win NOT found mailID %s" %(spaceEntity.getWinnerTongLevel()))
			return
			
		loseMailID = self.getMailByLevel(spaceEntity.getLoserTongLevel(), self.loseMailIDList)
		if winMailID is None:
			KBEDebug.ERROR_MSG("lose NOT found mailID %s" %(spaceEntity.getLoserTongLevel()))
			return
		
		for m in spaceEntity.plunderMemberDatas.getMembers():
			if m.belongSide == spaceEntity.winnerTongBelongSide:
				g_mailContentDataLoader.sendSpaceReward(winMailID, m.roleName)
			else:
				g_mailContentDataLoader.sendSpaceReward(loseMailID, m.roleName)
		
	def getMailByLevel(self, level, mailIDList):
		for index, levelsegment in enumerate(self.levelsegment):
			if level >= levelsegment[0] and level <= levelsegment[1]:
				return mailIDList[index]
		return None	

SEActionBase.setActionClass("SEAction466", SEAction466)
