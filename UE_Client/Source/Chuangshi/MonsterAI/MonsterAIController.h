// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "AIController.h"
#include "Entity/Monster/CMonster.h"
#include "BehaviorTree/BehaviorTree.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "MonsterAIEnum.h"
#include "SKill/SkillBase/Skill.h"
#include "MonsterCommonController.h"

#include "MonsterAIController.generated.h"



UCLASS(ClassGroup = AI, meta = (BlueprintSpawnableComponent))
class CHUANGSHI_API AMonsterAIController : public AMonsterCommonController
{
	GENERATED_BODY()

public:
	AMonsterAIController(const FObjectInitializer& ObjectInitializer = FObjectInitializer::Get());

public:
	
	int32 ControllerEntityID;

public:
	UPROPERTY(transient)
		UBehaviorTreeComponent* behaviorComponent;
	UPROPERTY(transient)
		UBlackboardComponent* blackboardComponent;
	virtual  void OnPossess(APawn* InPawn) override;
	virtual void OnUnPossess() override;


	KBEngine::Entity* GetControllerEntity();

	AActor* GetControllerActor();

	CMonster* GetSelfEntity();

	MONSTER_AI_MOVETYPE MoveType = MONSTER_AI_MOVETYPE::Stop;
	void SetMoveType(MONSTER_AI_MOVETYPE MoveType);
	bool CanMoveCheck(MONSTER_AI_MOVETYPE MoveType);

	virtual void OnMoveCompleted(FAIRequestID RequestID, const FPathFollowingResult& Result) override;

	TMap<MONSTER_AI_MOVETYPE, uint8> MovePriority;
	void InitMovePriority();

	
	///普通移动到某坐标
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
	EPathFollowingRequestResult::Type MoveToPos(const FVector& Dest, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
		bool bUsePathfinding = true, bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
		TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);
	
	///追击某Actor
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
	EPathFollowingRequestResult::Type MoveChaseActor(AActor* Goal, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
		bool bUsePathfinding = true, bool bCanStrafe = true,
		TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);
	
	///冲锋移动
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
	EPathFollowingRequestResult::Type MoveCharge(const FVector& Dest, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
		bool bUsePathfinding = true, bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
		TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);

	///行军移动
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
	EPathFollowingRequestResult::Type MoveMarch(const FVector& Dest, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
		bool bUsePathfinding = true, bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
		TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);

	///跟随移动
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
		EPathFollowingRequestResult::Type MoveFollow(const FVector& Dest, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
			bool bUsePathfinding = true, bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
			TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);

	///矩形移动
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
		EPathFollowingRequestResult::Type MoveRect(const FVector& Dest, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
			bool bUsePathfinding = true, bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
			TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);

	///圆形移动
	UFUNCTION(BlueprintCallable, Category = "MonsterAIController")
		EPathFollowingRequestResult::Type MoveCircle(const FVector& Dest, float MoveSpeed = 600.0, float AcceptanceRadius = -1, bool bStopOnOverlap = true,
			bool bUsePathfinding = true, bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
			TSubclassOf<UNavigationQueryFilter> FilterClass = NULL, bool bAllowPartialPath = true);

	void OnMoveMarchCompleted(FAIRequestID RequestID, const FPathFollowingResult & Result);

	void OnMoveFollowCompleted(FAIRequestID RequestID, const FPathFollowingResult & Result);
	
};























































