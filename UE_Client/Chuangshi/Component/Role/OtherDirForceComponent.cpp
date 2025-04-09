// Fill out your copyright notice in the Description page of Project Settings.


#include "OtherDirForceComponent.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "Util/CS3Debug.h"


void UOtherDirForceComponent::SetOtherCharacter(ACharacter* OtherActor)
{
	if (IsValid(OtherActor))
	{
		OtherCharacter = OtherActor;
	}
}

void UOtherDirForceComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	if (!IsForceCanMove)
	{
		return;
	}

	if (!IsValid(OtherCharacter))
	{
		Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	}
	else
	{
		switch (CurLocalDire)
		{
			case ELOCAL_FORCE_DIRE::None:
			{
				CS3_Warning(TEXT("UOtherDirForceComponent::TickComponent --- CurLocalDire Is None!"));
				return;
			}
			case ELOCAL_FORCE_DIRE::UP_DIRE:
			{
				ForceDirection = OtherCharacter->GetActorUpVector();
				break;
			}
			case ELOCAL_FORCE_DIRE::DOWN_DIRE:
			{
				ForceDirection = -OtherCharacter->GetActorUpVector();
				break;
			}
			case ELOCAL_FORCE_DIRE::LIFT_DIRE:
			{
				ForceDirection = -OtherCharacter->GetActorRightVector();
				break;
			}
			case ELOCAL_FORCE_DIRE::RIGHT_DIRE:
			{
				ForceDirection = OtherCharacter->GetActorRightVector();
				break;
			}
			case ELOCAL_FORCE_DIRE::FORWARD_DIRE:
			{
				ForceDirection = OtherCharacter->GetActorForwardVector();
				break;
			}
			case ELOCAL_FORCE_DIRE::BACK_DIRE:
			{
				ForceDirection = -OtherCharacter->GetActorForwardVector();
				break;
			}
			case ELOCAL_FORCE_DIRE::LOOKAT_DIRE:
			{
				ForceDirection = OtherCharacter->GetActorLocation() - GetOwner()->GetActorLocation();
				ForceDirection = ForceDirection.GetSafeNormal2D();
				break;
			}
			default:
				return;
		}

		ACharacter* Character = Cast<ACharacter>(GetOwner());
		if (Character)
		{
			float StepLength = Character->GetCapsuleComponent()->GetScaledCapsuleRadius() - 1;
			float Length = (ForceSpeed + ForceSpeed * ForcePercentage) * DeltaTime;
			float Direction = Length > 0 ? 1 : -1;
			Length = FMath::Abs(Length);

			while (Length > StepLength)
			{
				GetOwner()->AddActorWorldOffset(Direction * StepLength * ForceDirection, true);
				Length -= StepLength;
			}

			GetOwner()->AddActorWorldOffset(Direction * Length * ForceDirection, true);
		}
	}
}
