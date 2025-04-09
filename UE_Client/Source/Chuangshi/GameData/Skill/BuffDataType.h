#pragma once

#include "GameData/CS3Object.h"
#include "GameData/GameDeFine.h"
#include "BuffDataType.generated.h"

/**
* 文件名称：BuffDataType.h
* 功能说明：buff数据
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-12-19
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffDataType :public UCS3Object
{
	GENERATED_BODY()
public:
	UBuffDataType();
	~UBuffDataType();

public:
	void setTempData(FString key, FVariant value);
	FVariant getTempData(FString key, FVariant default = FVariant(NULL));
	
public:
	int32 index = 0;
	int32 buffID = 0;
	float holdTime = 0.0;
	int64 endTime = 0;
	FTimerHandle timerID;
	int32 casterID = 0;
	int32 casterIsSelf = 0;
	int32 layer = 1;
	FString className = "";
	TMap<FString, FVariant> param;
};


