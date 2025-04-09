// Fill out your copyright notice in the Description page of Project Settings.

#include "Component/FightComponent.h"
#include "GameData/BossArea.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"

UFightComponent::UFightComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UFightComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UFightComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Cast<AServerCharacter>(GetOwner())->FightComponent = nullptr;

	Super::EndPlay(EndPlayReason);
}

void UFightComponent::EnterFightState()
{
	AServerCharacter* Owner = Cast<AServerCharacter>(GetOwner());
	OnEnterFightState.Broadcast();
	if (!Owner)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightComponent::EnterFightState : Owner!"));
		return;
	}

	if (Owner->GetBaseAnimInstance())
	{
		if (Owner->IsActiveMoveing())
		{
			Owner->GetBaseAnimInstance()->PlayMoveAction();
		}
		else
		{
			Owner->GetBaseAnimInstance()->PlayStandbyAction();
		}
	}
}

UMonsterFightComponent::UMonsterFightComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}
