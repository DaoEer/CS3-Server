#pragma once
#include "CoreMinimal.h"
#include "ZYJJRewardData.generated.h"
/**
* 文件名称：ZYJJRewardData.h
* 功能说明：阵营5人竞技奖励数据结构
* 文件作者：fangpengjun
* 目前维护：fangpengjun
* 创建时间：2020-01-09
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FZYJJRewardData
{
	GENERATED_USTRUCT_BODY()
public:
	//经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Exp;
	//功勋
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Feats;
	//军功
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Exploit;
	//帮贡
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Contribution;
};