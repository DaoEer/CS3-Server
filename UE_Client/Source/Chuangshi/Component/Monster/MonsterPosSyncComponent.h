// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "../FilterActorComponent.h"
#include "GameData/PlayerControllerData.h"
#include "MonsterPosSyncComponent.generated.h"


UENUM(BlueprintType)
enum class MONSTER_MOVE_TYPE : uint8
{
	None = 0,    ///<无移动
	Wander = 1,	///<游荡
	Chase = 2,	///<追击
	HitBack = 3,///<受迫移动
	GoBack = 4, ///<回走
};
/*
* 文件名称：MonsterPosSyncComponent.h
* 功能说明：怪物同步移动位置组件（主要向服务器发送同步怪物当前移动位置）
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-1-19
*/

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class CHUANGSHI_API UMonsterPosSyncComponent : public UFilterActorComponent
{
	GENERATED_BODY()

public:
	UMonsterPosSyncComponent();
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

};
