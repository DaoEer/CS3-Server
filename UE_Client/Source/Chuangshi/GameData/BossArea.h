// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/GameDeFine.h"
#include "GameData/CsvTableRowBase.h"
#include "BossArea.generated.h"

/**
* 文件名称：BossArea.h
* 功能说明：BOSS战斗区域
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-1-5
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBOSS_AREA_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///BOSS ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BossArea", DisplayName = "ScriptID")
		FString ScriptID;
	///多边形区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BossArea", DisplayName = "Polygon")
		TArray<FVector> Polygon;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool ScriptIDResult = !ScriptID.IsEmpty() && ScriptID.TrimStartAndEnd().IsNumeric();
		bool PolygonResult = Polygon.Num() > 0;
		bool result = ScriptIDResult && PolygonResult;
		if (result)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!ScriptIDResult) ResultInfo.CheckLog += FString::Printf(TEXT("ScriptID: \"%s\" is config error!  "), *ScriptID);
			if (!PolygonResult) ResultInfo.CheckLog += FString::Printf(TEXT("Polygonis is empty!"));
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLIGHT_WALL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///光墙类型
	///支持：
	///	位面边界范围显示（@CST-1204）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "WallType")
		AREA_LIGHT_WALL_TYPE_ENUM WallType;
	///等分距离（厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "EqualLength")
		float EqualLength;
	///有效落差高度（厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "ValidHeight")
		float ValidHeight;
	///忽略对象
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "Object")
		TArray<FString> Object;
	///射线向上检测的距离（厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "UpLength")
		float UpLength;
	///射线向下检测的距离（厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "DownLength")
		float DownLength;
	///高度修正（厘米）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "HeightCorrection")
		float HeightCorrection;
	///是否闭合
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LightWall", DisplayName = "IsClose")
		bool bIsClose = true;
};