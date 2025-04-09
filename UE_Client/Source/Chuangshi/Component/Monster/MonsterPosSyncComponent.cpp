// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterPosSyncComponent.h"
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
#include "Component/Role/JumpComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START
UMonsterPosSyncComponent::UMonsterPosSyncComponent()
{
	//bWantsBeginPlay = false;
	PrimaryComponentTick.bCanEverTick = true;
}
KBEngine::Entity* UMonsterPosSyncComponent::GetMEntity()
{
	AMonsterCharacter* owner = Cast<AMonsterCharacter>(GetOwner());

	if (!IsValid(owner)) return nullptr;

	return owner->GetSelfEntity();
}
void UMonsterPosSyncComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	if (Cast<AMonsterCharacter>(GetOwner())->IsState(ENTITY_STATE::EntityStateDead))return;
	UStateInterface* StateInterface = Cast<AMonsterCharacter>(GetOwner())->GetEntityInterface_Cache().StateInterface;
	if (StateInterface && StateInterface->IsActionForbid(ACTION_FLAG::ACTION_FORBID_MOVE))
	{
		SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
		return;
	}
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------UMonsterPosSyncComponent::TickComponent--------------"));
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
		if (GetCurMonsterMoveType() != MONSTER_MOVE_TYPE::None)
		{
			if (GetCurMonsterMoveType() == MONSTER_MOVE_TYPE::Chase)
			{
				if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetActor)
				{
					if (IsValid(TraceTargetInfo.TraceTarget))
					{
						if (UGolbalBPFunctionLibrary::GetActorDistance(GetOwner(), TraceTargetInfo.TraceTarget) <= TraceTargetInfo.NearbyRange*100.0f)
						{
							TraceTargetInfo.TraceCallback.ExecuteIfBound(true);
							if (TraceTargetInfo.IsStopMove)
							{
								SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
							}
							TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(true);
						}
					}
					else
					{
						TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
						SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
						TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(false);
					}
				}
			}
			else if (GetCurMonsterMoveType() == MONSTER_MOVE_TYPE::Wander)
			{
				if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetPoint)
				{
					float dist = FVector::Dist(GetOwner()->GetActorLocation(), TraceTargetInfo.TracePostion);
					if (dist <= TraceTargetInfo.NearbyRange*100.0f)
					{
						TraceTargetInfo.TraceCallback.ExecuteIfBound(true);
						if (TraceTargetInfo.IsStopMove)
						{
							SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
						}
						TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(true);
					}
				}
			}
			else if (GetCurMonsterMoveType() == MONSTER_MOVE_TYPE::GoBack)
			{
				if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetPoint)
				{
					if (FVector::Dist(GetOwner()->GetActorLocation(), TraceTargetInfo.TracePostion) <= TraceTargetInfo.NearbyRange*100.0f)
					{
						TraceTargetInfo.TraceCallback.ExecuteIfBound(true);
						if (TraceTargetInfo.IsStopMove)
						{
							SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
						}
						TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(true);
					}
				}
			}
			//UPathFollowingComponent* PFollowComp = nullptr;
					//UObject* PFollowCompObj = nullptr;
					//GetWorld()->GetFirstPlayerController()->InitNavigationControl(PFollowCompObj);
					//以下几类移动都是引擎控制，所以需要自己去检查是否到达
			AController* Controller = Cast<AServerCharacter>(GetOwner())->GetController();
			UPathFollowingComponent* PFollowComp = nullptr;
			if (IsValid(Controller))
			{
				PFollowComp = UGolbalBPFunctionLibrary::InitNavigationControl(*Controller);
			}
			//UPathFollowingComponent * PFollowComp = Cast<UPathFollowingComponent>(PFollowCompObj);
			if (PFollowComp && PFollowComp->GetStatus() != EPathFollowingStatus::Moving)
			{
				TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
				SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
				TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(false);
			}
		}
		else
		{
			if (Cast<AMonsterCharacter>(GetOwner())->IsState(ENTITY_STATE::EntityStateFight))
			{
				ChaseTarget();
			}
			else if (Cast<AMonsterCharacter>(GetOwner())->IsState(ENTITY_STATE::EntityStateFree))
			{
				StartWander();
			}
		}
	}
}

MONSTER_MOVE_TYPE UMonsterPosSyncComponent::GetCurMonsterMoveType()
{
	return CurrMoveType;
}

MONSTER_MOVE_TYPE UMonsterPosSyncComponent::GetLastMonsterMoveType()
{
	return LastMoveType;
}

void UMonsterPosSyncComponent::ChaseTarget()
{
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	int32 targetID = GetTargetID();
	if (targetID)
	{
		KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(targetID);
		KBEngine::Entity* Entity = Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity();
		if (Entity == nullptr || TargetEntity == nullptr || !IsValid(TargetEntity->Actor()))
		{
			SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
			return;
		}
		APlayerCharacter* TargetActor = Cast<APlayerCharacter>(TargetEntity->Actor());
		if (!TargetActor)
		{
			SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
			return;
		}
		if (TargetActor->JumpComponent->IsJumpState)
		{
			SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
			return;
		}
		float Distance = Entity->GetDefinedProperty(TEXT("distance"));
		if (UGolbalBPFunctionLibrary::GetActorDistance(GetOwner(), TargetActor) <= Distance * 100.0f)
		{
			SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
			return;
		}
		TWeakObjectPtr<UMonsterPosSyncComponent>DelayAIComponentPtr(this);
		TraceTargetActor(TargetActor, Distance, FTraceCallback::CreateLambda([DelayAIComponentPtr](bool IsSuccess)
		{
			if (DelayAIComponentPtr.IsValid())
			{
				UMonsterPosSyncComponent* ThisPtr = DelayAIComponentPtr.Get();
				ThisPtr->SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
				if (IsSuccess)
				{
					ThisPtr->AttackTarget();
				}
			}
		}));
	}
}

