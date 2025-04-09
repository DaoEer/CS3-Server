// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/BTService.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "MAI_Ser_SearchEnemy.generated.h"

DECLARE_STATS_GROUP(TEXT("CS3_AISearchEnemy"), STATGROUP_CS3_AISearchEnemy, STATCAT_Advanced);

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Ser_SearchEnemy : public UBTService
{
	GENERATED_BODY()
protected:
	virtual void TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds) override;
public:
	/** ËÑË÷·¶Î§ */
	UPROPERTY(Category = Service, EditAnywhere, meta = (ClampMin = "0.0"))
		float SearchDistance;
};
