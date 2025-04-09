// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "MAI_Dec_CheckEntityState.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MAI_Dec_IsStateWarn.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Dec_IsStateWarn : public UMAI_Dec_CheckEntityState
{
	GENERATED_BODY()
protected:
	virtual bool CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const override;
};
