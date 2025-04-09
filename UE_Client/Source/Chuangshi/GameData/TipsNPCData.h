#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "TipsNPCData.generated.h"

/**
* 文件名称：TipsNPCData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-12-21
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTIPS_NPC_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	/// 模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ModelID = TEXT("Default");

	/// 动作ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ActionID = TEXT("Default");

	/// 特效ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EffectID = TEXT("Default");
		
	/// TipsNpc生成位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform ModelLocation ;

	/// 语音ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SoundID = TEXT("Default");

	/// 文字说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TextTips = TEXT("Default");

	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite,DisplayName = "备注")
		FString Remarks = TEXT("Default");
};