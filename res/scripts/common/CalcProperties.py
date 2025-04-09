# -*- coding: utf-8 -*-

import ItemSystemExp
import ItemTypeEnum



def calcProperty( baseVal, extraVal, percentVal, value ):
	return ( baseVal + extraVal ) * ( 1 + percentVal/ItemTypeEnum.PRECENTRATIO ) + value

class CalcProperties:
	def __init__( self ):
		pass


	def setRoleBaseProperties(self):
		self.corporeity_base = int(self.getBaseProperties().get(30001, 0))
		self.strength_base = int(self.getBaseProperties().get(30002, 0))
		self.intellect_base = int(self.getBaseProperties().get(30003, 0))
		self.discern_base = int(self.getBaseProperties().get(30004, 0))
		self.dexterity_base = int(self.getBaseProperties().get(30005, 0))
		self.HP_Max_base = int(self.getBaseProperties().get(30006, 0))
		self.MP_Max_base = int(self.getBaseProperties().get(30007, 0))
		self.damage_base = int(self.getBaseProperties().get(30008, 0))
		self.magic_damage_base = int(self.getBaseProperties().get(30009, 0))
		self.armor_base = int(self.getBaseProperties().get(30010, 0))
		self.magic_armor_base = int(self.getBaseProperties().get(30011, 0))
		self.criticalstrike_base = int(self.getBaseProperties().get(30012, 0))
		self.parry_base = int(self.getBaseProperties().get(30013, 0))
		self.speed_base = int(self.getBaseProperties().get(30014, 0))
		self.hitrate_base = int(self.getBaseProperties().get(30015, 0))
		self.dodgerate_base = int(self.getBaseProperties().get(30016, 0))
		self.healingrate_base = int(self.getBaseProperties().get(30017, 0))
		self.gangQiValue_Max_base = int(self.getBaseProperties().get(30018, 0))
		self.gangQi_damagePoint_base = int(self.getBaseProperties().get(30019, 0))
		self.gangQi_armorPoint_base = int(self.getBaseProperties().get(30020, 0))
		self.gangQi_qiJieRevive_base = int(self.getBaseProperties().get(30021, 0))
		self.gangQi_qiYingRevive_base = int(self.getBaseProperties().get(30022, 0))
		self.tempSpeed_base = int(self.getBaseProperties().get(30023, 0))
		self.cure_base = int(self.getBaseProperties().get(30024, 0))
		self.critRatio_base = int(self.getBaseProperties().get(30025, 0))
		self.parryRatio_base = int(self.getBaseProperties().get(30026, 0))
		self.damage_correction_base = int(self.getBaseProperties().get(40001, 0))
		self.armor_correction_base = int(self.getBaseProperties().get(40002, 0))
		self.attack_damage_correction_base = int(self.getBaseProperties().get(40003, 0))
		self.magic_damage_correction_base = int(self.getBaseProperties().get(40004, 0))
		self.attack_armor_correction_base = int(self.getBaseProperties().get(40005, 0))
		self.magic_armor_correction_base = int(self.getBaseProperties().get(40006, 0))
		self.role_damage_correction_base = int(self.getBaseProperties().get(40007, 0))
		self.pet_damage_correction_base = int(self.getBaseProperties().get(40008, 0))
		self.monster_damage_correction_base = int(self.getBaseProperties().get(40009, 0))
		self.role_armor_correction_base = int(self.getBaseProperties().get(40010, 0))
		self.pet_armor_correction_base = int(self.getBaseProperties().get(40011, 0))
		self.monster_armor_correction_base = int(self.getBaseProperties().get(40012, 0))
		self.curecorrection_base = int(self.getBaseProperties().get(40013, 0))
		self.becuredcorrection_base = int(self.getBaseProperties().get(40014, 0))
		self.ice_damage_base = int(self.getBaseProperties().get(30027, 0))
		self.fire_damage_base = int(self.getBaseProperties().get(30028, 0))
		self.thunder_damage_base = int(self.getBaseProperties().get(30029, 0))
		self.xuan_damage_base = int(self.getBaseProperties().get(30030, 0))
		self.ice_armor_base = int(self.getBaseProperties().get(30031, 0))
		self.fire_armor_base = int(self.getBaseProperties().get(30032, 0))
		self.thunder_armor_base = int(self.getBaseProperties().get(30033, 0))
		self.xuan_armor_base = int(self.getBaseProperties().get(30034, 0))
		self.ice_damage_correction_base = int(self.getBaseProperties().get(40015, 0))
		self.fire_damage_correction_base = int(self.getBaseProperties().get(40016, 0))
		self.thunder_damage_correction_base = int(self.getBaseProperties().get(40017, 0))
		self.xuan_damage_correction_base = int(self.getBaseProperties().get(40018, 0))
		self.ice_armor_correction_base = int(self.getBaseProperties().get(40019, 0))
		self.fire_armor_correction_base = int(self.getBaseProperties().get(40020, 0))
		self.thunder_armor_correction_base = int(self.getBaseProperties().get(40021, 0))
		self.xuan_armor_correction_base = int(self.getBaseProperties().get(40022, 0))
		self.hatred_correction_base = int(self.getBaseProperties().get(40023, 0))
		self.related_hatred_correction_base = int(self.getBaseProperties().get(40024, 0))
		self.damage_ignore_base = int(self.getBaseProperties().get(30035, 0))
		self.magic_damage_ignore_base = int(self.getBaseProperties().get(30036, 0))
		self.armor_ignore_base = int(self.getBaseProperties().get(30037, 0))
		self.magic_armor_ignore_base = int(self.getBaseProperties().get(30038, 0))
		self.criticalstrike_ignore_base = int(self.getBaseProperties().get(30039, 0))
		self.parry_ignore_base = int(self.getBaseProperties().get(30040, 0))
		self.hitrate_ignore_base = int(self.getBaseProperties().get(30041, 0))
		self.dodgerate_ignore_base = int(self.getBaseProperties().get(30042, 0))
		self.ice_damage_ignore_base = int(self.getBaseProperties().get(30043, 0))
		self.fire_damage_ignore_base = int(self.getBaseProperties().get(30044, 0))
		self.thunder_damage_ignore_base = int(self.getBaseProperties().get(30045, 0))
		self.xuan_damage_ignore_base = int(self.getBaseProperties().get(30046, 0))
		self.ice_armor_ignore_base = int(self.getBaseProperties().get(30047, 0))
		self.fire_armor_ignore_base = int(self.getBaseProperties().get(30048, 0))
		self.thunder_armor_ignore_base = int(self.getBaseProperties().get(30049, 0))
		self.xuan_armor_ignore_base = int(self.getBaseProperties().get(30050, 0))
		self.depress_resist_base = int(self.getBaseProperties().get(30051, 0))
		self.hitback_resist_base = int(self.getBaseProperties().get(30052, 0))
		self.control_resist_base = int(self.getBaseProperties().get(30053, 0))
		self.insane_resist_base = int(self.getBaseProperties().get(30054, 0))

	def setMonsterBaseProperties(self):
		vv = int(self.getBaseProperties().get(30001, 0))
		self.corporeity_base = self.getBasicValue(30001,vv)

		vv = int(self.getBaseProperties().get(30002, 0))
		self.strength_base = self.getBasicValue(30002,vv)

		vv = int(self.getBaseProperties().get(30003, 0))
		self.intellect_base = self.getBasicValue(30003,vv)

		vv = int(self.getBaseProperties().get(30004, 0))
		self.discern_base = self.getBasicValue(30004,vv)

		vv = int(self.getBaseProperties().get(30005, 0))
		self.dexterity_base = self.getBasicValue(30005,vv)

		vv = int(self.getBaseProperties().get(30006, 0))
		self.HP_Max_base = self.getBasicValue(30006,vv)

		vv = int(self.getBaseProperties().get(30007, 0))
		self.MP_Max_base = self.getBasicValue(30007,vv)

		vv = int(self.getBaseProperties().get(30008, 0))
		self.damage_base = self.getBasicValue(30008,vv)

		vv = int(self.getBaseProperties().get(30009, 0))
		self.magic_damage_base = self.getBasicValue(30009,vv)

		vv = int(self.getBaseProperties().get(30010, 0))
		self.armor_base = self.getBasicValue(30010,vv)

		vv = int(self.getBaseProperties().get(30011, 0))
		self.magic_armor_base = self.getBasicValue(30011,vv)

		vv = int(self.getBaseProperties().get(30012, 0))
		self.criticalstrike_base = self.getBasicValue(30012,vv)

		vv = int(self.getBaseProperties().get(30013, 0))
		self.parry_base = self.getBasicValue(30013,vv)

		vv = int(self.getBaseProperties().get(30014, 0))
		self.speed_base = self.getBasicValue(30014,vv)

		vv = int(self.getBaseProperties().get(30015, 0))
		self.hitrate_base = self.getBasicValue(30015,vv)

		vv = int(self.getBaseProperties().get(30016, 0))
		self.dodgerate_base = self.getBasicValue(30016,vv)

		vv = int(self.getBaseProperties().get(30017, 0))
		self.healingrate_base = self.getBasicValue(30017,vv)

		vv = int(self.getBaseProperties().get(30018, 0))
		self.gangQiValue_Max_base = self.getBasicValue(30018,vv)

		vv = int(self.getBaseProperties().get(30019, 0))
		self.gangQi_damagePoint_base = self.getBasicValue(30019,vv)

		vv = int(self.getBaseProperties().get(30020, 0))
		self.gangQi_armorPoint_base = self.getBasicValue(30020,vv)

		vv = int(self.getBaseProperties().get(30021, 0))
		self.gangQi_qiJieRevive_base = self.getBasicValue(30021,vv)

		vv = int(self.getBaseProperties().get(30022, 0))
		self.gangQi_qiYingRevive_base = self.getBasicValue(30022,vv)

		vv = int(self.getBaseProperties().get(30023, 0))
		self.tempSpeed_base = self.getBasicValue(30023,vv)

		vv = int(self.getBaseProperties().get(30024, 0))
		self.cure_base = self.getBasicValue(30024,vv)

		vv = int(self.getBaseProperties().get(30025, 0))
		self.critRatio_base = self.getBasicValue(30025,vv)

		vv = int(self.getBaseProperties().get(30026, 0))
		self.parryRatio_base = self.getBasicValue(30026,vv)

		vv = int(self.getBaseProperties().get(40001, 0))
		self.damage_correction_base = self.getBasicValue(40001,vv)

		vv = int(self.getBaseProperties().get(40002, 0))
		self.armor_correction_base = self.getBasicValue(40002,vv)

		vv = int(self.getBaseProperties().get(40003, 0))
		self.attack_damage_correction_base = self.getBasicValue(40003,vv)

		vv = int(self.getBaseProperties().get(40004, 0))
		self.magic_damage_correction_base = self.getBasicValue(40004,vv)

		vv = int(self.getBaseProperties().get(40005, 0))
		self.attack_armor_correction_base = self.getBasicValue(40005,vv)

		vv = int(self.getBaseProperties().get(40006, 0))
		self.magic_armor_correction_base = self.getBasicValue(40006,vv)

		vv = int(self.getBaseProperties().get(40007, 0))
		self.role_damage_correction_base = self.getBasicValue(40007,vv)

		vv = int(self.getBaseProperties().get(40008, 0))
		self.pet_damage_correction_base = self.getBasicValue(40008,vv)

		vv = int(self.getBaseProperties().get(40009, 0))
		self.monster_damage_correction_base = self.getBasicValue(40009,vv)

		vv = int(self.getBaseProperties().get(40010, 0))
		self.role_armor_correction_base = self.getBasicValue(40010,vv)

		vv = int(self.getBaseProperties().get(40011, 0))
		self.pet_armor_correction_base = self.getBasicValue(40011,vv)

		vv = int(self.getBaseProperties().get(40012, 0))
		self.monster_armor_correction_base = self.getBasicValue(40012,vv)

		vv = int(self.getBaseProperties().get(40013, 0))
		self.curecorrection_base = self.getBasicValue(40013,vv)

		vv = int(self.getBaseProperties().get(40014, 0))
		self.becuredcorrection_base = self.getBasicValue(40014,vv)

		vv = int(self.getBaseProperties().get(30027, 0))
		self.ice_damage_base = self.getBasicValue(30027,vv)

		vv = int(self.getBaseProperties().get(30028, 0))
		self.fire_damage_base = self.getBasicValue(30028,vv)

		vv = int(self.getBaseProperties().get(30029, 0))
		self.thunder_damage_base = self.getBasicValue(30029,vv)

		vv = int(self.getBaseProperties().get(30030, 0))
		self.xuan_damage_base = self.getBasicValue(30030,vv)

		vv = int(self.getBaseProperties().get(30031, 0))
		self.ice_armor_base = self.getBasicValue(30031,vv)

		vv = int(self.getBaseProperties().get(30032, 0))
		self.fire_armor_base = self.getBasicValue(30032,vv)

		vv = int(self.getBaseProperties().get(30033, 0))
		self.thunder_armor_base = self.getBasicValue(30033,vv)

		vv = int(self.getBaseProperties().get(30034, 0))
		self.xuan_armor_base = self.getBasicValue(30034,vv)

		vv = int(self.getBaseProperties().get(40015, 0))
		self.ice_damage_correction_base = self.getBasicValue(40015,vv)

		vv = int(self.getBaseProperties().get(40016, 0))
		self.fire_damage_correction_base = self.getBasicValue(40016,vv)

		vv = int(self.getBaseProperties().get(40017, 0))
		self.thunder_damage_correction_base = self.getBasicValue(40017,vv)

		vv = int(self.getBaseProperties().get(40018, 0))
		self.xuan_damage_correction_base = self.getBasicValue(40018,vv)

		vv = int(self.getBaseProperties().get(40019, 0))
		self.ice_armor_correction_base = self.getBasicValue(40019,vv)

		vv = int(self.getBaseProperties().get(40020, 0))
		self.fire_armor_correction_base = self.getBasicValue(40020,vv)

		vv = int(self.getBaseProperties().get(40021, 0))
		self.thunder_armor_correction_base = self.getBasicValue(40021,vv)

		vv = int(self.getBaseProperties().get(40022, 0))
		self.xuan_armor_correction_base = self.getBasicValue(40022,vv)

		vv = int(self.getBaseProperties().get(40023, 0))
		self.hatred_correction_base = self.getBasicValue(40023,vv)

		vv = int(self.getBaseProperties().get(40024, 0))
		self.related_hatred_correction_base = self.getBasicValue(40024,vv)

		vv = int(self.getBaseProperties().get(30035, 0))
		self.damage_ignore_base = self.getBasicValue(30035,vv)

		vv = int(self.getBaseProperties().get(30036, 0))
		self.magic_damage_ignore_base = self.getBasicValue(30036,vv)

		vv = int(self.getBaseProperties().get(30037, 0))
		self.armor_ignore_base = self.getBasicValue(30037,vv)

		vv = int(self.getBaseProperties().get(30038, 0))
		self.magic_armor_ignore_base = self.getBasicValue(30038,vv)

		vv = int(self.getBaseProperties().get(30039, 0))
		self.criticalstrike_ignore_base = self.getBasicValue(30039,vv)

		vv = int(self.getBaseProperties().get(30040, 0))
		self.parry_ignore_base = self.getBasicValue(30040,vv)

		vv = int(self.getBaseProperties().get(30041, 0))
		self.hitrate_ignore_base = self.getBasicValue(30041,vv)

		vv = int(self.getBaseProperties().get(30042, 0))
		self.dodgerate_ignore_base = self.getBasicValue(30042,vv)

		vv = int(self.getBaseProperties().get(30043, 0))
		self.ice_damage_ignore_base = self.getBasicValue(30043,vv)

		vv = int(self.getBaseProperties().get(30044, 0))
		self.fire_damage_ignore_base = self.getBasicValue(30044,vv)

		vv = int(self.getBaseProperties().get(30045, 0))
		self.thunder_damage_ignore_base = self.getBasicValue(30045,vv)

		vv = int(self.getBaseProperties().get(30046, 0))
		self.xuan_damage_ignore_base = self.getBasicValue(30046,vv)

		vv = int(self.getBaseProperties().get(30047, 0))
		self.ice_armor_ignore_base = self.getBasicValue(30047,vv)

		vv = int(self.getBaseProperties().get(30048, 0))
		self.fire_armor_ignore_base = self.getBasicValue(30048,vv)

		vv = int(self.getBaseProperties().get(30049, 0))
		self.thunder_armor_ignore_base = self.getBasicValue(30049,vv)

		vv = int(self.getBaseProperties().get(30050, 0))
		self.xuan_armor_ignore_base = self.getBasicValue(30050,vv)

		vv = int(self.getBaseProperties().get(30051, 0))
		self.depress_resist_base = self.getBasicValue(30051,vv)

		vv = int(self.getBaseProperties().get(30052, 0))
		self.hitback_resist_base = self.getBasicValue(30052,vv)

		vv = int(self.getBaseProperties().get(30053, 0))
		self.control_resist_base = self.getBasicValue(30053,vv)

		vv = int(self.getBaseProperties().get(30054, 0))
		self.insane_resist_base = self.getBasicValue(30054,vv)


	def setVehiclePetBaseProperties(self):
		self.corporeity_base = int(self.getBaseProperties().get(30001, 0))
		self.strength_base = int(self.getBaseProperties().get(30002, 0))
		self.intellect_base = int(self.getBaseProperties().get(30003, 0))
		self.discern_base = int(self.getBaseProperties().get(30004, 0))
		self.dexterity_base = int(self.getBaseProperties().get(30005, 0))
		self.HP_Max_base = int(self.getBaseProperties().get(30006, 0))
		self.MP_Max_base = int(self.getBaseProperties().get(30007, 0))
		self.damage_base = int(self.getBaseProperties().get(30008, 0))
		self.magic_damage_base = int(self.getBaseProperties().get(30009, 0))
		self.armor_base = int(self.getBaseProperties().get(30010, 0))
		self.magic_armor_base = int(self.getBaseProperties().get(30011, 0))
		self.criticalstrike_base = int(self.getBaseProperties().get(30012, 0))
		self.parry_base = int(self.getBaseProperties().get(30013, 0))
		self.speed_base = int(self.getBaseProperties().get(30014, 0))
		self.hitrate_base = int(self.getBaseProperties().get(30015, 0))
		self.dodgerate_base = int(self.getBaseProperties().get(30016, 0))
		self.healingrate_base = int(self.getBaseProperties().get(30017, 0))
		self.gangQiValue_Max_base = int(self.getBaseProperties().get(30018, 0))
		self.gangQi_damagePoint_base = int(self.getBaseProperties().get(30019, 0))
		self.gangQi_armorPoint_base = int(self.getBaseProperties().get(30020, 0))
		self.gangQi_qiJieRevive_base = int(self.getBaseProperties().get(30021, 0))
		self.gangQi_qiYingRevive_base = int(self.getBaseProperties().get(30022, 0))
		self.tempSpeed_base = int(self.getBaseProperties().get(30023, 0))
		self.cure_base = int(self.getBaseProperties().get(30024, 0))
		self.critRatio_base = int(self.getBaseProperties().get(30025, 0))
		self.parryRatio_base = int(self.getBaseProperties().get(30026, 0))
		self.damage_correction_base = int(self.getBaseProperties().get(40001, 0))
		self.armor_correction_base = int(self.getBaseProperties().get(40002, 0))
		self.attack_damage_correction_base = int(self.getBaseProperties().get(40003, 0))
		self.magic_damage_correction_base = int(self.getBaseProperties().get(40004, 0))
		self.attack_armor_correction_base = int(self.getBaseProperties().get(40005, 0))
		self.magic_armor_correction_base = int(self.getBaseProperties().get(40006, 0))
		self.role_damage_correction_base = int(self.getBaseProperties().get(40007, 0))
		self.pet_damage_correction_base = int(self.getBaseProperties().get(40008, 0))
		self.monster_damage_correction_base = int(self.getBaseProperties().get(40009, 0))
		self.role_armor_correction_base = int(self.getBaseProperties().get(40010, 0))
		self.pet_armor_correction_base = int(self.getBaseProperties().get(40011, 0))
		self.monster_armor_correction_base = int(self.getBaseProperties().get(40012, 0))
		self.curecorrection_base = int(self.getBaseProperties().get(40013, 0))
		self.becuredcorrection_base = int(self.getBaseProperties().get(40014, 0))
		self.ice_damage_base = int(self.getBaseProperties().get(30027, 0))
		self.fire_damage_base = int(self.getBaseProperties().get(30028, 0))
		self.thunder_damage_base = int(self.getBaseProperties().get(30029, 0))
		self.xuan_damage_base = int(self.getBaseProperties().get(30030, 0))
		self.ice_armor_base = int(self.getBaseProperties().get(30031, 0))
		self.fire_armor_base = int(self.getBaseProperties().get(30032, 0))
		self.thunder_armor_base = int(self.getBaseProperties().get(30033, 0))
		self.xuan_armor_base = int(self.getBaseProperties().get(30034, 0))
		self.ice_damage_correction_base = int(self.getBaseProperties().get(40015, 0))
		self.fire_damage_correction_base = int(self.getBaseProperties().get(40016, 0))
		self.thunder_damage_correction_base = int(self.getBaseProperties().get(40017, 0))
		self.xuan_damage_correction_base = int(self.getBaseProperties().get(40018, 0))
		self.ice_armor_correction_base = int(self.getBaseProperties().get(40019, 0))
		self.fire_armor_correction_base = int(self.getBaseProperties().get(40020, 0))
		self.thunder_armor_correction_base = int(self.getBaseProperties().get(40021, 0))
		self.xuan_armor_correction_base = int(self.getBaseProperties().get(40022, 0))
		self.hatred_correction_base = int(self.getBaseProperties().get(40023, 0))
		self.related_hatred_correction_base = int(self.getBaseProperties().get(40024, 0))
		self.damage_ignore_base = int(self.getBaseProperties().get(30035, 0))
		self.magic_damage_ignore_base = int(self.getBaseProperties().get(30036, 0))
		self.armor_ignore_base = int(self.getBaseProperties().get(30037, 0))
		self.magic_armor_ignore_base = int(self.getBaseProperties().get(30038, 0))
		self.criticalstrike_ignore_base = int(self.getBaseProperties().get(30039, 0))
		self.parry_ignore_base = int(self.getBaseProperties().get(30040, 0))
		self.hitrate_ignore_base = int(self.getBaseProperties().get(30041, 0))
		self.dodgerate_ignore_base = int(self.getBaseProperties().get(30042, 0))
		self.ice_damage_ignore_base = int(self.getBaseProperties().get(30043, 0))
		self.fire_damage_ignore_base = int(self.getBaseProperties().get(30044, 0))
		self.thunder_damage_ignore_base = int(self.getBaseProperties().get(30045, 0))
		self.xuan_damage_ignore_base = int(self.getBaseProperties().get(30046, 0))
		self.ice_armor_ignore_base = int(self.getBaseProperties().get(30047, 0))
		self.fire_armor_ignore_base = int(self.getBaseProperties().get(30048, 0))
		self.thunder_armor_ignore_base = int(self.getBaseProperties().get(30049, 0))
		self.xuan_armor_ignore_base = int(self.getBaseProperties().get(30050, 0))
		self.depress_resist_base = int(self.getBaseProperties().get(30051, 0))
		self.hitback_resist_base = int(self.getBaseProperties().get(30052, 0))
		self.control_resist_base = int(self.getBaseProperties().get(30053, 0))
		self.insane_resist_base = int(self.getBaseProperties().get(30054, 0))

	def setRoleExtraProperties(self, dic):
		vv = int( dic.get(30001, 0) )
		self.corporeity_extra = vv + self.getXiuweiExtraProperties(30001)
		vv = int( dic.get(30002, 0) )
		self.strength_extra = vv + self.getXiuweiExtraProperties(30002)
		vv = int( dic.get(30003, 0) )
		self.intellect_extra = vv + self.getXiuweiExtraProperties(30003)
		vv = int( dic.get(30004, 0) )
		self.discern_extra = vv + self.getXiuweiExtraProperties(30004)
		vv = int( dic.get(30005, 0) )
		self.dexterity_extra = vv + self.getXiuweiExtraProperties(30005)
		vv = int( dic.get(30006, 0) )
		self.HP_Max_extra = vv + self.getXiuweiExtraProperties(30006)
		vv = int( dic.get(30007, 0) )
		self.MP_Max_extra = vv + self.getXiuweiExtraProperties(30007)
		vv = int( dic.get(30008, 0) )
		self.damage_extra = vv + self.getXiuweiExtraProperties(30008)
		vv = int( dic.get(30009, 0) )
		self.magic_damage_extra = vv + self.getXiuweiExtraProperties(30009)
		vv = int( dic.get(30010, 0) )
		self.armor_extra = vv + self.getXiuweiExtraProperties(30010)
		vv = int( dic.get(30011, 0) )
		self.magic_armor_extra = vv + self.getXiuweiExtraProperties(30011)
		vv = int( dic.get(30012, 0) )
		self.criticalstrike_extra = vv + self.getXiuweiExtraProperties(30012)
		vv = int( dic.get(30013, 0) )
		self.parry_extra = vv + self.getXiuweiExtraProperties(30013)
		vv = int( dic.get(30014, 0) )
		self.speed_extra = vv + self.getXiuweiExtraProperties(30014)
		vv = int( dic.get(30015, 0) )
		self.hitrate_extra = vv + self.getXiuweiExtraProperties(30015)
		vv = int( dic.get(30016, 0) )
		self.dodgerate_extra = vv + self.getXiuweiExtraProperties(30016)
		vv = int( dic.get(30017, 0) )
		self.healingrate_extra = vv + self.getXiuweiExtraProperties(30017)
		vv = int( dic.get(30018, 0) )
		self.gangQiValue_Max_extra = vv + self.getXiuweiExtraProperties(30018)
		vv = int( dic.get(30019, 0) )
		self.gangQi_damagePoint_extra = vv + self.getXiuweiExtraProperties(30019)
		vv = int( dic.get(30020, 0) )
		self.gangQi_armorPoint_extra = vv + self.getXiuweiExtraProperties(30020)
		vv = int( dic.get(30021, 0) )
		self.gangQi_qiJieRevive_extra = vv + self.getXiuweiExtraProperties(30021)
		vv = int( dic.get(30022, 0) )
		self.gangQi_qiYingRevive_extra = vv + self.getXiuweiExtraProperties(30022)
		vv = int( dic.get(30023, 0) )
		self.tempSpeed_extra = vv + self.getXiuweiExtraProperties(30023)
		vv = int( dic.get(30024, 0) )
		self.cure_extra = vv + self.getXiuweiExtraProperties(30024)
		vv = int( dic.get(30025, 0) )
		self.critRatio_extra = vv + self.getXiuweiExtraProperties(30025)
		vv = int( dic.get(30026, 0) )
		self.parryRatio_extra = vv + self.getXiuweiExtraProperties(30026)
		vv = int( dic.get(40001, 0) )
		self.damage_correction_extra = vv + self.getXiuweiExtraProperties(40001)
		vv = int( dic.get(40002, 0) )
		self.armor_correction_extra = vv + self.getXiuweiExtraProperties(40002)
		vv = int( dic.get(40003, 0) )
		self.attack_damage_correction_extra = vv + self.getXiuweiExtraProperties(40003)
		vv = int( dic.get(40004, 0) )
		self.magic_damage_correction_extra = vv + self.getXiuweiExtraProperties(40004)
		vv = int( dic.get(40005, 0) )
		self.attack_armor_correction_extra = vv + self.getXiuweiExtraProperties(40005)
		vv = int( dic.get(40006, 0) )
		self.magic_armor_correction_extra = vv + self.getXiuweiExtraProperties(40006)
		vv = int( dic.get(40007, 0) )
		self.role_damage_correction_extra = vv + self.getXiuweiExtraProperties(40007)
		vv = int( dic.get(40008, 0) )
		self.pet_damage_correction_extra = vv + self.getXiuweiExtraProperties(40008)
		vv = int( dic.get(40009, 0) )
		self.monster_damage_correction_extra = vv + self.getXiuweiExtraProperties(40009)
		vv = int( dic.get(40010, 0) )
		self.role_armor_correction_extra = vv + self.getXiuweiExtraProperties(40010)
		vv = int( dic.get(40011, 0) )
		self.pet_armor_correction_extra = vv + self.getXiuweiExtraProperties(40011)
		vv = int( dic.get(40012, 0) )
		self.monster_armor_correction_extra = vv + self.getXiuweiExtraProperties(40012)
		vv = int( dic.get(40013, 0) )
		self.curecorrection_extra = vv + self.getXiuweiExtraProperties(40013)
		vv = int( dic.get(40014, 0) )
		self.becuredcorrection_extra = vv + self.getXiuweiExtraProperties(40014)
		vv = int( dic.get(30027, 0) )
		self.ice_damage_extra = vv + self.getXiuweiExtraProperties(30027)
		vv = int( dic.get(30028, 0) )
		self.fire_damage_extra = vv + self.getXiuweiExtraProperties(30028)
		vv = int( dic.get(30029, 0) )
		self.thunder_damage_extra = vv + self.getXiuweiExtraProperties(30029)
		vv = int( dic.get(30030, 0) )
		self.xuan_damage_extra = vv + self.getXiuweiExtraProperties(30030)
		vv = int( dic.get(30031, 0) )
		self.ice_armor_extra = vv + self.getXiuweiExtraProperties(30031)
		vv = int( dic.get(30032, 0) )
		self.fire_armor_extra = vv + self.getXiuweiExtraProperties(30032)
		vv = int( dic.get(30033, 0) )
		self.thunder_armor_extra = vv + self.getXiuweiExtraProperties(30033)
		vv = int( dic.get(30034, 0) )
		self.xuan_armor_extra = vv + self.getXiuweiExtraProperties(30034)
		vv = int( dic.get(40015, 0) )
		self.ice_damage_correction_extra = vv + self.getXiuweiExtraProperties(40015)
		vv = int( dic.get(40016, 0) )
		self.fire_damage_correction_extra = vv + self.getXiuweiExtraProperties(40016)
		vv = int( dic.get(40017, 0) )
		self.thunder_damage_correction_extra = vv + self.getXiuweiExtraProperties(40017)
		vv = int( dic.get(40018, 0) )
		self.xuan_damage_correction_extra = vv + self.getXiuweiExtraProperties(40018)
		vv = int( dic.get(40019, 0) )
		self.ice_armor_correction_extra = vv + self.getXiuweiExtraProperties(40019)
		vv = int( dic.get(40020, 0) )
		self.fire_armor_correction_extra = vv + self.getXiuweiExtraProperties(40020)
		vv = int( dic.get(40021, 0) )
		self.thunder_armor_correction_extra = vv + self.getXiuweiExtraProperties(40021)
		vv = int( dic.get(40022, 0) )
		self.xuan_armor_correction_extra = vv + self.getXiuweiExtraProperties(40022)
		vv = int( dic.get(40023, 0) )
		self.hatred_correction_extra = vv + self.getXiuweiExtraProperties(40023)
		vv = int( dic.get(40024, 0) )
		self.related_hatred_correction_extra = vv + self.getXiuweiExtraProperties(40024)
		vv = int( dic.get(30035, 0) )
		self.damage_ignore_extra = vv + self.getXiuweiExtraProperties(30035)
		vv = int( dic.get(30036, 0) )
		self.magic_damage_ignore_extra = vv + self.getXiuweiExtraProperties(30036)
		vv = int( dic.get(30037, 0) )
		self.armor_ignore_extra = vv + self.getXiuweiExtraProperties(30037)
		vv = int( dic.get(30038, 0) )
		self.magic_armor_ignore_extra = vv + self.getXiuweiExtraProperties(30038)
		vv = int( dic.get(30039, 0) )
		self.criticalstrike_ignore_extra = vv + self.getXiuweiExtraProperties(30039)
		vv = int( dic.get(30040, 0) )
		self.parry_ignore_extra = vv + self.getXiuweiExtraProperties(30040)
		vv = int( dic.get(30041, 0) )
		self.hitrate_ignore_extra = vv + self.getXiuweiExtraProperties(30041)
		vv = int( dic.get(30042, 0) )
		self.dodgerate_ignore_extra = vv + self.getXiuweiExtraProperties(30042)
		vv = int( dic.get(30043, 0) )
		self.ice_damage_ignore_extra = vv + self.getXiuweiExtraProperties(30043)
		vv = int( dic.get(30044, 0) )
		self.fire_damage_ignore_extra = vv + self.getXiuweiExtraProperties(30044)
		vv = int( dic.get(30045, 0) )
		self.thunder_damage_ignore_extra = vv + self.getXiuweiExtraProperties(30045)
		vv = int( dic.get(30046, 0) )
		self.xuan_damage_ignore_extra = vv + self.getXiuweiExtraProperties(30046)
		vv = int( dic.get(30047, 0) )
		self.ice_armor_ignore_extra = vv + self.getXiuweiExtraProperties(30047)
		vv = int( dic.get(30048, 0) )
		self.fire_armor_ignore_extra = vv + self.getXiuweiExtraProperties(30048)
		vv = int( dic.get(30049, 0) )
		self.thunder_armor_ignore_extra = vv + self.getXiuweiExtraProperties(30049)
		vv = int( dic.get(30050, 0) )
		self.xuan_armor_ignore_extra = vv + self.getXiuweiExtraProperties(30050)
		vv = int( dic.get(30051, 0) )
		self.depress_resist_extra = vv + self.getXiuweiExtraProperties(30051)
		vv = int( dic.get(30052, 0) )
		self.hitback_resist_extra = vv + self.getXiuweiExtraProperties(30052)
		vv = int( dic.get(30053, 0) )
		self.control_resist_extra = vv + self.getXiuweiExtraProperties(30053)
		vv = int( dic.get(30054, 0) )
		self.insane_resist_extra = vv + self.getXiuweiExtraProperties(30054)

	def setMonsterExtraProperties(self, dic):
		self.corporeity_extra = int( dic.get(30001, 0) )
		self.strength_extra = int( dic.get(30002, 0) )
		self.intellect_extra = int( dic.get(30003, 0) )
		self.discern_extra = int( dic.get(30004, 0) )
		self.dexterity_extra = int( dic.get(30005, 0) )
		self.HP_Max_extra = int( dic.get(30006, 0) )
		self.MP_Max_extra = int( dic.get(30007, 0) )
		self.damage_extra = int( dic.get(30008, 0) )
		self.magic_damage_extra = int( dic.get(30009, 0) )
		self.armor_extra = int( dic.get(30010, 0) )
		self.magic_armor_extra = int( dic.get(30011, 0) )
		self.criticalstrike_extra = int( dic.get(30012, 0) )
		self.parry_extra = int( dic.get(30013, 0) )
		self.speed_extra = int( dic.get(30014, 0) )
		self.hitrate_extra = int( dic.get(30015, 0) )
		self.dodgerate_extra = int( dic.get(30016, 0) )
		self.healingrate_extra = int( dic.get(30017, 0) )
		self.gangQiValue_Max_extra = int( dic.get(30018, 0) )
		self.gangQi_damagePoint_extra = int( dic.get(30019, 0) )
		self.gangQi_armorPoint_extra = int( dic.get(30020, 0) )
		self.gangQi_qiJieRevive_extra = int( dic.get(30021, 0) )
		self.gangQi_qiYingRevive_extra = int( dic.get(30022, 0) )
		self.tempSpeed_extra = int( dic.get(30023, 0) )
		self.cure_extra = int( dic.get(30024, 0) )
		self.critRatio_extra = int( dic.get(30025, 0) )
		self.parryRatio_extra = int( dic.get(30026, 0) )
		self.damage_correction_extra = int( dic.get(40001, 0) )
		self.armor_correction_extra = int( dic.get(40002, 0) )
		self.attack_damage_correction_extra = int( dic.get(40003, 0) )
		self.magic_damage_correction_extra = int( dic.get(40004, 0) )
		self.attack_armor_correction_extra = int( dic.get(40005, 0) )
		self.magic_armor_correction_extra = int( dic.get(40006, 0) )
		self.role_damage_correction_extra = int( dic.get(40007, 0) )
		self.pet_damage_correction_extra = int( dic.get(40008, 0) )
		self.monster_damage_correction_extra = int( dic.get(40009, 0) )
		self.role_armor_correction_extra = int( dic.get(40010, 0) )
		self.pet_armor_correction_extra = int( dic.get(40011, 0) )
		self.monster_armor_correction_extra = int( dic.get(40012, 0) )
		self.curecorrection_extra = int( dic.get(40013, 0) )
		self.becuredcorrection_extra = int( dic.get(40014, 0) )
		self.ice_damage_extra = int( dic.get(30027, 0) )
		self.fire_damage_extra = int( dic.get(30028, 0) )
		self.thunder_damage_extra = int( dic.get(30029, 0) )
		self.xuan_damage_extra = int( dic.get(30030, 0) )
		self.ice_armor_extra = int( dic.get(30031, 0) )
		self.fire_armor_extra = int( dic.get(30032, 0) )
		self.thunder_armor_extra = int( dic.get(30033, 0) )
		self.xuan_armor_extra = int( dic.get(30034, 0) )
		self.ice_damage_correction_extra = int( dic.get(40015, 0) )
		self.fire_damage_correction_extra = int( dic.get(40016, 0) )
		self.thunder_damage_correction_extra = int( dic.get(40017, 0) )
		self.xuan_damage_correction_extra = int( dic.get(40018, 0) )
		self.ice_armor_correction_extra = int( dic.get(40019, 0) )
		self.fire_armor_correction_extra = int( dic.get(40020, 0) )
		self.thunder_armor_correction_extra = int( dic.get(40021, 0) )
		self.xuan_armor_correction_extra = int( dic.get(40022, 0) )
		self.hatred_correction_extra = int( dic.get(40023, 0) )
		self.related_hatred_correction_extra = int( dic.get(40024, 0) )
		self.damage_ignore_extra = int( dic.get(30035, 0) )
		self.magic_damage_ignore_extra = int( dic.get(30036, 0) )
		self.armor_ignore_extra = int( dic.get(30037, 0) )
		self.magic_armor_ignore_extra = int( dic.get(30038, 0) )
		self.criticalstrike_ignore_extra = int( dic.get(30039, 0) )
		self.parry_ignore_extra = int( dic.get(30040, 0) )
		self.hitrate_ignore_extra = int( dic.get(30041, 0) )
		self.dodgerate_ignore_extra = int( dic.get(30042, 0) )
		self.ice_damage_ignore_extra = int( dic.get(30043, 0) )
		self.fire_damage_ignore_extra = int( dic.get(30044, 0) )
		self.thunder_damage_ignore_extra = int( dic.get(30045, 0) )
		self.xuan_damage_ignore_extra = int( dic.get(30046, 0) )
		self.ice_armor_ignore_extra = int( dic.get(30047, 0) )
		self.fire_armor_ignore_extra = int( dic.get(30048, 0) )
		self.thunder_armor_ignore_extra = int( dic.get(30049, 0) )
		self.xuan_armor_ignore_extra = int( dic.get(30050, 0) )
		self.depress_resist_extra = int( dic.get(30051, 0) )
		self.hitback_resist_extra = int( dic.get(30052, 0) )
		self.control_resist_extra = int( dic.get(30053, 0) )
		self.insane_resist_extra = int( dic.get(30054, 0) )

	def setVehiclePetExtraProperties(self, dic):
		self.corporeity_extra = int( dic.get(30001, 0) )
		self.strength_extra = int( dic.get(30002, 0) )
		self.intellect_extra = int( dic.get(30003, 0) )
		self.discern_extra = int( dic.get(30004, 0) )
		self.dexterity_extra = int( dic.get(30005, 0) )
		self.HP_Max_extra = int( dic.get(30006, 0) )
		self.MP_Max_extra = int( dic.get(30007, 0) )
		self.damage_extra = int( dic.get(30008, 0) )
		self.magic_damage_extra = int( dic.get(30009, 0) )
		self.armor_extra = int( dic.get(30010, 0) )
		self.magic_armor_extra = int( dic.get(30011, 0) )
		self.criticalstrike_extra = int( dic.get(30012, 0) )
		self.parry_extra = int( dic.get(30013, 0) )
		self.speed_extra = int( dic.get(30014, 0) )
		self.hitrate_extra = int( dic.get(30015, 0) )
		self.dodgerate_extra = int( dic.get(30016, 0) )
		self.healingrate_extra = int( dic.get(30017, 0) )
		self.gangQiValue_Max_extra = int( dic.get(30018, 0) )
		self.gangQi_damagePoint_extra = int( dic.get(30019, 0) )
		self.gangQi_armorPoint_extra = int( dic.get(30020, 0) )
		self.gangQi_qiJieRevive_extra = int( dic.get(30021, 0) )
		self.gangQi_qiYingRevive_extra = int( dic.get(30022, 0) )
		self.tempSpeed_extra = int( dic.get(30023, 0) )
		self.cure_extra = int( dic.get(30024, 0) )
		self.critRatio_extra = int( dic.get(30025, 0) )
		self.parryRatio_extra = int( dic.get(30026, 0) )
		self.damage_correction_extra = int( dic.get(40001, 0) )
		self.armor_correction_extra = int( dic.get(40002, 0) )
		self.attack_damage_correction_extra = int( dic.get(40003, 0) )
		self.magic_damage_correction_extra = int( dic.get(40004, 0) )
		self.attack_armor_correction_extra = int( dic.get(40005, 0) )
		self.magic_armor_correction_extra = int( dic.get(40006, 0) )
		self.role_damage_correction_extra = int( dic.get(40007, 0) )
		self.pet_damage_correction_extra = int( dic.get(40008, 0) )
		self.monster_damage_correction_extra = int( dic.get(40009, 0) )
		self.role_armor_correction_extra = int( dic.get(40010, 0) )
		self.pet_armor_correction_extra = int( dic.get(40011, 0) )
		self.monster_armor_correction_extra = int( dic.get(40012, 0) )
		self.curecorrection_extra = int( dic.get(40013, 0) )
		self.becuredcorrection_extra = int( dic.get(40014, 0) )
		self.ice_damage_extra = int( dic.get(30027, 0) )
		self.fire_damage_extra = int( dic.get(30028, 0) )
		self.thunder_damage_extra = int( dic.get(30029, 0) )
		self.xuan_damage_extra = int( dic.get(30030, 0) )
		self.ice_armor_extra = int( dic.get(30031, 0) )
		self.fire_armor_extra = int( dic.get(30032, 0) )
		self.thunder_armor_extra = int( dic.get(30033, 0) )
		self.xuan_armor_extra = int( dic.get(30034, 0) )
		self.ice_damage_correction_extra = int( dic.get(40015, 0) )
		self.fire_damage_correction_extra = int( dic.get(40016, 0) )
		self.thunder_damage_correction_extra = int( dic.get(40017, 0) )
		self.xuan_damage_correction_extra = int( dic.get(40018, 0) )
		self.ice_armor_correction_extra = int( dic.get(40019, 0) )
		self.fire_armor_correction_extra = int( dic.get(40020, 0) )
		self.thunder_armor_correction_extra = int( dic.get(40021, 0) )
		self.xuan_armor_correction_extra = int( dic.get(40022, 0) )
		self.hatred_correction_extra = int( dic.get(40023, 0) )
		self.related_hatred_correction_extra = int( dic.get(40024, 0) )
		self.damage_ignore_extra = int( dic.get(30035, 0) )
		self.magic_damage_ignore_extra = int( dic.get(30036, 0) )
		self.armor_ignore_extra = int( dic.get(30037, 0) )
		self.magic_armor_ignore_extra = int( dic.get(30038, 0) )
		self.criticalstrike_ignore_extra = int( dic.get(30039, 0) )
		self.parry_ignore_extra = int( dic.get(30040, 0) )
		self.hitrate_ignore_extra = int( dic.get(30041, 0) )
		self.dodgerate_ignore_extra = int( dic.get(30042, 0) )
		self.ice_damage_ignore_extra = int( dic.get(30043, 0) )
		self.fire_damage_ignore_extra = int( dic.get(30044, 0) )
		self.thunder_damage_ignore_extra = int( dic.get(30045, 0) )
		self.xuan_damage_ignore_extra = int( dic.get(30046, 0) )
		self.ice_armor_ignore_extra = int( dic.get(30047, 0) )
		self.fire_armor_ignore_extra = int( dic.get(30048, 0) )
		self.thunder_armor_ignore_extra = int( dic.get(30049, 0) )
		self.xuan_armor_ignore_extra = int( dic.get(30050, 0) )
		self.depress_resist_extra = int( dic.get(30051, 0) )
		self.hitback_resist_extra = int( dic.get(30052, 0) )
		self.control_resist_extra = int( dic.get(30053, 0) )
		self.insane_resist_extra = int( dic.get(30054, 0) )

	def setPrecentProperties(self, dic):
		self.corporeity_percent = dic.get(30001, 0)
		self.strength_percent = dic.get(30002, 0)
		self.intellect_percent = dic.get(30003, 0)
		self.discern_percent = dic.get(30004, 0)
		self.dexterity_percent = dic.get(30005, 0)
		self.HP_Max_percent = dic.get(30006, 0)
		self.MP_Max_percent = dic.get(30007, 0)
		self.damage_percent = dic.get(30008, 0)
		self.magic_damage_percent = dic.get(30009, 0)
		self.armor_percent = dic.get(30010, 0)
		self.magic_armor_percent = dic.get(30011, 0)
		self.criticalstrike_percent = dic.get(30012, 0)
		self.parry_percent = dic.get(30013, 0)
		self.speed_percent = dic.get(30014, 0)
		self.hitrate_percent = dic.get(30015, 0)
		self.dodgerate_percent = dic.get(30016, 0)
		self.healingrate_percent = dic.get(30017, 0)
		self.gangQiValue_Max_percent = dic.get(30018, 0)
		self.gangQi_damagePoint_percent = dic.get(30019, 0)
		self.gangQi_armorPoint_percent = dic.get(30020, 0)
		self.gangQi_qiJieRevive_percent = dic.get(30021, 0)
		self.gangQi_qiYingRevive_percent = dic.get(30022, 0)
		self.tempSpeed_percent = dic.get(30023, 0)
		self.cure_percent = dic.get(30024, 0)
		self.critRatio_percent = dic.get(30025, 0)
		self.parryRatio_percent = dic.get(30026, 0)
		self.damage_correction_percent = dic.get(40001, 0)
		self.armor_correction_percent = dic.get(40002, 0)
		self.attack_damage_correction_percent = dic.get(40003, 0)
		self.magic_damage_correction_percent = dic.get(40004, 0)
		self.attack_armor_correction_percent = dic.get(40005, 0)
		self.magic_armor_correction_percent = dic.get(40006, 0)
		self.role_damage_correction_percent = dic.get(40007, 0)
		self.pet_damage_correction_percent = dic.get(40008, 0)
		self.monster_damage_correction_percent = dic.get(40009, 0)
		self.role_armor_correction_percent = dic.get(40010, 0)
		self.pet_armor_correction_percent = dic.get(40011, 0)
		self.monster_armor_correction_percent = dic.get(40012, 0)
		self.curecorrection_percent = dic.get(40013, 0)
		self.becuredcorrection_percent = dic.get(40014, 0)
		self.ice_damage_percent = dic.get(30027, 0)
		self.fire_damage_percent = dic.get(30028, 0)
		self.thunder_damage_percent = dic.get(30029, 0)
		self.xuan_damage_percent = dic.get(30030, 0)
		self.ice_armor_percent = dic.get(30031, 0)
		self.fire_armor_percent = dic.get(30032, 0)
		self.thunder_armor_percent = dic.get(30033, 0)
		self.xuan_armor_percent = dic.get(30034, 0)
		self.ice_damage_correction_percent = dic.get(40015, 0)
		self.fire_damage_correction_percent = dic.get(40016, 0)
		self.thunder_damage_correction_percent = dic.get(40017, 0)
		self.xuan_damage_correction_percent = dic.get(40018, 0)
		self.ice_armor_correction_percent = dic.get(40019, 0)
		self.fire_armor_correction_percent = dic.get(40020, 0)
		self.thunder_armor_correction_percent = dic.get(40021, 0)
		self.xuan_armor_correction_percent = dic.get(40022, 0)
		self.hatred_correction_percent = dic.get(40023, 0)
		self.related_hatred_correction_percent = dic.get(40024, 0)
		self.damage_ignore_percent = dic.get(30035, 0)
		self.magic_damage_ignore_percent = dic.get(30036, 0)
		self.armor_ignore_percent = dic.get(30037, 0)
		self.magic_armor_ignore_percent = dic.get(30038, 0)
		self.criticalstrike_ignore_percent = dic.get(30039, 0)
		self.parry_ignore_percent = dic.get(30040, 0)
		self.hitrate_ignore_percent = dic.get(30041, 0)
		self.dodgerate_ignore_percent = dic.get(30042, 0)
		self.ice_damage_ignore_percent = dic.get(30043, 0)
		self.fire_damage_ignore_percent = dic.get(30044, 0)
		self.thunder_damage_ignore_percent = dic.get(30045, 0)
		self.xuan_damage_ignore_percent = dic.get(30046, 0)
		self.ice_armor_ignore_percent = dic.get(30047, 0)
		self.fire_armor_ignore_percent = dic.get(30048, 0)
		self.thunder_armor_ignore_percent = dic.get(30049, 0)
		self.xuan_armor_ignore_percent = dic.get(30050, 0)
		self.depress_resist_percent = dic.get(30051, 0)
		self.hitback_resist_percent = dic.get(30052, 0)
		self.control_resist_percent = dic.get(30053, 0)
		self.insane_resist_percent = dic.get(30054, 0)

	def setValueProperties(self, dic):
		self.corporeity_value = dic.get(30001, 0)
		self.strength_value = dic.get(30002, 0)
		self.intellect_value = dic.get(30003, 0)
		self.discern_value = dic.get(30004, 0)
		self.dexterity_value = dic.get(30005, 0)
		self.HP_Max_value = dic.get(30006, 0)
		self.MP_Max_value = dic.get(30007, 0)
		self.damage_value = dic.get(30008, 0)
		self.magic_damage_value = dic.get(30009, 0)
		self.armor_value = dic.get(30010, 0)
		self.magic_armor_value = dic.get(30011, 0)
		self.criticalstrike_value = dic.get(30012, 0)
		self.parry_value = dic.get(30013, 0)
		self.speed_value = dic.get(30014, 0)
		self.hitrate_value = dic.get(30015, 0)
		self.dodgerate_value = dic.get(30016, 0)
		self.healingrate_value = dic.get(30017, 0)
		self.gangQiValue_Max_value = dic.get(30018, 0)
		self.gangQi_damagePoint_value = dic.get(30019, 0)
		self.gangQi_armorPoint_value = dic.get(30020, 0)
		self.gangQi_qiJieRevive_value = dic.get(30021, 0)
		self.gangQi_qiYingRevive_value = dic.get(30022, 0)
		self.tempSpeed_value = dic.get(30023, 0)
		self.cure_value = dic.get(30024, 0)
		self.critRatio_value = dic.get(30025, 0)
		self.parryRatio_value = dic.get(30026, 0)
		self.damage_correction_value = dic.get(40001, 0)
		self.armor_correction_value = dic.get(40002, 0)
		self.attack_damage_correction_value = dic.get(40003, 0)
		self.magic_damage_correction_value = dic.get(40004, 0)
		self.attack_armor_correction_value = dic.get(40005, 0)
		self.magic_armor_correction_value = dic.get(40006, 0)
		self.role_damage_correction_value = dic.get(40007, 0)
		self.pet_damage_correction_value = dic.get(40008, 0)
		self.monster_damage_correction_value = dic.get(40009, 0)
		self.role_armor_correction_value = dic.get(40010, 0)
		self.pet_armor_correction_value = dic.get(40011, 0)
		self.monster_armor_correction_value = dic.get(40012, 0)
		self.curecorrection_value = dic.get(40013, 0)
		self.becuredcorrection_value = dic.get(40014, 0)
		self.ice_damage_value = dic.get(30027, 0)
		self.fire_damage_value = dic.get(30028, 0)
		self.thunder_damage_value = dic.get(30029, 0)
		self.xuan_damage_value = dic.get(30030, 0)
		self.ice_armor_value = dic.get(30031, 0)
		self.fire_armor_value = dic.get(30032, 0)
		self.thunder_armor_value = dic.get(30033, 0)
		self.xuan_armor_value = dic.get(30034, 0)
		self.ice_damage_correction_value = dic.get(40015, 0)
		self.fire_damage_correction_value = dic.get(40016, 0)
		self.thunder_damage_correction_value = dic.get(40017, 0)
		self.xuan_damage_correction_value = dic.get(40018, 0)
		self.ice_armor_correction_value = dic.get(40019, 0)
		self.fire_armor_correction_value = dic.get(40020, 0)
		self.thunder_armor_correction_value = dic.get(40021, 0)
		self.xuan_armor_correction_value = dic.get(40022, 0)
		self.hatred_correction_value = dic.get(40023, 0)
		self.related_hatred_correction_value = dic.get(40024, 0)
		self.damage_ignore_value = dic.get(30035, 0)
		self.magic_damage_ignore_value = dic.get(30036, 0)
		self.armor_ignore_value = dic.get(30037, 0)
		self.magic_armor_ignore_value = dic.get(30038, 0)
		self.criticalstrike_ignore_value = dic.get(30039, 0)
		self.parry_ignore_value = dic.get(30040, 0)
		self.hitrate_ignore_value = dic.get(30041, 0)
		self.dodgerate_ignore_value = dic.get(30042, 0)
		self.ice_damage_ignore_value = dic.get(30043, 0)
		self.fire_damage_ignore_value = dic.get(30044, 0)
		self.thunder_damage_ignore_value = dic.get(30045, 0)
		self.xuan_damage_ignore_value = dic.get(30046, 0)
		self.ice_armor_ignore_value = dic.get(30047, 0)
		self.fire_armor_ignore_value = dic.get(30048, 0)
		self.thunder_armor_ignore_value = dic.get(30049, 0)
		self.xuan_armor_ignore_value = dic.get(30050, 0)
		self.depress_resist_value = dic.get(30051, 0)
		self.hitback_resist_value = dic.get(30052, 0)
		self.control_resist_value = dic.get(30053, 0)
		self.insane_resist_value = dic.get(30054, 0)

	def setLVOneProperties(self):
		basevalue =  self.getBaseResultPropertyValue( self.corporeity_base)
		extravalue = self.getExtraResultPropertyValue( self.corporeity_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.corporeity_percent )
		vvalue = self.getValueResultPropertyValue( self.corporeity_value)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		if self.corporeity != int(result):
			self.corporeity = int(result)

		basevalue =  self.getBaseResultPropertyValue( self.strength_base)
		extravalue = self.getExtraResultPropertyValue( self.strength_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.strength_percent )
		vvalue = self.getValueResultPropertyValue( self.strength_value)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		if self.strength != int(result):
			self.strength = int(result)

		basevalue =  self.getBaseResultPropertyValue( self.intellect_base)
		extravalue = self.getExtraResultPropertyValue( self.intellect_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.intellect_percent )
		vvalue = self.getValueResultPropertyValue( self.intellect_value)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		if self.intellect != int(result):
			self.intellect = int(result)

		basevalue =  self.getBaseResultPropertyValue( self.discern_base)
		extravalue = self.getExtraResultPropertyValue( self.discern_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.discern_percent )
		vvalue = self.getValueResultPropertyValue( self.discern_value)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		if self.discern != int(result):
			self.discern = int(result)

		basevalue =  self.getBaseResultPropertyValue( self.dexterity_base)
		extravalue = self.getExtraResultPropertyValue( self.dexterity_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.dexterity_percent )
		vvalue = self.getValueResultPropertyValue( self.dexterity_value)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		if self.dexterity != int(result):
			self.dexterity = int(result)


	def setLVTwoProperties(self ):
		List = ["HP_Max", "MP_Max", "gangQiValue_Max", "damage", "magic_damage", "cure"]
		basevalue =  self.getBaseResultPropertyValue( self.HP_Max_base )
		extravalue = self.getExtraResultPropertyValue( self.HP_Max_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.HP_Max_percent )
		vvalue = self.getValueResultPropertyValue( self.HP_Max_value )
		extravalue += self.getExchangeTwoPropertyValue(30006)	#把兑换值加在成长值中
		self.HP_Max_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30006] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.HP_Max != int( result ):
			self.HP_Max = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.MP_Max_base )
		extravalue = self.getExtraResultPropertyValue( self.MP_Max_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.MP_Max_percent )
		vvalue = self.getValueResultPropertyValue( self.MP_Max_value )
		extravalue += self.getExchangeTwoPropertyValue(30007)	#把兑换值加在成长值中
		self.MP_Max_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30007] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.MP_Max != int( result ):
			self.MP_Max = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.damage_base )
		extravalue = self.getExtraResultPropertyValue( self.damage_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.damage_percent )
		vvalue = self.getValueResultPropertyValue( self.damage_value )
		extravalue += self.getExchangeTwoPropertyValue(30008)	#把兑换值加在成长值中
		self.damage_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30008] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.damage != int( result ):
			self.damage = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.magic_damage_base )
		extravalue = self.getExtraResultPropertyValue( self.magic_damage_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.magic_damage_percent )
		vvalue = self.getValueResultPropertyValue( self.magic_damage_value )
		extravalue += self.getExchangeTwoPropertyValue(30009)	#把兑换值加在成长值中
		self.magic_damage_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30009] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.magic_damage != int( result ):
			self.magic_damage = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.armor_base )
		extravalue = self.getExtraResultPropertyValue( self.armor_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.armor_percent )
		vvalue = self.getValueResultPropertyValue( self.armor_value )
		extravalue += self.getExchangeTwoPropertyValue(30010)	#把兑换值加在成长值中
		self.armor_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30010] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.armor != int( result ):
			self.armor = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.magic_armor_base )
		extravalue = self.getExtraResultPropertyValue( self.magic_armor_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.magic_armor_percent )
		vvalue = self.getValueResultPropertyValue( self.magic_armor_value )
		extravalue += self.getExchangeTwoPropertyValue(30011)	#把兑换值加在成长值中
		self.magic_armor_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30011] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.magic_armor != int( result ):
			self.magic_armor = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.criticalstrike_base )
		extravalue = self.getExtraResultPropertyValue( self.criticalstrike_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.criticalstrike_percent )
		vvalue = self.getValueResultPropertyValue( self.criticalstrike_value )
		extravalue += self.getExchangeTwoPropertyValue(30012)	#把兑换值加在成长值中
		self.criticalstrike_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30012] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.criticalstrike != int( result ):
			self.criticalstrike = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.parry_base )
		extravalue = self.getExtraResultPropertyValue( self.parry_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.parry_percent )
		vvalue = self.getValueResultPropertyValue( self.parry_value )
		extravalue += self.getExchangeTwoPropertyValue(30013)	#把兑换值加在成长值中
		self.parry_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30013] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.parry != int( result ):
			self.parry = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.speed_base )
		extravalue = self.getExtraResultPropertyValue( self.speed_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.speed_percent )
		vvalue = self.getValueResultPropertyValue( self.speed_value )
		extravalue += self.getExchangeTwoPropertyValue(30014)	#把兑换值加在成长值中
		self.speed_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30014] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.speed != int( result ):
			self.speed = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.hitrate_base )
		extravalue = self.getExtraResultPropertyValue( self.hitrate_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.hitrate_percent )
		vvalue = self.getValueResultPropertyValue( self.hitrate_value )
		extravalue += self.getExchangeTwoPropertyValue(30015)	#把兑换值加在成长值中
		self.hitrate_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30015] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.hitrate != int( result ):
			self.hitrate = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.dodgerate_base )
		extravalue = self.getExtraResultPropertyValue( self.dodgerate_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.dodgerate_percent )
		vvalue = self.getValueResultPropertyValue( self.dodgerate_value )
		extravalue += self.getExchangeTwoPropertyValue(30016)	#把兑换值加在成长值中
		self.dodgerate_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30016] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.dodgerate != int( result ):
			self.dodgerate = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.healingrate_base )
		extravalue = self.getExtraResultPropertyValue( self.healingrate_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.healingrate_percent )
		vvalue = self.getValueResultPropertyValue( self.healingrate_value )
		extravalue += self.getExchangeTwoPropertyValue(30017)	#把兑换值加在成长值中
		self.healingrate_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30017] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.healingrate != int( result ):
			self.healingrate = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.gangQiValue_Max_base )
		extravalue = self.getExtraResultPropertyValue( self.gangQiValue_Max_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.gangQiValue_Max_percent )
		vvalue = self.getValueResultPropertyValue( self.gangQiValue_Max_value )
		extravalue += self.getExchangeTwoPropertyValue(30018)	#把兑换值加在成长值中
		self.gangQiValue_Max_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30018] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.gangQiValue_Max != int( result ):
			self.gangQiValue_Max = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.gangQi_damagePoint_base )
		extravalue = self.getExtraResultPropertyValue( self.gangQi_damagePoint_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.gangQi_damagePoint_percent )
		vvalue = self.getValueResultPropertyValue( self.gangQi_damagePoint_value )
		extravalue += self.getExchangeTwoPropertyValue(30019)	#把兑换值加在成长值中
		self.gangQi_damagePoint_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30019] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.gangQi_damagePoint != int( result ):
			self.gangQi_damagePoint = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.gangQi_armorPoint_base )
		extravalue = self.getExtraResultPropertyValue( self.gangQi_armorPoint_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.gangQi_armorPoint_percent )
		vvalue = self.getValueResultPropertyValue( self.gangQi_armorPoint_value )
		extravalue += self.getExchangeTwoPropertyValue(30020)	#把兑换值加在成长值中
		self.gangQi_armorPoint_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30020] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.gangQi_armorPoint != int( result ):
			self.gangQi_armorPoint = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.gangQi_qiJieRevive_base )
		extravalue = self.getExtraResultPropertyValue( self.gangQi_qiJieRevive_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.gangQi_qiJieRevive_percent )
		vvalue = self.getValueResultPropertyValue( self.gangQi_qiJieRevive_value )
		extravalue += self.getExchangeTwoPropertyValue(30021)	#把兑换值加在成长值中
		self.gangQi_qiJieRevive_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30021] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.gangQi_qiJieRevive != int( result ):
			self.gangQi_qiJieRevive = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.gangQi_qiYingRevive_base )
		extravalue = self.getExtraResultPropertyValue( self.gangQi_qiYingRevive_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.gangQi_qiYingRevive_percent )
		vvalue = self.getValueResultPropertyValue( self.gangQi_qiYingRevive_value )
		extravalue += self.getExchangeTwoPropertyValue(30022)	#把兑换值加在成长值中
		self.gangQi_qiYingRevive_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30022] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.gangQi_qiYingRevive != int( result ):
			self.gangQi_qiYingRevive = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40001)	#把兑换值加在成长值中
		self.damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40001] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.damage_correction != int( result ):
			self.damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40002)	#把兑换值加在成长值中
		self.armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40002] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.armor_correction != int( result ):
			self.armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.attack_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.attack_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.attack_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.attack_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40003)	#把兑换值加在成长值中
		self.attack_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40003] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.attack_damage_correction != int( result ):
			self.attack_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.magic_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.magic_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.magic_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.magic_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40004)	#把兑换值加在成长值中
		self.magic_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40004] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.magic_damage_correction != int( result ):
			self.magic_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.attack_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.attack_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.attack_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.attack_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40005)	#把兑换值加在成长值中
		self.attack_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40005] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.attack_armor_correction != int( result ):
			self.attack_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.magic_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.magic_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.magic_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.magic_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40006)	#把兑换值加在成长值中
		self.magic_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40006] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.magic_armor_correction != int( result ):
			self.magic_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.role_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.role_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.role_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.role_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40007)	#把兑换值加在成长值中
		self.role_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40007] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.role_damage_correction != int( result ):
			self.role_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.pet_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.pet_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.pet_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.pet_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40008)	#把兑换值加在成长值中
		self.pet_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40008] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.pet_damage_correction != int( result ):
			self.pet_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.monster_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.monster_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.monster_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.monster_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40009)	#把兑换值加在成长值中
		self.monster_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40009] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.monster_damage_correction != int( result ):
			self.monster_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.role_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.role_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.role_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.role_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40010)	#把兑换值加在成长值中
		self.role_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40010] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.role_armor_correction != int( result ):
			self.role_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.pet_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.pet_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.pet_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.pet_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40011)	#把兑换值加在成长值中
		self.pet_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40011] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.pet_armor_correction != int( result ):
			self.pet_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.monster_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.monster_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.monster_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.monster_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40012)	#把兑换值加在成长值中
		self.monster_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40012] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.monster_armor_correction != int( result ):
			self.monster_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.cure_base )
		extravalue = self.getExtraResultPropertyValue( self.cure_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.cure_percent )
		vvalue = self.getValueResultPropertyValue( self.cure_value )
		extravalue += self.getExchangeTwoPropertyValue(30024)	#把兑换值加在成长值中
		self.cure_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30024] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.cure != int( result ):
			self.cure = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.curecorrection_base )
		extravalue = self.getExtraResultPropertyValue( self.curecorrection_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.curecorrection_percent )
		vvalue = self.getValueResultPropertyValue( self.curecorrection_value )
		extravalue += self.getExchangeTwoPropertyValue(40013)	#把兑换值加在成长值中
		self.curecorrection_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40013] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.curecorrection != int( result ):
			self.curecorrection = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.becuredcorrection_base )
		extravalue = self.getExtraResultPropertyValue( self.becuredcorrection_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.becuredcorrection_percent )
		vvalue = self.getValueResultPropertyValue( self.becuredcorrection_value )
		extravalue += self.getExchangeTwoPropertyValue(40014)	#把兑换值加在成长值中
		self.becuredcorrection_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40014] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.becuredcorrection != int( result ):
			self.becuredcorrection = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.parryRatio_base )
		extravalue = self.getExtraResultPropertyValue( self.parryRatio_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.parryRatio_percent )
		vvalue = self.getValueResultPropertyValue( self.parryRatio_value )
		extravalue += self.getExchangeTwoPropertyValue(30026)	#把兑换值加在成长值中
		self.parryRatio_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30026] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.parryRatio != int( result ):
			self.parryRatio = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.critRatio_base )
		extravalue = self.getExtraResultPropertyValue( self.critRatio_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.critRatio_percent )
		vvalue = self.getValueResultPropertyValue( self.critRatio_value )
		extravalue += self.getExchangeTwoPropertyValue(30025)	#把兑换值加在成长值中
		self.critRatio_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30025] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.critRatio != int( result ):
			self.critRatio = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.ice_damage_base )
		extravalue = self.getExtraResultPropertyValue( self.ice_damage_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.ice_damage_percent )
		vvalue = self.getValueResultPropertyValue( self.ice_damage_value )
		extravalue += self.getExchangeTwoPropertyValue(30027)	#把兑换值加在成长值中
		self.ice_damage_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30027] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.ice_damage != int( result ):
			self.ice_damage = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.fire_damage_base )
		extravalue = self.getExtraResultPropertyValue( self.fire_damage_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.fire_damage_percent )
		vvalue = self.getValueResultPropertyValue( self.fire_damage_value )
		extravalue += self.getExchangeTwoPropertyValue(30028)	#把兑换值加在成长值中
		self.fire_damage_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30028] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.fire_damage != int( result ):
			self.fire_damage = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.thunder_damage_base )
		extravalue = self.getExtraResultPropertyValue( self.thunder_damage_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.thunder_damage_percent )
		vvalue = self.getValueResultPropertyValue( self.thunder_damage_value )
		extravalue += self.getExchangeTwoPropertyValue(30029)	#把兑换值加在成长值中
		self.thunder_damage_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30029] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.thunder_damage != int( result ):
			self.thunder_damage = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.xuan_damage_base )
		extravalue = self.getExtraResultPropertyValue( self.xuan_damage_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.xuan_damage_percent )
		vvalue = self.getValueResultPropertyValue( self.xuan_damage_value )
		extravalue += self.getExchangeTwoPropertyValue(30030)	#把兑换值加在成长值中
		self.xuan_damage_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30030] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.xuan_damage != int( result ):
			self.xuan_damage = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.ice_armor_base )
		extravalue = self.getExtraResultPropertyValue( self.ice_armor_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.ice_armor_percent )
		vvalue = self.getValueResultPropertyValue( self.ice_armor_value )
		extravalue += self.getExchangeTwoPropertyValue(30031)	#把兑换值加在成长值中
		self.ice_armor_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30031] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.ice_armor != int( result ):
			self.ice_armor = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.fire_armor_base )
		extravalue = self.getExtraResultPropertyValue( self.fire_armor_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.fire_armor_percent )
		vvalue = self.getValueResultPropertyValue( self.fire_armor_value )
		extravalue += self.getExchangeTwoPropertyValue(30032)	#把兑换值加在成长值中
		self.fire_armor_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30032] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.fire_armor != int( result ):
			self.fire_armor = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.thunder_armor_base )
		extravalue = self.getExtraResultPropertyValue( self.thunder_armor_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.thunder_armor_percent )
		vvalue = self.getValueResultPropertyValue( self.thunder_armor_value )
		extravalue += self.getExchangeTwoPropertyValue(30033)	#把兑换值加在成长值中
		self.thunder_armor_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30033] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.thunder_armor != int( result ):
			self.thunder_armor = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.xuan_armor_base )
		extravalue = self.getExtraResultPropertyValue( self.xuan_armor_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.xuan_armor_percent )
		vvalue = self.getValueResultPropertyValue( self.xuan_armor_value )
		extravalue += self.getExchangeTwoPropertyValue(30034)	#把兑换值加在成长值中
		self.xuan_armor_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30034] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.xuan_armor != int( result ):
			self.xuan_armor = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.ice_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.ice_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.ice_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.ice_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40015)	#把兑换值加在成长值中
		self.ice_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40015] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.ice_damage_correction != int( result ):
			self.ice_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.fire_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.fire_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.fire_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.fire_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40016)	#把兑换值加在成长值中
		self.fire_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40016] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.fire_damage_correction != int( result ):
			self.fire_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.thunder_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.thunder_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.thunder_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.thunder_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40017)	#把兑换值加在成长值中
		self.thunder_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40017] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.thunder_damage_correction != int( result ):
			self.thunder_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.xuan_damage_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.xuan_damage_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.xuan_damage_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.xuan_damage_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40018)	#把兑换值加在成长值中
		self.xuan_damage_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40018] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.xuan_damage_correction != int( result ):
			self.xuan_damage_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.ice_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.ice_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.ice_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.ice_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40019)	#把兑换值加在成长值中
		self.ice_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40019] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.ice_armor_correction != int( result ):
			self.ice_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.fire_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.fire_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.fire_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.fire_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40020)	#把兑换值加在成长值中
		self.fire_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40020] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.fire_armor_correction != int( result ):
			self.fire_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.thunder_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.thunder_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.thunder_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.thunder_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40021)	#把兑换值加在成长值中
		self.thunder_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40021] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.thunder_armor_correction != int( result ):
			self.thunder_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.xuan_armor_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.xuan_armor_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.xuan_armor_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.xuan_armor_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40022)	#把兑换值加在成长值中
		self.xuan_armor_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40022] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.xuan_armor_correction != int( result ):
			self.xuan_armor_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.hatred_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.hatred_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.hatred_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.hatred_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40023)	#把兑换值加在成长值中
		self.hatred_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40023] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.hatred_correction != int( result ):
			self.hatred_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.related_hatred_correction_base )
		extravalue = self.getExtraResultPropertyValue( self.related_hatred_correction_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.related_hatred_correction_percent )
		vvalue = self.getValueResultPropertyValue( self.related_hatred_correction_value )
		extravalue += self.getExchangeTwoPropertyValue(40024)	#把兑换值加在成长值中
		self.related_hatred_correction_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[40024] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.related_hatred_correction != int( result ):
			self.related_hatred_correction = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.damage_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.damage_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.damage_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.damage_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30035)	#把兑换值加在成长值中
		self.damage_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30035] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.damage_ignore != int( result ):
			self.damage_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.magic_damage_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.magic_damage_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.magic_damage_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.magic_damage_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30036)	#把兑换值加在成长值中
		self.magic_damage_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30036] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.magic_damage_ignore != int( result ):
			self.magic_damage_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.armor_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.armor_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.armor_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.armor_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30037)	#把兑换值加在成长值中
		self.armor_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30037] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.armor_ignore != int( result ):
			self.armor_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.magic_armor_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.magic_armor_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.magic_armor_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.magic_armor_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30038)	#把兑换值加在成长值中
		self.magic_armor_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30038] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.magic_armor_ignore != int( result ):
			self.magic_armor_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.criticalstrike_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.criticalstrike_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.criticalstrike_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.criticalstrike_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30039)	#把兑换值加在成长值中
		self.criticalstrike_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30039] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.criticalstrike_ignore != int( result ):
			self.criticalstrike_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.parry_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.parry_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.parry_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.parry_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30040)	#把兑换值加在成长值中
		self.parry_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30040] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.parry_ignore != int( result ):
			self.parry_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.hitrate_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.hitrate_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.hitrate_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.hitrate_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30041)	#把兑换值加在成长值中
		self.hitrate_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30041] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.hitrate_ignore != int( result ):
			self.hitrate_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.dodgerate_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.dodgerate_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.dodgerate_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.dodgerate_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30042)	#把兑换值加在成长值中
		self.dodgerate_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30042] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.dodgerate_ignore != int( result ):
			self.dodgerate_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.ice_damage_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.ice_damage_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.ice_damage_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.ice_damage_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30043)	#把兑换值加在成长值中
		self.ice_damage_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30043] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.ice_damage_ignore != int( result ):
			self.ice_damage_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.fire_damage_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.fire_damage_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.fire_damage_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.fire_damage_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30044)	#把兑换值加在成长值中
		self.fire_damage_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30044] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.fire_damage_ignore != int( result ):
			self.fire_damage_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.thunder_damage_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.thunder_damage_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.thunder_damage_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.thunder_damage_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30045)	#把兑换值加在成长值中
		self.thunder_damage_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30045] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.thunder_damage_ignore != int( result ):
			self.thunder_damage_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.xuan_damage_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.xuan_damage_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.xuan_damage_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.xuan_damage_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30046)	#把兑换值加在成长值中
		self.xuan_damage_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30046] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.xuan_damage_ignore != int( result ):
			self.xuan_damage_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.ice_armor_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.ice_armor_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.ice_armor_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.ice_armor_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30047)	#把兑换值加在成长值中
		self.ice_armor_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30047] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.ice_armor_ignore != int( result ):
			self.ice_armor_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.fire_armor_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.fire_armor_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.fire_armor_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.fire_armor_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30048)	#把兑换值加在成长值中
		self.fire_armor_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30048] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.fire_armor_ignore != int( result ):
			self.fire_armor_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.thunder_armor_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.thunder_armor_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.thunder_armor_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.thunder_armor_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30049)	#把兑换值加在成长值中
		self.thunder_armor_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30049] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.thunder_armor_ignore != int( result ):
			self.thunder_armor_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.xuan_armor_ignore_base )
		extravalue = self.getExtraResultPropertyValue( self.xuan_armor_ignore_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.xuan_armor_ignore_percent )
		vvalue = self.getValueResultPropertyValue( self.xuan_armor_ignore_value )
		extravalue += self.getExchangeTwoPropertyValue(30050)	#把兑换值加在成长值中
		self.xuan_armor_ignore_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30050] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.xuan_armor_ignore != int( result ):
			self.xuan_armor_ignore = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.depress_resist_base )
		extravalue = self.getExtraResultPropertyValue( self.depress_resist_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.depress_resist_percent )
		vvalue = self.getValueResultPropertyValue( self.depress_resist_value )
		extravalue += self.getExchangeTwoPropertyValue(30051)	#把兑换值加在成长值中
		self.depress_resist_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30051] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.depress_resist != int( result ):
			self.depress_resist = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.hitback_resist_base )
		extravalue = self.getExtraResultPropertyValue( self.hitback_resist_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.hitback_resist_percent )
		vvalue = self.getValueResultPropertyValue( self.hitback_resist_value )
		extravalue += self.getExchangeTwoPropertyValue(30052)	#把兑换值加在成长值中
		self.hitback_resist_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30052] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.hitback_resist != int( result ):
			self.hitback_resist = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.control_resist_base )
		extravalue = self.getExtraResultPropertyValue( self.control_resist_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.control_resist_percent )
		vvalue = self.getValueResultPropertyValue( self.control_resist_value )
		extravalue += self.getExchangeTwoPropertyValue(30053)	#把兑换值加在成长值中
		self.control_resist_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30053] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.control_resist != int( result ):
			self.control_resist = int( result )

		basevalue =  self.getBaseResultPropertyValue( self.insane_resist_base )
		extravalue = self.getExtraResultPropertyValue( self.insane_resist_extra )
		precentvalue = self.getPrecentResultPropertyValue( self.insane_resist_percent )
		vvalue = self.getValueResultPropertyValue( self.insane_resist_value )
		extravalue += self.getExchangeTwoPropertyValue(30054)	#把兑换值加在成长值中
		self.insane_resist_extra = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if ItemTypeEnum.PROPERTYIDTOSTR[30054] in List:
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		if self.insane_resist != int( result ):
			self.insane_resist = int( result )


	def getExchangeTwoProperty(self, propertyID):
		result = 0
		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30001).get(propertyID, 0)
		result += (self.corporeity * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30002).get(propertyID, 0)
		result += (self.strength * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30003).get(propertyID, 0)
		result += (self.intellect * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30004).get(propertyID, 0)
		result += (self.discern * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30005).get(propertyID, 0)
		result += (self.dexterity * exchangeratio)


		return result


	def getRoleExchangeTwoProperty(self, propertyID):
		result = 0
		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30001).get(propertyID, 0)
		exchangeratio += ItemSystemExp.g_SkillPostureExchangeCfg.getData(self.skillPosture, 30001).get(propertyID, 0)
		result += (self.corporeity * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30002).get(propertyID, 0)
		exchangeratio += ItemSystemExp.g_SkillPostureExchangeCfg.getData(self.skillPosture, 30002).get(propertyID, 0)
		result += (self.strength * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30003).get(propertyID, 0)
		exchangeratio += ItemSystemExp.g_SkillPostureExchangeCfg.getData(self.skillPosture, 30003).get(propertyID, 0)
		result += (self.intellect * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30004).get(propertyID, 0)
		exchangeratio += ItemSystemExp.g_SkillPostureExchangeCfg.getData(self.skillPosture, 30004).get(propertyID, 0)
		result += (self.discern * exchangeratio)

		exchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, 30005).get(propertyID, 0)
		exchangeratio += ItemSystemExp.g_SkillPostureExchangeCfg.getData(self.skillPosture, 30005).get(propertyID, 0)
		result += (self.dexterity * exchangeratio)


		return result


	def getRolePropertyFactor(self):
		M1 = 0.0
		M1 += self.corporeity * 119.04
		M1 += self.strength * 113.4
		M1 += self.intellect * 88.38
		M1 += self.discern * 62.58
		M1 += self.dexterity * 62.58
		M1 += self.HP_Max * 15.83
		M1 += self.MP_Max * 5.28
		M1 += self.damage * 34.72
		M1 += self.magic_damage * 32.21
		M1 += self.armor * 104.66
		M1 += self.magic_armor * 103.82
		M1 += self.criticalstrike * 39.27
		M1 += self.parry * 63.5

		return M1

	def getProfessionCorrectoin(self):
		M1= 0.0
		M1 += self.corporeity * 136.676
		M1 += self.strength * 103.0808
		M1 += self.intellect * 50.5575
		M1 += self.discern * 58.905
		M1 += self.dexterity * 12.7
		M2= 0.0
		M2 += self.corporeity * 120.846
		M2 += self.strength * 113.1496
		M2 += self.intellect * 68.273
		M2 += self.discern * 58.905
		M2 += self.dexterity * 12.7
		M3= 0.0
		M3 += self.corporeity * 120.846
		M3 += self.strength * 115.58
		M3 += self.intellect * 70.5277
		M3 += self.discern * 58.905
		M3 += self.dexterity * 12.7
		M4= 0.0
		M4 += self.corporeity * 105.016
		M4 += self.strength * 89.54
		M4 += self.intellect * 74.715
		M4 += self.discern * 58.905
		M4 += self.dexterity * 12.7
		return {
			1 : M1,
			2 : M2,
			3 : M3,
			4 : M4,
			}


	def getVehiclePetPropertyFactor(self, correct):
		M1 = 0.0
		abilityList = ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']
		ability = 1
		if 'corporeity' in abilityList:
			ability = correct
		M1 += self.corporeity * 119.04 * ability

		ability = 1
		if 'strength' in abilityList:
			ability = correct
		M1 += self.strength * 113.4 * ability

		ability = 1
		if 'intellect' in abilityList:
			ability = correct
		M1 += self.intellect * 88.38 * ability

		ability = 1
		if 'discern' in abilityList:
			ability = correct
		M1 += self.discern * 62.58 * ability

		ability = 1
		if 'dexterity' in abilityList:
			ability = correct
		M1 += self.dexterity * 62.58 * ability

		ability = 1
		if 'HP_Max' in abilityList:
			ability = correct
		M1 += self.HP_Max * 15.83 * ability

		ability = 1
		if 'MP_Max' in abilityList:
			ability = correct
		M1 += self.MP_Max * 5.28 * ability

		ability = 1
		if 'damage' in abilityList:
			ability = correct
		M1 += self.damage * 34.72 * ability

		ability = 1
		if 'magic_damage' in abilityList:
			ability = correct
		M1 += self.magic_damage * 32.21 * ability

		ability = 1
		if 'armor' in abilityList:
			ability = correct
		M1 += self.armor * 104.66 * ability

		ability = 1
		if 'magic_armor' in abilityList:
			ability = correct
		M1 += self.magic_armor * 103.82 * ability

		ability = 1
		if 'criticalstrike' in abilityList:
			ability = correct
		M1 += self.criticalstrike * 39.27 * ability

		ability = 1
		if 'parry' in abilityList:
			ability = correct
		M1 += self.parry * 63.5 * ability

		return M1

	def setPetBaseLVOneProperties(self, propertiesDict):
		basevalue =  propertiesDict[ "corporeity_base" ]
		extravalue = propertiesDict[ "corporeity_extra" ]
		precentvalue = propertiesDict[ "corporeity_percent" ]
		vvalue = propertiesDict[ "corporeity_value" ]
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict.update( { "corporeity" : result } )
		if "corporeity" in ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']:
			self.corporeity = result

		basevalue =  propertiesDict[ "strength_base" ]
		extravalue = propertiesDict[ "strength_extra" ]
		precentvalue = propertiesDict[ "strength_percent" ]
		vvalue = propertiesDict[ "strength_value" ]
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict.update( { "strength" : result } )
		if "strength" in ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']:
			self.strength = result

		basevalue =  propertiesDict[ "intellect_base" ]
		extravalue = propertiesDict[ "intellect_extra" ]
		precentvalue = propertiesDict[ "intellect_percent" ]
		vvalue = propertiesDict[ "intellect_value" ]
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict.update( { "intellect" : result } )
		if "intellect" in ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']:
			self.intellect = result

		basevalue =  propertiesDict[ "discern_base" ]
		extravalue = propertiesDict[ "discern_extra" ]
		precentvalue = propertiesDict[ "discern_percent" ]
		vvalue = propertiesDict[ "discern_value" ]
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict.update( { "discern" : result } )
		if "discern" in ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']:
			self.discern = result

		basevalue =  propertiesDict[ "dexterity_base" ]
		extravalue = propertiesDict[ "dexterity_extra" ]
		precentvalue = propertiesDict[ "dexterity_percent" ]
		vvalue = propertiesDict[ "dexterity_value" ]
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict.update( { "dexterity" : result } )
		if "dexterity" in ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']:
			self.dexterity = result

		return propertiesDict

	def setPetBaseLVTwoProperties(self, propertiesDict):
		basevalue =  propertiesDict[ "HP_Max_base" ]
		extravalue = propertiesDict[ "HP_Max_extra" ]
		precentvalue = propertiesDict[ "HP_Max_percent" ]
		vvalue = propertiesDict[ "HP_Max_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30006) #把兑换值加在成长值中
		propertiesDict[ "HP_Max_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "HP_Max" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["HP_Max"] = result
		if "HP_Max" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.HP_Max = result

		basevalue =  propertiesDict[ "MP_Max_base" ]
		extravalue = propertiesDict[ "MP_Max_extra" ]
		precentvalue = propertiesDict[ "MP_Max_percent" ]
		vvalue = propertiesDict[ "MP_Max_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30007) #把兑换值加在成长值中
		propertiesDict[ "MP_Max_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "MP_Max" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["MP_Max"] = result
		if "MP_Max" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.MP_Max = result

		basevalue =  propertiesDict[ "damage_base" ]
		extravalue = propertiesDict[ "damage_extra" ]
		precentvalue = propertiesDict[ "damage_percent" ]
		vvalue = propertiesDict[ "damage_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30008) #把兑换值加在成长值中
		propertiesDict[ "damage_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "damage" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["damage"] = result
		if "damage" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.damage = result

		basevalue =  propertiesDict[ "magic_damage_base" ]
		extravalue = propertiesDict[ "magic_damage_extra" ]
		precentvalue = propertiesDict[ "magic_damage_percent" ]
		vvalue = propertiesDict[ "magic_damage_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30009) #把兑换值加在成长值中
		propertiesDict[ "magic_damage_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "magic_damage" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["magic_damage"] = result
		if "magic_damage" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.magic_damage = result

		basevalue =  propertiesDict[ "armor_base" ]
		extravalue = propertiesDict[ "armor_extra" ]
		precentvalue = propertiesDict[ "armor_percent" ]
		vvalue = propertiesDict[ "armor_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30010) #把兑换值加在成长值中
		propertiesDict[ "armor_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "armor" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["armor"] = result
		if "armor" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.armor = result

		basevalue =  propertiesDict[ "magic_armor_base" ]
		extravalue = propertiesDict[ "magic_armor_extra" ]
		precentvalue = propertiesDict[ "magic_armor_percent" ]
		vvalue = propertiesDict[ "magic_armor_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30011) #把兑换值加在成长值中
		propertiesDict[ "magic_armor_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "magic_armor" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["magic_armor"] = result
		if "magic_armor" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.magic_armor = result

		basevalue =  propertiesDict[ "criticalstrike_base" ]
		extravalue = propertiesDict[ "criticalstrike_extra" ]
		precentvalue = propertiesDict[ "criticalstrike_percent" ]
		vvalue = propertiesDict[ "criticalstrike_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30012) #把兑换值加在成长值中
		propertiesDict[ "criticalstrike_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "criticalstrike" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["criticalstrike"] = result
		if "criticalstrike" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.criticalstrike = result

		basevalue =  propertiesDict[ "parry_base" ]
		extravalue = propertiesDict[ "parry_extra" ]
		precentvalue = propertiesDict[ "parry_percent" ]
		vvalue = propertiesDict[ "parry_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30013) #把兑换值加在成长值中
		propertiesDict[ "parry_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "parry" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["parry"] = result
		if "parry" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.parry = result

		basevalue =  propertiesDict[ "speed_base" ]
		extravalue = propertiesDict[ "speed_extra" ]
		precentvalue = propertiesDict[ "speed_percent" ]
		vvalue = propertiesDict[ "speed_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30014) #把兑换值加在成长值中
		propertiesDict[ "speed_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "speed" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["speed"] = result
		if "speed" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.speed = result

		basevalue =  propertiesDict[ "hitrate_base" ]
		extravalue = propertiesDict[ "hitrate_extra" ]
		precentvalue = propertiesDict[ "hitrate_percent" ]
		vvalue = propertiesDict[ "hitrate_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30015) #把兑换值加在成长值中
		propertiesDict[ "hitrate_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "hitrate" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["hitrate"] = result
		if "hitrate" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.hitrate = result

		basevalue =  propertiesDict[ "dodgerate_base" ]
		extravalue = propertiesDict[ "dodgerate_extra" ]
		precentvalue = propertiesDict[ "dodgerate_percent" ]
		vvalue = propertiesDict[ "dodgerate_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30016) #把兑换值加在成长值中
		propertiesDict[ "dodgerate_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "dodgerate" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["dodgerate"] = result
		if "dodgerate" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.dodgerate = result

		basevalue =  propertiesDict[ "healingrate_base" ]
		extravalue = propertiesDict[ "healingrate_extra" ]
		precentvalue = propertiesDict[ "healingrate_percent" ]
		vvalue = propertiesDict[ "healingrate_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30017) #把兑换值加在成长值中
		propertiesDict[ "healingrate_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "healingrate" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["healingrate"] = result
		if "healingrate" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.healingrate = result

		basevalue =  propertiesDict[ "gangQiValue_Max_base" ]
		extravalue = propertiesDict[ "gangQiValue_Max_extra" ]
		precentvalue = propertiesDict[ "gangQiValue_Max_percent" ]
		vvalue = propertiesDict[ "gangQiValue_Max_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30018) #把兑换值加在成长值中
		propertiesDict[ "gangQiValue_Max_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "gangQiValue_Max" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["gangQiValue_Max"] = result
		if "gangQiValue_Max" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.gangQiValue_Max = result

		basevalue =  propertiesDict[ "gangQi_damagePoint_base" ]
		extravalue = propertiesDict[ "gangQi_damagePoint_extra" ]
		precentvalue = propertiesDict[ "gangQi_damagePoint_percent" ]
		vvalue = propertiesDict[ "gangQi_damagePoint_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30019) #把兑换值加在成长值中
		propertiesDict[ "gangQi_damagePoint_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "gangQi_damagePoint" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["gangQi_damagePoint"] = result
		if "gangQi_damagePoint" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.gangQi_damagePoint = result

		basevalue =  propertiesDict[ "gangQi_armorPoint_base" ]
		extravalue = propertiesDict[ "gangQi_armorPoint_extra" ]
		precentvalue = propertiesDict[ "gangQi_armorPoint_percent" ]
		vvalue = propertiesDict[ "gangQi_armorPoint_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30020) #把兑换值加在成长值中
		propertiesDict[ "gangQi_armorPoint_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "gangQi_armorPoint" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["gangQi_armorPoint"] = result
		if "gangQi_armorPoint" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.gangQi_armorPoint = result

		basevalue =  propertiesDict[ "gangQi_qiJieRevive_base" ]
		extravalue = propertiesDict[ "gangQi_qiJieRevive_extra" ]
		precentvalue = propertiesDict[ "gangQi_qiJieRevive_percent" ]
		vvalue = propertiesDict[ "gangQi_qiJieRevive_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30021) #把兑换值加在成长值中
		propertiesDict[ "gangQi_qiJieRevive_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "gangQi_qiJieRevive" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["gangQi_qiJieRevive"] = result
		if "gangQi_qiJieRevive" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.gangQi_qiJieRevive = result

		basevalue =  propertiesDict[ "gangQi_qiYingRevive_base" ]
		extravalue = propertiesDict[ "gangQi_qiYingRevive_extra" ]
		precentvalue = propertiesDict[ "gangQi_qiYingRevive_percent" ]
		vvalue = propertiesDict[ "gangQi_qiYingRevive_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30022) #把兑换值加在成长值中
		propertiesDict[ "gangQi_qiYingRevive_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "gangQi_qiYingRevive" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["gangQi_qiYingRevive"] = result
		if "gangQi_qiYingRevive" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.gangQi_qiYingRevive = result

		basevalue =  propertiesDict[ "damage_correction_base" ]
		extravalue = propertiesDict[ "damage_correction_extra" ]
		precentvalue = propertiesDict[ "damage_correction_percent" ]
		vvalue = propertiesDict[ "damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40001) #把兑换值加在成长值中
		propertiesDict[ "damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["damage_correction"] = result
		if "damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.damage_correction = result

		basevalue =  propertiesDict[ "armor_correction_base" ]
		extravalue = propertiesDict[ "armor_correction_extra" ]
		precentvalue = propertiesDict[ "armor_correction_percent" ]
		vvalue = propertiesDict[ "armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40002) #把兑换值加在成长值中
		propertiesDict[ "armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["armor_correction"] = result
		if "armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.armor_correction = result

		basevalue =  propertiesDict[ "attack_damage_correction_base" ]
		extravalue = propertiesDict[ "attack_damage_correction_extra" ]
		precentvalue = propertiesDict[ "attack_damage_correction_percent" ]
		vvalue = propertiesDict[ "attack_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40003) #把兑换值加在成长值中
		propertiesDict[ "attack_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "attack_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["attack_damage_correction"] = result
		if "attack_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.attack_damage_correction = result

		basevalue =  propertiesDict[ "magic_damage_correction_base" ]
		extravalue = propertiesDict[ "magic_damage_correction_extra" ]
		precentvalue = propertiesDict[ "magic_damage_correction_percent" ]
		vvalue = propertiesDict[ "magic_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40004) #把兑换值加在成长值中
		propertiesDict[ "magic_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "magic_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["magic_damage_correction"] = result
		if "magic_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.magic_damage_correction = result

		basevalue =  propertiesDict[ "attack_armor_correction_base" ]
		extravalue = propertiesDict[ "attack_armor_correction_extra" ]
		precentvalue = propertiesDict[ "attack_armor_correction_percent" ]
		vvalue = propertiesDict[ "attack_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40005) #把兑换值加在成长值中
		propertiesDict[ "attack_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "attack_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["attack_armor_correction"] = result
		if "attack_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.attack_armor_correction = result

		basevalue =  propertiesDict[ "magic_armor_correction_base" ]
		extravalue = propertiesDict[ "magic_armor_correction_extra" ]
		precentvalue = propertiesDict[ "magic_armor_correction_percent" ]
		vvalue = propertiesDict[ "magic_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40006) #把兑换值加在成长值中
		propertiesDict[ "magic_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "magic_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["magic_armor_correction"] = result
		if "magic_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.magic_armor_correction = result

		basevalue =  propertiesDict[ "role_damage_correction_base" ]
		extravalue = propertiesDict[ "role_damage_correction_extra" ]
		precentvalue = propertiesDict[ "role_damage_correction_percent" ]
		vvalue = propertiesDict[ "role_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40007) #把兑换值加在成长值中
		propertiesDict[ "role_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "role_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["role_damage_correction"] = result
		if "role_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.role_damage_correction = result

		basevalue =  propertiesDict[ "pet_damage_correction_base" ]
		extravalue = propertiesDict[ "pet_damage_correction_extra" ]
		precentvalue = propertiesDict[ "pet_damage_correction_percent" ]
		vvalue = propertiesDict[ "pet_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40008) #把兑换值加在成长值中
		propertiesDict[ "pet_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "pet_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["pet_damage_correction"] = result
		if "pet_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.pet_damage_correction = result

		basevalue =  propertiesDict[ "monster_damage_correction_base" ]
		extravalue = propertiesDict[ "monster_damage_correction_extra" ]
		precentvalue = propertiesDict[ "monster_damage_correction_percent" ]
		vvalue = propertiesDict[ "monster_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40009) #把兑换值加在成长值中
		propertiesDict[ "monster_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "monster_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["monster_damage_correction"] = result
		if "monster_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.monster_damage_correction = result

		basevalue =  propertiesDict[ "role_armor_correction_base" ]
		extravalue = propertiesDict[ "role_armor_correction_extra" ]
		precentvalue = propertiesDict[ "role_armor_correction_percent" ]
		vvalue = propertiesDict[ "role_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40010) #把兑换值加在成长值中
		propertiesDict[ "role_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "role_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["role_armor_correction"] = result
		if "role_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.role_armor_correction = result

		basevalue =  propertiesDict[ "pet_armor_correction_base" ]
		extravalue = propertiesDict[ "pet_armor_correction_extra" ]
		precentvalue = propertiesDict[ "pet_armor_correction_percent" ]
		vvalue = propertiesDict[ "pet_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40011) #把兑换值加在成长值中
		propertiesDict[ "pet_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "pet_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["pet_armor_correction"] = result
		if "pet_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.pet_armor_correction = result

		basevalue =  propertiesDict[ "monster_armor_correction_base" ]
		extravalue = propertiesDict[ "monster_armor_correction_extra" ]
		precentvalue = propertiesDict[ "monster_armor_correction_percent" ]
		vvalue = propertiesDict[ "monster_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40012) #把兑换值加在成长值中
		propertiesDict[ "monster_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "monster_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["monster_armor_correction"] = result
		if "monster_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.monster_armor_correction = result

		basevalue =  propertiesDict[ "cure_base" ]
		extravalue = propertiesDict[ "cure_extra" ]
		precentvalue = propertiesDict[ "cure_percent" ]
		vvalue = propertiesDict[ "cure_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30024) #把兑换值加在成长值中
		propertiesDict[ "cure_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "cure" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["cure"] = result
		if "cure" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.cure = result

		basevalue =  propertiesDict[ "curecorrection_base" ]
		extravalue = propertiesDict[ "curecorrection_extra" ]
		precentvalue = propertiesDict[ "curecorrection_percent" ]
		vvalue = propertiesDict[ "curecorrection_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40013) #把兑换值加在成长值中
		propertiesDict[ "curecorrection_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "curecorrection" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["curecorrection"] = result
		if "curecorrection" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.curecorrection = result

		basevalue =  propertiesDict[ "becuredcorrection_base" ]
		extravalue = propertiesDict[ "becuredcorrection_extra" ]
		precentvalue = propertiesDict[ "becuredcorrection_percent" ]
		vvalue = propertiesDict[ "becuredcorrection_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40014) #把兑换值加在成长值中
		propertiesDict[ "becuredcorrection_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "becuredcorrection" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["becuredcorrection"] = result
		if "becuredcorrection" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.becuredcorrection = result

		basevalue =  propertiesDict[ "parryRatio_base" ]
		extravalue = propertiesDict[ "parryRatio_extra" ]
		precentvalue = propertiesDict[ "parryRatio_percent" ]
		vvalue = propertiesDict[ "parryRatio_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30026) #把兑换值加在成长值中
		propertiesDict[ "parryRatio_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "parryRatio" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["parryRatio"] = result
		if "parryRatio" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.parryRatio = result

		basevalue =  propertiesDict[ "critRatio_base" ]
		extravalue = propertiesDict[ "critRatio_extra" ]
		precentvalue = propertiesDict[ "critRatio_percent" ]
		vvalue = propertiesDict[ "critRatio_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30025) #把兑换值加在成长值中
		propertiesDict[ "critRatio_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "critRatio" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["critRatio"] = result
		if "critRatio" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.critRatio = result

		basevalue =  propertiesDict[ "ice_damage_base" ]
		extravalue = propertiesDict[ "ice_damage_extra" ]
		precentvalue = propertiesDict[ "ice_damage_percent" ]
		vvalue = propertiesDict[ "ice_damage_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30027) #把兑换值加在成长值中
		propertiesDict[ "ice_damage_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "ice_damage" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["ice_damage"] = result
		if "ice_damage" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.ice_damage = result

		basevalue =  propertiesDict[ "fire_damage_base" ]
		extravalue = propertiesDict[ "fire_damage_extra" ]
		precentvalue = propertiesDict[ "fire_damage_percent" ]
		vvalue = propertiesDict[ "fire_damage_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30028) #把兑换值加在成长值中
		propertiesDict[ "fire_damage_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "fire_damage" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["fire_damage"] = result
		if "fire_damage" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.fire_damage = result

		basevalue =  propertiesDict[ "thunder_damage_base" ]
		extravalue = propertiesDict[ "thunder_damage_extra" ]
		precentvalue = propertiesDict[ "thunder_damage_percent" ]
		vvalue = propertiesDict[ "thunder_damage_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30029) #把兑换值加在成长值中
		propertiesDict[ "thunder_damage_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "thunder_damage" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["thunder_damage"] = result
		if "thunder_damage" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.thunder_damage = result

		basevalue =  propertiesDict[ "xuan_damage_base" ]
		extravalue = propertiesDict[ "xuan_damage_extra" ]
		precentvalue = propertiesDict[ "xuan_damage_percent" ]
		vvalue = propertiesDict[ "xuan_damage_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30030) #把兑换值加在成长值中
		propertiesDict[ "xuan_damage_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "xuan_damage" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["xuan_damage"] = result
		if "xuan_damage" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.xuan_damage = result

		basevalue =  propertiesDict[ "ice_armor_base" ]
		extravalue = propertiesDict[ "ice_armor_extra" ]
		precentvalue = propertiesDict[ "ice_armor_percent" ]
		vvalue = propertiesDict[ "ice_armor_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30031) #把兑换值加在成长值中
		propertiesDict[ "ice_armor_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "ice_armor" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["ice_armor"] = result
		if "ice_armor" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.ice_armor = result

		basevalue =  propertiesDict[ "fire_armor_base" ]
		extravalue = propertiesDict[ "fire_armor_extra" ]
		precentvalue = propertiesDict[ "fire_armor_percent" ]
		vvalue = propertiesDict[ "fire_armor_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30032) #把兑换值加在成长值中
		propertiesDict[ "fire_armor_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "fire_armor" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["fire_armor"] = result
		if "fire_armor" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.fire_armor = result

		basevalue =  propertiesDict[ "thunder_armor_base" ]
		extravalue = propertiesDict[ "thunder_armor_extra" ]
		precentvalue = propertiesDict[ "thunder_armor_percent" ]
		vvalue = propertiesDict[ "thunder_armor_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30033) #把兑换值加在成长值中
		propertiesDict[ "thunder_armor_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "thunder_armor" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["thunder_armor"] = result
		if "thunder_armor" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.thunder_armor = result

		basevalue =  propertiesDict[ "xuan_armor_base" ]
		extravalue = propertiesDict[ "xuan_armor_extra" ]
		precentvalue = propertiesDict[ "xuan_armor_percent" ]
		vvalue = propertiesDict[ "xuan_armor_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30034) #把兑换值加在成长值中
		propertiesDict[ "xuan_armor_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "xuan_armor" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["xuan_armor"] = result
		if "xuan_armor" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.xuan_armor = result

		basevalue =  propertiesDict[ "ice_damage_correction_base" ]
		extravalue = propertiesDict[ "ice_damage_correction_extra" ]
		precentvalue = propertiesDict[ "ice_damage_correction_percent" ]
		vvalue = propertiesDict[ "ice_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40015) #把兑换值加在成长值中
		propertiesDict[ "ice_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "ice_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["ice_damage_correction"] = result
		if "ice_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.ice_damage_correction = result

		basevalue =  propertiesDict[ "fire_damage_correction_base" ]
		extravalue = propertiesDict[ "fire_damage_correction_extra" ]
		precentvalue = propertiesDict[ "fire_damage_correction_percent" ]
		vvalue = propertiesDict[ "fire_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40016) #把兑换值加在成长值中
		propertiesDict[ "fire_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "fire_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["fire_damage_correction"] = result
		if "fire_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.fire_damage_correction = result

		basevalue =  propertiesDict[ "thunder_damage_correction_base" ]
		extravalue = propertiesDict[ "thunder_damage_correction_extra" ]
		precentvalue = propertiesDict[ "thunder_damage_correction_percent" ]
		vvalue = propertiesDict[ "thunder_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40017) #把兑换值加在成长值中
		propertiesDict[ "thunder_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "thunder_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["thunder_damage_correction"] = result
		if "thunder_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.thunder_damage_correction = result

		basevalue =  propertiesDict[ "xuan_damage_correction_base" ]
		extravalue = propertiesDict[ "xuan_damage_correction_extra" ]
		precentvalue = propertiesDict[ "xuan_damage_correction_percent" ]
		vvalue = propertiesDict[ "xuan_damage_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40018) #把兑换值加在成长值中
		propertiesDict[ "xuan_damage_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "xuan_damage_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["xuan_damage_correction"] = result
		if "xuan_damage_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.xuan_damage_correction = result

		basevalue =  propertiesDict[ "ice_armor_correction_base" ]
		extravalue = propertiesDict[ "ice_armor_correction_extra" ]
		precentvalue = propertiesDict[ "ice_armor_correction_percent" ]
		vvalue = propertiesDict[ "ice_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40019) #把兑换值加在成长值中
		propertiesDict[ "ice_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "ice_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["ice_armor_correction"] = result
		if "ice_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.ice_armor_correction = result

		basevalue =  propertiesDict[ "fire_armor_correction_base" ]
		extravalue = propertiesDict[ "fire_armor_correction_extra" ]
		precentvalue = propertiesDict[ "fire_armor_correction_percent" ]
		vvalue = propertiesDict[ "fire_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40020) #把兑换值加在成长值中
		propertiesDict[ "fire_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "fire_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["fire_armor_correction"] = result
		if "fire_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.fire_armor_correction = result

		basevalue =  propertiesDict[ "thunder_armor_correction_base" ]
		extravalue = propertiesDict[ "thunder_armor_correction_extra" ]
		precentvalue = propertiesDict[ "thunder_armor_correction_percent" ]
		vvalue = propertiesDict[ "thunder_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40021) #把兑换值加在成长值中
		propertiesDict[ "thunder_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "thunder_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["thunder_armor_correction"] = result
		if "thunder_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.thunder_armor_correction = result

		basevalue =  propertiesDict[ "xuan_armor_correction_base" ]
		extravalue = propertiesDict[ "xuan_armor_correction_extra" ]
		precentvalue = propertiesDict[ "xuan_armor_correction_percent" ]
		vvalue = propertiesDict[ "xuan_armor_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40022) #把兑换值加在成长值中
		propertiesDict[ "xuan_armor_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "xuan_armor_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["xuan_armor_correction"] = result
		if "xuan_armor_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.xuan_armor_correction = result

		basevalue =  propertiesDict[ "hatred_correction_base" ]
		extravalue = propertiesDict[ "hatred_correction_extra" ]
		precentvalue = propertiesDict[ "hatred_correction_percent" ]
		vvalue = propertiesDict[ "hatred_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40023) #把兑换值加在成长值中
		propertiesDict[ "hatred_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "hatred_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["hatred_correction"] = result
		if "hatred_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.hatred_correction = result

		basevalue =  propertiesDict[ "related_hatred_correction_base" ]
		extravalue = propertiesDict[ "related_hatred_correction_extra" ]
		precentvalue = propertiesDict[ "related_hatred_correction_percent" ]
		vvalue = propertiesDict[ "related_hatred_correction_value" ]
		extravalue += self.getExchangeTwoPropertyValue(40024) #把兑换值加在成长值中
		propertiesDict[ "related_hatred_correction_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "related_hatred_correction" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["related_hatred_correction"] = result
		if "related_hatred_correction" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.related_hatred_correction = result

		basevalue =  propertiesDict[ "damage_ignore_base" ]
		extravalue = propertiesDict[ "damage_ignore_extra" ]
		precentvalue = propertiesDict[ "damage_ignore_percent" ]
		vvalue = propertiesDict[ "damage_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30035) #把兑换值加在成长值中
		propertiesDict[ "damage_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "damage_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["damage_ignore"] = result
		if "damage_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.damage_ignore = result

		basevalue =  propertiesDict[ "magic_damage_ignore_base" ]
		extravalue = propertiesDict[ "magic_damage_ignore_extra" ]
		precentvalue = propertiesDict[ "magic_damage_ignore_percent" ]
		vvalue = propertiesDict[ "magic_damage_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30036) #把兑换值加在成长值中
		propertiesDict[ "magic_damage_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "magic_damage_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["magic_damage_ignore"] = result
		if "magic_damage_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.magic_damage_ignore = result

		basevalue =  propertiesDict[ "armor_ignore_base" ]
		extravalue = propertiesDict[ "armor_ignore_extra" ]
		precentvalue = propertiesDict[ "armor_ignore_percent" ]
		vvalue = propertiesDict[ "armor_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30037) #把兑换值加在成长值中
		propertiesDict[ "armor_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "armor_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["armor_ignore"] = result
		if "armor_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.armor_ignore = result

		basevalue =  propertiesDict[ "magic_armor_ignore_base" ]
		extravalue = propertiesDict[ "magic_armor_ignore_extra" ]
		precentvalue = propertiesDict[ "magic_armor_ignore_percent" ]
		vvalue = propertiesDict[ "magic_armor_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30038) #把兑换值加在成长值中
		propertiesDict[ "magic_armor_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "magic_armor_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["magic_armor_ignore"] = result
		if "magic_armor_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.magic_armor_ignore = result

		basevalue =  propertiesDict[ "criticalstrike_ignore_base" ]
		extravalue = propertiesDict[ "criticalstrike_ignore_extra" ]
		precentvalue = propertiesDict[ "criticalstrike_ignore_percent" ]
		vvalue = propertiesDict[ "criticalstrike_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30039) #把兑换值加在成长值中
		propertiesDict[ "criticalstrike_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "criticalstrike_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["criticalstrike_ignore"] = result
		if "criticalstrike_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.criticalstrike_ignore = result

		basevalue =  propertiesDict[ "parry_ignore_base" ]
		extravalue = propertiesDict[ "parry_ignore_extra" ]
		precentvalue = propertiesDict[ "parry_ignore_percent" ]
		vvalue = propertiesDict[ "parry_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30040) #把兑换值加在成长值中
		propertiesDict[ "parry_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "parry_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["parry_ignore"] = result
		if "parry_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.parry_ignore = result

		basevalue =  propertiesDict[ "hitrate_ignore_base" ]
		extravalue = propertiesDict[ "hitrate_ignore_extra" ]
		precentvalue = propertiesDict[ "hitrate_ignore_percent" ]
		vvalue = propertiesDict[ "hitrate_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30041) #把兑换值加在成长值中
		propertiesDict[ "hitrate_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "hitrate_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["hitrate_ignore"] = result
		if "hitrate_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.hitrate_ignore = result

		basevalue =  propertiesDict[ "dodgerate_ignore_base" ]
		extravalue = propertiesDict[ "dodgerate_ignore_extra" ]
		precentvalue = propertiesDict[ "dodgerate_ignore_percent" ]
		vvalue = propertiesDict[ "dodgerate_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30042) #把兑换值加在成长值中
		propertiesDict[ "dodgerate_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "dodgerate_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["dodgerate_ignore"] = result
		if "dodgerate_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.dodgerate_ignore = result

		basevalue =  propertiesDict[ "ice_damage_ignore_base" ]
		extravalue = propertiesDict[ "ice_damage_ignore_extra" ]
		precentvalue = propertiesDict[ "ice_damage_ignore_percent" ]
		vvalue = propertiesDict[ "ice_damage_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30043) #把兑换值加在成长值中
		propertiesDict[ "ice_damage_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "ice_damage_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["ice_damage_ignore"] = result
		if "ice_damage_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.ice_damage_ignore = result

		basevalue =  propertiesDict[ "fire_damage_ignore_base" ]
		extravalue = propertiesDict[ "fire_damage_ignore_extra" ]
		precentvalue = propertiesDict[ "fire_damage_ignore_percent" ]
		vvalue = propertiesDict[ "fire_damage_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30044) #把兑换值加在成长值中
		propertiesDict[ "fire_damage_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "fire_damage_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["fire_damage_ignore"] = result
		if "fire_damage_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.fire_damage_ignore = result

		basevalue =  propertiesDict[ "thunder_damage_ignore_base" ]
		extravalue = propertiesDict[ "thunder_damage_ignore_extra" ]
		precentvalue = propertiesDict[ "thunder_damage_ignore_percent" ]
		vvalue = propertiesDict[ "thunder_damage_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30045) #把兑换值加在成长值中
		propertiesDict[ "thunder_damage_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "thunder_damage_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["thunder_damage_ignore"] = result
		if "thunder_damage_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.thunder_damage_ignore = result

		basevalue =  propertiesDict[ "xuan_damage_ignore_base" ]
		extravalue = propertiesDict[ "xuan_damage_ignore_extra" ]
		precentvalue = propertiesDict[ "xuan_damage_ignore_percent" ]
		vvalue = propertiesDict[ "xuan_damage_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30046) #把兑换值加在成长值中
		propertiesDict[ "xuan_damage_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "xuan_damage_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["xuan_damage_ignore"] = result
		if "xuan_damage_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.xuan_damage_ignore = result

		basevalue =  propertiesDict[ "ice_armor_ignore_base" ]
		extravalue = propertiesDict[ "ice_armor_ignore_extra" ]
		precentvalue = propertiesDict[ "ice_armor_ignore_percent" ]
		vvalue = propertiesDict[ "ice_armor_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30047) #把兑换值加在成长值中
		propertiesDict[ "ice_armor_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "ice_armor_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["ice_armor_ignore"] = result
		if "ice_armor_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.ice_armor_ignore = result

		basevalue =  propertiesDict[ "fire_armor_ignore_base" ]
		extravalue = propertiesDict[ "fire_armor_ignore_extra" ]
		precentvalue = propertiesDict[ "fire_armor_ignore_percent" ]
		vvalue = propertiesDict[ "fire_armor_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30048) #把兑换值加在成长值中
		propertiesDict[ "fire_armor_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "fire_armor_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["fire_armor_ignore"] = result
		if "fire_armor_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.fire_armor_ignore = result

		basevalue =  propertiesDict[ "thunder_armor_ignore_base" ]
		extravalue = propertiesDict[ "thunder_armor_ignore_extra" ]
		precentvalue = propertiesDict[ "thunder_armor_ignore_percent" ]
		vvalue = propertiesDict[ "thunder_armor_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30049) #把兑换值加在成长值中
		propertiesDict[ "thunder_armor_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "thunder_armor_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["thunder_armor_ignore"] = result
		if "thunder_armor_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.thunder_armor_ignore = result

		basevalue =  propertiesDict[ "xuan_armor_ignore_base" ]
		extravalue = propertiesDict[ "xuan_armor_ignore_extra" ]
		precentvalue = propertiesDict[ "xuan_armor_ignore_percent" ]
		vvalue = propertiesDict[ "xuan_armor_ignore_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30050) #把兑换值加在成长值中
		propertiesDict[ "xuan_armor_ignore_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "xuan_armor_ignore" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["xuan_armor_ignore"] = result
		if "xuan_armor_ignore" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.xuan_armor_ignore = result

		basevalue =  propertiesDict[ "depress_resist_base" ]
		extravalue = propertiesDict[ "depress_resist_extra" ]
		precentvalue = propertiesDict[ "depress_resist_percent" ]
		vvalue = propertiesDict[ "depress_resist_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30051) #把兑换值加在成长值中
		propertiesDict[ "depress_resist_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "depress_resist" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["depress_resist"] = result
		if "depress_resist" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.depress_resist = result

		basevalue =  propertiesDict[ "hitback_resist_base" ]
		extravalue = propertiesDict[ "hitback_resist_extra" ]
		precentvalue = propertiesDict[ "hitback_resist_percent" ]
		vvalue = propertiesDict[ "hitback_resist_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30052) #把兑换值加在成长值中
		propertiesDict[ "hitback_resist_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "hitback_resist" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["hitback_resist"] = result
		if "hitback_resist" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.hitback_resist = result

		basevalue =  propertiesDict[ "control_resist_base" ]
		extravalue = propertiesDict[ "control_resist_extra" ]
		precentvalue = propertiesDict[ "control_resist_percent" ]
		vvalue = propertiesDict[ "control_resist_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30053) #把兑换值加在成长值中
		propertiesDict[ "control_resist_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "control_resist" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["control_resist"] = result
		if "control_resist" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.control_resist = result

		basevalue =  propertiesDict[ "insane_resist_base" ]
		extravalue = propertiesDict[ "insane_resist_extra" ]
		precentvalue = propertiesDict[ "insane_resist_percent" ]
		vvalue = propertiesDict[ "insane_resist_value" ]
		extravalue += self.getExchangeTwoPropertyValue(30054) #把兑换值加在成长值中
		propertiesDict[ "insane_resist_extra" ] = int(extravalue)
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)
		if "insane_resist" == "HP_Max":
			result = max(result, 1)
		result = int(self.getResultPropertyValue( result ))
		propertiesDict["insane_resist"] = result
		if "insane_resist" in ['HP_Max', 'MP_Max', 'damage', 'magic_damage', 'armor', 'magic_armor', 'criticalstrike', 'parry', 'speed', 'hitrate', 'dodgerate', 'gangQiValue_Max', 'gangQi_damagePoint', 'gangQi_armorPoint', 'combatPower', 'cure', 'ice_damage', 'fire_damage', 'thunder_damage', 'xuan_damage', 'ice_armor', 'fire_armor', 'thunder_armor', 'xuan_armor', 'damage_ignore', 'magic_damage_ignore', 'armor_ignore', 'magic_armor_ignore', 'criticalstrike_ignore', 'parry_ignore', 'hitrate_ignore', 'dodgerate_ignore', 'ice_damage_ignore', 'fire_damage_ignore', 'thunder_damage_ignore', 'xuan_damage_ignore', 'ice_armor_ignore', 'fire_armor_ignore', 'thunder_armor_ignore', 'xuan_armor_ignore', 'depress_resist', 'hitback_resist', 'control_resist', 'insane_resist']:
			self.insane_resist = result

		return propertiesDict

	def onPetStepChangeSetProperties(self):
		self.updatePetEpitomeDatas( "corporeity", self.corporeity )
		self.updatePetEpitomeDatas( "strength", self.strength )
		self.updatePetEpitomeDatas( "intellect", self.intellect )
		self.updatePetEpitomeDatas( "discern", self.discern )
		self.updatePetEpitomeDatas( "dexterity", self.dexterity )
		self.updatePetEpitomeDatas( "HP_Max", self.HP_Max )
		self.updatePetEpitomeDatas( "MP_Max", self.MP_Max )
		self.updatePetEpitomeDatas( "damage", self.damage )
		self.updatePetEpitomeDatas( "magic_damage", self.magic_damage )
		self.updatePetEpitomeDatas( "armor", self.armor )
		self.updatePetEpitomeDatas( "magic_armor", self.magic_armor )
		self.updatePetEpitomeDatas( "criticalstrike", self.criticalstrike )
		self.updatePetEpitomeDatas( "parry", self.parry )
		self.updatePetEpitomeDatas( "speed", self.speed )
		self.updatePetEpitomeDatas( "hitrate", self.hitrate )
		self.updatePetEpitomeDatas( "dodgerate", self.dodgerate )
		self.updatePetEpitomeDatas( "gangQiValue_Max", self.gangQiValue_Max )
		self.updatePetEpitomeDatas( "gangQi_damagePoint", self.gangQi_damagePoint )
		self.updatePetEpitomeDatas( "gangQi_armorPoint", self.gangQi_armorPoint )
		self.updatePetEpitomeDatas( "combatPower", self.combatPower )
		self.updatePetEpitomeDatas( "cure", self.cure )
		self.updatePetEpitomeDatas( "ice_damage", self.ice_damage )
		self.updatePetEpitomeDatas( "fire_damage", self.fire_damage )
		self.updatePetEpitomeDatas( "thunder_damage", self.thunder_damage )
		self.updatePetEpitomeDatas( "xuan_damage", self.xuan_damage )
		self.updatePetEpitomeDatas( "ice_armor", self.ice_armor )
		self.updatePetEpitomeDatas( "fire_armor", self.fire_armor )
		self.updatePetEpitomeDatas( "thunder_armor", self.thunder_armor )
		self.updatePetEpitomeDatas( "xuan_armor", self.xuan_armor )
		self.updatePetEpitomeDatas( "damage_ignore", self.damage_ignore )
		self.updatePetEpitomeDatas( "magic_damage_ignore", self.magic_damage_ignore )
		self.updatePetEpitomeDatas( "armor_ignore", self.armor_ignore )
		self.updatePetEpitomeDatas( "magic_armor_ignore", self.magic_armor_ignore )
		self.updatePetEpitomeDatas( "criticalstrike_ignore", self.criticalstrike_ignore )
		self.updatePetEpitomeDatas( "parry_ignore", self.parry_ignore )
		self.updatePetEpitomeDatas( "hitrate_ignore", self.hitrate_ignore )
		self.updatePetEpitomeDatas( "dodgerate_ignore", self.dodgerate_ignore )
		self.updatePetEpitomeDatas( "ice_damage_ignore", self.ice_damage_ignore )
		self.updatePetEpitomeDatas( "fire_damage_ignore", self.fire_damage_ignore )
		self.updatePetEpitomeDatas( "thunder_damage_ignore", self.thunder_damage_ignore )
		self.updatePetEpitomeDatas( "xuan_damage_ignore", self.xuan_damage_ignore )
		self.updatePetEpitomeDatas( "ice_armor_ignore", self.ice_armor_ignore )
		self.updatePetEpitomeDatas( "fire_armor_ignore", self.fire_armor_ignore )
		self.updatePetEpitomeDatas( "thunder_armor_ignore", self.thunder_armor_ignore )
		self.updatePetEpitomeDatas( "xuan_armor_ignore", self.xuan_armor_ignore )
		self.updatePetEpitomeDatas( "depress_resist", self.depress_resist )
		self.updatePetEpitomeDatas( "hitback_resist", self.hitback_resist )
		self.updatePetEpitomeDatas( "control_resist", self.control_resist )
		self.updatePetEpitomeDatas( "insane_resist", self.insane_resist )

	def onOriginPetStepChangeSetProperties(self, playerMB):
		self.updateOriginPetEpitomeDatas( playerMB, "corporeity", self.corporeity )
		self.updateOriginPetEpitomeDatas( playerMB, "strength", self.strength )
		self.updateOriginPetEpitomeDatas( playerMB, "intellect", self.intellect )
		self.updateOriginPetEpitomeDatas( playerMB, "discern", self.discern )
		self.updateOriginPetEpitomeDatas( playerMB, "dexterity", self.dexterity )
		self.updateOriginPetEpitomeDatas( playerMB, "HP_Max", self.HP_Max )
		self.updateOriginPetEpitomeDatas( playerMB, "MP_Max", self.MP_Max )
		self.updateOriginPetEpitomeDatas( playerMB, "damage", self.damage )
		self.updateOriginPetEpitomeDatas( playerMB, "magic_damage", self.magic_damage )
		self.updateOriginPetEpitomeDatas( playerMB, "armor", self.armor )
		self.updateOriginPetEpitomeDatas( playerMB, "magic_armor", self.magic_armor )
		self.updateOriginPetEpitomeDatas( playerMB, "criticalstrike", self.criticalstrike )
		self.updateOriginPetEpitomeDatas( playerMB, "parry", self.parry )
		self.updateOriginPetEpitomeDatas( playerMB, "speed", self.speed )
		self.updateOriginPetEpitomeDatas( playerMB, "hitrate", self.hitrate )
		self.updateOriginPetEpitomeDatas( playerMB, "dodgerate", self.dodgerate )
		self.updateOriginPetEpitomeDatas( playerMB, "gangQiValue_Max", self.gangQiValue_Max )
		self.updateOriginPetEpitomeDatas( playerMB, "gangQi_damagePoint", self.gangQi_damagePoint )
		self.updateOriginPetEpitomeDatas( playerMB, "gangQi_armorPoint", self.gangQi_armorPoint )
		self.updateOriginPetEpitomeDatas( playerMB, "combatPower", self.combatPower )
		self.updateOriginPetEpitomeDatas( playerMB, "cure", self.cure )
		self.updateOriginPetEpitomeDatas( playerMB, "ice_damage", self.ice_damage )
		self.updateOriginPetEpitomeDatas( playerMB, "fire_damage", self.fire_damage )
		self.updateOriginPetEpitomeDatas( playerMB, "thunder_damage", self.thunder_damage )
		self.updateOriginPetEpitomeDatas( playerMB, "xuan_damage", self.xuan_damage )
		self.updateOriginPetEpitomeDatas( playerMB, "ice_armor", self.ice_armor )
		self.updateOriginPetEpitomeDatas( playerMB, "fire_armor", self.fire_armor )
		self.updateOriginPetEpitomeDatas( playerMB, "thunder_armor", self.thunder_armor )
		self.updateOriginPetEpitomeDatas( playerMB, "xuan_armor", self.xuan_armor )
		self.updateOriginPetEpitomeDatas( playerMB, "damage_ignore", self.damage_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "magic_damage_ignore", self.magic_damage_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "armor_ignore", self.armor_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "magic_armor_ignore", self.magic_armor_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "criticalstrike_ignore", self.criticalstrike_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "parry_ignore", self.parry_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "hitrate_ignore", self.hitrate_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "dodgerate_ignore", self.dodgerate_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "ice_damage_ignore", self.ice_damage_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "fire_damage_ignore", self.fire_damage_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "thunder_damage_ignore", self.thunder_damage_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "xuan_damage_ignore", self.xuan_damage_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "ice_armor_ignore", self.ice_armor_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "fire_armor_ignore", self.fire_armor_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "thunder_armor_ignore", self.thunder_armor_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "xuan_armor_ignore", self.xuan_armor_ignore )
		self.updateOriginPetEpitomeDatas( playerMB, "depress_resist", self.depress_resist )
		self.updateOriginPetEpitomeDatas( playerMB, "hitback_resist", self.hitback_resist )
		self.updateOriginPetEpitomeDatas( playerMB, "control_resist", self.control_resist )
		self.updateOriginPetEpitomeDatas( playerMB, "insane_resist", self.insane_resist )

	def pickPetDataForClient(self, data):
		data["scriptID"] = self.scriptID
		data["step"] = self.step
		data["exp"] = self.exp
		data["quality"] = self.quality
		data["name"] = self.name
		data["ability"] = self.ability
		data["ability_Max"] = self.ability_Max
		data["HP"] = self.HP
		data["MP"] = self.MP
		data["sleepTime"] = self.sleepTime
		data["gangQiValue"] = self.gangQiValue
		data["corporeity"] = self.corporeity
		data["strength"] = self.strength
		data["intellect"] = self.intellect
		data["discern"] = self.discern
		data["dexterity"] = self.dexterity
		data["HP_Max"] = self.HP_Max
		data["MP_Max"] = self.MP_Max
		data["damage"] = self.damage
		data["magic_damage"] = self.magic_damage
		data["armor"] = self.armor
		data["magic_armor"] = self.magic_armor
		data["criticalstrike"] = self.criticalstrike
		data["parry"] = self.parry
		data["speed"] = self.speed
		data["hitrate"] = self.hitrate
		data["dodgerate"] = self.dodgerate
		data["gangQiValue_Max"] = self.gangQiValue_Max
		data["gangQi_damagePoint"] = self.gangQi_damagePoint
		data["gangQi_armorPoint"] = self.gangQi_armorPoint
		data["combatPower"] = self.combatPower
		data["cure"] = self.cure
		data["ice_damage"] = self.ice_damage
		data["fire_damage"] = self.fire_damage
		data["thunder_damage"] = self.thunder_damage
		data["xuan_damage"] = self.xuan_damage
		data["ice_armor"] = self.ice_armor
		data["fire_armor"] = self.fire_armor
		data["thunder_armor"] = self.thunder_armor
		data["xuan_armor"] = self.xuan_armor
		data["damage_ignore"] = self.damage_ignore
		data["magic_damage_ignore"] = self.magic_damage_ignore
		data["armor_ignore"] = self.armor_ignore
		data["magic_armor_ignore"] = self.magic_armor_ignore
		data["criticalstrike_ignore"] = self.criticalstrike_ignore
		data["parry_ignore"] = self.parry_ignore
		data["hitrate_ignore"] = self.hitrate_ignore
		data["dodgerate_ignore"] = self.dodgerate_ignore
		data["ice_damage_ignore"] = self.ice_damage_ignore
		data["fire_damage_ignore"] = self.fire_damage_ignore
		data["thunder_damage_ignore"] = self.thunder_damage_ignore
		data["xuan_damage_ignore"] = self.xuan_damage_ignore
		data["ice_armor_ignore"] = self.ice_armor_ignore
		data["fire_armor_ignore"] = self.fire_armor_ignore
		data["thunder_armor_ignore"] = self.thunder_armor_ignore
		data["xuan_armor_ignore"] = self.xuan_armor_ignore
		data["depress_resist"] = self.depress_resist
		data["hitback_resist"] = self.hitback_resist
		data["control_resist"] = self.control_resist
		data["insane_resist"] = self.insane_resist
		return data

	def pickPetDataForCell(self, pet ):
		pet.uid = self.uid
		pet.scriptID = self.scriptID
		pet.step = self.step
		pet.exp = self.exp
		pet.quality = self.quality
		pet.sleepTime = self.sleepTime
		pet.name = self.name
		return pet

def getEffectProperty(receiver):
	data={}
	data.update({"corporeity": receiver.corporeity})
	data.update({"corporeity_base": receiver.corporeity_base})
	data.update({"corporeity_extra": receiver.corporeity_extra})
	data.update({"corporeity_percent": receiver.corporeity_percent})
	data.update({"corporeity_value": receiver.corporeity_value})

	data.update({"strength": receiver.strength})
	data.update({"strength_base": receiver.strength_base})
	data.update({"strength_extra": receiver.strength_extra})
	data.update({"strength_percent": receiver.strength_percent})
	data.update({"strength_value": receiver.strength_value})

	data.update({"intellect": receiver.intellect})
	data.update({"intellect_base": receiver.intellect_base})
	data.update({"intellect_extra": receiver.intellect_extra})
	data.update({"intellect_percent": receiver.intellect_percent})
	data.update({"intellect_value": receiver.intellect_value})

	data.update({"discern": receiver.discern})
	data.update({"discern_base": receiver.discern_base})
	data.update({"discern_extra": receiver.discern_extra})
	data.update({"discern_percent": receiver.discern_percent})
	data.update({"discern_value": receiver.discern_value})

	data.update({"dexterity": receiver.dexterity})
	data.update({"dexterity_base": receiver.dexterity_base})
	data.update({"dexterity_extra": receiver.dexterity_extra})
	data.update({"dexterity_percent": receiver.dexterity_percent})
	data.update({"dexterity_value": receiver.dexterity_value})

	data.update({"HP_Max": receiver.HP_Max})
	data.update({"HP_Max_base": receiver.HP_Max_base})
	data.update({"HP_Max_extra": receiver.HP_Max_extra})
	data.update({"HP_Max_percent": receiver.HP_Max_percent})
	data.update({"HP_Max_value": receiver.HP_Max_value})

	data.update({"MP_Max": receiver.MP_Max})
	data.update({"MP_Max_base": receiver.MP_Max_base})
	data.update({"MP_Max_extra": receiver.MP_Max_extra})
	data.update({"MP_Max_percent": receiver.MP_Max_percent})
	data.update({"MP_Max_value": receiver.MP_Max_value})

	data.update({"damage": receiver.damage})
	data.update({"damage_base": receiver.damage_base})
	data.update({"damage_extra": receiver.damage_extra})
	data.update({"damage_percent": receiver.damage_percent})
	data.update({"damage_value": receiver.damage_value})

	data.update({"magic_damage": receiver.magic_damage})
	data.update({"magic_damage_base": receiver.magic_damage_base})
	data.update({"magic_damage_extra": receiver.magic_damage_extra})
	data.update({"magic_damage_percent": receiver.magic_damage_percent})
	data.update({"magic_damage_value": receiver.magic_damage_value})

	data.update({"armor": receiver.armor})
	data.update({"armor_base": receiver.armor_base})
	data.update({"armor_extra": receiver.armor_extra})
	data.update({"armor_percent": receiver.armor_percent})
	data.update({"armor_value": receiver.armor_value})

	data.update({"magic_armor": receiver.magic_armor})
	data.update({"magic_armor_base": receiver.magic_armor_base})
	data.update({"magic_armor_extra": receiver.magic_armor_extra})
	data.update({"magic_armor_percent": receiver.magic_armor_percent})
	data.update({"magic_armor_value": receiver.magic_armor_value})

	data.update({"criticalstrike": receiver.criticalstrike})
	data.update({"criticalstrike_base": receiver.criticalstrike_base})
	data.update({"criticalstrike_extra": receiver.criticalstrike_extra})
	data.update({"criticalstrike_percent": receiver.criticalstrike_percent})
	data.update({"criticalstrike_value": receiver.criticalstrike_value})

	data.update({"parry": receiver.parry})
	data.update({"parry_base": receiver.parry_base})
	data.update({"parry_extra": receiver.parry_extra})
	data.update({"parry_percent": receiver.parry_percent})
	data.update({"parry_value": receiver.parry_value})

	data.update({"speed": receiver.speed})
	data.update({"speed_base": receiver.speed_base})
	data.update({"speed_extra": receiver.speed_extra})
	data.update({"speed_percent": receiver.speed_percent})
	data.update({"speed_value": receiver.speed_value})

	data.update({"hitrate": receiver.hitrate})
	data.update({"hitrate_base": receiver.hitrate_base})
	data.update({"hitrate_extra": receiver.hitrate_extra})
	data.update({"hitrate_percent": receiver.hitrate_percent})
	data.update({"hitrate_value": receiver.hitrate_value})

	data.update({"dodgerate": receiver.dodgerate})
	data.update({"dodgerate_base": receiver.dodgerate_base})
	data.update({"dodgerate_extra": receiver.dodgerate_extra})
	data.update({"dodgerate_percent": receiver.dodgerate_percent})
	data.update({"dodgerate_value": receiver.dodgerate_value})

	data.update({"healingrate": receiver.healingrate})
	data.update({"healingrate_base": receiver.healingrate_base})
	data.update({"healingrate_extra": receiver.healingrate_extra})
	data.update({"healingrate_percent": receiver.healingrate_percent})
	data.update({"healingrate_value": receiver.healingrate_value})

	data.update({"gangQiValue_Max": receiver.gangQiValue_Max})
	data.update({"gangQiValue_Max_base": receiver.gangQiValue_Max_base})
	data.update({"gangQiValue_Max_extra": receiver.gangQiValue_Max_extra})
	data.update({"gangQiValue_Max_percent": receiver.gangQiValue_Max_percent})
	data.update({"gangQiValue_Max_value": receiver.gangQiValue_Max_value})

	data.update({"gangQi_damagePoint": receiver.gangQi_damagePoint})
	data.update({"gangQi_damagePoint_base": receiver.gangQi_damagePoint_base})
	data.update({"gangQi_damagePoint_extra": receiver.gangQi_damagePoint_extra})
	data.update({"gangQi_damagePoint_percent": receiver.gangQi_damagePoint_percent})
	data.update({"gangQi_damagePoint_value": receiver.gangQi_damagePoint_value})

	data.update({"gangQi_armorPoint": receiver.gangQi_armorPoint})
	data.update({"gangQi_armorPoint_base": receiver.gangQi_armorPoint_base})
	data.update({"gangQi_armorPoint_extra": receiver.gangQi_armorPoint_extra})
	data.update({"gangQi_armorPoint_percent": receiver.gangQi_armorPoint_percent})
	data.update({"gangQi_armorPoint_value": receiver.gangQi_armorPoint_value})

	data.update({"gangQi_qiJieRevive": receiver.gangQi_qiJieRevive})
	data.update({"gangQi_qiJieRevive_base": receiver.gangQi_qiJieRevive_base})
	data.update({"gangQi_qiJieRevive_extra": receiver.gangQi_qiJieRevive_extra})
	data.update({"gangQi_qiJieRevive_percent": receiver.gangQi_qiJieRevive_percent})
	data.update({"gangQi_qiJieRevive_value": receiver.gangQi_qiJieRevive_value})

	data.update({"gangQi_qiYingRevive": receiver.gangQi_qiYingRevive})
	data.update({"gangQi_qiYingRevive_base": receiver.gangQi_qiYingRevive_base})
	data.update({"gangQi_qiYingRevive_extra": receiver.gangQi_qiYingRevive_extra})
	data.update({"gangQi_qiYingRevive_percent": receiver.gangQi_qiYingRevive_percent})
	data.update({"gangQi_qiYingRevive_value": receiver.gangQi_qiYingRevive_value})

	data.update({"tempSpeed": receiver.tempSpeed})
	data.update({"tempSpeed_base": receiver.tempSpeed_base})
	data.update({"tempSpeed_extra": receiver.tempSpeed_extra})
	data.update({"tempSpeed_percent": receiver.tempSpeed_percent})
	data.update({"tempSpeed_value": receiver.tempSpeed_value})

	data.update({"cure": receiver.cure})
	data.update({"cure_base": receiver.cure_base})
	data.update({"cure_extra": receiver.cure_extra})
	data.update({"cure_percent": receiver.cure_percent})
	data.update({"cure_value": receiver.cure_value})

	data.update({"critRatio": receiver.critRatio})
	data.update({"critRatio_base": receiver.critRatio_base})
	data.update({"critRatio_extra": receiver.critRatio_extra})
	data.update({"critRatio_percent": receiver.critRatio_percent})
	data.update({"critRatio_value": receiver.critRatio_value})

	data.update({"parryRatio": receiver.parryRatio})
	data.update({"parryRatio_base": receiver.parryRatio_base})
	data.update({"parryRatio_extra": receiver.parryRatio_extra})
	data.update({"parryRatio_percent": receiver.parryRatio_percent})
	data.update({"parryRatio_value": receiver.parryRatio_value})

	data.update({"damage_correction": receiver.damage_correction})
	data.update({"damage_correction_base": receiver.damage_correction_base})
	data.update({"damage_correction_extra": receiver.damage_correction_extra})
	data.update({"damage_correction_percent": receiver.damage_correction_percent})
	data.update({"damage_correction_value": receiver.damage_correction_value})

	data.update({"armor_correction": receiver.armor_correction})
	data.update({"armor_correction_base": receiver.armor_correction_base})
	data.update({"armor_correction_extra": receiver.armor_correction_extra})
	data.update({"armor_correction_percent": receiver.armor_correction_percent})
	data.update({"armor_correction_value": receiver.armor_correction_value})

	data.update({"attack_damage_correction": receiver.attack_damage_correction})
	data.update({"attack_damage_correction_base": receiver.attack_damage_correction_base})
	data.update({"attack_damage_correction_extra": receiver.attack_damage_correction_extra})
	data.update({"attack_damage_correction_percent": receiver.attack_damage_correction_percent})
	data.update({"attack_damage_correction_value": receiver.attack_damage_correction_value})

	data.update({"magic_damage_correction": receiver.magic_damage_correction})
	data.update({"magic_damage_correction_base": receiver.magic_damage_correction_base})
	data.update({"magic_damage_correction_extra": receiver.magic_damage_correction_extra})
	data.update({"magic_damage_correction_percent": receiver.magic_damage_correction_percent})
	data.update({"magic_damage_correction_value": receiver.magic_damage_correction_value})

	data.update({"attack_armor_correction": receiver.attack_armor_correction})
	data.update({"attack_armor_correction_base": receiver.attack_armor_correction_base})
	data.update({"attack_armor_correction_extra": receiver.attack_armor_correction_extra})
	data.update({"attack_armor_correction_percent": receiver.attack_armor_correction_percent})
	data.update({"attack_armor_correction_value": receiver.attack_armor_correction_value})

	data.update({"magic_armor_correction": receiver.magic_armor_correction})
	data.update({"magic_armor_correction_base": receiver.magic_armor_correction_base})
	data.update({"magic_armor_correction_extra": receiver.magic_armor_correction_extra})
	data.update({"magic_armor_correction_percent": receiver.magic_armor_correction_percent})
	data.update({"magic_armor_correction_value": receiver.magic_armor_correction_value})

	data.update({"role_damage_correction": receiver.role_damage_correction})
	data.update({"role_damage_correction_base": receiver.role_damage_correction_base})
	data.update({"role_damage_correction_extra": receiver.role_damage_correction_extra})
	data.update({"role_damage_correction_percent": receiver.role_damage_correction_percent})
	data.update({"role_damage_correction_value": receiver.role_damage_correction_value})

	data.update({"pet_damage_correction": receiver.pet_damage_correction})
	data.update({"pet_damage_correction_base": receiver.pet_damage_correction_base})
	data.update({"pet_damage_correction_extra": receiver.pet_damage_correction_extra})
	data.update({"pet_damage_correction_percent": receiver.pet_damage_correction_percent})
	data.update({"pet_damage_correction_value": receiver.pet_damage_correction_value})

	data.update({"monster_damage_correction": receiver.monster_damage_correction})
	data.update({"monster_damage_correction_base": receiver.monster_damage_correction_base})
	data.update({"monster_damage_correction_extra": receiver.monster_damage_correction_extra})
	data.update({"monster_damage_correction_percent": receiver.monster_damage_correction_percent})
	data.update({"monster_damage_correction_value": receiver.monster_damage_correction_value})

	data.update({"role_armor_correction": receiver.role_armor_correction})
	data.update({"role_armor_correction_base": receiver.role_armor_correction_base})
	data.update({"role_armor_correction_extra": receiver.role_armor_correction_extra})
	data.update({"role_armor_correction_percent": receiver.role_armor_correction_percent})
	data.update({"role_armor_correction_value": receiver.role_armor_correction_value})

	data.update({"pet_armor_correction": receiver.pet_armor_correction})
	data.update({"pet_armor_correction_base": receiver.pet_armor_correction_base})
	data.update({"pet_armor_correction_extra": receiver.pet_armor_correction_extra})
	data.update({"pet_armor_correction_percent": receiver.pet_armor_correction_percent})
	data.update({"pet_armor_correction_value": receiver.pet_armor_correction_value})

	data.update({"monster_armor_correction": receiver.monster_armor_correction})
	data.update({"monster_armor_correction_base": receiver.monster_armor_correction_base})
	data.update({"monster_armor_correction_extra": receiver.monster_armor_correction_extra})
	data.update({"monster_armor_correction_percent": receiver.monster_armor_correction_percent})
	data.update({"monster_armor_correction_value": receiver.monster_armor_correction_value})

	data.update({"curecorrection": receiver.curecorrection})
	data.update({"curecorrection_base": receiver.curecorrection_base})
	data.update({"curecorrection_extra": receiver.curecorrection_extra})
	data.update({"curecorrection_percent": receiver.curecorrection_percent})
	data.update({"curecorrection_value": receiver.curecorrection_value})

	data.update({"becuredcorrection": receiver.becuredcorrection})
	data.update({"becuredcorrection_base": receiver.becuredcorrection_base})
	data.update({"becuredcorrection_extra": receiver.becuredcorrection_extra})
	data.update({"becuredcorrection_percent": receiver.becuredcorrection_percent})
	data.update({"becuredcorrection_value": receiver.becuredcorrection_value})

	data.update({"ice_damage": receiver.ice_damage})
	data.update({"ice_damage_base": receiver.ice_damage_base})
	data.update({"ice_damage_extra": receiver.ice_damage_extra})
	data.update({"ice_damage_percent": receiver.ice_damage_percent})
	data.update({"ice_damage_value": receiver.ice_damage_value})

	data.update({"fire_damage": receiver.fire_damage})
	data.update({"fire_damage_base": receiver.fire_damage_base})
	data.update({"fire_damage_extra": receiver.fire_damage_extra})
	data.update({"fire_damage_percent": receiver.fire_damage_percent})
	data.update({"fire_damage_value": receiver.fire_damage_value})

	data.update({"thunder_damage": receiver.thunder_damage})
	data.update({"thunder_damage_base": receiver.thunder_damage_base})
	data.update({"thunder_damage_extra": receiver.thunder_damage_extra})
	data.update({"thunder_damage_percent": receiver.thunder_damage_percent})
	data.update({"thunder_damage_value": receiver.thunder_damage_value})

	data.update({"xuan_damage": receiver.xuan_damage})
	data.update({"xuan_damage_base": receiver.xuan_damage_base})
	data.update({"xuan_damage_extra": receiver.xuan_damage_extra})
	data.update({"xuan_damage_percent": receiver.xuan_damage_percent})
	data.update({"xuan_damage_value": receiver.xuan_damage_value})

	data.update({"ice_armor": receiver.ice_armor})
	data.update({"ice_armor_base": receiver.ice_armor_base})
	data.update({"ice_armor_extra": receiver.ice_armor_extra})
	data.update({"ice_armor_percent": receiver.ice_armor_percent})
	data.update({"ice_armor_value": receiver.ice_armor_value})

	data.update({"fire_armor": receiver.fire_armor})
	data.update({"fire_armor_base": receiver.fire_armor_base})
	data.update({"fire_armor_extra": receiver.fire_armor_extra})
	data.update({"fire_armor_percent": receiver.fire_armor_percent})
	data.update({"fire_armor_value": receiver.fire_armor_value})

	data.update({"thunder_armor": receiver.thunder_armor})
	data.update({"thunder_armor_base": receiver.thunder_armor_base})
	data.update({"thunder_armor_extra": receiver.thunder_armor_extra})
	data.update({"thunder_armor_percent": receiver.thunder_armor_percent})
	data.update({"thunder_armor_value": receiver.thunder_armor_value})

	data.update({"xuan_armor": receiver.xuan_armor})
	data.update({"xuan_armor_base": receiver.xuan_armor_base})
	data.update({"xuan_armor_extra": receiver.xuan_armor_extra})
	data.update({"xuan_armor_percent": receiver.xuan_armor_percent})
	data.update({"xuan_armor_value": receiver.xuan_armor_value})

	data.update({"ice_damage_correction": receiver.ice_damage_correction})
	data.update({"ice_damage_correction_base": receiver.ice_damage_correction_base})
	data.update({"ice_damage_correction_extra": receiver.ice_damage_correction_extra})
	data.update({"ice_damage_correction_percent": receiver.ice_damage_correction_percent})
	data.update({"ice_damage_correction_value": receiver.ice_damage_correction_value})

	data.update({"fire_damage_correction": receiver.fire_damage_correction})
	data.update({"fire_damage_correction_base": receiver.fire_damage_correction_base})
	data.update({"fire_damage_correction_extra": receiver.fire_damage_correction_extra})
	data.update({"fire_damage_correction_percent": receiver.fire_damage_correction_percent})
	data.update({"fire_damage_correction_value": receiver.fire_damage_correction_value})

	data.update({"thunder_damage_correction": receiver.thunder_damage_correction})
	data.update({"thunder_damage_correction_base": receiver.thunder_damage_correction_base})
	data.update({"thunder_damage_correction_extra": receiver.thunder_damage_correction_extra})
	data.update({"thunder_damage_correction_percent": receiver.thunder_damage_correction_percent})
	data.update({"thunder_damage_correction_value": receiver.thunder_damage_correction_value})

	data.update({"xuan_damage_correction": receiver.xuan_damage_correction})
	data.update({"xuan_damage_correction_base": receiver.xuan_damage_correction_base})
	data.update({"xuan_damage_correction_extra": receiver.xuan_damage_correction_extra})
	data.update({"xuan_damage_correction_percent": receiver.xuan_damage_correction_percent})
	data.update({"xuan_damage_correction_value": receiver.xuan_damage_correction_value})

	data.update({"ice_armor_correction": receiver.ice_armor_correction})
	data.update({"ice_armor_correction_base": receiver.ice_armor_correction_base})
	data.update({"ice_armor_correction_extra": receiver.ice_armor_correction_extra})
	data.update({"ice_armor_correction_percent": receiver.ice_armor_correction_percent})
	data.update({"ice_armor_correction_value": receiver.ice_armor_correction_value})

	data.update({"fire_armor_correction": receiver.fire_armor_correction})
	data.update({"fire_armor_correction_base": receiver.fire_armor_correction_base})
	data.update({"fire_armor_correction_extra": receiver.fire_armor_correction_extra})
	data.update({"fire_armor_correction_percent": receiver.fire_armor_correction_percent})
	data.update({"fire_armor_correction_value": receiver.fire_armor_correction_value})

	data.update({"thunder_armor_correction": receiver.thunder_armor_correction})
	data.update({"thunder_armor_correction_base": receiver.thunder_armor_correction_base})
	data.update({"thunder_armor_correction_extra": receiver.thunder_armor_correction_extra})
	data.update({"thunder_armor_correction_percent": receiver.thunder_armor_correction_percent})
	data.update({"thunder_armor_correction_value": receiver.thunder_armor_correction_value})

	data.update({"xuan_armor_correction": receiver.xuan_armor_correction})
	data.update({"xuan_armor_correction_base": receiver.xuan_armor_correction_base})
	data.update({"xuan_armor_correction_extra": receiver.xuan_armor_correction_extra})
	data.update({"xuan_armor_correction_percent": receiver.xuan_armor_correction_percent})
	data.update({"xuan_armor_correction_value": receiver.xuan_armor_correction_value})

	data.update({"hatred_correction": receiver.hatred_correction})
	data.update({"hatred_correction_base": receiver.hatred_correction_base})
	data.update({"hatred_correction_extra": receiver.hatred_correction_extra})
	data.update({"hatred_correction_percent": receiver.hatred_correction_percent})
	data.update({"hatred_correction_value": receiver.hatred_correction_value})

	data.update({"related_hatred_correction": receiver.related_hatred_correction})
	data.update({"related_hatred_correction_base": receiver.related_hatred_correction_base})
	data.update({"related_hatred_correction_extra": receiver.related_hatred_correction_extra})
	data.update({"related_hatred_correction_percent": receiver.related_hatred_correction_percent})
	data.update({"related_hatred_correction_value": receiver.related_hatred_correction_value})

	data.update({"damage_ignore": receiver.damage_ignore})
	data.update({"damage_ignore_base": receiver.damage_ignore_base})
	data.update({"damage_ignore_extra": receiver.damage_ignore_extra})
	data.update({"damage_ignore_percent": receiver.damage_ignore_percent})
	data.update({"damage_ignore_value": receiver.damage_ignore_value})

	data.update({"magic_damage_ignore": receiver.magic_damage_ignore})
	data.update({"magic_damage_ignore_base": receiver.magic_damage_ignore_base})
	data.update({"magic_damage_ignore_extra": receiver.magic_damage_ignore_extra})
	data.update({"magic_damage_ignore_percent": receiver.magic_damage_ignore_percent})
	data.update({"magic_damage_ignore_value": receiver.magic_damage_ignore_value})

	data.update({"armor_ignore": receiver.armor_ignore})
	data.update({"armor_ignore_base": receiver.armor_ignore_base})
	data.update({"armor_ignore_extra": receiver.armor_ignore_extra})
	data.update({"armor_ignore_percent": receiver.armor_ignore_percent})
	data.update({"armor_ignore_value": receiver.armor_ignore_value})

	data.update({"magic_armor_ignore": receiver.magic_armor_ignore})
	data.update({"magic_armor_ignore_base": receiver.magic_armor_ignore_base})
	data.update({"magic_armor_ignore_extra": receiver.magic_armor_ignore_extra})
	data.update({"magic_armor_ignore_percent": receiver.magic_armor_ignore_percent})
	data.update({"magic_armor_ignore_value": receiver.magic_armor_ignore_value})

	data.update({"criticalstrike_ignore": receiver.criticalstrike_ignore})
	data.update({"criticalstrike_ignore_base": receiver.criticalstrike_ignore_base})
	data.update({"criticalstrike_ignore_extra": receiver.criticalstrike_ignore_extra})
	data.update({"criticalstrike_ignore_percent": receiver.criticalstrike_ignore_percent})
	data.update({"criticalstrike_ignore_value": receiver.criticalstrike_ignore_value})

	data.update({"parry_ignore": receiver.parry_ignore})
	data.update({"parry_ignore_base": receiver.parry_ignore_base})
	data.update({"parry_ignore_extra": receiver.parry_ignore_extra})
	data.update({"parry_ignore_percent": receiver.parry_ignore_percent})
	data.update({"parry_ignore_value": receiver.parry_ignore_value})

	data.update({"hitrate_ignore": receiver.hitrate_ignore})
	data.update({"hitrate_ignore_base": receiver.hitrate_ignore_base})
	data.update({"hitrate_ignore_extra": receiver.hitrate_ignore_extra})
	data.update({"hitrate_ignore_percent": receiver.hitrate_ignore_percent})
	data.update({"hitrate_ignore_value": receiver.hitrate_ignore_value})

	data.update({"dodgerate_ignore": receiver.dodgerate_ignore})
	data.update({"dodgerate_ignore_base": receiver.dodgerate_ignore_base})
	data.update({"dodgerate_ignore_extra": receiver.dodgerate_ignore_extra})
	data.update({"dodgerate_ignore_percent": receiver.dodgerate_ignore_percent})
	data.update({"dodgerate_ignore_value": receiver.dodgerate_ignore_value})

	data.update({"ice_damage_ignore": receiver.ice_damage_ignore})
	data.update({"ice_damage_ignore_base": receiver.ice_damage_ignore_base})
	data.update({"ice_damage_ignore_extra": receiver.ice_damage_ignore_extra})
	data.update({"ice_damage_ignore_percent": receiver.ice_damage_ignore_percent})
	data.update({"ice_damage_ignore_value": receiver.ice_damage_ignore_value})

	data.update({"fire_damage_ignore": receiver.fire_damage_ignore})
	data.update({"fire_damage_ignore_base": receiver.fire_damage_ignore_base})
	data.update({"fire_damage_ignore_extra": receiver.fire_damage_ignore_extra})
	data.update({"fire_damage_ignore_percent": receiver.fire_damage_ignore_percent})
	data.update({"fire_damage_ignore_value": receiver.fire_damage_ignore_value})

	data.update({"thunder_damage_ignore": receiver.thunder_damage_ignore})
	data.update({"thunder_damage_ignore_base": receiver.thunder_damage_ignore_base})
	data.update({"thunder_damage_ignore_extra": receiver.thunder_damage_ignore_extra})
	data.update({"thunder_damage_ignore_percent": receiver.thunder_damage_ignore_percent})
	data.update({"thunder_damage_ignore_value": receiver.thunder_damage_ignore_value})

	data.update({"xuan_damage_ignore": receiver.xuan_damage_ignore})
	data.update({"xuan_damage_ignore_base": receiver.xuan_damage_ignore_base})
	data.update({"xuan_damage_ignore_extra": receiver.xuan_damage_ignore_extra})
	data.update({"xuan_damage_ignore_percent": receiver.xuan_damage_ignore_percent})
	data.update({"xuan_damage_ignore_value": receiver.xuan_damage_ignore_value})

	data.update({"ice_armor_ignore": receiver.ice_armor_ignore})
	data.update({"ice_armor_ignore_base": receiver.ice_armor_ignore_base})
	data.update({"ice_armor_ignore_extra": receiver.ice_armor_ignore_extra})
	data.update({"ice_armor_ignore_percent": receiver.ice_armor_ignore_percent})
	data.update({"ice_armor_ignore_value": receiver.ice_armor_ignore_value})

	data.update({"fire_armor_ignore": receiver.fire_armor_ignore})
	data.update({"fire_armor_ignore_base": receiver.fire_armor_ignore_base})
	data.update({"fire_armor_ignore_extra": receiver.fire_armor_ignore_extra})
	data.update({"fire_armor_ignore_percent": receiver.fire_armor_ignore_percent})
	data.update({"fire_armor_ignore_value": receiver.fire_armor_ignore_value})

	data.update({"thunder_armor_ignore": receiver.thunder_armor_ignore})
	data.update({"thunder_armor_ignore_base": receiver.thunder_armor_ignore_base})
	data.update({"thunder_armor_ignore_extra": receiver.thunder_armor_ignore_extra})
	data.update({"thunder_armor_ignore_percent": receiver.thunder_armor_ignore_percent})
	data.update({"thunder_armor_ignore_value": receiver.thunder_armor_ignore_value})

	data.update({"xuan_armor_ignore": receiver.xuan_armor_ignore})
	data.update({"xuan_armor_ignore_base": receiver.xuan_armor_ignore_base})
	data.update({"xuan_armor_ignore_extra": receiver.xuan_armor_ignore_extra})
	data.update({"xuan_armor_ignore_percent": receiver.xuan_armor_ignore_percent})
	data.update({"xuan_armor_ignore_value": receiver.xuan_armor_ignore_value})

	data.update({"depress_resist": receiver.depress_resist})
	data.update({"depress_resist_base": receiver.depress_resist_base})
	data.update({"depress_resist_extra": receiver.depress_resist_extra})
	data.update({"depress_resist_percent": receiver.depress_resist_percent})
	data.update({"depress_resist_value": receiver.depress_resist_value})

	data.update({"hitback_resist": receiver.hitback_resist})
	data.update({"hitback_resist_base": receiver.hitback_resist_base})
	data.update({"hitback_resist_extra": receiver.hitback_resist_extra})
	data.update({"hitback_resist_percent": receiver.hitback_resist_percent})
	data.update({"hitback_resist_value": receiver.hitback_resist_value})

	data.update({"control_resist": receiver.control_resist})
	data.update({"control_resist_base": receiver.control_resist_base})
	data.update({"control_resist_extra": receiver.control_resist_extra})
	data.update({"control_resist_percent": receiver.control_resist_percent})
	data.update({"control_resist_value": receiver.control_resist_value})

	data.update({"insane_resist": receiver.insane_resist})
	data.update({"insane_resist_base": receiver.insane_resist_base})
	data.update({"insane_resist_extra": receiver.insane_resist_extra})
	data.update({"insane_resist_percent": receiver.insane_resist_percent})
	data.update({"insane_resist_value": receiver.insane_resist_value})

	return data
