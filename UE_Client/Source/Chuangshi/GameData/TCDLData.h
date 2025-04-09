#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "TCDLData.generated.h"

/**
* 文件名称：TCDLData.h
* 功能说明：逃出丹炉副本，岩浆充能时间数据
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-04-09
*/

UENUM(BlueprintType)
enum class UV_TYPE_ENUM :uint8
{
	UV_U	UMETA(DisplayName = "UV_U"),
	UV_V	UMETA(DisplayName = "UV_V"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTCDLData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//使用的UV类型，由程序设定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "UVType")
		UV_TYPE_ENUM UVType;

	//模型，由程序设定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "Mesh")
		TSoftObjectPtr<UStaticMesh> Mesh;

	//充能时间，策划配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "RechargeTime")
		float RechargeTime;

	//喷火时间，策划配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "EruptionTime")
		float EruptionTime = 10.f;

	//光效ID，策划配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "EffectID")
		TArray<FString> EffectID;

	//光效位置，策划配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "EffectTransform")
		TArray<FTransform> EffectTransform;

	//位置，由程序设定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "Tranform")
		FTransform Tranform;

	//起始，由程序设定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "StartValue")
		float StartValue;

	//完毕，由程序设定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TCDLData", DisplayName = "EndValue")
		float EndValue = 1.f;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (Mesh.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(Mesh.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Mesh\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Mesh\" is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}

};