// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/BTDecorator.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MAI_Dec_CheckPlayerDistance.generated.h"

/**
 *
 */
UCLASS()
class CHUANGSHI_API UMAI_Dec_CheckPlayerDistance : public UBTDecorator
{
	GENERATED_BODY()
protected:
	virtual bool CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const override;

public:
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
		float Distance;
};
