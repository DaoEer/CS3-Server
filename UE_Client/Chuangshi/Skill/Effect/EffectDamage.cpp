#include "EffectDamage.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Skill/SkillBase/Skill.h"

UEffectDamage::UEffectDamage()
{
}

UEffectDamage::~UEffectDamage()
{
}

void UEffectDamage::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);

	//伤害百分比（浮点型）|固定值（整型）
	if (dictDat.Param1 != "")
	{
		TArray<FString> Param1Split = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
		_percent = FSTRING_TO_FLOAT(Param1Split[0]);
		if (Param1Split.Num() > 1)
		{
			_damageValue = FSTRING_TO_INT(Param1Split[1]);
		}
	}

	//标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
	if (dictDat.Param2 != "")
	{
		TArray<FString> Param2Split = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2);
		for (auto i : Param2Split)
		{
			TArray<FString> List = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
			if (List[0] == "IsDoDeadEffect")
			{
				_deadEffect = 1;
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

bool UEffectDamage::canEffect(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	int32 CurrentState = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("state"));
	if (CurrentState == (int32)ENTITY_STATE::EntityStateDead)
	{
		return false;
	}
	return UEffectSkillBase::canEffect(skill, caster, receiver);
}

void UEffectDamage::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("HP_Max"));
	int32 finalDamage = ceil(HP_Max*_percent + (double)_damageValue);
	finalDamage = finalDamage > 0 ? finalDamage : 0;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		if (skill != nullptr && !_isSkipEvent)
		{
			UCSkillInterface * CCSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
			if (IsValid(CCSkillInterface))
			{
				TMap<FString, FVariant> pDict1;
				pDict1.Add("actForbid", FVariant((int32)_casterActForbid));
				pDict1.Add("type", FVariant(0));
				pDict1.Add("takeDamage", FVariant(finalDamage));
				CCSkillInterface->triggerSkillEvent(ENUM_SKILL_EVENT::HurtEvent, receiver->ID(), pDict1);
			}
			TMap<FString, FVariant> pDict2;
			pDict2.Add("actForbid", FVariant((int32)_receiverActForbid));
			pDict2.Add("type", FVariant(1));
			pDict2.Add("takeDamage", FVariant(finalDamage));
			CSkillInterface->triggerSkillEvent(ENUM_SKILL_EVENT::HurtEvent, caster->ID(), pDict2);
		}

		int32 ActForbid = 0;
		if (_receiverActForbid != ACTION_FLAG::ACTION_FORBID_NONE)
		{
			uint32 actionFlagValue1 = uint32(1) << uint32(_receiverActForbid);
			ActForbid = (int32)actionFlagValue1;
		}
		int32 SkillID = 0;
		if (nullptr != skill)
		{
			SkillID = skill->getID();
		}
		CSkillInterface->receiveDamage(caster->ID(), SkillID, 1, finalDamage, 0, 0, _deadEffect, ActForbid);
	}
}
