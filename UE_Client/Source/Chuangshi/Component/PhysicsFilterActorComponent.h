// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "FilterActorComponent.h"
#include "PhysicsFilterActorComponent.generated.h"

/*
* 文件名称：PhysicsFilterActorComponent.h
* 功能说明：
* 文件作者：wangzheng
* 目前维护：wuxiaoou
* 创建时间：2017-03-16
*/

/**
* 一个自定义改变位置的过滤器，用于模拟战斗受击表现(服务器控制的怪物模拟击退)
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UPhysicsFilterActorComponent : public UFilterActorComponent
{
	GENERATED_BODY()
		typedef UFilterActorComponent Supper;

public:
	UPhysicsFilterActorComponent();

	virtual void SimulateMovement(float DeltaTime) override;
	void InitData(const float& MoveSpeed, const FVector& DstPos);

	virtual void OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID) override;
private:
	float GetDestDistance();//获取与目标点的距离
public:
	float Velocity;
	bool IsIgnoreServerPos;
	FVector DestPos;
};


/**
* 客户端模拟怪物抛物线移动Filter(纯客户端移动)
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCurveFilterActorComponent : public UFilterActorComponent
{
	GENERATED_BODY()
		typedef UFilterActorComponent Supper;
public:
	UCurveFilterActorComponent();

	virtual void SimulateMovement(float DeltaTime) override;
	virtual void SetDirection(const FVector& direction, int32 parentID) override;

	//移动数据相关
	void InitData(float Gravity, float UpTime, float XSpeed, FVector DstPos);
	void ClearMoveData();

private:
	float ZUpTime;//上升时间
	float ZGravity;//重力加速度
	float MoveTime;//移动时间
	float NeedTime;//移动总时间
	FVector XMoveDir;//平面移动向量
	FVector DstPosition;//移动目标点
	FVector DstDirection;//目标朝向

};

/**
* 纯客户端，用于模拟击退表现
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UHitBackMoveFilterActorComponent : public UFilterActorComponent
{
	GENERATED_BODY()
		typedef UFilterActorComponent Supper;

public:
	UHitBackMoveFilterActorComponent();

	virtual void SimulateMovement(float DeltaTime) override;
	virtual void SetDirection(const FVector& direction, int32 parentID) override;

	void InitData(float InMoveSpeed, const FVector& InDestination, const FVector& InStartPos, const FVector& InDestPos);

	float Velocity;			//速度
	FVector DestPos;		//目标位置 
	FVector Destination; 	//击退的距离
	FVector StartPos;      	//击退的起始位置，服务器位置
private:
	FQuat Dir;
};