// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotifyState_PlayEffect.h"
#include "Util/CS3Debug.h"
#include "UObjectGlobals.h"
#include "Actor/GameCharacter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ParticleManager.h"

CONTROL_COMPILE_OPTIMIZE_START
UAnimNotifyState_PlayEffect::UAnimNotifyState_PlayEffect(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(72, 255, 235, 255);
#endif // WITH_EDITORONLY_DATA
}

void UAnimNotifyState_PlayEffect::NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	Super::NotifyBegin(MeshComp, Animation, TotalDuration);

	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (!IsValid(GameCharacter))
	{
		return;
	}

	if (!EffectID.IsEmpty())
	{
		EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, GameCharacter, GameCharacter);
	}
}

void UAnimNotifyState_PlayEffect::NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime)
{
	Super::NotifyTick(MeshComp, Animation, FrameDeltaTime);
}

void UAnimNotifyState_PlayEffect::NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation)
{
	Super::NotifyEnd(MeshComp, Animation);

	if (EffectUID != 0)
	{ 
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID);
	}
} 

void UAnimNotifyState_PlayEffect::StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (EffectUID != 0)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID);
	}
	Super::StopNotifyEffect(MeshComp, Animation);
}


CONTROL_COMPILE_OPTIMIZE_END
