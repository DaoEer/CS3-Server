#include "HoldEffectUncontrollable.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"

UHoldEffectUncontrollable::UHoldEffectUncontrollable()
{
}

UHoldEffectUncontrollable::~UHoldEffectUncontrollable()
{
}

void UHoldEffectUncontrollable::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillAddEffectState(EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE);
	}
}

void UHoldEffectUncontrollable::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRemoveEffectState(EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE);
	}
	UHoldEffect::onEnd(effectData, receiver);
}
