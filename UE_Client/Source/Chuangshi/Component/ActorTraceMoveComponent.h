// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"

#include "GameData/PlayerControllerData.h"
#include "ActorTraceMoveComponent.generated.h"



/*
* 文件名称：ActorTraceMoveComponent.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-11-29
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTRACE_TARGET
{
	GENERATED_BODY()
		ENUM_TRACE_TARGET_TYPE TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	///是否追踪中
	bool IsChasing = false;
	///靠近距离
	float NearbyRange = 0.0f;
	///移动速度(像素)
	float MoveSpeed = 0.0f;
	///追踪目标 
	AActor* TraceTarget = nullptr;
	///追踪位置
	FVector TracePostion = FVector::ZeroVector;
	///追踪回调
	FTraceCallback TraceCallback = FTraceCallback();
};


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UActorTraceMoveComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UActorTraceMoveComponent();
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	void TraceTargetActor(const AActor* TargetActor, float NearbyRange = 0.0f, float MoveSpeed = 0.0f, FTraceCallback TraceCallback = FTraceCallback());

	void StopMove();

protected:
	// Called when the game starts
	virtual void BeginPlay() override;

private:
	void ExecuteMoveToTarget();
	FVector OnGroundPostion(const FVector &Vector);

private:
	FTRACE_TARGET TraceTarget;
	bool bIsMoving;
	
};
