// Fill out your copyright notice in the Description page of Project Settings.


#include "FilterActorComponent.h"
#include "Actor/ServerCharacter.h"
#include "CS3Base/GameObject.h"

DECLARE_CYCLE_STAT(TEXT("SafeMove(Filter)"), STAT_AvatarFilterSafeMove, STATGROUP_CS3EntityActorSynchLocation);

UFilterActorComponent::UFilterActorComponent()
{
	//bWantsBeginPlay = true;
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.TickGroup = ETickingGroup::TG_PrePhysics;
	PrimaryComponentTick.bStartWithTickEnabled = false;
}

void UFilterActorComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UFilterActorComponent::TickComponent( float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction )
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	SimulateMovement(DeltaTime);
}

void UFilterActorComponent::InitFilter(bool IsActiveTickEnabled /*= true*/)
{
	SetActiveComponentTick(IsActiveTickEnabled);
}

void UFilterActorComponent::SetActiveComponentTick(bool bNewActive)
{
	SetActive(bNewActive);
}

bool UFilterActorComponent::GetPositionAndDirection(const FVector& position, const FVector& direction, int32 parentID, FVector& OutPosition, FVector& OutDirection)
{
	OutPosition = position;
	OutDirection = direction;
	if (parentID > 0)
	{
		if (UUECS3GameInstance::pKBEApp == nullptr)
		{
			return false;
		}
		auto *parent = UUECS3GameInstance::pKBEApp->FindEntity(parentID);

		if (parent && parent->Actor())
		{
			OutPosition = parent->PositionLocalToWorld(position);
			OutDirection = parent->DirectionLocalToWorld(direction);
		}
		else
		{
			return false;  // 有父对象，但找不到了，则啥都不做，保持原位置不变
		}	
	}
	return true;
}

bool UFilterActorComponent::SafeMove(const FVector& position, const FVector& direction, bool bCheckGround /*= false*/)
{
	SCOPE_CYCLE_COUNTER(STAT_AvatarFilterSafeMove);

	AServerCharacter* Owner = Cast<AServerCharacter>(GetOwner());
	if (!IsValid(Owner)) return false;
	FVector newPos = position;
	FVector newDir = direction;
	//飞行状态不检测地面直接返回entity位置
	if (bCheckGround)
	{
		if (!Owner->IsMoveFlying())
		{
			newPos = Owner->FloorTrace(newPos);
		} 

	} 
	Owner->SetActorLocationAndRotation(newPos, FQuat::MakeFromEuler(newDir));
	return true;
}

