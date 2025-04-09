// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "EffectScreenData.generated.h"

/**
* 文件名称：EffectScreenData.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2018-01-29
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FEFFECT_SCREEN_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///粒子资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UParticleSystem> ParticleSystemPtr;
	///颜色标签：红色，蓝色，金色，紫色，绿色，黑色，白色，其他
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EffectColor = TEXT("其他色");
	///元素标签：火，雷，风，毒，金，木，水，土，其他
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EffectElement = TEXT("其他");
	///光效持续时间模式（1：瞬发，2：持续）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EffectTime;
	///形状标签：球型，旋风，喷，柱型，罩子，法阵，刀光，冲，雪，雨，雾，爆炸，聚气，闪，其他
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EffectShape = TEXT("其他");

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (ParticleSystemPtr.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(ParticleSystemPtr.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ParticleSystemPtr\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ParticleSystemPtr\" is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};