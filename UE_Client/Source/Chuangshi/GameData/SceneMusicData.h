#pragma once

#include "CsvTableRowBase.h"
#include "SceneMusicData.generated.h"

/**
* 文件名称：SceneMusicData.h
* 功能说明：场景资源配置表
* 文件作者：liushuang
* 目前维护：huting
* 创建时间：2016-11-23
*/

///@struct FSCENEMUSIC_DATA
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSCENEMUSIC_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///默认音乐资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TSoftObjectPtr<USoundBase> DefaultBgMusic;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TSoftObjectPtr<USoundBase> DefaultFightMusic;

	///场景背景音乐资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<TSoftObjectPtr<USoundBase>> BgMusicList;
	///场景战斗音乐资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<TSoftObjectPtr<USoundBase>> FightMusicList;

	///环境音效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<USoundBase> EnvironmentMusic;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "环境音效备注")
		FString Remarks;

public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		bool DefaultBgMusicIsNull = this->DefaultBgMusic.IsNull();

		bool DefaultFightMusicResult = this->DefaultFightMusic.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->DefaultFightMusic.ToString());

		bool IsError = false;

		if (DefaultBgMusicIsNull) {
			IsError = true;
			ResultInfo.CheckLog += FString::Printf(TEXT("DefaultBgMusic Format Is Empty! \n"));
		}
		else if(!FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->DefaultBgMusic.ToString())){
			IsError = true;
			ResultInfo.CheckLog += FString::Printf(TEXT("%s Is Error! \n"),*this->DefaultBgMusic.ToString());
		}
		if (!DefaultFightMusicResult) {
			IsError = true;
			ResultInfo.CheckLog += FString::Printf(TEXT("%s Is Error! \n"), *this->DefaultFightMusic.ToString());
		}
		for (int i = 0; i < this->BgMusicList.Num(); i++) {
			bool BgMusicListResult = this->BgMusicList[i].IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->BgMusicList[i].ToString());
			if (!BgMusicListResult) {
				IsError = true;
				ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error! \n"), *this->BgMusicList[i].ToString());
			}
		}
		for (int i = 0; i < this->FightMusicList.Num(); i++) {
			bool FightMusicListResult = this->FightMusicList[i].IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->FightMusicList[i].ToString());
			if (!FightMusicListResult) {
				IsError = true;
				ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error! \n"), *this->FightMusicList[i].ToString());
			}
		}
		if (IsError)
		{
			ResultInfo.Result = Error;
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
