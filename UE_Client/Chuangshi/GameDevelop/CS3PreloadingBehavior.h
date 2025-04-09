// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "PreloadingBehavior.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3PreloadingBehavior.generated.h"

/**
 * 
 */
UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UCS3PreloadingBehavior : public UPreloadingBehavior
{
	GENERATED_BODY()
public:
    UFUNCTION(BlueprintImplementableEvent)
    void OnPostCS3GameInstanceInit(UUECS3GameInstance* CS3GameInstance);
};
