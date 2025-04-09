// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotifyState_AttachMeshPart.h"
#include "../CS3Debug.h"
#include "Actor/GameCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START
UAnimNotifyState_AttachMeshPart::UAnimNotifyState_AttachMeshPart()
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(255, 236, 0, 255);
#endif // WITH_EDITORONLY_DATA
}

#if WITH_EDITOR
void UAnimNotifyState_AttachMeshPart::PreEditChange(UProperty* PropertyAboutToChange)
{

}
#endif

void UAnimNotifyState_AttachMeshPart::NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (IsValid(GameCharacter))
	{
		GameCharacter->BindMesh(AttachMeshId);
	}
}

void UAnimNotifyState_AttachMeshPart::NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime)
{

}

void UAnimNotifyState_AttachMeshPart::NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation)
{
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (IsValid(GameCharacter))
	{
		GameCharacter->UnBindMesh(AttachMeshId);
	}
}

void UAnimNotifyState_AttachMeshPart::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	Super::StopNotifyEffect(MeshComp, Animation);
}
CONTROL_COMPILE_OPTIMIZE_END