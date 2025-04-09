#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "MinimapData.generated.h"

/**
* 文件名称：MinimapData.h
* 功能说明：
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2019-01-02
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMINIMAP_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	//地图实际关卡尺寸（单位：厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "MiniMap", DisplayName = "LevelSize")
		FVector2D LevelSize;
	//关卡的原点坐标（单位：厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "MiniMap", DisplayName = "LevelOrign")
		FVector2D LevelOrign;
	//地图实际图片的纹理尺寸（单位：像素）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "MiniMap", DisplayName = "MiniMapSize")
		FVector2D MiniMapSize;
	//小地图可视范围的默认缩放倍数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "MiniMap", DisplayName = "ViewDefaultScale")
		float ViewDefaultScale = 0.5f;
	//是否显示小地图
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "MiniMap", DisplayName = "IsShowMiniMap")
		bool IsShowMiniMap = true;
	//地图贴图资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "MiniMap", DisplayName = "MapTexture")
		TSoftObjectPtr<UTexture2D> MapTexture;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		bool LevelSizeResult = LevelSize.X > 0 && LevelSize.Y > 0;
		bool MiniMapSizeResult = MiniMapSize.X > 0 && MiniMapSize.X < 16384 && MiniMapSize.Y > 0 && MiniMapSize.Y < 16384;
		bool ViewDefaultScaleResult = ViewDefaultScale > 0.0f;
		if (!LevelSizeResult) ResultInfo.CheckLog += FString::Printf(TEXT("Levelsize value must be greater than 0!  "));
		if (!MiniMapSizeResult) ResultInfo.CheckLog += FString::Printf(TEXT("MiniMapSize value is config error!  "));
		if (!ViewDefaultScaleResult) ResultInfo.CheckLog += FString::Printf(TEXT("ViewDefaultScale value must be greater than 0!  "));
		bool MapTextureResult = true;
		if (MapTexture.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(MapTexture.ToString()))
			{
				MapTextureResult = false;
				ResultInfo.CheckLog += FString::Printf(TEXT("MapTexture resource does not exist!  "));
			}
		}
		if (LevelSizeResult && MiniMapSizeResult && ViewDefaultScaleResult && MapTextureResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};