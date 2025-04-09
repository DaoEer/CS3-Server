// Fill out your copyright notice in the Description page of Project Settings.


#include "PerformanceComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ParticleManager.h"
#include "Util/CS3Debug.h"

UPerformanceComponent::UPerformanceComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UPerformanceComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (!IsValid(UUECS3GameInstance::Instance))return;
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;

	if (!ParticleManager)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPerformanceComponent::EndPlay : ParticleManager!"));
		return;
	}
		
	for (size_t i = 0; i < EffectUIDList.Num(); i++)
	{
		if (ParticleManager->CheckEffectValidByUID(EffectUIDList[i]))
		{
			ParticleManager->StopEffectByUID(EffectUIDList[i], false, false, true, false);
		}
	}
}
