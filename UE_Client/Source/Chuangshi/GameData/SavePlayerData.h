#pragma once

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "SavePlayerData.generated.h"

/**
* 文件名称：SavePlayerData.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-05-03
*/

/**
* 使用OpenLevel过关卡，会销毁玩家，需要重新创建玩家，玩家的部分数据需要保存
*/


UCLASS(BlueprintType)
class USavePlayerData : public USaveGame
{
	GENERATED_BODY()
public:
	///Cagetory = SaveGame,这样写可以，可以方便把此内容序列化到文件中保存，采用SaveGameToSlot和LoadGameFromSlot
	UPROPERTY(BlueprintReadOnly, Category = SaveGame)
		TMap<int, FString> CurPartMap;
	UPROPERTY(BlueprintReadOnly, Category = SaveGame)
		bool IsValidData;			///< 此数据在被Load之后就失效了

};
