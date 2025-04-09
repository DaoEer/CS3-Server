// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "TipsCharacter.generated.h"

/*
* 文件名称：HeadProxyCharacter.h
* 功能说明：用于选择阵营时旁边的TIPS NPC
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-12-21
*/
UCLASS()
class CHUANGSHI_API ATipsCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	virtual void BeginPlay()override;
	virtual void OnCreateModelOver() override;

	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void CreateModel(FString ModelID);

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TypeID;///每个阵营对应ID
	

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
};
