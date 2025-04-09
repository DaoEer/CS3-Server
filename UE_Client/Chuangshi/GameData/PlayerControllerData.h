// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include "CoreMinimal.h"
#include "../Util/EventDelegate.h"
#include "PlayerControllerData.generated.h"

/**
* 文件名称：CharacterData.h
* 功能说明：玩家控制
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-12-19
*/

/**
*追踪目标
*@enum ENUM_TRACE_TARGET_TYPE
*/
UENUM(BlueprintType)
enum class ENUM_TRACE_TARGET_TYPE : uint8
{
	///0-追踪目标对象
	TraceTargetActor = 0 UMETA(DisplayName = "TraceTargetActor"),
	///1-追踪目标位置
	TraceTargetPoint = 1 UMETA(DisplayName = "TraceTargetPoint"),
	///2-追踪目标对象在客戶端
	TraceTargetActorAtClient = 2 UMETA(DisplayName = "TraceTargetActorAtClient"),
};

UENUM(BlueprintType)
enum class CS3_MOVE_TYPE : uint8
{
	//无移动
	MOVE_TYPE_NONE = 0 UMETA(DisplayName = "none"),
	//鼠标移动
	MOVE_TYPE_MOUSE = 1 UMETA(DisplayName = "mouse"),
	//自主移动
	MOVE_TYPE_CONTROL = 2 UMETA(DisplayName = "control"),
	//追踪移动
	MOVE_TYPE_TRACE = 3 UMETA(DisplayName = "trace"),
	//飞行移动
	MOVE_TYPE_FLY = 4 UMETA(DisplayName = "fly"),
	//受击移动
	MOVE_TYPE_BACK = 5 UMETA(DisplayName = "back"),
	//寻路移动
	MOVE_TYPE_NAVIGATE = 6 UMETA(DisplayName = "navigate"),
	//组队跟随
	MOVE_TYPE_TEAM_FOLLOW = 7 UMETA(DisplayName = "teamFollow"),
	//自动寻路
	MOVE_TYPE_AUTO_NAVIGATE = 8 UMETA(DisplayName = "autoNavigate"),
};

UENUM(BlueprintType)
enum class ENUM_NAVIGATE_TARGET_TYPE : uint8
{
	///0-寻路单位
	NavigateTargetActor = 0 UMETA(DisplayName = "NavigateTargetActor"),
	///1-寻路位置
	NavigateTargetPosition = 1 UMETA(DisplayName = "NavigateTargetPosition"),
};

///追踪信息
///@sturct FTRACE_TARGET_INFO
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTRACE_TARGET_INFO
{
	GENERATED_BODY()
		ENUM_TRACE_TARGET_TYPE TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	///是否追踪中
	bool IsChasing = false;
	///靠近距离
	float NearbyRange = 0.0f;
	///追踪目标
	AActor* TraceTarget = nullptr;
	///追踪位置
	FVector TracePostion = FVector::ZeroVector;
	///追踪结束是否停止移动
	bool IsStopMove = true;
	///追踪回调
	FTraceCallback TraceCallback = FTraceCallback();
	///追踪停止移动的回调
	FTraceCallback TraceStopMoveCallback = FTraceCallback();
};

///飞行移动信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLY_MOVE_INFO
{
	GENERATED_BODY()
	///正在飞行至某点中
	bool bIsFlyTo = false;
	///飞行目标点
	FVector FlyLocation = FVector::ZeroVector;
	///是否飞行传送
	bool bIsFlyPatrol = false;
	///是否固定玩家朝向
	bool bIsFixedDirection = false;
	///飞行结束回调
	FTraceCallback FlyCallback = FTraceCallback();

	void Reset()
	{
		this->bIsFlyTo = false;
		this->FlyLocation = FVector::ZeroVector;
		this->bIsFlyPatrol = false;
		this->bIsFixedDirection = false;
		if ((this->FlyCallback).IsBound())
		{
			(this->FlyCallback).Unbind();
		}
		this->FlyCallback = FTraceCallback();
	};
};

///自动寻路信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FNAVIGATE_TARGET_INFO
{
	GENERATED_BODY()
		
		ENUM_NAVIGATE_TARGET_TYPE NavigateTargetType = ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetPosition;

	///是否自动寻路中
	bool IsAutoNavigate = false;
	///是否同地图寻路
	bool IsSameSpace = false;
	///寻路目标所在地图
	FString SpaceName = "";
	///寻路目标
	AActor* NavigateTarget = nullptr;
	///寻路位置
	FVector NavigatePosition = FVector::ZeroVector;
	///靠近距离
	float NearbyRange = 0.0f;
	///寻路结束回调
	FTraceCallback AutoNavigateCallback = FTraceCallback();
};