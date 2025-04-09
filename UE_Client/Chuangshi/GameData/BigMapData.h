#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "Engine/Texture2D.h"
#include "BigMapData.generated.h"

/**
* 文件名称：BigMapData.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2018-08-23
*/

///区域数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSUBAREA_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///区域的ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName ScriptID;

	///区域名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString AreaName;

	///是否显示子区域地图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsShowSub = false;
	
	///是否为洞穴子区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCaveSub = false;	
	///默认缩放比
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float DefaultScale = 1;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBIGMAP_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///地图名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MapName;

	///是否忽略在大地图下拉菜单显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsIgnore = true;

	///默认缩放比
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float DefaultScale = 1;

	///子区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaMap", DisplayName = "SubArea")
		TArray<FSUBAREA_DATA> SubArea;

	///位面区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaMap", DisplayName = "PlaneArea")
		TArray<FSUBAREA_DATA> PlaneArea;
};

/**
*地图上绘制点的图标数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSIGN_ICON_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///地图ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BigMap", DisplayName = "ScriptID")
		FString ScriptID;
	///阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BigMap", DisplayName = "Camp")
		int32 Camp;
	///点的图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BigMap", DisplayName = "Icon")
		TSoftObjectPtr<UTexture2D> Icon;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (Icon.ToSoftObjectPath().IsValid())
		{
			if (CheckIsScriptPackage(Icon.ToString()))
			{
				if (!CheckScriptSoftPtrIsValid(Icon))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Icon\" resource does not exist"));
				}
			}
			else if (!CheckResourceFileIsExist(Icon.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Icon\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Icon\" config is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
 * 洞穴类子区域配置
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAVE_SUBAREA_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///关卡地图的ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SubCaveMap", DisplayName = "MapScriptID")
		FName MapScriptID;
	
	///洞穴区域ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SubCaveMap", DisplayName = "CaveScriptID")
		FName CaveScriptID;
	///子区域地图纹理
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SubCaveMap", DisplayName = "CaveMapTexture")
		TSoftObjectPtr<UTexture2D> CaveMapTexture;
	///子区域地图大小
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SubCaveMap", DisplayName = "TextureSize")
		FVector2D TextureSize = FVector2D(0.0, 0.0);

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (CaveMapTexture.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(CaveMapTexture.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"CaveMapTexture\" resource does not exist"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};