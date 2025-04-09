// Fill out your copyright notice in the Description page of Project Settings.


#include "BaseSubAnimInstance.h"
#include "../Player/PlayerCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START
UBaseSubAnimInstance::UBaseSubAnimInstance()
{

}

UBaseSubAnimInstance::~UBaseSubAnimInstance()
{

}

void UBaseSubAnimInstance::PostInitProperties()
{
	Super::PostInitProperties();
}

void UBaseSubAnimInstance::NativeInitializeAnimation()
{
}

void UBaseSubAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
	if (!IsValid(CurCharacter) || !IsValid(CurCharacterMovement) || !IsValid(LadderCustomMovementCpt))
	{
		APlayerCharacter * OwnerCharacter = Cast<APlayerCharacter>(GetOwningActor());
		if (IsValid(OwnerCharacter))
		{
			CurCharacter = OwnerCharacter;
			LadderCustomMovementCpt = OwnerCharacter->LadderCustomMovmentCpt;
			CurCharacterMovement = CurCharacter->GetCharacterMovement();
		}
	}

	if (!ASLadderUpLoop)
	{
		if (IsValid(CurCharacter) && IsValid(CurCharacter->GetBaseAnimInstance()))
		{
			FACTION_DATA ActionData = CurCharacter->GetBaseAnimInstance()->GetActionDataById(TEXT("Ladder_loop"));
			ASLadderUpLoop = Cast<UAnimSequence>(ActionData.CurAnimSquenceBase);
		}
	}
}
CONTROL_COMPILE_OPTIMIZE_END