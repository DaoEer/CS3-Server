// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "FlyPatrolData.generated.h"

/**
* 文件名称：FlyPatrolData.h
* 功能说明：飞行路线配置
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2016-12-08
*/

/**
*	飞行事件类型
*/
UENUM(Blueprintable)
enum class EFLYEVENT : uint8
{
	///无
	NONE = 0,
	///镜头
	STORY,
	///技能
	SKILL,
	///摄像机固定视角
	CAMERALOCK,
	///停止飞行
	STOPFLY,
	///开始接入循环飞行
	STARTCYCLEFLY,
	///接出循环飞行
	ENDCYCLEFLY,
	///空间动态效果
	SPACEDYNAMIC,
};

/**
*	飞行事件数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLYEVENT_DATA
{
	GENERATED_USTRUCT_BODY()
	/** 飞行路点 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 FlyIndex = 0;
	/** 飞行事件类型 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EFLYEVENT FlyEventType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Params;
};

/**
*	飞行时间轴事件数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLYEVENTTIME_DATA
{
	GENERATED_USTRUCT_BODY()

	/** 飞行事件时间*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float FlyEventTime;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FFLYEVENT_DATA FlyEventData;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLY_PATROL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///地图ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FlyPatrol", DisplayName = "SpaceName")
		FString SpaceName;
	///飞行路点
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FlyPatrol", DisplayName = "FlyPoints")
		TArray<FVector> FlyPoints;
	///路径速度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FlyPatrol", DisplayName = "FlySpeeds")
		TArray<float> FlySpeeds;
	///路点事件ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FlyPatrol", DisplayName = "FlyEventIDs")
		TArray<FFLYEVENT_DATA> FlyEventIDs;
	///路点时间轴事件ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FlyPatrol", DisplayName = "FlyTimeEventIDs")
		TArray<FFLYEVENTTIME_DATA> FlyTimeEventIDs;
	///<效果列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> EffectList;

public:

	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		for (int i = 0; i < FlyEventIDs.Num(); i++)
		{
			auto EventData = FlyEventIDs[i];
			if (!EventData.Params.IsEmpty() && EventData.FlyEventType == EFLYEVENT::SKILL || EventData.FlyEventType == EFLYEVENT::STOPFLY)
			{
				if (EventData.Params != "0" && FCString::Atoi(*EventData.Params) == 0)
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"FlyEventIDs\" index(%d) \"Params\" config error"), i);
				}
			}
		}
		for (int i = 0; i < FlyTimeEventIDs.Num(); i++)
		{
			auto EventData = FlyTimeEventIDs[i].FlyEventData;
			if (!EventData.Params.IsEmpty() && EventData.FlyEventType == EFLYEVENT::SKILL || EventData.FlyEventType == EFLYEVENT::STOPFLY)
			{
				if (EventData.Params != "0" && FCString::Atoi(*EventData.Params) == 0)
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"FlyTimeEventIDs\" index(%d) \"FlyEventData.Params\" config error"), i);
				}
			}
		}

		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
*	幻阵迷宫飞行数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLYSUBSPACE_DATA
{
	GENERATED_USTRUCT_BODY()
	/** 飞行ID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PatrolID;
	/** 子飞行路径ID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SubPatrolID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 StartPoint = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 EndPoint = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Speed;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector EndPos;

	void Init(FString patrolID, FString subPatrolID, int32 startPoint, int32 endPoint, float speed, FVector endPos)
	{
		this->PatrolID = patrolID;
		this->SubPatrolID = subPatrolID;
		this->StartPoint = startPoint;
		this->EndPoint = endPoint;
		this->Speed = speed;
		this->EndPos = endPos;
	}

	void Reset()
	{
		this->PatrolID = TEXT("");
		this->SubPatrolID = TEXT("");
		this->StartPoint = 0;
		this->EndPoint = 0;
		this->Speed = 0.0f;
		this->EndPos = FVector::ZeroVector;
	}
};

/** 飞行载具Mesh绑定结构体 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLY_PATROL_BIND_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///模型资源路径
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "SkeletaMeshPath")
		TSoftObjectPtr<USkeletalMesh> SkeletalMeshPath;
	///动画资源的路径
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "AnimationAssetPath")
		TSoftObjectPtr<UAnimationAsset> AnimationAssetPath;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Remarks")
		FString Remarks;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;
		if (SkeletalMeshPath.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(SkeletalMeshPath.ToString()))
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"SkeletalMeshPath\" resource does not exist"));
			}
		}
		else
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"SkeletalMeshPath\" is None"));
		}
		if (AnimationAssetPath.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(AnimationAssetPath.ToString()))
			{
				ResultInfo.Result = Error;
				if (bHasError)
				{
					ResultInfo.CheckLog += FString::Printf(TEXT(", \"AnimationAssetPath\" resource does not exist"));
				}
				else
				{
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"AnimationAssetPath\" resource does not exist"));
				}
			}
		}
		else
		{
			ResultInfo.Result = Error;
			if (bHasError)
			{
				ResultInfo.CheckLog += FString::Printf(TEXT(", \"AnimationAssetPath\" is None"));
			}
			else
			{
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"AnimationAssetPath\" is None"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};