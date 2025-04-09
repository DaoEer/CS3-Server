// Fill out your copyright notice in the Description page of Project Settings.

#include "CS3AnimNotifyState.h"
#include "../CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UCS3AnimNotifyState::UCS3AnimNotifyState(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	bStopNotifyEffect = false;
}

void UCS3AnimNotifyState::NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, float TotalDuration)
{
	bStopNotifyEffect = false;
	Super::NotifyBegin(MeshComp, Animation,TotalDuration);
}

void UCS3AnimNotifyState::StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	bStopNotifyEffect = true;
	NotifyEnd(MeshComp, Animation);
	Received_StopNotifyEffect(MeshComp, Animation);
}
CONTROL_COMPILE_OPTIMIZE_END