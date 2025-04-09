// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "LocalKitbagData.generated.h"

/**
* 文件名称：ULocalItemData.h
* 功能说明：物品本地数据
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-07-30
*/

class UItemBase;


USTRUCT(BlueprintType)
struct CHUANGSHI_API FLOCAL_ITEM_DATA
{
	GENERATED_USTRUCT_BODY()

	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ItemID;
	///物品UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ItemUID;
	///创建时间(服务器时间，与客户端时间)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FDateTime CreateTime;
	///是否显示 new 字样
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isShowNew;

};

UCLASS()
class CHUANGSHI_API ULocalKitbagData : public USaveGame
{
	GENERATED_BODY()	
public:
	ULocalKitbagData();
	UFUNCTION(BlueprintCallable, Category = "LocalTongSettingData")
		const FString& GetFileName();

	void AddLocalItem(UItemBase* Item);

	void RemoveLocalItem(const FString& ItemUID);

	bool IsShowNewTip(const FString& ItemUID);

	void SaveNewTip(const FString& ItemUID, const bool& IsShowNew);

private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字
public:
	///物品保存数据
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalTongSettingData")
		TMap<FString, FLOCAL_ITEM_DATA> KitbagData;
};
