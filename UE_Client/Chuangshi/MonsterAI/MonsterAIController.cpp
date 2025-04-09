// Fill out your copyright notice in the Description page of Project Settings.
#include "MonsterAIController.h"

#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"
#include "Navigation/CrowdFollowingComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "KBEngine.h"

CONTROL_COMPILE_OPTIMIZE_START

//AMonsterAIController::AMonsterAIController(const FObjectInitializer& ObjectInitializer):
//	Super(ObjectInitializer.SetDefaultSubobjectClass<UCrowdFollowingComponent>(TEXT("PathFollowingComponent")))
//{
//	blackboardComponent = ObjectInitializer.CreateDefaultSubobject<UBlackboardComponent>(this, TEXT("BlackboardComp"));
//	BrainComponent = behaviorComponent = ObjectInitializer.CreateDefaultSubobject<UBehaviorTreeComponent>(this, TEXT("BehaviorComp"));
//	bWantsPlayerState = true;
//
//	InitMovePriority();
//}

AMonsterAIController::AMonsterAIController(const FObjectInitializer& ObjectInitializer)
{
	blackboardComponent = ObjectInitializer.CreateDefaultSubobject<UBlackboardComponent>(this, TEXT("BlackboardComp"));
	BrainComponent = behaviorComponent = ObjectInitializer.CreateDefaultSubobject<UBehaviorTreeComponent>(this, TEXT("BehaviorComp"));
	bWantsPlayerState = true;

	BrainComponent->SetComponentTickInterval(0.1f);
	
	InitMovePriority();
}



void AMonsterAIController::OnPossess(class APawn* inPawn)
{
	Super::OnPossess(inPawn);
	AMonsterCharacter* mc = Cast< AMonsterCharacter >(inPawn);

	if (!IsValid(mc) || mc->GetSelfEntity() == nullptr)
	{
		CS3_Log(TEXT("The AMonsterAIController possessed is not an instance of CMonster([%d])."), mc->GetSelfEntity() ? mc->GetSelfEntity()->ID() : 0);
		return;
	}
	CMonster* e = static_cast<CMonster*>(mc->GetSelfEntity());
	if ( e->BehaviorTree() )
	{
		if (e->BehaviorTree()->BlackboardAsset)
		{
			blackboardComponent->InitializeBlackboard(*(e->BehaviorTree()->BlackboardAsset));
			blackboardComponent->SetValueAsEnum(FName("CurrAIState"), uint8(MONSTER_AI_STATE::NORMAL));
			blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::FOLLOW));
			blackboardComponent->SetValueAsInt(FName("EntityID"), e->ID());
			
			
			//blackboardComponent->InitializeBlackboard(*e->BehaviorTree()->BlackboardAsset);
			//RunBehaviorTree(e->BehaviorTree());
			behaviorComponent->StartTree(*(e->BehaviorTree()) );
		}
		else
		{
			CS3_Log(TEXT("No blackboard is assigned to the CMonster's([%d]) behavior tree."), mc->GetSelfEntity()? mc->GetSelfEntity()->ID():0 );
		}
	}
	else
	{
		CS3_Log(TEXT("No behavior tree is assigned to CMonster([%d])."), mc->GetSelfEntity() ? mc->GetSelfEntity()->ID() : 0);
	}
}

void AMonsterAIController::OnUnPossess()
{
	Super::OnUnPossess();
	behaviorComponent->StopTree();
}

KBEngine::Entity* AMonsterAIController::GetControllerEntity()
{
	KBEngine::Entity* ControllerEntity = UGolbalBPFunctionLibrary::FindEntity(ControllerEntityID);
	return ControllerEntity ? ControllerEntity : nullptr;
}

AActor* AMonsterAIController::GetControllerActor()
{
	KBEngine::Entity* ControllerEntity = GetControllerEntity();
	
	return ControllerEntity ? ControllerEntity->Actor() : nullptr;
}


CMonster* AMonsterAIController::GetSelfEntity()
{
	
	AMonsterCharacter* MC = Cast<AMonsterCharacter>(GetCharacter());
	if (IsValid(MC))
	{
		return static_cast<CMonster*>(MC->GetSelfEntity());
	}
	return nullptr;
}

void AMonsterAIController::SetMoveType(MONSTER_AI_MOVETYPE newType)
{
	MoveType = newType;
	return;
}

