// Fill out your copyright notice in the Description page of Project Settings.


#include "LineToPointFilterActorComponent.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"

void ULineToPointFilterActorComponent::SimulateMovement(float DeltaTime)
{
	Super::SimulateMovement(DeltaTime);

	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetOwner());
	if (!IsValid(MonsterActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ULineToPointFilterActorComponent::TickComponent : MonsterActor!"));
		return;
	}

	FVector CurrPos = MonsterActor->GetActorLocation();
	float Distance = DeltaTime * Velocity * 100.f;
	FVector Pos = DestPos - CurrPos;
	Pos.Normalize();

	if (FMath::Abs((DestPos - CurrPos).Size2D()) <= Distance)
	{
		DestPos = FVector::ZeroVector;
		MonsterActor->OnMonsterAppearLineToPoint();
		MonsterActor->ResetFilter();
	}
	else
	{
		FVector Position = CurrPos;
		Position.X += Pos.X * Distance;
		Position.Y += Pos.Y * Distance;
		MonsterActor->SetActorLocation(Position);
	}
}

void ULineToPointFilterActorComponent::InitData(float InVelocity, const FVector& InDestPos)
{
	Velocity = InVelocity;
	DestPos = InDestPos;
}

