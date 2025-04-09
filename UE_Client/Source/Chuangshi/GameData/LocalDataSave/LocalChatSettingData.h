// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "GameData/ChatSettingData.h"
#include "LocalChatSettingData.generated.h"

/**
* 文件名称：LocalChatSettingData.h
* 功能说明：聊天设置数据
* 文件作者：huting
* 目前维护：huting
* 创建时间：2019-09-3
*/


UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API ULocalChatSettingData : public USaveGame
{
	GENERATED_BODY()
public:
	ULocalChatSettingData();
	UFUNCTION(BlueprintCallable, Category = "LocalChatSettingData")
		const FString& GetFileName();
	/**
	*保存默认数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalChatSettingData")
		void DefaultDataToFile();

	UFUNCTION(BlueprintCallable, Category = "LocalChatSettingData")
		void SaveDataToFile(FChatSettingData data);
	
	FChatSettingData GetDefaultChatSettingData();
private:
	///初始化数据
	void InitLocalChatSettingData();

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalChatSettingData")
		FChatSettingData  ChatSettingData;
private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字

};
