#-*-coding:utf-8-*-
import random
import ItemFactory
import KBEDebug
import KBEngine
import csdefine
import csstatus
import Functions
import Const
import QuestEventDefine
from ConfigObject.ChuanChengSkillLoader import g_ChuanChengSkillLoader

CHUANCHNEG_SKILL_BAR = {
	2:(50000, 80000),
	3:(150000, 200000)
}

class RoleChuanChengInterface:
	"""
	传承技能
	"""
	def __init__(self):
		if len(self.chuanChengSkillsBar) <= 0:				#新账号初始化被动技能栏
			self.initChuanChengSkillsBar()

#-------------------------------------传承技能使用---------------------------------------
	def initChuanChengSkillsBar(self):
		if len(self.chuanChengSkillsBar) > 0: return
		for i in range(4):
			dct = {}
			dct["id"] = i+1
			dct["isLock"] = True
			if i == 0:
				dct["isLock"] = False
			self.chuanChengSkillsBar.adSkillBarData(dct)

	def initChuanChengSKill(self):
		# 初始化传承技能快捷栏
		for i in self.chuanChengSkillsBar.values():
			self.client.UpdateChuanChengSkillBar(i)
		# 初始化传承技能当前经验
		for skillID, exp in self.chuanChengUpgrade.items():
			self.client.UpdateChaunChengExp(skillID, 0, exp )

	def requestUnlockChuanChengSkillBar(self, srcEntityID, index):
		"""
		Exposed method
		解锁传承技能装备栏位
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		if index > len(self.chuanChengSkillsBar) -1:
			return
		#自己前面一个栏位是否已经解锁
		skillBar = self.chuanChengSkillsBar.get((index-1), None)
		if skillBar and skillBar["isLock"]:return
		
		#当前栏位是否已经解锁
		skillBar = self.chuanChengSkillsBar.get(index, None)
		if not skillBar or not skillBar["isLock"]:return
		if index == 2 or index == 3:
			potential = CHUANCHNEG_SKILL_BAR[index][1]
			money = CHUANCHNEG_SKILL_BAR[index][0]
			self.inquireMessage(csstatus.CC_SKILL_BAR_IS_OPEN, [Functions.moneyToStr(potential), Functions.moneyToStr(money)], "payUnlockChuanChengSkillBar", index, potential, money)
			return
		elif index == 4:
			if self.title != csdefine.CAMP_FENG_MING_VEV_TITLE:
				self.statusMessage( csstatus.POTENTIAL_NO_EMOUGHT, "" )
				return
		self.chuanChengSkillsBar[index]["isLock"] = 0
		self.client.OnUnlockChuanChengSkillBar(index)
		self.client.UpdateChuanChengSkillBar(self.chuanChengSkillsBar[index])

	def payUnlockChuanChengSkillBar(self, reply, index, potential, money):
		"""
		支付解锁传承技能栏
		"""
		if reply:
			if self.potential < potential:
				self.statusMessage( csstatus.CC_SKILL_BAR_POTENTIAL_NOT_ENOUGH, "" )
				return
			if self.getBindMoney() < money:
				self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(money)], "continueUnlockChuanChengSkillBar", index, potential, money)
				return
			self.subBindMoney( money, csdefine.MONEY_SUB_REASON_UNLOCK_CHUANCHENGSKILLBAR )
			self.subPotential( potential, csdefine.POTENTIAL_REMOVE_REASON_UNLOCK_CHUANCHENGSKILLBAR )
			self.chuanChengSkillsBar[index]["isLock"] = 0
			self.client.OnUnlockChuanChengSkillBar(index)
			self.client.UpdateChuanChengSkillBar(self.chuanChengSkillsBar[index])

	def continueUnlockChuanChengSkillBar(self, reply, index, potential, money):
		if reply:
			if self.getMoney()<money:
				self.statusMessage( csstatus.CC_SKILL_BAR_MONEY_NOT_ENOUGH, "" )
				return
			self.subMoney( money, csdefine.MONEY_SUB_REASON_UNLOCK_CHUANCHENGSKILLBAR )
			self.subPotential( potential, csdefine.POTENTIAL_REMOVE_REASON_UNLOCK_CHUANCHENGSKILLBAR )
			self.chuanChengSkillsBar[index]["isLock"] = 0
			self.client.OnUnlockChuanChengSkillBar(index)
			self.client.UpdateChuanChengSkillBar(self.chuanChengSkillsBar[index])

	def requestFitChuanChengSkill(self, srcEntityID, skillID, index):
		"""
		Exposed method
		装上传承技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		dstSkillBar = self.chuanChengSkillsBar.get(index, None)
		if not dstSkillBar or dstSkillBar["isLock"]: return
		
		#技能本来就在指定的位置上
		dstSkill = dstSkillBar["skillID"]
		if dstSkill == skillID: return
		
		#没有学习该技能或不是被动技能
		if skillID not in self.attrSkills: return
		
		srcIndex = 0
		for i in range(1, index):
			if i not in self.chuanChengSkillsBar: break
			#判断当前技能是否已在被动技能栏中（已激活）
			if self.chuanChengSkillsBar[i]["skillID"] == skillID:
				srcIndex = i
				break
		
		self.chuanChengSkillsBar[index]["skillID"] = skillID
		self.client.UpdateChuanChengSkillBar(self.chuanChengSkillsBar[index])
		
		#skillID本来就已经在技能栏中了（已激活）
		if srcIndex:
			self.chuanChengSkillsBar[srcIndex]["skillID"] = dstSkill
			self.client.UpdateChuanChengSkillBar(self.chuanChengSkillsBar[srcIndex])
	
	def requestUnloadChuanChengSkill(self, srcEntityID, index):
		"""
		Exposed method
		卸下传承技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		skillBar = self.chuanChengSkillsBar.get(index, None)
		if not skillBar or skillBar["isLock"]: return
		
		#没有技能在指定的位置上
		if not skillBar["skillID"]: return
		skillID = self.chuanChengSkillsBar[index]["skillID"]
		self.chuanChengSkillsBar[index]["skillID"] = 0
		self.client.UpdateChuanChengSkillBar(self.chuanChengSkillsBar[index])

	def learnChuanChengSkill( self, skillID ):
		"""
		学习传承技能
		"""
		if self.hasSkill(skillID):
			self.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )
			return
		self.onSuccessPayChuanChengSkill(0, skillID)

#---------------------------------------传承技能升级--------------------------------------------
	def requestChuanChengSkillUpgrade(self, srcEntityID, skillID):
		"""
		<Exposed method>
		请求升级一个传承技能

		@param  srcEntityID: 玩家id
		@param  skillID: 目标技能ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return	

		if self.hasSkill(skillID):
			self.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )
			return
		skillLearnData = g_ChuanChengSkillLoader.getSkillLearnData(skillID)
		if skillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find skill(%d) learn config!"%skillID)
			return
		if not skillLearnData["ReqSkill"] in self.attrSkills:
			KBEDebug.ERROR_MSG("Learn skill(%d) err!cannot find reqSkill(%d)"%(skillID,skillLearnData["ReqSkill"]))
			return
		if self.level < skillLearnData["ReqLevel"]:
			self.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_LEVEL_NOT_ENOUGH )
			return
		
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_POTENTIAL] = skillLearnData["ReqPotential"]
		payItems.update( self.getSkillLearnCostMoneyDatas(skillLearnData["Money"]) )
		self.requestPay(csdefine.TRADE_TYPE_LEARN_CHUANCHENG_SKILL, 0, payItems, skillLearnData["ReqSkill"], skillID)

	def onSuccessPayChuanChengSkill( self, oldSkillID, newSkillID ):
		"""
		学习传承技能

		@param  oldSkillID: 升级前技能id（如果为激活技能，该变量为0）
		@param   newSkillID: 新技能id
		"""
		if oldSkillID != 0:
			self.removeSkill(oldSkillID, csdefine.SKILL_REMOVE_REASON_LEARN_SKILL)
		self.addSkill(newSkillID)
		# 玩家学习某个技能任务目标完成
		self.triggerQuestEvent( QuestEventDefine.EVENT_LEARN_SKILL, newSkillID )