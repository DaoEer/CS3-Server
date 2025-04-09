// Fill out your copyright notice in the Description page of Project Settings.
#include "MonsterFollowComponent.h"
#include "Entity/Monster/MonsterFollowRole.h"
#include "Actor/ServerCharacter.h"
#include "Manager/GameStatus.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Navigation/PathFollowingComponent.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"
#include "Interface/StateInterface.h"
#include "Interface/Monster/MonsterInterface.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Interface/Monster/MonsterInterface.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

UMonsterFollowComponent::UMonsterFollowComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

KBEngine::Entity* UMonsterFollowComponent::GetMEntity()
{
	AMonsterCharacter* owner = Cast<AMonsterCharacter>(GetOwner());

	if (!IsValid(owner)) return nullptr;

	return owner->GetSelfEntity();
}

void UMonsterFollowComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	if (Cast<AMonsterCharacter>(GetOwner())->IsState(ENTITY_STATE::EntityStateDead))return;
	UStateInterface* StateInterface = Cast<AMonsterCharacter>(GetOwner())->GetEntityInterface_Cache().StateInterface;
	if (StateInterface && StateInterface->IsActionForbid(ACTION_FLAG::ACTION_FORBID_MOVE))
	{
		SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE::None);
		return;
	}
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		//CS3_DEBUG(TEXT("---------------------------UMonsterPosSyncComponent::TickComponent--------------"));
		return;
	}
	if (GetMEntity())
	{
		AMonsterCharacter* MyCharacter = Cast<AMonsterCharacter>(GetMEntity()->Actor());

		if (IsValid(MyCharacter))
		{
			FVector ActorLocation = GetOwner()->GetActorLocation();
			//float CapsuleHalfHeight = (MyCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight());
			//ActorLocation.Z -= CapsuleHalfHeight;
			FVector ActorDirection = GetMEntity()->Direction();
			ActorDirection.Z = GetOwner()->GetActorRotation().Euler().Z;
			//每tick都把坐标同步到底层，以便底层能同步最新的位置信息到其它人身上
			float ModelScale = GetMEntity()->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
			float DisScale = ModelScale - 1.0;
			float DisHeight = DisScale * MyCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
			GetMEntity()->UpdateVolatileDataToServer(ActorLocation - FVector(0.0, 0.0, DisHeight), ActorDirection);
		}
		if (CurrMoveType == MONSTER_FOLLOW_MOVE_TYPE::None || CurrMoveType == MONSTER_FOLLOW_MOVE_TYPE::StopMove)
		{
			StartMoveTargetPostion();
			return;
		}
		if (CurrMoveType != MONSTER_FOLLOW_MOVE_TYPE::StopMove)
		{
			if (CurrMoveType == MONSTER_FOLLOW_MOVE_TYPE::Moving)
			{
				if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetPoint)
				{
					float dist = (GetOwner()->GetActorLocation() - TraceTargetInfo.TracePostion).Size2D();
					float Radius = Cast<ACharacter>(GetOwner())->GetCapsuleComponent()->GetScaledCapsuleRadius();
					if (dist - Radius <= TraceTargetInfo.NearbyRange * 100)
					{
						TraceTargetInfo.TraceCallback.ExecuteIfBound(true);
						if (TraceTargetInfo.IsStopMove)
						{
							SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE::StopMove);
						}
						TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(true);
					}
				}
			}
			//以下几类移动都是引擎控制，所以需要自己去检查是否到达
			AController* Controller = Cast<AServerCharacter>(GetOwner())->GetController();
			UPathFollowingComponent* PFollowComp = nullptr;
			if (IsValid(Controller))
			{
				PFollowComp = UGolbalBPFunctionLibrary::InitNavigationControl(*Controller);
			}
			if (PFollowComp && PFollowComp->GetStatus() != EPathFollowingStatus::Moving)
			{
				TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
				SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE::StopMove);
				TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(false);
			}
		}
	}
}

MONSTER_FOLLOW_MOVE_TYPE UMonsterFollowComponent::GetCurMonsterMoveType()
{
	return CurrMoveType;
}

FVector UMonsterFollowComponent::GetMovePosition()
{
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) 
		return FVector(0, 0, 0);

	MonsterFollowRole* e = (MonsterFollowRole*)(GetMEntity());
	if (e != nullptr)
	{
		if (e->getNextPosition() != FVector(0, 0, 0))
		{
			if ((e->getNextPosition() - e->Position()).Size2D() >= 0.1)
			{
				return e->getNextPosition();
			}
		}
	}
	return FVector(0, 0, 0);
}

void UMonsterFollowComponent::StartMoveTargetPostion()
{
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	FVector targetPosition = GetMovePosition();
	if (targetPosition == FVector(0, 0, 0)) return;

	float dist = (GetOwner()->GetActorLocation() - targetPosition).Size2D();
	if (dist <= 1)
	{
		SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE::StopMove);
		return;
	}
	TWeakObjectPtr<UMonsterFollowComponent>DelayAIComponentPtr(this);
	MoveTargetPostion(targetPosition, 0.01, FTraceCallback::CreateLambda([DelayAIComponentPtr](bool IsSuccess)
	{
		if (DelayAIComponentPtr.IsValid())
		{
			UMonsterFollowComponent* ThisPtr = DelayAIComponentPtr.Get();
			ThisPtr->SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE::StopMove);
		}
	}));
}

void UMonsterFollowComponent::MoveTargetPostion(const FVector& TargetPostion, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE::Moving);
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetPoint;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TracePostion = TargetPostion;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	UAIBlueprintHelperLibrary::SimpleMoveToLocation(Cast<AMonsterCharacter>(GetOwner())->GetController(), TargetPostion);
}

void UMonsterFollowComponent::ClearTraceData()
{
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTargetInfo.IsChasing = false;
	TraceTargetInfo.NearbyRange = 0.0f;
	TraceTargetInfo.TraceTarget = nullptr;
	TraceTargetInfo.IsStopMove = true;
	TraceTargetInfo.TracePostion = FVector::ZeroVector;
	TraceTargetInfo.TraceCallback = FTraceCallback();
}

void UMonsterFollowComponent::SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE MonsterMoveType)
{
	CurrMoveType = MonsterMoveType;
	ClearTraceData();
	Cast<AMonsterCharacter>(GetOwner())->GetCharacterMovement()->StopMovementImmediately();
}
