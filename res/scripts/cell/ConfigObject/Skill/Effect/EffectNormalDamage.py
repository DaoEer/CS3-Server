# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""
#python
import KBEDebug
import random
import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
from ItemSystemExp import g_CombatNormalDamager
import ItemTypeEnum
import Settings


class EffectNormalDamage( EffectSkillBase ):
	"""
	标准伤害效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._damageType = csdefine.DAMAGE_TYPE_PHYSICS
		self._skillRadio = 0.0					# 技能效率
		self._skillValue = 0					# 技能固定值
		self._isIceDamage = False				# 是否计算冰元素伤害
		self._isFireDamage = False				# 是否计算火元素伤害
		self._isThunderDamage = False			# 是否计算雷元素伤害
		self._isXuanDamage = False				# 是否计算玄元素伤害
		self._iceDamageRadio = 0.0				# 冰元素伤害百分比
		self._iceDamageValue = 0				# 冰元素伤害固定值
		self._fireDamageRadio = 0.0				# 火元素伤害百分比
		self._fireDamageValue = 0				# 火元素伤害固定值
		self._thunderDamageRadio = 0.0			# 雷元素伤害百分比
		self._thunderDamageValue = 0			# 雷元素伤害固定值
		self._xuanDamageRadio = 0.0				# 玄元素伤害百分比
		self._xuanDamageValue = 0				# 玄元素伤害固定值
		self._deadEffect = 0					# 死亡时，是否播放特殊效果（暴尸）
		self._customAttrC = {}					# 施法者属性修正列表
		self._customAttrR = {}					# 受术者属性修正列表
		self._isSkipEvent = False
		self._passiveIDOnKill = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		
		if dictDat["Param1"]:
			self._damageType = 2**int( dictDat["Param1"] )
		
		# 生命伤害百分比（如“0.5”代表“50%物理攻击”）|生命伤害固定值（整型）	
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			self._skillRadio = float( Param2[0] )
			if len(Param2) > 1:
				self._skillValue = int( Param2[1] )

		# 冰元素伤害百分比 : 冰元素伤害固定值|火百分比:固定值|雷百分比:固定值|玄百分比:固定值
		# 支持部分缺省，如"|0:100||"，代表"火元素伤害固定100点"
		if dictDat["Param3"]:
			Param3 = dictDat["Param3"].split("|")
			if len(Param3) > 0 and Param3[0]:
				i = Param3[0].split(":")
				self._iceDamageRadio = float( i[0] )
				self._iceDamageValue = int( i[1] )
				self._isIceDamage = True
			if len(Param3) > 1 and Param3[1]:
				i = Param3[1].split(":")
				self._fireDamageRadio = float( i[0] )
				self._fireDamageValue = int( i[1] )
				self._isFireDamage = True
			if len(Param3) > 2 and Param3[2]:
				i = Param3[2].split(":")
				self._thunderDamageRadio = float( i[0] )
				self._thunderDamageValue = int( i[1] )
				self._isThunderDamage = True
			if len(Param3) > 3 and Param3[3]:
				i = Param3[3].split(":")
				self._xuanDamageRadio = float( i[0] )
				self._xuanDamageValue = int( i[1] )
				self._isXuanDamage = True

		# 标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
		if dictDat and dictDat["Param4"]:
			Param4 = dictDat["Param4"].split("|")
			for i in Param4:
				List = i.split(":")
				if List[0] == "IsReAttrC":		# “IsReAttrC:30008:50”代表“施法者物攻校正＋50”
					propertyStr = ItemTypeEnum.PROPERTYIDTOSTR[int(List[1])]
					self._customAttrC[propertyStr]  = int(List[2])
				elif List[0] == "IsReAttrR":	# “IsReAttrR:30010:-50”代表“受术者物防校正－50”
					propertyStr = ItemTypeEnum.PROPERTYIDTOSTR[int(List[1])]
					self._customAttrR[propertyStr] = int(List[2])
				elif List[0] == "IsDoDeadEffect":	# “IsDoDeadEffect”代表“需要播放击杀表现”
					self._deadEffect = 1
				elif List[0] == "IsSkipEvent":	# “IsSkipEvent”代表“需要跳过事件触发”
					self._isSkipEvent = True
				elif List[0] == "IsDoPrivateOnKill":	# “IsDoPrivateOnKill:99900102”代表“此效果击杀时，额外触发被动技能99900102”
					self._passiveIDOnKill = int(List[1])
				else:
					KBEDebug.ERROR_MSG("EffectNormalDamage: %s is not a correct tag name "%List[0])

	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getState() == csdefine.ENTITY_STATE_DEAD:
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		# ---------------再HP伤害---------------
		casterBaseCom = g_CombatNormalDamager.getBaseCombatData( caster.getLevel(), caster.getProfession() )
		receiverBaseCom = g_CombatNormalDamager.getBaseCombatData( receiver.getLevel(), receiver.getProfession() )
		
		# 伤害量 = 伤害了初值 * （ 技能效果 + 伤害波动 ） + 伤害固定值
		if self._damageType == csdefine.DAMAGE_TYPE_MAGIC:
			damage = self.CustomAttrC("magic_damage", caster.magic_damage) - self.CustomAttrR("magic_damage_ignore", receiver.magic_damage_ignore)
		else:
			damage = self.CustomAttrC("damage", caster.damage) - self.CustomAttrR("damage_ignore", receiver.damage_ignore)
		damage = max(0, damage)	
		recDamage = math.ceil((damage * self._skillRadio + self._skillValue) * (1.0 + casterBaseCom["DamRandom"] * random.uniform(-1,1)))
		recDamage = max(0, recDamage)

		# 计算修正伤害, 伤害值*(各种造成伤害修正相乘)
		damage_correction = 1
		damage_correction *=  self.CustomAttrC("damage_correction", caster.damage_correction)/ItemTypeEnum.PRECENTRATIO
		if self._damageType == csdefine.DAMAGE_TYPE_PHYSICS:
			damage_correction *=  self.CustomAttrC("attack_damage_correction", caster.attack_damage_correction)/ItemTypeEnum.PRECENTRATIO
		elif self._damageType == csdefine.DAMAGE_TYPE_MAGIC:
			damage_correction *=  self.CustomAttrC("magic_damage_correction", caster.magic_damage_correction)/ItemTypeEnum.PRECENTRATIO
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			damage_correction *= self.CustomAttrC("role_damage_correction", caster.role_damage_correction)/ItemTypeEnum.PRECENTRATIO
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			damage_correction *=  self.CustomAttrC("pet_damage_correction", caster.pet_damage_correction)/ItemTypeEnum.PRECENTRATIO
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			damage_correction *= self.CustomAttrC("monster_damage_correction", caster.monster_damage_correction)/ItemTypeEnum.PRECENTRATIO
		recDamage *= damage_correction

		# 暴击率 = 暴击点 / 基准暴击点
		# 暴击伤害 = 伤害量 * 基准暴击倍率
		isCritical = False
		critRatio = 1
		critRatio = caster.critRatio / ItemTypeEnum.PRECENTRATIO
		criticalstrike = self.CustomAttrC("criticalstrike", caster.criticalstrike) - self.CustomAttrR("criticalstrike_ignore", receiver.criticalstrike_ignore)
		criticalstrike = max(0, criticalstrike)
		critical = criticalstrike / casterBaseCom["BCritPoint"]
		if critical >= random.random():
			isCritical = True
			#recDamage = math.ceil( recDamage * casterBaseCom["BCritRatio"] )
			recDamage = math.ceil( recDamage * critRatio )
		
		# 招架率 = 招架点 / （ 招架点 * （1-基准招架倍率）+ [受术者]基准招架点 ）
		isParry = False
		parryRatio = 1
		parryRatio = receiver.parryRatio / ItemTypeEnum.PRECENTRATIO
		parry = self.CustomAttrR("parry", receiver.parry) - self.CustomAttrC("parry_ignore", caster.parry_ignore)
		parry = max(0, parry)
		parry /= parry * (1-receiverBaseCom["BParryRatio"]) + receiverBaseCom["BParryPoint"]
		#parry = self.CustomAttrR("parry", receiver.parry) / ( self.CustomAttrR("parry", receiver.parry) * (1-parryRatio) + receiverBaseCom["BParryPoint"])
		if parry >= random.random():
			isParry = True
			#recDamage = math.ceil( recDamage * receiverBaseCom["BParryRatio"] )
			recDamage = math.ceil( recDamage * parryRatio )

		# 护甲伤害减免率 = 防御 / （防御+[受术者]基准防御点）
		# 伤害量 *= （1-护甲伤害减免率）
		if self._damageType == csdefine.DAMAGE_TYPE_MAGIC:
			armor = self.CustomAttrR("magic_armor", receiver.magic_armor) - self.CustomAttrC("magic_armor_ignore", caster.magic_armor_ignore)
		else:
			armor = self.CustomAttrR("armor", receiver.armor) - self.CustomAttrC("armor_ignore", caster.armor_ignore)
		armor = max(0, armor)
		recDamage = math.ceil(recDamage * ( 1 - armor / (armor + receiverBaseCom["BArmorPoint"])))
		# 计算普通伤害的护盾buff抵扣
		recDamage = self.getFinalDamageByBuffShield( receiver, caster, self._damageType, recDamage)
		takeDamage = recDamage  #携带伤害量

		# 计算修正伤害, 伤害值/(各种承受伤害修正相乘)
		armor_correction = 1
		armor_correction *= self.CustomAttrR("armor_correction", receiver.armor_correction)/ItemTypeEnum.PRECENTRATIO
		if self._damageType == csdefine.DAMAGE_TYPE_PHYSICS:
			armor_correction *= self.CustomAttrR("attack_armor_correction", receiver.attack_armor_correction)/ItemTypeEnum.PRECENTRATIO
		elif self._damageType == csdefine.DAMAGE_TYPE_MAGIC:
			armor_correction *= self.CustomAttrR("magic_armor_correction", receiver.magic_armor_correction)/ItemTypeEnum.PRECENTRATIO
		if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			armor_correction *= self.CustomAttrR("role_armor_correction", receiver.role_armor_correction)/ItemTypeEnum.PRECENTRATIO
		if caster.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			armor_correction *=  self.CustomAttrR("pet_armor_correction", receiver.pet_armor_correction)/ItemTypeEnum.PRECENTRATIO
		if caster.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			armor_correction *=  self.CustomAttrR("monster_armor_correction", receiver.monster_armor_correction)/ItemTypeEnum.PRECENTRATIO
		if armor_correction != 0:
			recDamage /= armor_correction

		# 计算元素伤害
		iceDamage = 0
		fireDamage = 0
		thunderDamage = 0
		xuanDamage = 0
		if self._isIceDamage:
			# 计算元素伤害初值
			ice_damage = self.CustomAttrC("ice_damage", caster.ice_damage) - self.CustomAttrR("ice_damage_ignore", receiver.ice_damage_ignore)
			ice_damage = max(0, ice_damage)
			iceDamage = math.ceil(ice_damage * self._iceDamageRadio + self._iceDamageValue)
			iceDamage = max(0, iceDamage)
			# 计算元素修正伤害, 元素伤害＝（元素伤害初值－受术者元素防御）×造成元素伤害修正终值
			ice_damage_correction = self.CustomAttrC("ice_damage_correction", caster.ice_damage_correction)/ItemTypeEnum.PRECENTRATIO
			ice_armor = self.CustomAttrR("ice_armor", receiver.ice_armor) - self.CustomAttrC("ice_armor_ignore", caster.ice_armor_ignore)
			ice_armor = max(0, ice_armor)
			iceDamage = math.ceil((iceDamage - ice_armor)) * ice_damage_correction
			iceDamage = max(0, iceDamage)
			# 计算元素修正伤害, 元素伤害÷＝承受元素伤害修正终值
			ice_armor_correction = self.CustomAttrR("ice_armor_correction", receiver.ice_armor_correction)
			if ice_armor_correction != 0:
				iceDamage /= (ice_armor_correction/ItemTypeEnum.PRECENTRATIO)
			# 计算元素伤害的护盾buff抵扣
			if iceDamage > 0:
				iceDamage = self.getFinalDamageByBuffShield( receiver, caster, csdefine.DAMAGE_TYPE_ICE, iceDamage)
		if self._isFireDamage:
			# 计算元素伤害初值
			fire_damage = self.CustomAttrC("fire_damage", caster.fire_damage) - self.CustomAttrR("fire_damage_ignore", receiver.fire_damage_ignore)
			fire_damage = max(0, fire_damage)
			fireDamage = math.ceil(fire_damage * self._fireDamageRadio + self._fireDamageValue)
			fireDamage = max(0, fireDamage)
			# 计算元素修正伤害, 元素伤害＝（元素伤害初值－受术者元素防御）×造成元素伤害修正终值
			fire_damage_correction = self.CustomAttrC("fire_damage_correction", caster.fire_damage_correction)/ItemTypeEnum.PRECENTRATIO
			fire_armor = self.CustomAttrR("fire_armor", receiver.fire_armor) - self.CustomAttrC("fire_armor_ignore", caster.fire_armor_ignore)
			fire_armor = max(0, fire_armor)
			fireDamage = math.ceil((fireDamage - fire_armor)) * fire_damage_correction
			fireDamage = max(0, fireDamage)
			# 计算元素修正伤害, 元素伤害÷＝承受元素伤害修正终值
			fire_armor_correction = self.CustomAttrR("fire_armor_correction", receiver.fire_armor_correction)
			if fire_armor_correction != 0:
				fireDamage /= (fire_armor_correction/ItemTypeEnum.PRECENTRATIO)
			# 计算元素伤害的护盾buff抵扣
			if fireDamage > 0:
				fireDamage = self.getFinalDamageByBuffShield( receiver, caster, csdefine.DAMAGE_TYPE_FIRE, fireDamage)
		if self._isThunderDamage:
			# 计算元素伤害初值
			thunder_damage = self.CustomAttrC("thunder_damage", caster.thunder_damage) - self.CustomAttrR("thunder_damage_ignore", receiver.thunder_damage_ignore)
			thunder_damage = max(0, thunder_damage)
			thunderDamage = math.ceil(thunder_damage * self._thunderDamageRadio + self._thunderDamageValue)
			thunderDamage = max(0, thunderDamage)
			# 计算元素修正伤害, 元素伤害＝（元素伤害初值－受术者元素防御）×造成元素伤害修正终值
			thunder_damage_correction = self.CustomAttrC("thunder_damage_correction", caster.thunder_damage_correction)/ItemTypeEnum.PRECENTRATIO
			thunder_armor = self.CustomAttrR("thunder_armor", receiver.thunder_armor) - self.CustomAttrC("thunder_armor_ignore", caster.thunder_armor_ignore)
			thunder_armor = max(0, thunder_armor)
			thunderDamage = math.ceil((thunderDamage - thunder_armor)) * thunder_damage_correction
			thunderDamage = max(0, thunderDamage)
			# 计算元素修正伤害, 元素伤害÷＝承受元素伤害修正终值
			thunder_armor_correction = self.CustomAttrR("thunder_armor_correction", receiver.thunder_armor_correction)
			if thunder_armor_correction != 0:
				thunderDamage /= (thunder_armor_correction/ItemTypeEnum.PRECENTRATIO)
			# 计算元素伤害的护盾buff抵扣
			if thunderDamage > 0:
				thunderDamage = self.getFinalDamageByBuffShield( receiver, caster, csdefine.DAMAGE_TYPE_THUNDER, thunderDamage)
		if self._isXuanDamage:
			# 计算元素伤害初值	
			xuan_damage = self.CustomAttrC("xuan_damage", caster.xuan_damage) - self.CustomAttrR("xuan_damage_ignore", receiver.xuan_damage_ignore)
			xuan_damage = max(0, xuan_damage)
			xuanDamage = math.ceil(xuan_damage * self._xuanDamageRadio + self._xuanDamageValue)		
			xuanDamage = max(0, xuanDamage)
			# 计算元素修正伤害, 元素伤害＝（元素伤害初值－受术者元素防御）×造成元素伤害修正终值
			xuan_damage_correction = self.CustomAttrC("xuan_damage_correction", caster.xuan_damage_correction)/ItemTypeEnum.PRECENTRATIO	
			xuan_armor = self.CustomAttrR("xuan_armor", receiver.xuan_armor) - self.CustomAttrC("xuan_armor_ignore", caster.xuan_armor_ignore)
			xuan_armor = max(0, xuan_armor)
			xuanDamage = math.ceil((xuanDamage - xuan_armor)) * xuan_damage_correction
			xuanDamage = max(0, xuanDamage)
			# 计算元素修正伤害, 元素伤害÷＝承受元素伤害修正终值		
			xuan_armor_correction = self.CustomAttrR("xuan_armor_correction", receiver.xuan_armor_correction)
			if xuan_armor_correction != 0:
				xuanDamage /= (xuan_armor_correction/ItemTypeEnum.PRECENTRATIO)
			# 计算元素伤害的护盾buff抵扣	
			if xuanDamage > 0:
				xuanDamage = self.getFinalDamageByBuffShield( receiver, caster, csdefine.DAMAGE_TYPE_XUAN, xuanDamage)

		# 总伤害计算
		allDamage = recDamage + iceDamage + fireDamage + thunderDamage + xuanDamage

		skillID = 0
		if skill:
			skillID = skill.getID()
			
		receiver.receiveDamage( caster.id, skillID, self._damageType, int(allDamage), isCritical, isParry, self._deadEffect, self._actForbid )
		if skill and (skill.getScriptType() == csdefine.SCRIPT_TYPE_BUFF or not skill.isPassiveSkill()): #buff的打击也需要触发
			if not self._isSkipEvent:
				caster.triggerSkillEvent( csdefine.SKILL_EVENT_HURT, receiver.id, { "actForbid": self._actForbid, "type":csdefine.SKILL_EVENT_CASTER_HURT, "takeDamage": takeDamage, "IsCritical":isCritical, "IsParry":isParry } )
				receiver.triggerSkillEvent( csdefine.SKILL_EVENT_HURT, caster.id, { "actForbid": self._actForbid, "type":csdefine.SKILL_EVENT_RECEIVER_HURT, "takeDamage":takeDamage, "IsCritical":isCritical, "IsParry":isParry } )
				if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_ENEMY:
					caster.onStartDoubleHit()
				if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_ENEMY:
					receiver.onStartBeDoubleHit()

		if self._passiveIDOnKill and receiver.isWillDead(int(allDamage)):
			requestSkill = receiver.getSkill(self._passiveIDOnKill)		
			requestSkill.requestPassiveSkill(caster, receiver.id, {"takeDamage": takeDamage})			

	def getFinalDamageByBuffShield( self, receiver, caster, damageType, damageValue ):
		"""
		伤害计算时，考虑护盾Buff的抵扣
		"""
		buffIndexList = receiver.findBuffsByBuffScript("BuffShield") #护盾Buff
		countBuff = len( buffIndexList )
		if countBuff == 0:
			return damageValue
		tempDamage = damageValue
		buffs = receiver.getAttrBuffs()
		buffIndexList.sort()
		index = 0
		while countBuff:
			buffData = buffs[buffIndexList[index]] #获得Buff
			buff = receiver.getBuff(buffData.buffID)
			if damageType in buffData.getTempData("DamgeType"):
				reduceDamage = math.ceil(tempDamage * buffData.getTempData("ReduceDamageRatio") + buffData.getTempData("reduceDamageValue")) #伤害抵扣
				if reduceDamage <= 0:
					reduceDamage = 0
				if reduceDamage > tempDamage:
					reduceDamage = tempDamage
				shieldValue = buffData.getTempData("ShieldValue")	#护盾值
				shieldCount = buffData.getTempData("ShieldCount")	#护盾抵挡次数
				if shieldValue < 0:	#护盾值小于0
					if shieldCount != 0: #护盾抵挡次数
						tempDamage = tempDamage - reduceDamage
						if shieldCount > 0:
							buffData.setTempData("ShieldCount",(shieldCount - 1))
				elif shieldValue > reduceDamage and shieldCount != 0:
					tempDamage = tempDamage - reduceDamage
					buffData.setTempData("ShieldValue",(shieldValue - reduceDamage))
					if shieldCount > 0:
						buffData.setTempData("ShieldCount",(shieldCount - 1))
				else:
					tempDamage = tempDamage - shieldValue
					buffData.setTempData("ShieldValue",0)
					buffData.setTempData("ShieldCount",0)
				if buffData.getTempData("ShieldValue") == 0 or buffData.getTempData("ShieldCount") == 0:
					receiver.triggerSkillEvent( csdefine.SKILL_EVENT_SHIELD_BROKEN, caster.id, {"buffIndex":buffIndexList[index]} )
				buff.updataExtraTips( receiver, buffData.index, [buffData.getTempData("ShieldValue"),buffData.getTempData("ShieldCount")] )
			index +=1
			countBuff -= 1
			if tempDamage <= 0:
				return 0
		return tempDamage

	def CustomAttrC(self, propertyStr, propertyValue):
		if propertyStr in self._customAttrC:
			propertyValue += self._customAttrC[propertyStr]
		if propertyStr in ["damage", "magic_damage"]:
			propertyValue = max(propertyValue, 1)
		else:
			propertyValue = max(propertyValue, 0)
		return propertyValue

	def CustomAttrR(self, propertyStr, propertyValue):
		if propertyStr in self._customAttrR:
			propertyValue += self._customAttrR[propertyStr]
		if propertyStr in ["damage", "magic_damage"]:
			propertyValue = max(propertyValue, 1)
		else:
			propertyValue = max(propertyValue, 0)	
		return propertyValue