#pragma once

#include "CoreMinimal.h"
#include "TestStructA.h"
#include "TestStructAArray.generated.h"

/**
* 文件名称：TestStructAArray.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-06
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTestStructAArray
{
	GENERATED_USTRUCT_BODY()
		FTestStructAArray() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "list")
		TArray<FTestStructA> StructAArray;

};