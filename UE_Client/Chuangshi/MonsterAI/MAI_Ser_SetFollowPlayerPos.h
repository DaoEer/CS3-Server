// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/BTService.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MAI_Ser_SetFollowPlayerPos.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Ser_SetFollowPlayerPos : public UBTService
{
	GENERATED_BODY()
public:
	virtual void TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds) override;
};
