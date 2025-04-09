#pragma once

#include "CsvTableRowBase.h"
#include "TextEmoteData.generated.h"

/**
* 文件名称：TextEmoteData.h
* 功能说明：文字表情配置表
* 文件作者：FangPengJun
* 目前维护：FangPengJun
* 创建时间：2017-07-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTEXT_EMOTE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	/*表情类型*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Type")
		int32  Type = 0;

	/*表情符号*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Sign")
		FString Sign;

	/*表情名称*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Name")
		FString Name;

	/*表情无目标时描述*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NoTargetDes")
		FString NoTargetDes;

	/*表情有目标时描述*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HasTargetDes")
		FString HasTargetDes;


};