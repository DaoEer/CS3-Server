// Fill out your copyright notice in the Description page of Project Settings.


#include "ForceComponent.h"
#include "GameFramework/Character.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
// Sets default values
UForceComponent::UForceComponent()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryComponentTick.bCanEverTick = true;
	IsForceCanMove = false;
	ForceSpeed = 0.0f;
	CurLocalDire = ELOCAL_FORCE_DIRE::None;
	ForceDirection = FVector::ZeroVector;
	ForcePercentage = 0.0f;
}

void UForceComponent::BeginForce(float _ForceSpeed,FVector _ForceDirection)
{
	if (_ForceSpeed > 0)
	{
		ForceSpeed = _ForceSpeed;
	}
	if (_ForceDirection != FVector::ZeroVector)
	{
		ForceDirection = _ForceDirection;
	}

	if (ForceSpeed <= 0.0f)
	{
		IsForceCanMove = false;
	}
	else
	{
		IsForceCanMove = true;
	}
}

void UForceComponent::BeginForce(float _ForceSpeed, ELOCAL_FORCE_DIRE LocalDire)
{
	ForceSpeed = _ForceSpeed;

	if (ELOCAL_FORCE_DIRE::None == LocalDire)
	{
		IsForceCanMove = false;

		return;
	}
	else
	{
		CurLocalDire = LocalDire;
	}

	IsForceCanMove = true;
}

void UForceComponent::StopForce()
{
	IsForceCanMove = false;
}

// Called every frame
void UForceComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	if (!IsForceCanMove)
	{
		return;
	}

	AActor* Owner = GetOwner();
	if (IsValid(Owner))
	{
		FVector AddLocation = FVector::ZeroVector;

		switch (CurLocalDire)
		{
			case ELOCAL_FORCE_DIRE::None:
			{
				AddLocation = (ForceSpeed + ForceSpeed * ForcePercentage) * DeltaTime * ForceDirection;
				Owner->AddActorWorldOffset(AddLocation, true);
				return;
			}
			case ELOCAL_FORCE_DIRE::UP_DIRE:
			{
				ForceDirection = FVector(0.0f, 0.0f, 1.0f);
				break;
			}
			case ELOCAL_FORCE_DIRE::DOWN_DIRE:
			{
				ForceDirection = FVector(0.0f, 0.0f, -1.0f);
				break;
			}
			case ELOCAL_FORCE_DIRE::LIFT_DIRE:
			{
				ForceDirection = FVector(0.0f, -1.0f, 0.0f);
				break;
			}
			case ELOCAL_FORCE_DIRE::RIGHT_DIRE:
			{
				ForceDirection = FVector(0.0f, 1.0f, 0.0f);
				break;
			}
			case ELOCAL_FORCE_DIRE::FORWARD_DIRE:
			{
				ForceDirection = FVector(1.0f, 0.0f, 0.0f);
				break;
			}
			case ELOCAL_FORCE_DIRE::BACK_DIRE:
			{
				ForceDirection = FVector(-1.0f, 0.0f, 0.0f);
				break;
			}
			default:
				return;

		}


		ForceDirection.Normalize();
		AddLocation = (ForceSpeed + ForceSpeed * ForcePercentage) * DeltaTime * ForceDirection;
		Owner->AddActorLocalOffset(AddLocation, true);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
