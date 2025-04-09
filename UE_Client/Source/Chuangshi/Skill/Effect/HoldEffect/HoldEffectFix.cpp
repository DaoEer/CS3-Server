#include "HoldEffectFix.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"

UHoldEffectFix::UHoldEffectFix()
{
}

UHoldEffectFix::~UHoldEffectFix()
{
}

void UHoldEffectFix::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillAddEffectState(EFFECT_STATE::EFFECT_STATE_FIX);
	}
}

void UHoldEffectFix::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRemoveEffectState(EFFECT_STATE::EFFECT_STATE_FIX);
	}
	UHoldEffect::onEnd(effectData, receiver);
}
