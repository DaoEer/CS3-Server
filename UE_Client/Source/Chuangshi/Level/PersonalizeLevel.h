// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Level/CS3LevelScriptActor.h"
#include "PersonalizeLevel.generated.h"

/**
* 文件名称：PersonalizeLevel.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2019-3-29
 */
UCLASS()
class CHUANGSHI_API APersonalizeLevel : public ACS3LevelScriptActor
{
	GENERATED_BODY()
public:
	virtual void BeginPlay() override;
	virtual void CreateDynamicRes() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void OnLoadLevelFinished() override;


	void SetModifyCurrBone();

	//设置画质，捏脸关卡强制完美画质
	void SetScreenPercentage();
	//恢复画质
	void ResetScreenPercentage();

	//捏脸Actor
	UPROPERTY(BlueprintReadOnly, Category = "CreateRoleLevel")
		AActor* ModifyFaceCharacter;
	
	UPROPERTY(BlueprintReadOnly, Category = "SelectRoleLevel")
		TArray<AActor*> AccountActors; ///<创建的角色BP_Account的列表
};
