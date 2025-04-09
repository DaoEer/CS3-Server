// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "BehaviorTree/BehaviorTree.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "ClientMonsterAIData.generated.h"

/**
* 文件名称：ClientMonsterAIData.h
* 功能说明：客户端怪物AI行为树配置
* 文件作者：HeJingke
* 目前维护：HeJingke
* 创建时间：2016-11-23
*/


///跟随模式数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCLIENT_MONSTER_FOLLOW_DATA
{
	GENERATED_BODY()

public:
	///模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "ModelID")
		FString ModelID;
	///攻击范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "AttackRange")
		float AttackRange;
	///搜索（敌人）范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "SearchRange")
		float SearchRange;
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "SkillIDs")
		TArray<int32> SkillID;
	///起始距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "FollowStartDist")
		float FollowStartDist = 300.f;
	///间隔距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "FollowSpace")
		float FollowSpace = 300.f;
	///每排最大数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "FollowMaxIndex")
		int FollowMaxIndex = 5;
	///AvoidanceConsiderationRadius
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "AvoidanceConsiderationRadius")
		float AvoidanceConsiderationRadius = 300.f;
};


///攻击模式数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCLIENT_MONSTER_ATTACK_DATA
{
	GENERATED_BODY()

public:
	///模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAttackData", DisplayName = "ModelID")
		FString ModelID;
	///攻击范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAttackData", DisplayName = "AttackRange")
		float AttackRange;
	///搜索（敌人）范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAttackData", DisplayName = "SearchRange")
		float SearchRange;
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAttackData", DisplayName = "SkillIDs")
		TArray<int32> SkillID;
	///AvoidanceConsiderationRadius
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "AvoidanceConsiderationRadius")
		float AvoidanceConsiderationRadius = 300.f;
};


///阵型数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCLIENT_MONSTER_FORMATION_DATA
{
	GENERATED_BODY()

public:
	///模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFormationData", DisplayName = "ModelID")
		FString ModelID;
	///攻击范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFormationData", DisplayName = "AttackRange")
		float AttackRange;	
	///搜索（敌人）范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFormationData", DisplayName = "SearchRange")
		float SearchRange;
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFormationData", DisplayName = "SkillIDs")
		TArray<int32> SkillID;
	///起始距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "FollowStartDist")
	float FollowStartDist = 300.f;
	///间隔距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "FollowSpace")
		float FollowSpace = 300.f;
	///每排最大数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "FollowMaxIndex")
		int FollowMaxIndex = 5;
	///AvoidanceConsiderationRadius
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterFollowData", DisplayName = "AvoidanceConsiderationRadius")
		float AvoidanceConsiderationRadius = 300.f;
};


///@struct FCLIENT_MOSNTER_AI_DATA
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCLIENT_MOSNTER_AI_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "BTree")
		UBehaviorTree* BTree;
	///主动攻击范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "InitiativeRange")
		float InitiativeRange;
	///距离控制者最大距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "DistanceControler")
		float DistanceControler;
	///部队指挥技能（玩家技能）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "CmdSkillID")
		int32 CmdSkillID;
	///初始增加的霸体buff
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "initBuffID")
		int32 initBuffID;
	///是否是远程
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "isRemote")
		bool isRemote = false;
	///跟随
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "CmdFollow")
		FCLIENT_MONSTER_FOLLOW_DATA Follow;
	///列阵
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "CmdFormation")
		TMap<MONSTER_AI_FORMATION,FCLIENT_MONSTER_FORMATION_DATA> Formations;
	///自由攻击
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ClientMonsterAI", DisplayName = "CmdAttack")
		FCLIENT_MONSTER_ATTACK_DATA Attack;	

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (!IsValid(BTree))
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: BTree字段配置为空"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};