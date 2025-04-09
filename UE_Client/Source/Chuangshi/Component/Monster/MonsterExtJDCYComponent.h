// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "../FilterActorComponent.h"
#include "Component/Monster/MonsterPosSyncComponent.h"
#include "GameData/PlayerControllerData.h"
#include "MonsterExtJDCYComponent.generated.h"


/*
* 文件名称：MonsterExtJDCYComponent.h
* 功能说明：禁地采药怪物同步移动位置组件（主要向服务器发送同步怪物当前移动位置）
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-8-5
*/


UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class CHUANGSHI_API UMonsterExtJDCYComponent : public UFilterActorComponent
{
	GENERATED_BODY()

public:
	UMonsterExtJDCYComponent();
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	MONSTER_MOVE_TYPE GetCurMonsterMoveType();
	MONSTER_MOVE_TYPE GetLastMonsterMoveType();
	void SetMonsterMoveType(MONSTER_MOVE_TYPE MonsterMoveType);
	/*追击*/
	void ChaseTarget();

	/*攻击*/
	void AttackTarget();

	/*搜索玩家目标*/
	int32 GetTargetID();

	/*游荡*/
	void StartWander();
	/*受迫移动*/
	void BeHitBack();

	/*回走*/
	void GoBack();

private:
	bool bEnableTick = false;
	void TraceTargetActor(const AActor* TargetActor, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	//随机位置移动
	void WanderTargetPostion(const FVector& TargetPostion, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	//回走
	void BackTargetPostion(const FVector& TargetPostion, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	//清理追踪数据
	void ClearTraceData();
public:
	MONSTER_MOVE_TYPE LastMoveType = MONSTER_MOVE_TYPE::None;
	MONSTER_MOVE_TYPE CurrMoveType = MONSTER_MOVE_TYPE::None;
	///追踪信息
	FTRACE_TARGET_INFO TraceTargetInfo;
private:
	KBEngine::Entity* GetMEntity();
	float OldBlendMoveDirection;
	FVector WanderPosition = FVector::ZeroVector;

};
