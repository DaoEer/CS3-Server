#pragma once
#include "CsvTableRowBase.h"
#include "CameraParamsEventData.generated.h"

/**
* 文件名称：CameraParamsEventData.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017--7-11
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAMERA_PARAMS_EVENT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	/** UI屏蔽相关 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HideUI;

	/**屏蔽键鼠 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HideInput;

	/**是否可中断 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool CanBreak;

	/** AOI半径(单位:米) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Aoi;

	/**时间 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Time;

	/**旋转角度*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FRotator Rotator;

	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (Aoi != "")
		{
			if (Aoi.TrimStartAndEnd() != "0" && Aoi.TrimStartAndEnd() != "0.0" && FCString::Atof(*Aoi) == 0)
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Aoi\" config error"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};