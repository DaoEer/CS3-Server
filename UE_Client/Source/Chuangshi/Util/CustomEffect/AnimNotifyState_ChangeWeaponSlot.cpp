// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotifyState_ChangeWeaponSlot.h"
#include "../CS3Debug.h"
#include "Animation/AnimSequenceBase.h"
#include "Components/SkeletalMeshComponent.h"

#include "Actor/GameCharacter.h"
#include "Component/AppearanceComponent.h"
#include "time.h"

CONTROL_COMPILE_OPTIMIZE_START
UAnimNotifyState_ChangeWeaponSlot::UAnimNotifyState_ChangeWeaponSlot(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(255, 236, 0, 255);
#endif // WITH_EDITORONLY_DATA
}

void UAnimNotifyState_ChangeWeaponSlot::NotifyBegin(class USkeletalMeshComponent * MeshComp,
	class UAnimSequenceBase * Animation, float TotalDuration)
{
	Super::NotifyBegin(MeshComp, Animation, TotalDuration);
	
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAnimNotifyState:  [time=%d,  name=%s,  SwichWeapon[begin]]"), clock(), *Animation->GetName());
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (IsValid(GameCharacter) && IsValid(GameCharacter->GetAppearanceComponent()))
	{
		GameCharacter->IsLockChangeWeaponSlotNotify = true;
		GameCharacter->GetAppearanceComponent()->UpdateWeaponRightToLeft(true, RoleProfession);
	}
}

void UAnimNotifyState_ChangeWeaponSlot::NotifyTick(class USkeletalMeshComponent * MeshComp,
	class UAnimSequenceBase * Animation, float FrameDeltaTime)
{
	Super::NotifyTick(MeshComp, Animation, FrameDeltaTime);
}

void UAnimNotifyState_ChangeWeaponSlot::NotifyEnd(class USkeletalMeshComponent * MeshComp,
	class UAnimSequenceBase * Animation)
{
	Super::NotifyEnd(MeshComp, Animation);
	
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAnimNotifyState:  [time=%d,  name=%s,  SwichWeapon[end]]"), clock(), *Animation->GetName());
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (IsValid(GameCharacter) && IsValid(GameCharacter->GetAppearanceComponent()))
	{
		GameCharacter->IsLockChangeWeaponSlotNotify = false;
		GameCharacter->GetAppearanceComponent()->UpdateWeaponRightToLeft(false, RoleProfession);
	}
}

void UAnimNotifyState_ChangeWeaponSlot::StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	Super::StopNotifyEffect(MeshComp, Animation);
}

CONTROL_COMPILE_OPTIMIZE_END