void AMonsterAIController::InitMovePriority()
{
	MovePriority.Add(MONSTER_AI_MOVETYPE::Stop, 0);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveToPos, 0);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveChaseActor, 0);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveMarch, 0);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveCharge, 1);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveFollow, 0);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveRect, 0);
	MovePriority.Add(MONSTER_AI_MOVETYPE::MoveCircle, 0);
}

void AMonsterAIController::OnMoveCompleted(FAIRequestID RequestID, const FPathFollowingResult & Result)
{
	AMonsterCommonController::OnMoveCompleted(RequestID, Result);
	
	switch (MoveType)
	{
	case MONSTER_AI_MOVETYPE::MoveMarch:
		OnMoveMarchCompleted(RequestID, Result);
		break;
	case MONSTER_AI_MOVETYPE::Stop:
		break;
	case MONSTER_AI_MOVETYPE::MoveToPos:
		break;
	case MONSTER_AI_MOVETYPE::MoveChaseActor:
		break;
	case MONSTER_AI_MOVETYPE::MoveCharge:
		break;
	case MONSTER_AI_MOVETYPE::MoveFollow:
		OnMoveFollowCompleted(RequestID, Result);
		break;
	case MONSTER_AI_MOVETYPE::MoveRect:
		break;
	case MONSTER_AI_MOVETYPE::MoveCircle:
		break;
	default:
		break;
	}
	SetMoveType(MONSTER_AI_MOVETYPE::Stop);
}


bool AMonsterAIController::CanMoveCheck(MONSTER_AI_MOVETYPE NewType)
{
	return MovePriority[NewType] >= MovePriority[MoveType];
}

EPathFollowingRequestResult::Type AMonsterAIController::MoveToPos(const FVector& Dest, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bProjectDestinationToNavigation, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPaths)
{
	if (!CanMoveCheck(MONSTER_AI_MOVETYPE::MoveToPos))
	{
		return EPathFollowingRequestResult::Type::Failed;
	}
	EPathFollowingRequestResult::Type Result = MoveToLocation(Dest, AcceptanceRadius, bStopOnOverlap, bUsePathfinding, bProjectDestinationToNavigation, bCanStrafe, FilterClass, bAllowPartialPaths);
	if (Result == EPathFollowingRequestResult::Type::RequestSuccessful)
	{
		AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
		MCharacter->SetMaxWalkSpeed(MoveSpeed);
		SetMoveType(MONSTER_AI_MOVETYPE::MoveToPos);
	}
	return Result;
}

EPathFollowingRequestResult::Type AMonsterAIController::MoveChaseActor(AActor * Goal, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPath)
{
	if (!CanMoveCheck(MONSTER_AI_MOVETYPE::MoveChaseActor))
	{
		return EPathFollowingRequestResult::Type::Failed;
	}
	EPathFollowingRequestResult::Type Result = MoveToActor(Goal, AcceptanceRadius, bStopOnOverlap, bUsePathfinding, bCanStrafe, FilterClass, bAllowPartialPath);
	if (Result == EPathFollowingRequestResult::Type::RequestSuccessful)
	{
		AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
		MCharacter->SetMaxWalkSpeed(MoveSpeed);
		SetMoveType(MONSTER_AI_MOVETYPE::MoveChaseActor);
	}
	return Result;
}

EPathFollowingRequestResult::Type AMonsterAIController::MoveCharge(const FVector& Dest, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bProjectDestinationToNavigation, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPath)
{
	if (!CanMoveCheck(MONSTER_AI_MOVETYPE::MoveCharge))
	{
		return EPathFollowingRequestResult::Type::Failed;
	}
	EPathFollowingRequestResult::Type Result = MoveToLocation(Dest, AcceptanceRadius, bStopOnOverlap, bUsePathfinding, bProjectDestinationToNavigation, bCanStrafe, FilterClass, bAllowPartialPath);
	if (Result == EPathFollowingRequestResult::Type::RequestSuccessful)
	{
		AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
		MCharacter->SetMaxWalkSpeed(MoveSpeed);
		SetMoveType(MONSTER_AI_MOVETYPE::MoveCharge);
	}
	return Result;
}


