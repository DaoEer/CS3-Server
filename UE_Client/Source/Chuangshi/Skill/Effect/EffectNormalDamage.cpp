#include "EffectNormalDamage.h"
#include "GameData/ConstData.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Skill/SkillBase/Skill.h"
#include "CS3Base/GameObject.h"
#include "GameData/EntityProperty/CombatDamager.h"
#include "GameData/EntityProperty/CombatDamagerLoader.h"

CONTROL_COMPILE_OPTIMIZE_START
UEffectNormalDamage::UEffectNormalDamage()
{
}

UEffectNormalDamage::~UEffectNormalDamage()
{
}

void UEffectNormalDamage::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);
	if (dictDat.Param1 != "")
	{
		_damageType = FSTRING_TO_INT(dictDat.Param1);
	}
	//生命伤害百分比（如“0.5”代表“50%物理攻击”）|生命伤害固定值（整型）	
	if (dictDat.Param2 != "")
	{
		TArray<FString> Param2 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2, false, TEXT("|"));
		_skillRadio = FSTRING_TO_FLOAT(Param2[0]);
		if (Param2.Num() > 1)
		{
			_skillValue = FSTRING_TO_INT(Param2[1]);
		}
	}

	//罡气伤害百分比（如“0.5”代表“50%罡气攻击”）|罡气伤害固定值（整型）
	if (dictDat.Param3 != "")
	{
		TArray<FString> Param3 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param3, false, TEXT("|"));
		_skillGangQiRadio = FSTRING_TO_FLOAT(Param3[0]);
		if (Param3.Num() > 1)
		{
			_skillGangQiValue = FSTRING_TO_INT(Param3[1]);
		}
	}

	//标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
	if (dictDat.Param4 != "")
	{
		TArray<FString> Param4 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param4);
		for (auto i : Param4)
		{
			TArray<FString> List = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
			if (List[0] == "IsDoDeadEffect")
			{
				_deadEffect = 1;
			}
			else if (List[0] == "IsReAttrC")
			{
				FString propertyStr = PROPERTYIDTOSTR[FSTRING_TO_INT(List[1])];
				_customAttrC.Add(propertyStr, FSTRING_TO_INT(List[2]));
			}
			else if (List[0] == "IsReAttrR")
			{
				FString propertyStr = PROPERTYIDTOSTR[FSTRING_TO_INT(List[1])];
				_customAttrR.Add(propertyStr, FSTRING_TO_INT(List[2]));
			}
			else if (List[0] == "IsSkipEvent")
			{
				_isSkipEvent = true;
			}
			else
			{
				CS3_Warning(TEXT("EffectDamage: %s is not a correct tag name!"), *List[0]);
			}

		}
	}

}

bool UEffectNormalDamage::canEffect(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	int32 CurrentState = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("state"));
	if (CurrentState == (int32)ENTITY_STATE::EntityStateDead)
	{
		return false;
	}
	return UEffectSkillBase::canEffect(skill, caster, receiver);
}

