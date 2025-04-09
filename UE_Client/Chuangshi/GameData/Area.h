// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "Area.generated.h"

/**
* 文件名称：FAREA_DATA.h
* 功能说明：区域数据
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-11-23
*/

///@struct FAREA_DATA
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAREA_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///映射到大地图ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "MapScriptID")
		FString MapScriptID;
	///地图ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "ScriptID")
		FString ScriptID;
	///区域名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "AreaName")
		FString AreaName;
	///天空高度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "CeilHeight")
		float CeilHeight;
	///区域高度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "FloorHeight")
		float FloorHeight;
	///区域区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "Polygon")
		TArray<FVector2D> Polygon;
	///区域类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "AreaType")
		UClass* AreaType;
	///区域死亡高度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "DeathHeight")
		float DeathHeight;
	///区域飞行高度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "FlyHeight")
		float FlyHeight;
	///区域复活地图
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "ReviveSpace")
		FString ReviveSpace;
	///区域复活位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "RevivePosition")
		FVector RevivePosition;
	///区域复活朝向
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "ReviveDirection")
		FRotator ReviveDirection;
	///地图传送开关，如果开启（true）当前地图不能使用传送点传送
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "ForbidUseTeleportPoint")
		bool ForbidUseTeleportPoint = false;
	///通用参数一
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "Param1")
		FString Param1;
	///通用参数二
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "Param2")
		FString Param2;
	///通用参数三
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Area", DisplayName = "Param3")
		FString Param3;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (!IsValid(AreaType))
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"AreaType\" is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};