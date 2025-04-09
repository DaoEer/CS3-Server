// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "FrozenFightData.generated.h"

/**
* 文件名称：FrozenFightData.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2018-08-16
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFrozenFightData
{
	GENERATED_USTRUCT_BODY()
		FFrozenFightData() {};
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
	/// 提交冰晶个数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "submit")
		int32 submits = 0;
};