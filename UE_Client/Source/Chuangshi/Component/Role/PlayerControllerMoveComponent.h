// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Components/ActorComponent.h"
#include "Util/EventDelegate.h"
#include "GameData/PlayerControllerData.h"
#include "PlayerControllerMoveComponent.generated.h"

/*
* 文件名称：PlayerControllerMoveComponent.h
* 功能说明：玩家控制移动组件
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2016-12-06
*/

DECLARE_STATS_GROUP(TEXT("UPlayerControllerMoveComponent"), STATGROUP_UPlayerControllerMoveComponent, STATCAT_Advanced);

DECLARE_DYNAMIC_DELEGATE_OneParam(FTraceMoveCallback, bool, IsSuccess);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMoveTypeChange, CS3_MOVE_TYPE, NewMoveType, CS3_MOVE_TYPE, OldMoveType);

UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UPlayerControllerMoveComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	UPlayerControllerMoveComponent();
	//~ Begin UActorComponent Interface.
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
	//~ End UActorComponent Interface.

	//鼠标点地移动
	void MouseClickMove();
	//鼠标飞行移动
	void MouseClickFly();
	//受击移动
	void MoveBackToPostion(const float MoveSpeed, const FVector& TargetPostion);
	void EndMoveBack();
	//追踪Actor移动
	void TraceTargetActor(const AActor* TargetActor, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	void TraceTargetActorAtClient(const AActor* TargetActor, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	//组队跟随
	void TeamFollowTraceTarget(const AActor* TargetActor, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	//追踪位置移动
	void TraceTargetPostion(const FVector& TargetPostion, float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	//飞行至目标点移动
	void FlyToLocation(const FVector& Location, bool IsFlyPatrol = false, bool IsFixedDirection = false, FTraceCallback FlyCallback = FTraceCallback());
	
	//自动寻路追踪Actor移动
	void AutoNavigateTargetActor(const AActor* TargetActor, const FString& spaceName, float NearbyRange = 2.0f, FTraceCallback NavigateCallback = FTraceCallback());
	//自动寻路追踪位置移动
	void AutoNavigateTargetPosition(const FVector& TargetPosition, const FString& spaceName = "", float NearbyRange = 2.0f, FTraceCallback NavigateCallback = FTraceCallback());
	//自动寻路到指定位置--鼠标点击时
	void AutoNavigateMousePosition(const FVector& TargetPosition, FTraceCallback NavigateCallback = FTraceCallback());
	//基于寻路数据的自主移动
	void ConsumeKeyMovementInput(TArray<FVector>& MovementInput);
	//获得当前移动模式
	CS3_MOVE_TYPE GetMoveType();
	//停止移动并清除数据
	void StopMove();
	///<获取飞行数据
	FFLY_MOVE_INFO GetFlyMoveInfo() { return FlyMoveInfo; };
public:
	///<移动模式改变回调
	UPROPERTY(BlueprintAssignable, Category = "PlayerControllerMoveComponent")
	FOnMoveTypeChange OnPlayerMoveTypeChange;
private:
	//设置移动模式
	void SetMoveType(CS3_MOVE_TYPE MoveType);
	
	// 追踪移动
	void HandleTraceMove();
	//  队伍跟随移动
	void HandleTeamFollowMove();
	// 飞行移动
	void HandleFlyMove(const float& DeltaTime);
	// 自动寻路移动
	void HandleAutoNavigateMove();
	// 鼠标点击移动
	void HandleMouseClickMove();
	// 寻路移动
	void HandleNavigateMove();
	// 击退移动
	void HandleHitBackMove(const float& DeltaTime);

	//清理飞行数据
	void ClearFlyData();
	//清理追踪数据
	void ClearTraceData();
	//清除自动寻路数据
	void ClearAutoNavigate();
	//清理击退移动数据
	void ClearHitBackData();

	//追踪失败回调
	void TraceFailCallBack();

	void SetTraceResult(bool IsSuccess);///<设置追踪的结果
private:
	///追踪信息
	FTRACE_TARGET_INFO TraceTargetInfo;
	///飞行移动信息
	FFLY_MOVE_INFO FlyMoveInfo;
	CS3_MOVE_TYPE CurrMoveType;
	CS3_MOVE_TYPE LastMoveType;
	///自动寻路信息
	FNAVIGATE_TARGET_INFO NavigateTargetInfo;
	// 击退速度
	float MoveHitBackSpeed;
	// 击退ForceID
	int32 MoveHitBackForceID;
};
