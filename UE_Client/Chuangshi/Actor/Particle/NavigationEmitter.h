// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/EffectEmitter.h"
#include "NavigationEmitter.generated.h"

class USplineComponent;
/*
* 文件名称：NavigationEmitter.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-09-26
*/
/**
 * 
 */
UCLASS(abstract)
class CHUANGSHI_API ANavigationEmitter : public AEffectEmitter
{
	GENERATED_BODY()

public:
	ANavigationEmitter();

	virtual void BeginPlay() override;

	virtual void Tick(float DeltaSeconds) override;

private:

	// 初始化导航粒子轨迹
	void InitNavigationTrace();

	// 计算比例
	void CalculateScale();

	// 更新速度
	void UpdateMoveSpeed(float DeltaSeconds);

private:

	// 导航点总距离对于曲线轨迹总距离的比例
	float Scale;

	// 当前距离(在)
	float Distance;

	// 螺旋距离和上升距离公用
	float OtherDistance;

	// 导航点
	TArray<FVector> NavLocationList;

	// 是否是正常速度
	bool bNormalSpeed = false;

	// 是否螺旋上升
	bool bSpiralRising = false;

	// 随机旋转频率
	int RandFrequency = 5;

	// 随机旋转计时器
	float RandTime = 0.0f;

	// 旋转速度
	float SpiralSpeed = 100.f;

	// 粒子在正常速度下，在玩家前方的距离
	float ForwardDiatance;

	// 粒子修正放缩比
	float AdjustScale = 0.f;

	// 处于加速状态
	bool bSpeedUp = false;

public:
	///导航轨迹
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		USplineComponent* NavigationTrace;

	///螺旋轨迹
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		USplineComponent* SpiralTrace;

	///上升轨迹
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		USplineComponent* RisingTrace;
};
