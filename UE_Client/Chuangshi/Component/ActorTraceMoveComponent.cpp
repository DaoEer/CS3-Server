// Fill out your copyright notice in the Description page of Project Settings.


#include "ActorTraceMoveComponent.h"
//UE4
#include "Kismet/KismetMathLibrary.h"
#include "CollisionQueryParams.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "NoExportTypes.h"
#include "Engine/EngineTypes.h"
//CS3
#include "CS3Base/GameObject.h"
#include "Actor/ServerCharacter.h"
#include "Role/PlayerControllerMoveComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

// Sets default values for this component's properties
UActorTraceMoveComponent::UActorTraceMoveComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// Called when the game starts
void UActorTraceMoveComponent::BeginPlay()
{
	Super::BeginPlay();

	// ...
	
}


void UActorTraceMoveComponent::ExecuteMoveToTarget()
{
	if (IsValid(TraceTarget.TraceTarget))
	{
		FVector TargetLocation = TraceTarget.TraceTarget->GetActorLocation();
		FRotator TargetRotation = TraceTarget.TraceTarget->GetActorRotation();
		FVector OwnerLocation = GetOwner()->GetActorLocation();

		FVector NewDirection = TargetLocation - OwnerLocation;
		FRotator OwnMoveRotator = FRotator(0.0f, UKismetMathLibrary::DegAtan2(NewDirection.Y, NewDirection.X), 0.0f);
		FVector OwnerMoveLocation = OwnerLocation + TraceTarget.MoveSpeed * UKismetMathLibrary::GetForwardVector(OwnMoveRotator);

		float distanceLocation = UGolbalBPFunctionLibrary::GetActorDistance(GetOwner(), TraceTarget.TraceTarget);
		if (distanceLocation <= TraceTarget.NearbyRange*100.0f)
		{
			TraceTarget.TraceCallback.ExecuteIfBound(true);
			StopMove();
		}
		else
		{
			GetOwner()->SetActorLocationAndRotation(OnGroundPostion(OwnerMoveLocation), OwnMoveRotator);
		}
	}
}

// Called every frame
void UActorTraceMoveComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (bIsMoving)
	{
		if (TraceTarget.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetActor)
		{
			ExecuteMoveToTarget();
		}
		else if (TraceTarget.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetPoint)
		{

		}
	}
}

void UActorTraceMoveComponent::TraceTargetActor(const AActor* TargetActor, float NearbyRange /*= 0.0f*/, float MoveSpeed /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/)
{
	bIsMoving = true;

	TraceTarget.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTarget.IsChasing = true;
	TraceTarget.NearbyRange = NearbyRange;
	TraceTarget.MoveSpeed = MoveSpeed;
	TraceTarget.TraceTarget = (AActor*)TargetActor;
	TraceTarget.TraceCallback = TraceCallback;
}

void UActorTraceMoveComponent::StopMove()
{
	bIsMoving = false;
}

FVector UActorTraceMoveComponent::OnGroundPostion(const FVector &Vector)
{
	ACharacter *OwnerCharacter = Cast<ACharacter>(GetOwner());

	FVector newPos(Vector);
	FHitResult HitOut(ForceInit);
	FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true, OwnerCharacter);
	TraceParams.bTraceComplex = false;
	//TraceParams.bTraceAsyncScene = false;
	TraceParams.bReturnPhysicalMaterial = false;
	TArray<AActor*> ActorList;
	ActorList = UGolbalBPFunctionLibrary::GetActorsInRange(nullptr, 200.0f, OwnerCharacter->GetActorLocation());
	for (int i = 0; i < ActorList.Num(); i++)
	{
		AActor* Actor_i = ActorList[i];
		AServerCharacter* Actor_s = Cast<AServerCharacter>(Actor_i);
		GameObject* entity = (GameObject*)Actor_s->GetSelfEntity();
		if (entity && entity->GetActorName() == TEXT("MovingPlatform"))  continue;
		if (IsValid(Actor_s))
		{
			TraceParams.AddIgnoredActor(Actor_s);
		}
	}
	TraceParams.AddIgnoredActor(OwnerCharacter);

	if (this->GetWorld()->LineTraceSingleByChannel(HitOut, newPos + FVector(0.0f, 0.0f, 200.0f),
		newPos + FVector(0.0f, 0.0f, -10000.0f), ECC_Pawn, TraceParams))
	{
		AServerCharacter* Actor = Cast<AServerCharacter>(HitOut.GetActor());
		float OwnerScaledCapsuleHalfHeight = OwnerCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
		if (IsValid(Actor))
		{
			GameObject* entity = (GameObject*)Actor->GetSelfEntity();
			if (entity && entity->GetActorName() == TEXT("MovingPlatform"))
			{
				newPos.Z = HitOut.Location.Z + OwnerScaledCapsuleHalfHeight;
			}
			else
			{
				if (Actor->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() < 200.0f)
				{
					newPos.Z = HitOut.Location.Z - OwnerScaledCapsuleHalfHeight*2.0 + OwnerScaledCapsuleHalfHeight;
				}
			}
		}
		else
		{
			newPos.Z = HitOut.Location.Z + OwnerScaledCapsuleHalfHeight;
		}
	}
	return newPos;
}
CONTROL_COMPILE_OPTIMIZE_END
