// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/Tasks/BTTask_BlueprintBase.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MonsterAIEnum.h"
#include "MAI_Task_CMD.generated.h"


/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Task_CMD : public UBTTask_BlueprintBase
{
	GENERATED_BODY()

public:
	virtual EBTNodeResult::Type ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) override;

	virtual MONSTER_AI_COMMAND_PROCESS ExecuteCMD( UBehaviorTreeComponent& OwnerComp );
	virtual void OverCMD( UBehaviorTreeComponent& OwnerComp );
	
};
