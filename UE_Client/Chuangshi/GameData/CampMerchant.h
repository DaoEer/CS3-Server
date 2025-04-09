#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "CampMerchant.generated.h"

/**
* 文件名称：CampMerchant.h
* 功能说明：阵营商人数据相关
* 文件作者：zhuangzhenguo
* 目前维护：zhuangzhenguo
* 创建时间：2019-02-18
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAMP_MERCHANT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:

	///阵营商人ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CAMP_MERCHANT_DATA", DisplayName = "CampMerChantId")
		int32  UCampMerChantId= 0;
	///阵营商人名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CAMP_MERCHANT_DATA", DisplayName = "CampMerChantName")
		FString  UCampMerChantName;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (UCampMerChantName.TrimStartAndEnd().IsEmpty())
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("CampMerChantName cannot be empty!\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};