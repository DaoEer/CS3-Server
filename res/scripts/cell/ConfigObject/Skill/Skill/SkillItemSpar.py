# -*- coding: utf-8 -*-

import time
import csdefine
import csstatus
import ItemTypeEnum
import KBEDebug

from ConfigObject.Skill.Skill.SkillItemBase import SkillItemBase



class SkillItemSpar( SkillItemBase ):
	"""
	晶石炼化
	"""
	def __init__( self ):
		SkillItemBase.__init__( self )
		self._isImmortal = False					# 是否仙化
		self._preActionID = ""						# 开始衔接动作
		self._cycleActionID = ""					# 循环动作
		self._postActionID = ""						# 结束衔接动作
		self._intonateName = ""						# 吟唱名字
		self._iconName     = ""						# 图标
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		SkillItemBase.init( self, dictDat )
		self._isInstantSkill = False
		self._isImmortal = dictDat["Param1"]
		self._preActionID = dictDat["Param2"]
		self._cycleActionID = dictDat["Param3"]
		self._postActionID = dictDat["Param4"]
		self._intonateName = dictDat["IntonateName"]
		iconName = dictDat["SkillIcon"].strip().split(".")
		if len(iconName)>1:
			self._iconName = iconName[len(iconName)-1]    #"SkillIcon": "/Game/Textures/Icons/T_Icon_2258_D.T_Icon_2258_D", 只需要T_Icon_2258_D这部分 暂时用技能图标
	

	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		#是否有禁止施法标记
		if caster.actionForbidSign( csdefine.ACTION_FORBID_SPELL ):
			return csstatus.SKILL_STATE_CANT_CAST
		
		if not caster.isState( csdefine.ENTITY_STATE_FREE ):
			return csstatus.SKILL_STATE_CANT_CAST
			
		if caster.isChangeModel():
			return csstatus.SKILL_STATE_CANT_CAST
			
		return SkillItemBase.useableCheck( self, caster, target )
		
	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		SkillItemBase.onSkillBegin( self, caster, target )
		
		preActionID = ""
		if caster.queryTemp("isFirstTimeShowSpar", True):
			caster.setTemp("isFirstTimeShowSpar", False )
			preActionID = self._preActionID
		
		caster.allClients.PlayArtificeSpar( preActionID, self._cycleActionID )
		caster.client.intonateSparSpell( self.getSkillTotalTime(), self.getID() )
		if self._isImmortal:
			#
			if time.time() - caster.sparCDTime >= 30:
				caster.sparCDTime = time.time()
				caster.showMessagePlaySound( self._isImmortal )
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		usingItemUid = caster.getUsingItem()
		if not usingItemUid:
			KBEDebug.ERROR_MSG("use skill(%d) cannot find using item UID!!"%self._id)
			SkillItemBase.onSkillEnd( self, caster, target, castResult )
			return
		item = caster.getItemInstByUid( usingItemUid )
		SkillItemBase.onSkillEnd( self, caster, target, castResult )
		
		caster.client.intonateSparSpellOver()
		if castResult:									# 如果炼化成功
			xiuweiValue = item.getXiuweiValue( self._isImmortal )
			caster.addXiuwei( xiuweiValue, csdefine.XIUWEI_ADD_REASON_USE_SPAR_ITEM )
			
			# 自动使用炼化物品
			sparItems = caster.getItemListByKBType( ItemTypeEnum.BAG_SPAR )
			for item in sparItems:
				if item.__class__.__name__ == "ItemSpar":
					if item.checkUse( caster ) == csstatus.ITEM_USE_GO_ON_MSG:
						item.use( caster, caster )
						return
					else:
						break
			# 没有炼化物品
			caster.removeTemp("isFirstTimeShowSpar" )
			caster.allClients.StopArtificeSpar(self._postActionID)
		else:											# 中断炼化
			newItemID = item.getAddItemID( self._isImmortal )
			if newItemID:
				caster.removeItemByAmount(item, 1, csdefine.ITEM_REMOVE_BY_USE)
				caster.addItemByID( newItemID )
			caster.removeTemp("isFirstTimeShowSpar" )
			caster.allClients.StopArtificeSpar(self._postActionID)