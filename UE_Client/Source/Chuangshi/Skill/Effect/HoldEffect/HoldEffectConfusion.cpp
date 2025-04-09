#include "HoldEffectConfusion.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/GameObjectInterface.h"
#include "CS3Base/GameObject.h"

UHoldEffectConfusion::UHoldEffectConfusion()
{
}

UHoldEffectConfusion::~UHoldEffectConfusion()
{
}

void UHoldEffectConfusion::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillAddEffectState(EFFECT_STATE::EFFECT_STATE_CONFUSION);
	}
	UGameObjectInterface * Interface = ((GameObject*)receiver)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		URolePerformanceInterface *RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), receiver->ID()));
		if (IsValid(RolePerformanceInterface))
		{
			RolePerformanceInterface->onBeginConfusion();
		}
	}
}

void UHoldEffectConfusion::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRemoveEffectState(EFFECT_STATE::EFFECT_STATE_CONFUSION);
	}
	UGameObjectInterface * Interface = ((GameObject*)receiver)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		URolePerformanceInterface *RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), receiver->ID()));
		if (IsValid(RolePerformanceInterface))
		{
			RolePerformanceInterface->onEndConfusion();
		}
	}
	UHoldEffect::onEnd(effectData, receiver);
}
