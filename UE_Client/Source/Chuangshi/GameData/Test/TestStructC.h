#pragma once

#include "CoreMinimal.h"
#include "TestStructC.generated.h"

/**
* 文件名称：TestStructC.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-06
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTestStructC
{
	GENERATED_USTRUCT_BODY()
		FTestStructC() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "aa")
		int32 aa = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "bb")
		float bb = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "cc")
		FString cc;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "cc")
		TArray<FString> dd;
};