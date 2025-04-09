# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""
#KBEngine
import KBEDebug
import KBEngine
#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import ItemTypeEnum
import csdefine


CORRECT_ATTR = {
	ItemTypeEnum.EXPCORRECTION: 				['exp', 'addExp', csdefine.EXP_ADD_REASON_ATTR_CORRECT],
	ItemTypeEnum.POTENTIALCORRECTION: 			['potential', 'addPotential', csdefine.POTENTIAL_ADD_REASON_ATTR_CORRECT],
	ItemTypeEnum.XIUWEICORRECTION: 				['xiuwei', 'addXiuwei', csdefine.XIUWEI_ADD_REASON_SPACE_SENTLEMENT],
	ItemTypeEnum.MONEYCORRECTION: 				['money', 'addMoney', csdefine.MONEY_ADD_REASON_MAIL_ATTR_CORRECT],
	ItemTypeEnum.FEATSCORRECTION: 				['feats', 'addFeats', csdefine.FEATS_ADD_REASON_ATTR_CORRECT],
	ItemTypeEnum.BARRACKSEXPCORRECTION: 		['barracksExp', 'addBarracksExp', ''],
	ItemTypeEnum.INTEGRALCORRECTION: 			['sparHunTingTotalIntegral', 'addSparHunTingIntegral', ''],
	ItemTypeEnum.PSIONICCORRECTION: 			['psionic', 'addPsionic', ''],
	ItemTypeEnum.EXPLOITCORRECTION: 			['exploit', 'addExploit', ''],
	ItemTypeEnum.BINDMONEYCORRECTION: 			['bindMoney', 'addBindMoney', csdefine.MONEY_ADD_REASON_MAIL_ATTR_CORRECT]
}

CORRECT_SPECIAL_ATTR = {
	ItemTypeEnum.BANGGONGCORRECTION: 			'tongContribution',
	ItemTypeEnum.MORALECORRECTION: 				'dayCampMorale',
	ItemTypeEnum.XIANSHICORRECTION: 			'xianshi',
	ItemTypeEnum.LINGSHICORRECTION: 			'lingshi',
	ItemTypeEnum.XUANSHICORRECTION: 			'xuanshi'
}

ADD_CORRECT_REASON = 0
EXTRAL_VAL = 0

