#pragma once

#include "GameData/CS3Object.h"
#include "GameData/GameDeFine.h"
#include "HoldEffectDataType.generated.h"

/**
* 文件名称：HoldEffectDataType.h
* 功能说明：持有效果的数据
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-11-13
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectDataType :public UCS3Object
{
	GENERATED_BODY()
public:
	UHoldEffectDataType();
	~UHoldEffectDataType();
public:
	void setTempData(FString key, FVariant value);
	FVariant getTempData(FString key, FVariant default = FVariant(NULL));
public:
	int32 index;
	HOLD_EFFECT_SOURCE_TYPE sourceType;
	int32 sourceID;
	int32 configIndex;
	int32 buffIndex;
	int32 casterID;
	TMap<FString, FVariant> param;
};