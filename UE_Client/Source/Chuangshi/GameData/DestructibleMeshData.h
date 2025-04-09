#pragma once
#include "CsvTableRowBase.h"
#include "DestructibleMeshData.generated.h"


/**
* 文件名称：DestructibleMeshData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-08-15
*/
class UDestructibleMesh;

USTRUCT(BlueprintType)
struct CHUANGSHI_API FDESTRUCTIBLE_MESH_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///可破碎物体的资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DestructibleMesh")
		TSoftObjectPtr<UDestructibleMesh> DestructibleMesh;
	///破碎力度 数值越大破碎后所产生的力也就越大(在破碎物体勾选WorldDeth也就是区块破碎时需要很大的力度才能驱动)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float ImpulseStrength = 10.0f;
	///破碎半径 单位为米
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float DamageRadius = 10.0f;
	///破碎点(基于主Mesh下相对位置)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector HurtOrigin;
	///破碎前是否可站立
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StandUpBeforeBroken")
		bool bStandUpBeforeBroken;
	///破碎后是否可站立
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StandUpAfterBroken")
		bool bStandUpAfterBroken;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (DestructibleMesh.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(DestructibleMesh.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"DestructibleMesh\" resource does not exist"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FDESTRUCTIBLE_HIT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///可破碎物体，破碎网格体本身的枢轴点可能不在网格体上，导致破碎失败
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UDestructibleMesh> DestructibleMesh;
	///破碎点
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector HitPoint;
	///破碎方向
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector HitDirection;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (DestructibleMesh.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(DestructibleMesh.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"DestructibleMesh\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"DestructibleMesh\" is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};