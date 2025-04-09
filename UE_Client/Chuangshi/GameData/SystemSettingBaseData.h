#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "SystemSettingBaseData.generated.h"

/**
* 文件名称：SystemSettingBaseData.h
* 功能说明：系统设置基础数据配置
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-10-14
*/

/**
*	数据类型
*/
UENUM(Blueprintable)
enum class ESYSTEM_BASEDATA_TYPE_ENUM : uint8
{
	Resolution = 0,		///< 游戏分辨率
	CameraLen,			///< 镜头距离（摄像机与角色的距离）
	FocalLen,			///< 焦距
	ViewAngle,			///< 视角
	UIScale,			///< UI缩放
};

///@struct FSYSTEMBASESETTING_DATA 游戏设置配置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSYSTEM_SETTING_BASE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///数据类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SystemSettingBaseData")
		ESYSTEM_BASEDATA_TYPE_ENUM DataType;
	///数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SystemSettingBaseData")
		FString ConfigData;
};