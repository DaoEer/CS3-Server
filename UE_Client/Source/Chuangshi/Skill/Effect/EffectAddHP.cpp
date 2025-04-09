#include "EffectAddHP.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Skill/SkillBase/Skill.h"

UEffectAddHP::UEffectAddHP()
{
}

UEffectAddHP::~UEffectAddHP()
{
}

void UEffectAddHP::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);

	//伤害百分比（浮点型）|固定值（整型）
	if (dictDat.Param1 != "")
	{
		TArray<FString> Param1Split = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
		_percent = FSTRING_TO_FLOAT(Param1Split[0]);
		if (Param1Split.Num() > 1)
		{
			_addValue = FSTRING_TO_INT(Param1Split[1]);
		}
	}

	//标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
	if (dictDat.Param2 != "")
	{
		TArray<FString> Param2Split = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2);
		for (auto i : Param2Split)
		{
			TArray<FString> List = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
			if (List[0] == "IsSkipEvent")
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

bool UEffectAddHP::canEffect(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	int32 CurrentState = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("state"));
	if (CurrentState == (int32)ENTITY_STATE::EntityStateDead)
	{
		return false;
	}
	return UEffectSkillBase::canEffect(skill, caster, receiver);
}

void UEffectAddHP::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("HP_Max"));
	int32 value = ceil(HP_Max*_percent + (double)_addValue);
	value = value > 0 ? value : 0;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillSetHP(value);
		if (skill != nullptr && !_isSkipEvent)
		{
			UCSkillInterface * CCSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
			if (IsValid(CCSkillInterface))
			{
				TMap<FString, FVariant> pDict1;
				pDict1.Add("actForbid", FVariant((int32)_receiverActForbid));
				pDict1.Add("type", FVariant(0));
				CCSkillInterface->triggerSkillEvent(ENUM_SKILL_EVENT::CureEvent, receiver->ID(), pDict1);
			}
			TMap<FString, FVariant> pDict2;
			pDict2.Add("actForbid", FVariant((int32)_receiverActForbid));
			pDict2.Add("type", FVariant(1));
			CSkillInterface->triggerSkillEvent(ENUM_SKILL_EVENT::CureEvent, caster->ID(), pDict2);
		}
	}
}
