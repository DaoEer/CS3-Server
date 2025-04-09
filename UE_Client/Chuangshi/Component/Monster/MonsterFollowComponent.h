// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "../FilterActorComponent.h"
#include "GameData/PlayerControllerData.h"
#include "MonsterFollowComponent.generated.h"

UENUM(BlueprintType)
enum class MONSTER_FOLLOW_MOVE_TYPE : uint8
{
	None = 0,    ///<无移动
	Moving = 1,	 ///<移动
	StopMove = 2,///移动到目标点停止
};

/**
* 文件名称：UMonsterFollowComponent.h
* 功能说明：怪物跟随玩家移动位置组件
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2019-10-31
 */
UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class CHUANGSHI_API UMonsterFollowComponent : public UFilterActorComponent
{
	GENERATED_BODY()
	
public:
	UMonsterFollowComponent();

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	void SetMonsterMoveType(MONSTER_FOLLOW_MOVE_TYPE MonsterMoveType);

	void ClearTraceData();

	FVector GetMovePosition();

	void StartMoveTargetPostion();

	MONSTER_FOLLOW_MOVE_TYPE GetCurMonsterMoveType();

	///移动信息
	void MoveTargetPostion(const FVector& TargetPostion, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());

private:
	KBEngine::Entity* GetMEntity();

public:
	///追踪信息
	FTRACE_TARGET_INFO TraceTargetInfo;

private:
	///当前移动模式
	MONSTER_FOLLOW_MOVE_TYPE CurrMoveType = MONSTER_FOLLOW_MOVE_TYPE::None;
	///玩家上次坐标
	FVector RoleLastPosition;
	///目的坐标
	FVector NextMovePosition;
};