class HoldEffectAttrCorrect( HoldEffect ):
	"""
	持有效果：属性修正
	"""
	def __init__(self):
		HoldEffect.__init__(self)
		self._attrsList = []
		self._attrPercentList = []					# 加成百分比值
		self._attrValueList = []					# 附加值
		self._attrOtherCorrect = {}					# 受术者属性修正字典 {40025: 第一次修正后的值}
	
	def init(self, dictDat, skill):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if not dictDat["Param1"]:
			KBEDebug.ERROR_MSG("Buff HoldEffectAttrCorrect config is none! " )
		self._attrsList = list(map(int, dictDat["Param1"].split("|")))
		attrPercentList = list(map(float, dictDat["Param2"].split("|")))
		self._attrPercentList = [data * ItemTypeEnum.PRECENTRATIO for data in attrPercentList]
		self._attrValueList = list(map(float, dictDat["Param3"].split("|")))

		tempList = {len(self._attrsList), len(self._attrPercentList), len(self._attrValueList)}
		num = len(set(tempList))
		if num > 1:
			KBEDebug.ERROR_MSG("Num of attr, attrPercent, attrValue config is not same! " )
		if len(self._attrsList) != len(set(self._attrsList)):
			KBEDebug.ERROR_MSG("Buff HoldEffectAttrCorrect has duplicate configuration! " )

	def onBegin(self, effectData, receiver):
		"""
		效果开始
		"""
		HoldEffect.onBegin(self, effectData, receiver)
		self.doCorrectAttr(receiver)
	
	def doCorrectAttr(self, receiver):
		for index, attrID in enumerate(self._attrsList):
			if attrID not in CORRECT_ATTR and attrID not in CORRECT_SPECIAL_ATTR:
				KBEDebug.ERROR_MSG("AttrID of Buff HoldEffectAttrCorrect configuration! is wrong!")
				return

			baseVal = ItemTypeEnum.PRECENTRATIO
			extraVal = EXTRAL_VAL
			percentVal = self._attrPercentList[index]
			value = self._attrValueList[index]
			correctedCoeffi = self.calcAttrCorrectCoeffi(baseVal, extraVal, percentVal, value)
			totalCorrectCoeffi = self.overlayCorrectCoeffi(receiver, correctedCoeffi)

			if attrID in CORRECT_ATTR:
				currAttrVal = getattr(receiver, CORRECT_ATTR[attrID][0])
				finalAttrVal = round(self.getFinalCorrectAttr(currAttrVal, totalCorrectCoeffi))
				changedAttrVal = finalAttrVal - currAttrVal
				func = getattr(receiver, CORRECT_ATTR[attrID][1])
				func(changedAttrVal) if not CORRECT_ATTR[attrID][2] else func(changedAttrVal, CORRECT_ATTR[attrID][2])
			elif attrID in CORRECT_SPECIAL_ATTR:
				if attrID == ItemTypeEnum.BANGGONGCORRECTION:
					currAttrVal = receiver.tongContribution
					finalAttrVal = round(self.getFinalCorrectAttr(currAttrVal, totalCorrectCoeffi))
					changedAttrVal = finalAttrVal - currAttrVal
					if receiver.tongMB:
						receiver.tongMB.GM_CommandSetAttr(receiver.playerDBID, "contribution", changedAttrVal)
				elif attrID == ItemTypeEnum.MORALECORRECTION:
					currAttrVal = receiver.dayCampMorale
					finalAttrVal = round(self.getFinalCorrectAttr(currAttrVal, totalCorrectCoeffi))
					changedAttrVal = finalAttrVal - currAttrVal
					KBEngine.globalData["CampMgr"].addMorale(receiver.getCamp(), changedAttrVal)
				elif attrID == ItemTypeEnum.XIANSHICORRECTION:
					currAttrVal = receiver.xianshiForCell
					finalAttrVal = round(self.getFinalCorrectAttr(currAttrVal, totalCorrectCoeffi))
					receiver.base.setXianShi(finalAttrVal, csdefine.CHANGE_XIANSHI_ATTR_CORRECT)
				elif attrID == ItemTypeEnum.LINGSHICORRECTION:
					currAttrVal = receiver.lingshiForCell
					finalAttrVal = round(self.getFinalCorrectAttr(currAttrVal, totalCorrectCoeffi))
					receiver.base.addLingShi(finalAttrVal-currAttrVal, csdefine.CHANGE_LINGSHI_ATTR_CORRECT, 0)
				elif attrID == ItemTypeEnum.XUANSHICORRECTION:
					currAttrVal = receiver.xuanshiForCell
					finalAttrVal = round(self.getFinalCorrectAttr(currAttrVal, totalCorrectCoeffi))
					receiver.base.addXuanShi(finalAttrVal-currAttrVal, csdefine.CHANGE_XUANSHI_ATTR_CORRECT, 0)

	def calcAttrCorrectCoeffi(self, baseVal, extraVal, percentVal, value):
		return (baseVal + extraVal) * (1 + percentVal/ItemTypeEnum.PRECENTRATIO) + value
		
	def overlayCorrectCoeffi(self, receiver, attrCorrectCoeffi):
		for otherCorrectCoeffi in receiver.roleAttrCorrectCoeffis:
			attrCorrectCoeffi *= otherCorrectCoeffi

		return attrCorrectCoeffi

	def getFinalCorrectAttr(self, attr, correctCoeffi):
		return attr * correctCoeffi / 10000

	def onEnd(self, effectData, receiver):
		"""
		效果结束
		"""
		HoldEffect.onEnd(self, effectData, receiver)

