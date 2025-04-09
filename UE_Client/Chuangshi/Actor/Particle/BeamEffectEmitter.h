// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Actor/Particle/FlyEffectEmitter.h"
#include "BeamEffectEmitter.generated.h"

/*
* 文件名称：BeamEffectEmitter.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：zhangfudong
* 创建时间：2017-06-16
*/

DECLARE_STATS_GROUP(TEXT("ABeamEffectEmitter"), STATGROUP_ABeamEffectEmitter, STATCAT_Advanced);

/**
 * 连线光效基类
 */
UCLASS(abstract)
class CHUANGSHI_API ABeamEffectEmitter : public AFlyEffectEmitter
{
	GENERATED_BODY()

public:
	ABeamEffectEmitter();

	virtual void Tick(float DeltaTime) override;

	//重写获取开始的位置，因为连线光效可能会绑定源目标
	virtual FVector GetFlySourcePos(bool bInit = false) override;

protected:
	///初始化位置
	virtual void InitEmitterTransform() override;

	///光效碰撞开始
	//UFUNCTION()
	virtual void OnEmitterCollisionBegin(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	///更新是否可碰撞信息
	void UpdateBeamCollisionList(float DeltaTime);

private:
	///设置起始点
	void SetSourcePoint();

	///设置目标点
	void SetTargetPoint();

	///初始化特殊信息
	void SetBeamAttribute();

	///设置连线在目标那边的切线
	void SetTargetTangent();

	///移动
	void Move();

	///设置碰撞体的大小和动画的朝向位置
	void SetComponentTransform();

private:
	///当前移动的距离
	float CurrentDistance = 0.f;

	///用于判断碰撞数据的结构体
	struct Data
	{
		bool bOverlap;
		float Time;

		Data(bool bOverlap, float Time)
		{
			this->bOverlap = bOverlap;
			this->Time = Time;
		}
	};
	///连线光效的碰撞列表
	TMap<AActor*, Data> BeamCollisionList;
};
