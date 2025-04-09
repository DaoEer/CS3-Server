// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "GameData/ShortcutKey.h"
#include "LocalStortcutKeyData.generated.h"

/**
* 文件名称：LocalChatSettingData.h
* 功能说明：快捷键设置数据
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2020-05-06
*/

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API ULocalStortcutKeyData : public USaveGame
{
	GENERATED_BODY()
		
public:
	ULocalStortcutKeyData();
	UFUNCTION(BlueprintCallable, Category = "LocalChatSettingData")
		const FString& GetFileName();
	
	/**
	*保存快捷键设置数据
	*
	*@param SHORTCUTKEY_TYPE_ENUM 快捷键分类
	*@param TArray<FSHORTCUTKEY> 快捷键数组
	*
	*@return 无
	*/
	void SaveShortcutKeyDataByTypeToFile(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> NewKeys);

	/**
	*保存快捷键设置数据
	*
	*@param TArray<FSHORTCUTKEY> 快捷键数组
	*
	*@return 无
	*/
	void SaveShortcutKeyDataToFile(TArray<FSHORTCUTKEY> NewKeys);

public:
	/** 已修改快捷键保存链表 */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		TArray<FSHORTCUTKEY> ChangedKeys;
private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字
};