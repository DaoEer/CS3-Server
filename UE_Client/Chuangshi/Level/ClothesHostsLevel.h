// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Level/CS3LevelScriptActor.h"
#include "ClothesHostsLevel.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API AClothesHostsLevel : public ACS3LevelScriptActor
{
	GENERATED_BODY()
public:
	virtual void BeginPlay() override;
	virtual void CreateDynamicRes() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void OnLoadLevelFinished() override;

	void HideSettleAccounts();
	
	//设置画质，云裳阁关卡强制完美画质
	void SetScreenPercentage();
	//恢复画质
	void ResetScreenPercentage();

	//捏脸Actor
	UPROPERTY(BlueprintReadOnly, Category = "AClothesHostsLevel")
		AActor* ModifyFaceCharacter;
};
