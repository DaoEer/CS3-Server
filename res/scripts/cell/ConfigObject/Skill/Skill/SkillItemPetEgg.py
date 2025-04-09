# -*- coding: utf-8 -*-


import csdefine
import csstatus
import random
import KBEDebug

from ConfigObject.Skill.Skill.SkillItemBase import SkillItemBase



class SkillItemPetEgg( SkillItemBase ):
	"""
	幻兽蛋
	"""
	def __init__( self ):
		SkillItemBase.__init__( self )
		self._isShowIntonateUI = False							# 顯示吟唱條界面
		self._intonateName = ""									# 吟唱名字
		self._scriptID = 0										# 幻兽ScriptID
		self._eggQuality = 1									# 幻兽蛋品质
		self._abilityRoll = []									# 品质随机
		self._iconName = ""										# 图标
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		SkillItemBase.init( self, dictDat )
		self._isInstantSkill = False
		self._isShowIntonateUI = dictDat["ShowIntonate"]
		self._intonateName = dictDat["IntonateName"]
		iconName = dictDat["SkillIcon"].strip().split(".")
		if len(iconName)>1:
			self._iconName = iconName[len(iconName)-1]    #"SkillIcon": "/Game/Textures/Icons/T_Icon_2258_D.T_Icon_2258_D", 只需要T_Icon_2258_D这部分 暂时用技能图标

	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		if caster.petCageIsFull():
			return csstatus.PET_CANNOT_GET_MORE
		return SkillItemBase.useableCheck( self, caster, target )
		
	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		itemUid = caster.getUsingItem()
		itemInst = caster.getItemInstByUid( itemUid )

		if itemInst:										#见CST-8757，将该功能配置从技能转移到道具
			if itemInst.getItemDir("Param1") != "":
				self._scriptID = itemInst.getItemDir("Param1")
			if itemInst.getItemDir("Quality"):
				self._eggQuality = itemInst.getItemDir("Quality")
			if itemInst.getItemDir("Param2") != "":
				self._abilityRoll = [float(i) for i in itemInst.getItemDir("Param2").split("|")]
		else:
			KBEDebug.ERROR_MSG("This skill(%s) must be use item to release!" % self.getID())
			return

		if caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self._isShowIntonateUI:
			caster.intonateSpell( self.getSkillTotalTime(), self.getID() )
		
		SkillItemBase.onSkillBegin( self, caster, target )
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		if castResult:
			if self._scriptID != 0:
				roll = random.random()
				newOdds = 0.0
				for index, odds in enumerate( self._abilityRoll ):
					newOdds += odds
					if roll <= newOdds:
						quality = index + 1
						break
				
				caster.generatePet( self._scriptID, quality, self._eggQuality)
			else:
				caster.generateSealPet()
			
		if caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self._isShowIntonateUI:
			caster.intonateSpellOver()
		SkillItemBase.onSkillEnd( self, caster, target, castResult )