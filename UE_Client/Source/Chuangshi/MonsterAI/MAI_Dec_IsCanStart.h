// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "AIController.h"
#include "GameFramework/Pawn.h"
#include "BehaviorTree/BTDecorator.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MAI_Dec_IsCanStart.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Dec_IsCanStart : public UBTDecorator
{
	GENERATED_BODY()
protected:
	virtual bool CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const override;
};
