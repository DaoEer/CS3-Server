// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "BarracksTableData.h"
#include "RoleBarracksItemData.generated.h"



/**
* 文件名称：RoleBarracksItemData.h
* 功能说明：玩家兵营数据
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-12-24
*/
USTRUCT(BlueprintType)
struct FPASSIVESKILLDATA {
	GENERATED_USTRUCT_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SkillID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Exp = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxExp = 0;
};



USTRUCT(BlueprintType)
struct FROLEBARRACKSITEMDATA {
	GENERATED_USTRUCT_BODY()
	/// id 根据进行排序
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Id = 0;
	/// 兵的scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	/// 兵的类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_BARRACKS_SOLDIER_TYPE SoldierType;
	/// 兵的等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level = 0;
	/// 兵的当前经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Exp = 0;
	/// 兵的最大经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxExp = 0;
	/// 兵是否在部队中
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsInArmy = 0;
	/// 兵的被动技能(天赋)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FPASSIVESKILLDATA> PassiveSkillDatas;
	///是否激活
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsActive = 1;

	bool operator ==(const FROLEBARRACKSITEMDATA& other)
	{
		if (other.Id == Id)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};