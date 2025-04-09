// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/ServerCharacter.h"
#include "NPCBaseCharacter.generated.h"

class GameObject;
class UCapsuleComponent;
/**
 * 
 */
UCLASS()
class CHUANGSHI_API ANPCBaseCharacter : public AServerCharacter
{
	GENERATED_BODY()

public:
	ANPCBaseCharacter();

	virtual void InitCharacterComponent()override;

	virtual void UpdateCapsuleComponent() override;
	
public:
	UFUNCTION(BlueprintPure, Category = "NPCBaseCharacter")
		virtual int32 GetFinalfaction();///<获取最终势力

};