EPathFollowingRequestResult::Type AMonsterAIController::MoveMarch(const FVector & Dest, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bProjectDestinationToNavigation, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPath)
{
	if (!CanMoveCheck(MONSTER_AI_MOVETYPE::MoveMarch))
	{
		return EPathFollowingRequestResult::Type::Failed;
	}
	EPathFollowingRequestResult::Type Result = MoveToLocation(Dest, AcceptanceRadius, bStopOnOverlap, bUsePathfinding, bProjectDestinationToNavigation, bCanStrafe, FilterClass, bAllowPartialPath);
	
	if (Result == EPathFollowingRequestResult::Type::RequestSuccessful)
	{
		AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
		MCharacter->SetMaxWalkSpeed(MoveSpeed);
		SetMoveType(MONSTER_AI_MOVETYPE::MoveMarch);
	}
	return Result;
}

EPathFollowingRequestResult::Type AMonsterAIController::MoveFollow(const FVector & Dest, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bProjectDestinationToNavigation, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPath)
{
	if (!CanMoveCheck(MONSTER_AI_MOVETYPE::MoveFollow))
	{
		return EPathFollowingRequestResult::Type::Failed;
	}
	EPathFollowingRequestResult::Type Result = MoveToLocation(Dest, AcceptanceRadius, bStopOnOverlap, bUsePathfinding, bProjectDestinationToNavigation, bCanStrafe, FilterClass, bAllowPartialPath);

	if (Result == EPathFollowingRequestResult::Type::RequestSuccessful)
	{
		AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
		if (IsValid(MCharacter))
		{
			MCharacter->SetMaxWalkSpeed(MoveSpeed);
			SetMoveType(MONSTER_AI_MOVETYPE::MoveFollow);
		}
	}
	if (Result == EPathFollowingRequestResult::Type::Failed)
	{
		AActor* ControllerActor = GetControllerActor();
		AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
		if (IsValid(ControllerActor) && IsValid(MCharacter))
		{
			if (FVector::Dist(ControllerActor->GetActorLocation(), MCharacter->GetActorLocation()) > 500.f)
			{
				Result = MoveToLocation(ControllerActor->GetActorLocation(), FMath::RandRange(200.f, 500.f), bStopOnOverlap, bUsePathfinding, bProjectDestinationToNavigation, bCanStrafe, FilterClass, bAllowPartialPath);
			}
		}
	}
	return Result;
}

EPathFollowingRequestResult::Type AMonsterAIController::MoveRect(const FVector & Dest, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bProjectDestinationToNavigation, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPath)
{
	return EPathFollowingRequestResult::Type();
}

EPathFollowingRequestResult::Type AMonsterAIController::MoveCircle(const FVector & Dest, float MoveSpeed, float AcceptanceRadius, bool bStopOnOverlap, bool bUsePathfinding, bool bProjectDestinationToNavigation, bool bCanStrafe, TSubclassOf<UNavigationQueryFilter> FilterClass, bool bAllowPartialPath)
{
	return EPathFollowingRequestResult::Type();
}

void AMonsterAIController::OnMoveMarchCompleted(FAIRequestID RequestID, const FPathFollowingResult & Result)
{
	if(Result.IsSuccess())
	{
		APawn* SelfPawn = GetPawn();
		FRotator Rotator = blackboardComponent->GetValueAsRotator(FName("Rotation"));
		SelfPawn->SetActorRotation(Rotator);
	}
	
}

void AMonsterAIController::OnMoveFollowCompleted(FAIRequestID RequestID, const FPathFollowingResult & Result)
{
	if (Result.IsSuccess())
	{
		APawn* SelfPawn = GetPawn();
		FRotator Rotator = blackboardComponent->GetValueAsRotator(FName("Rotation"));
		SelfPawn->SetActorRotation(Rotator);
	}
	else if (Result.Code == EPathFollowingResult::Blocked || Result.Code == EPathFollowingResult::Aborted)
	{
		AActor* Actor = GetControllerActor();
		if (IsValid(Actor))
		{
			AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetPawn());
			FVector TargetPos = blackboardComponent->GetValueAsVector(FName("TargetPos"));
			MonsterCharacter->SetActorLocation(TargetPos);
			//if (IsValid(MonsterCharacter) && FVector::Dist(MonsterCharacter->GetActorLocation(), TargetPos) >= 1000.0f)
			//{
			//	MonsterCharacter->SetActorLocation(TargetPos);
			//}
			//if (!MonsterCharacter->GetMovementComponent()->Velocity.IsZero() && FMath::Abs(MonsterCharacter->GetMovementComponent()->Velocity.X) < 1.0f && FMath::Abs(MonsterCharacter->GetMovementComponent()->Velocity.Y) < 1.0f)
			//{
			//	
			//}
		}
	}

}


CONTROL_COMPILE_OPTIMIZE_END