void UMonsterPosSyncComponent::AttackTarget()
{
	//攻击玩家
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	KBEngine::Entity* Entity = Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity();
	if (Entity == nullptr) return;
	UMonsterInterface * MonsterInterface = Cast<UMonsterInterface>(((GameObject*)Entity)->Interface_Cache.GameObjectInterface);
	if (MonsterInterface)
	{
		MonsterInterface->RPC_CELL_onAttackTarget();
	}
	//KBEngine::FVariantArray args;
	//Entity->CellCall(TEXT("CELL_onAttackTarget"), args);
}

int32 UMonsterPosSyncComponent::GetTargetID()
{
	//寻找一定范围内的可攻击目标
	//if (CurrentTargetID) return;
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return 0;
	//获取范围内的entity
	TArray<AActor*> ActorList;
	KBEngine::Entity* Entity = Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity();
	float EnemyRange = Entity->GetDefinedProperty(TEXT("enemyRange"));
	ActorList = UGolbalBPFunctionLibrary::GetPlayersInRange(APlayerCharacter::StaticClass(), EnemyRange * 100, GetOwner()->GetActorLocation());
	UGolbalBPFunctionLibrary::SortActorByDistance(ActorList, GetOwner());
	//选择玩家为攻击目标
	if (ActorList.Num())
	{
		return Cast<APlayerCharacter>(ActorList[0])->EntityId;
	}
	return 0;
}

void UMonsterPosSyncComponent::StartWander()
{
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	KBEngine::Entity* Entity = Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity();
	float wanderRange = Entity->GetDefinedProperty(TEXT("wanderRange"));
	float radius = FMath::FRandRange(0.0, wanderRange * 2.0 * 100.0);
	float theta = FMath::FRandRange(0.0, 360.0);
	FVector targetPosition = Cast<AMonsterCharacter>(GetOwner())->SpawnPosition + FVector(FMath::Sin(PI / 180.0 * theta)*radius, FMath::Cos(PI / 180.0*theta)*radius, 0);
	if (FVector::Dist(GetOwner()->GetActorLocation(), targetPosition) < 1.0)
	{
		SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
		return;
	}
	TWeakObjectPtr<UMonsterPosSyncComponent>DelayAIComponentPtr(this);
	WanderTargetPostion(targetPosition, 0.01, FTraceCallback::CreateLambda([DelayAIComponentPtr](bool IsSuccess)
	{
		if (DelayAIComponentPtr.IsValid())
		{
			UMonsterPosSyncComponent* ThisPtr = DelayAIComponentPtr.Get();
			ThisPtr->SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
		}
	}));
}



void UMonsterPosSyncComponent::BeHitBack()
{
	SetMonsterMoveType(MONSTER_MOVE_TYPE::HitBack);
}

void UMonsterPosSyncComponent::GoBack()
{
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	FVector targetPosition = Cast<AMonsterCharacter>(GetOwner())->SpawnPosition;
	if (FVector::Dist(GetOwner()->GetActorLocation(), targetPosition) < 1.0)
	{
		SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
		return;
	}
	TWeakObjectPtr<UMonsterPosSyncComponent>DelayAIComponentPtr(this);
	BackTargetPostion(targetPosition, 0.01, FTraceCallback::CreateLambda([DelayAIComponentPtr](bool IsSuccess)
	{
		if (DelayAIComponentPtr.IsValid())
		{
			UMonsterPosSyncComponent* ThisPtr = DelayAIComponentPtr.Get();
			ThisPtr->SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
		}
	}));
}

void UMonsterPosSyncComponent::TraceTargetActor(const AActor* TargetActor, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	SetMonsterMoveType(MONSTER_MOVE_TYPE::Chase);
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TraceTarget = (AActor*)TargetActor;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	UAIBlueprintHelperLibrary::SimpleMoveToActor(Cast<AMonsterCharacter>(GetOwner())->GetController(), TargetActor);
}
void UMonsterPosSyncComponent::WanderTargetPostion(const FVector& TargetPostion, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	SetMonsterMoveType(MONSTER_MOVE_TYPE::Wander);
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetPoint;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TracePostion = TargetPostion;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	UAIBlueprintHelperLibrary::SimpleMoveToLocation(Cast<AMonsterCharacter>(GetOwner())->GetController(), TargetPostion);
}

void UMonsterPosSyncComponent::BackTargetPostion(const FVector& TargetPostion, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove /*= true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	SetMonsterMoveType(MONSTER_MOVE_TYPE::GoBack);
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetPoint;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TracePostion = TargetPostion;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	UAIBlueprintHelperLibrary::SimpleMoveToLocation(Cast<AMonsterCharacter>(GetOwner())->GetController(), TargetPostion);
}

void UMonsterPosSyncComponent::ClearTraceData()
{
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTargetInfo.IsChasing = false;
	TraceTargetInfo.NearbyRange = 0.0f;
	TraceTargetInfo.TraceTarget = nullptr;
	TraceTargetInfo.IsStopMove = true;
	TraceTargetInfo.TracePostion = FVector::ZeroVector;
	TraceTargetInfo.TraceCallback = FTraceCallback();
}

void UMonsterPosSyncComponent::SetMonsterMoveType(MONSTER_MOVE_TYPE MonsterMoveType)
{
	//set move type
	LastMoveType = CurrMoveType;
	CurrMoveType = MonsterMoveType;
	ClearTraceData();
	Cast<AMonsterCharacter>(GetOwner())->GetCharacterMovement()->StopMovementImmediately();
}
CONTROL_COMPILE_OPTIMIZE_END
