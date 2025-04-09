#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "TitleData.generated.h"

/**
* 文件名称：TitleData.h
* 功能说明：称号配置表
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-08-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTitleData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//称号ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TitleID = 0;
	//称号名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TitleName;
	//持续时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString LimitTime;
	//获取途径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Path;
	//特殊称号描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;
	//持有效果的说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EffectDescription;
	//持有效果ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString HoldEffectID;
	//属性ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PropertyID;
	//是否在全部称号中显示，配置0为默认显示，配置1为不显示 
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IsShow = 0;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool TitleNameResult = !this->TitleName.IsEmpty();
		bool LimitTimeResult = !this->LimitTime.IsEmpty() && this->LimitTime.IsNumeric();
		bool PathResult = !this->Path.IsEmpty();
		bool DescriptionResutl = !this->Description.IsEmpty();
		bool result = TitleNameResult && LimitTimeResult && PathResult && DescriptionResutl;
		if (result)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
		}
		if (!TitleNameResult) ResultInfo.CheckLog += FString::Printf(TEXT("TitleName is empty!  "));
		if (!LimitTimeResult) ResultInfo.CheckLog += FString::Printf(TEXT("LimitTime: %s is config error!  "), *this->LimitTime);
		if (!PathResult) ResultInfo.CheckLog += FString::Printf(TEXT("Path is empty!  "));
		if (!DescriptionResutl) ResultInfo.CheckLog += FString::Printf(TEXT("Description is empty!  "));
		if (!result) ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};