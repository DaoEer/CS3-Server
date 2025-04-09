#include "HoldEffectAddActCounter.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"

UHoldEffectAddActCounter::UHoldEffectAddActCounter()
{
}

UHoldEffectAddActCounter::~UHoldEffectAddActCounter()
{
}

void UHoldEffectAddActCounter::init(FHOLD_EFFECT dictDat, USkill * skill)
{
	UHoldEffect::init(dictDat, skill);
	if (dictDat.Param1 != "")
	{
		TArray<FString> Param1 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
		for (auto i : Param1)
		{
			_actList.Add(FSTRING_TO_INT(i));
		}
	}
}

void UHoldEffectAddActCounter::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface) && _actList.Num() > 0)
	{
		CSkillInterface->CSkillAddActCounters(_actList);
	}

}

void UHoldEffectAddActCounter::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface) && _actList.Num() > 0)
	{
		CSkillInterface->CSkillRemoveActCounters(_actList);
	}

	UHoldEffect::onEnd(effectData, receiver);
}
