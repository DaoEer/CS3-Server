#pragma once
#include "CoreMinimal.h"
#include "CampYCJMDData.generated.h"

/**
* 文件名称：CampYCJMDData.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020/02/28
*/


USTRUCT(BlueprintType)
struct CHUANGSHI_API FCampYCJMDData
{
	GENERATED_USTRUCT_BODY()
		FCampYCJMDData() {};
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
};