void UEffectNormalDamage::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	///先计算罡气伤害
	if ( _skillGangQiValue != 0 || _skillGangQiRadio!= 0 )
	{
		CSkillInterface->CSkillGangQiDamage(caster->ID(), _skillGangQiValue, _skillGangQiRadio);
	}
	
	int32 CLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("level"));
	int32 CProfession = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("profession"));
	FCOMBAT_DAMAGER_DATA CasterBaseCom = UCombatDamagerLoader::GetInstance()->GetCombatDamagerData(CLevel, CProfession);

	int32 RLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("level"));
	int32 RProfession = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("profession"));
	FCOMBAT_DAMAGER_DATA ReceiverBaseCom = UCombatDamagerLoader::GetInstance()->GetCombatDamagerData(RLevel, RProfession);
	///然后计算HP伤害
	int32 damage;
	///伤害量 = 伤害了初值 * （ 技能效果 + 伤害波动 ） + 伤害固定值
	if (_damageType == 1)
	{
		int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("damage"));
		damage = CustomAttrC("damage", value);
	} else {
		int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("magic_damage"));
		damage = CustomAttrC("magic_damage", value);
	}
	
	//float Romdan = 2.0 * (rand()%100) / 100.0 - 1.0;
	float Random = FMath::FRandRange(-1.0f, 1.0f);
	int32 recDamage = ceil((damage * _skillRadio + _skillValue) *(1.0 + CasterBaseCom.DamRandom * Random));
	recDamage = recDamage > 0 ? recDamage : 0;

	/// 计算修正伤害, 伤害值*(各种造成伤害修正相乘)
	float damage_correction = 1.0;
	int32 dcvalue = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("damage_correction"));
	damage_correction *= CustomAttrC("damage_correction", dcvalue)/10000.0;
	if (_damageType == 1)
	{
		int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("attack_damage_correction"));
		damage_correction *= CustomAttrC("attack_damage_correction", value) / 10000.0;
	}
	else if (_damageType == 2)
	{
		int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("magic_damage_correction"));
		damage_correction *= CustomAttrC("magic_damage_correction", value) / 10000.0;
	}
	UGameObjectInterface *Interface = ((GameObject*)caster)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface))
	{
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("role_damage_correction"));
			damage_correction *= CustomAttrC("role_damage_correction", value) / 10000.0;
		}
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
		{
			int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("pet_damage_correction"));
			damage_correction *= CustomAttrC("pet_damage_correction", value) / 10000.0;
		}
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
		{
			int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("monster_damage_correction"));
			damage_correction *= CustomAttrC("monster_damage_correction", value) / 10000.0;
		}
	}
	recDamage = FMath::CeilToInt(recDamage * damage_correction);
	//recDamage *= damage_correction;

	/// 暴击率 = 暴击点 / 基准暴击点
	/// 暴击伤害 = 伤害量 * 基准暴击倍率
	bool isCritical = false;
	int32 ccvalue = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("criticalstrike"));
	float critical = CustomAttrC("criticalstrike", ccvalue) / (float)CasterBaseCom.BCritPoint;
	float CRomdan = FMath::FRandRange(0.0f, 1.0f);
	if (critical >= CRomdan)
	{
		isCritical = true;
		recDamage = FMath::CeilToInt(recDamage * CasterBaseCom.BCritRatio);
	}
	///招架率 = 招架点 / （ 招架点 * （1-基准招架倍率）+ [受术者]基准招架点 ）
	bool isParry = false;
	int32 rpvalue = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("parry"));
	float parry = CustomAttrR("parry", rpvalue) / ( CustomAttrR("parry", rpvalue)*(1 - ReceiverBaseCom.BParryRatio) + ReceiverBaseCom.BParryPoint);
	float PRomdan = FMath::FRandRange(0.0f, 1.0f);
	if (parry >= PRomdan)
	{
		isParry = true;
		recDamage = FMath::CeilToInt(recDamage * ReceiverBaseCom.BParryRatio);
	}

	///护盾Buff的抵扣伤害
	/*未完待续*/

	///护甲伤害减免率 = 防御 / （防御 + [受术者]基准防御点）
	///伤害量 *= （1-护甲伤害减免率）
	///目前伤害量 -= 护甲值
	int32 armor = 0;
	if (_damageType == 1)
	{
		armor = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("armor"));
	}
	else {
		armor = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("magic_armor"));
	}
	recDamage = FMath::CeilToInt(recDamage*(1 - (float)armor / (armor + ReceiverBaseCom.BArmorPoint)));
	int32 takeDamage = recDamage; ///<携带伤害量

	///计算修正伤害, 伤害值/(各种承受伤害修正相乘)
	float armor_correction = 1.0;
	int32 acvalue = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("armor_correction"));
	armor_correction *= CustomAttrC("armor_correction", acvalue) / 10000.0;
	if (_damageType == 1)
	{
		int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("attack_armor_correction"));
		armor_correction *= CustomAttrC("attack_armor_correction", value) / 10000.0;
	}
	else if (_damageType == 2)
	{
		int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("magic_armor_correction"));
		armor_correction *= CustomAttrC("magic_armor_correction", value) / 10000.0;
	}
	if (IsValid(Interface))
	{
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("role_armor_correction"));
			armor_correction *= CustomAttrC("role_armor_correction", value) / 10000.0;
		}
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
		{
			int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("pet_armor_correction"));
			armor_correction *= CustomAttrC("pet_armor_correction", value) / 10000.0;
		}
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
		{
			int32 value = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("monster_armor_correction"));
			armor_correction *= CustomAttrC("monster_armor_correction", value) / 10000.0;
		}
	}
	if (armor_correction != 0.0)
	{
		float Damage;
		Damage = float(recDamage) / armor_correction;
		recDamage = FMath::CeilToInt(Damage);
	}

	int32 skillID = 0;
	if (skill != nullptr)
	{
		skillID = skill->getID();
	}
	if (skill != nullptr && !_isSkipEvent)
	{
		UCSkillInterface * CCSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CCSkillInterface))
		{
			TMap<FString, FVariant> pDict1;
			pDict1.Add("actForbid", FVariant((int32)_receiverActForbid));
			pDict1.Add("type", FVariant(0));
			pDict1.Add("takeDamage", FVariant(takeDamage));
			pDict1.Add("IsCritical", FVariant(isCritical));
			pDict1.Add("IsParry", FVariant(isParry));
			CCSkillInterface->triggerSkillEvent(ENUM_SKILL_EVENT::HurtEvent, receiver->ID(), pDict1);
		}
		TMap<FString, FVariant> pDict2;
		pDict2.Add("actForbid", FVariant((int32)_receiverActForbid));
		pDict2.Add("type", FVariant(1));
		pDict2.Add("takeDamage", FVariant(takeDamage));
		pDict2.Add("IsCritical", FVariant(isCritical));
		pDict2.Add("IsParry", FVariant(isParry));
		CSkillInterface->triggerSkillEvent(ENUM_SKILL_EVENT::HurtEvent, caster->ID(), pDict2);
	}

	///接受伤害
	int32 ActForbid = 0;
	if (_receiverActForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		uint32 actionFlagValue1 = uint32(1) << uint32(_receiverActForbid);
		ActForbid = (int32)actionFlagValue1;
	}
	CSkillInterface->receiveDamage(caster->ID(), skillID, _damageType, recDamage, (int)isCritical, (int)isParry, _deadEffect, ActForbid);
}

int32 UEffectNormalDamage::CustomAttrC(FString propertyStr, int32 propertyValue)
{
	if (_customAttrC.Contains(propertyStr))
	{
		propertyValue += _customAttrC[propertyStr];
	}

	if (_customAttrC.Contains("damage") || _customAttrC.Contains("magic_damage"))
	{
		propertyValue = propertyValue > 1 ? propertyValue : 1;
	}else {
		propertyValue = propertyValue > 0 ? propertyValue : 0;
	}
	return propertyValue;
}

int32 UEffectNormalDamage::CustomAttrR(FString propertyStr, int32 propertyValue)
{
	if (_customAttrR.Contains(propertyStr))
	{
		propertyValue += _customAttrR[propertyStr];
	}

	if (_customAttrR.Contains("damage") || _customAttrR.Contains("magic_damage"))
	{
		propertyValue = propertyValue > 1 ? propertyValue : 1;
	}else {
		propertyValue = propertyValue > 0 ? propertyValue : 0;
	}
	return propertyValue;
}
CONTROL_COMPILE_OPTIMIZE_END