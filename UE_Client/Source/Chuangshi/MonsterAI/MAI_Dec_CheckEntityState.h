// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "BehaviorTree/BTDecorator.h"
#include "GameData/GameDeFine.h"
#include "MAI_Dec_CheckEntityState.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMAI_Dec_CheckEntityState : public UBTDecorator
{
	GENERATED_BODY()
protected:
	bool EntityIsState(UBehaviorTreeComponent& OwnerComp, ENTITY_STATE state ) const;
};
