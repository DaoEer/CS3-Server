#pragma once

#include "CsvTableRowBase.h"
#include "AudioData.generated.h"

/**
* 文件名称：AudioData.h
* 功能说明：声音资源总表
* 文件作者：LiuShuang
* 目前维护：huting
* 创建时间：2016-11-03
*/

class USoundBase;
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAUDIO_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	/** 音频资源 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray< TSoftObjectPtr<USoundBase>> AudioAsset;

	/** 音频描叙 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;

public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		bool IsError = false;
		if (this->AudioAsset.Num() == 0) {
			IsError = true;
			ResultInfo.CheckLog += FString::Printf(TEXT("Audio Asset Format Is Empty, "));
		}
		else {
			for (int i = 0; i < this->AudioAsset.Num(); i++) {
				if (this->AudioAsset[i].IsNull()) {
					IsError = true;
					ResultInfo.CheckLog += FString::Printf(TEXT("Audio Asset Element %d Is None, "), i + 1);
				}
				else if (!FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->AudioAsset[i].ToString())) {
					IsError = true;
					ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error, "), *this->AudioAsset[i].ToString());
				}
				else {
					IsError = false;
				}
			}
		}
		if (IsError)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += TEXT("\n");
		}
		else {
			ResultInfo.Result = Ok;
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

UENUM(Blueprintable)
enum class EAUDIOCOMPTYLE : uint8
{
	NONE = 0,		//默认
	SKILL = 1,		//技能
	HOLDEEFFECT = 2,//持有效果
	EFFECT = 3,		//光效
};