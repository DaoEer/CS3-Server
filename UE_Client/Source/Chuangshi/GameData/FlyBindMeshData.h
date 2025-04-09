#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "GameData/BaseSplineAsset.h"
#include "GameData/GameDeFine.h"
#include "FlyBindMeshData.generated.h"

/**
* 文件名称：FlyBindMeshData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-07-09
*/

UENUM(Blueprintable)
enum class FLYBINDSKILL_STATE : uint8
{
	///幽冥花
	YOUMINGHUA = 0,
	///青光剑
	QINGGUANGJIAN = 1,
	///金击子
	JINJIZI = 2,
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLY_BIND_MESH_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:

	///绑定模型ID（@DT_ModelCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FlyModeID;
	///绑定的位置朝向和大小
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform FlyTransform;
	///飞行模型绑定点
	///	需要绑定在玩家身上的那个槽点，填写骨骼名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName FlyModeBindSocket;
	///路径资源（如@BP_Spline_Circle_Stand）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		TSubclassOf<ABaseSplineAsset> SplineAsset;
	///飞行路径偏移
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		FTransform FlySplineTransform;
	///飞行循环次数（次，暂不支持-1）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float FlyLoopNumber = 0.0f;
	///飞行速度（厘米/秒）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float FlySpeed = 0.0f;
	///路径：是否“保持本地位移”
	///	创建后不再跟随移动
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		bool IsAbsoluteLocation = false;
	///路径：是否“保持本地旋转”
	///	创建后不再跟随旋转
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		bool IsAbsoluteRotation = false;
	///路径：是否“保持本地缩放”
	///	创建后不再跟随缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		bool IsAbsoluteScale = false;
	///技能类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		FLYBINDSKILL_STATE SkillType;
	///法宝动作ID列表
	///	请根据动画流程顺序配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		TArray<FString> AnimID;
	///法宝光效ID列表
	///	请根据动画流程顺序配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		TArray<FString>EffectID;
	///动画延迟时间
	///	请根据动画流程顺序配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyBind")
		TArray<float> PlayTime;
	///备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;

public:
	///不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (IsValid(SplineAsset))
		{
			if (!CheckResourceFileIsExist(SplineAsset->GetPathName()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"SplineAsset\" resource does not exist"));
			}
		}
	}

	///会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}

};