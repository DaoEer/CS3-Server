// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "KBEngine.h"
#include "Component/AvatarFilterActorComponent.h"
#include "MonsterOptimizeComponent.generated.h"

/**
 * 
 */

UCLASS()
class CHUANGSHI_API UMonsterOptimizeComponent : public UAvatarFilterActorComponent
{
	GENERATED_BODY()
	typedef UAvatarFilterActorComponent Supper;
public:
	UMonsterOptimizeComponent();
	~UMonsterOptimizeComponent();

	virtual void OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void SetPosition(const FVector& position, int32 parentID) override;
	virtual void SetDirection(const FVector& direction, int32 parentID) override;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;


};
