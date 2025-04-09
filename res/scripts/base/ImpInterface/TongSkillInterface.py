# -*- coding: utf-8 -*-

import copy
import csdefine
import csstatus
import TongLoader
import KBEDebug

class TongSkillInterface( object ):
	def __init__( self ):
		pass

	def notifyClientTongSkill( self ):
		skillDict = {}
		skillDict["ResearchSkill"] = {}
		skillDict["PauseSkill"] = []
		skillDict["SkillList"] = list( self.researchSkillList )
		skillDict["SkillLevelList"] = list( self.curSkillLevelList )
		skillDict["ResearchSkill"].update( {"skillID": self.curResearchSkill.reaSkillID } )
		skillDict["ResearchSkill"].update( {"progress": self.curResearchSkill.reaProgress } )

		for skill in self.pauseResearchSkillList:
			skillDict["PauseSkill"].append( {"skillID": skill.reaSkillID, "progress": skill.reaProgress } )
		return skillDict

	def researchSkill( self, playerMB, playerDBID, skillID ):
		"""
		define method
		开始研发技能
		"""
		preSkillID = TongLoader.g_TongLoader.getPreSkill( skillID )
		if preSkillID == -1:return
		if preSkillID:
			if preSkillID not in self.researchSkillList:
				KBEDebug.ERROR_MSG("Research Tong skill(%d) err!preSkillID(%d) has not research!"%(skillID,preSkillID))
				return
		if self.curResearchSkill.reaSkillID:
			if self.curResearchSkill.reaSkillID == skillID:
				return
			else:
				playerMB.client.statusMessage( csstatus.TONG_RESEARCH_SAME_TIME_MUL_SKILLID, "" )
				return

		# 如果是暂停的技能，直接进入研发
		for reaSkillInst in self.pauseResearchSkillList:
			if reaSkillInst.reaSkillID == skillID:
				self.setResearchSkill( skillID, reaSkillInst.reaProgress )
				self.pauseResearchSkillList.remove( reaSkillInst )
				return

		reqBuildlevel = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "ResearchReqBuildIngLevel" )
		level = self.builds[csdefine.TONG_BUILDING_TYPE_YJY].getMaxLevel( self )
		if level < reqBuildlevel:
			playerMB.client.statusMessage( csstatus.TONG_RESEARCH_NO_ENOUGHT_BUILD_LEVEL, str(level) )
			return
		reqMoney = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "ResearchReqTongMoney")
		if not self.hasEnoughMoney( reqMoney ):
			playerMB.client.statusMessage( csstatus.TONG_RESEARCH_NO_ENOUGHT_MONEY, "" )
			return
		self.setResearchSkill( skillID, 0 )
		skillName = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "SkillName" )
		self.addRecord( csdefine.TONG_EVENT_REASEARCH_SKILL_BEG, self.members[playerDBID].name, skillName )

	def setResearchSkill( self, skillID, progress ):
		self.curResearchSkill.setResearchSkill( skillID, progress )
		for member in self.members.values():
			member.OnResearchTongSkill( skillID )

	def pauseSkill( self, playerMB, skillID ):
		"""
		define method
		暂停研发技能
		"""
		if self.curResearchSkill.reaSkillID:
			self.pauseResearchSkillList.append( copy.deepcopy( self.curResearchSkill ) )
			self.curResearchSkill.setResearchSkill( 0, 0 )
			for member in self.members.values():
				member.onPauseSkill( skillID )

	def tryStudyTongSkill( self, playerDBID, skillID):
		"""
		define method
		学习技能判断
		"""
		if skillID in self.researchSkillList:
			self.members[playerDBID].tryStudyTongSkill( self, skillID)
		else:
			if self.members[playerDBID].baseMailBox:
				self.members[playerDBID].baseMailBox.cell.remoteFailPay()
			KBEDebug.ERROR_MSG("Study tong skill(%d) err!cannot find research skill"%skillID )

	def onDailyTongQuestFinish( self, playerDBID ):
		"""
		define method
		帮会日常任务完成
		"""
		if not playerDBID in self.members:return
		#TongLoader.addRewardsByPlayType( self, playerDBID, csdefine.TONG_PLAY_TYPE_DAILY )
		skillID = self.curResearchSkill.reaSkillID
		if skillID:
			self.curResearchSkill.reaProgress += 1
			reqDaily = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "ResearchReqDaily" )
			if self.curResearchSkill.reaProgress >= reqDaily:
				self.onFinishResearchSkill()
			else:
				for member in self.members.values():
					member.onTongSkillProgressChange( self.curResearchSkill.reaProgress )

	def finishResearchSkill( self ):
		"""GM指令设置技能研发完成"""
		if self.curResearchSkill.reaSkillID:
			skillID = self.curResearchSkill.reaSkillID
			reqDaily = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "ResearchReqDaily" )
			self.curResearchSkill.reaProgress = reqDaily
			self.onFinishResearchSkill()

	def onFinishResearchSkill( self ):
		"""完成研发"""
		skillID = self.curResearchSkill.reaSkillID
		preSkillID = TongLoader.g_TongLoader.getPreSkill( skillID )
		if preSkillID:
			self.curSkillLevelList.remove(preSkillID)

		self.curSkillLevelList.append(skillID)
		self.researchSkillList.append(skillID)
		for member in self.members.values():
			member.onFinishResearchSkill( skillID )
		self.curResearchSkill.setResearchSkill( 0, 0 )
		skillName = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "SkillName" )
		level = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "Level" )
		self.addRecord( csdefine.TONG_EVENT_REASEARCH_SKILL_SUC, skillName, skillName, level )

	def getResearchMappingItems( self ):
		"""研发技能映射的物品"""
		return TongLoader.g_TongLoader.getItemsByResearchSkill( self.researchSkillList )