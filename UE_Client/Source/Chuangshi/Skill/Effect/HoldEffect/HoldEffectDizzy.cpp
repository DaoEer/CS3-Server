#include "HoldEffectDizzy.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"


UHoldEffectDizzy::UHoldEffectDizzy()
{
}

UHoldEffectDizzy::~UHoldEffectDizzy()
{
}

void UHoldEffectDizzy::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillAddEffectState(EFFECT_STATE::EFFECT_STATE_DIZZY);
	}
}

void UHoldEffectDizzy::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRemoveEffectState(EFFECT_STATE::EFFECT_STATE_DIZZY);
	}
	UHoldEffect::onEnd(effectData, receiver);
}
