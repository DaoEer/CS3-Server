// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/BTService.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MAI_Ser_UpdateGuardTargetPos.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Ser_UpdateGuardTargetPos : public UBTService
{
	GENERATED_BODY()
protected:
	virtual void TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds) override;
};
