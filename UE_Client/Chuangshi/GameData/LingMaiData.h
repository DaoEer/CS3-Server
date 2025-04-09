// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "LingMaiData.generated.h"

/**
* 文件名称：LingMaiData.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-07-05
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLingMaiData
{
	GENERATED_USTRUCT_BODY()
		FLingMaiData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "id")
		int32 id = 0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "name")
		FString name;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "camp")
		int32 camp = 0;
	/// 击杀数量
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "kill")
		int32 kill = 0;
	/// 死亡次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "dead")
		int32 dead = 0;
	/// 助攻次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "assist")
		int32 assist = 0;
	/// 占领次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "occupy")
		int32 occupy = 0;
	/// 抢夺次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "grab")
		int32 grab = 0;
};