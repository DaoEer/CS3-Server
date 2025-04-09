// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/BTDecorator.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MonsterAIEnum.h"
#include "MAI_Dec_CMD.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Dec_CMD : public UBTDecorator
{
	GENERATED_BODY()
protected:
	bool CheckCMD( UBehaviorTreeComponent& OwnerComp, MONSTER_AI_COMMAND cmd ) const;

};
