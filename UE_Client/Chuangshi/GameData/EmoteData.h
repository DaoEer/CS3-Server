#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "EmoteData.generated.h"

/**
* 文件名称：EmoteData.h
* 功能说明：表情符配置表
* 文件作者：FangPengJun
* 目前维护：FangPengJun
* 创建时间：2017-07-14
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FEMOTE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:		
	///表情类型，目前没用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "Type")
		int32  Type = 0;

	///标记，用于找富文本图片配置CS3SlateWidgetStyleAsset
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "Sign")
		FString Sign;

	///表情名称，用于在聊天输入框显示，显示为[#Name]
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "Name")
		FString Name;

	///表情描述，用于tips显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "Description")
		FString Description;

	///表情贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "Texture")
		TSoftObjectPtr<UTexture2D> Texture;

	///表情无目标时描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "NoTargetDes")
		FString NoTargetDes;

	///表情有目标时描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "EmoteData", DisplayName = "HasTargetDes")
		FString HasTargetDes;
};
