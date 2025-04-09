// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotify_PlayEffect.h"
#include "UObjectGlobals.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ParticleManager.h"
#include "Actor/GameCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START
UAnimNotify_PlayEffect::UAnimNotify_PlayEffect()
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(72, 255, 235, 255);
#endif // WITH_EDITORONLY_DATA
}

void UAnimNotify_PlayEffect::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	Super::Notify(MeshComp, Animation);

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

void UAnimNotify_PlayEffect::StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (EffectUID != 0)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID);
	}

	Super::StopNotifyEffect(MeshComp, Animation);
}

CONTROL_COMPILE_OPTIMIZE_END

