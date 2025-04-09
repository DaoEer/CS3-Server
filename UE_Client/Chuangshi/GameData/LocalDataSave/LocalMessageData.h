// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "GameData/MessageData.h"
#include "LocalMessageData.generated.h"

/**
* 文件名称：LocalMessageData.h
* 功能说明：提示框今日不再提示设置数据
* 文件作者：gaoruilian
* 目前维护：gaoriulian
* 创建时间：2019-09-3
*/


UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API ULocalMessageData : public USaveGame
{
	GENERATED_BODY()
public:
	ULocalMessageData();
	UFUNCTION(BlueprintCallable, Category = "LocalMessageData")
		const FString& GetFileName();

	UFUNCTION(BlueprintCallable, Category = "LocalMessageData")
		void SaveDataToFile(TArray<FUnRepeatData> data);
	
	TArray<FUnRepeatData> GetMessageData();
private:
	UPROPERTY(VisibleAnywhere, Category = "LocalMessageData")
		TArray<FUnRepeatData>  MessageSettingData;
public:
	///初始化数据
	void InitLocalMessageData();
private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字

};
