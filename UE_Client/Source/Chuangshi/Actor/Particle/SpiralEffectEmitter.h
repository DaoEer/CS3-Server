// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/FlyEffectEmitter.h"
#include "SpiralEffectEmitter.generated.h"

/*
* 文件名称：SpiralEffectEmitter.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-04-08
*/

DECLARE_STATS_GROUP(TEXT("ASpiralEffectEmitter"), STATGROUP_ASpiralEffectEmitter, STATCAT_Advanced);

UCLASS(abstract)
class CHUANGSHI_API ASpiralEffectEmitter : public AFlyEffectEmitter
{
	GENERATED_BODY()
	
private:

	//进度
	float Rate;

	//相对坐标X
	float RelPosX;

	//相对坐标Y
	float RelPosY;

	//相对坐标Z
	float RelPosZ;

	//距离
	float Distance;

	//相对目标Z角度
	float RelRotZ;

	//相对目标XY角度
	float RelRotXY;

	//偏向速度Z
	float SpeedZ;

	//当前偏角Z
	float CurAngleZ;

	//开始仰角XY
	float BeginAngleXY;

	//结束仰角XY
	float EndAngleXY;

	//仰向速度XY
	float SpeedXY;

	//当前仰角XY
	float CurAngleXY;

	//开始半径
	float BeginRadius = 0.0f;

	//结束半径
	float EndRadius;

	//径向速度
	float RadiusSpeed;

	//当前半径
	float CurrentRadius;

	//相对偏移
	FVector RelOffset;

public:
	virtual void Tick(float DeltaTime) override;

protected:
	
	///初始化位置
	virtual void InitEmitterTransform() override;
	
private:
	///准备数据
	UFUNCTION(BlueprintCallable, Category = "SpiralEffect")
	void PrepareTheData(float DeltaTime);
	
	///更新时间
	void UpdateTime(float DeltaTime);

	///更新相对坐标和角度以及距离
	void UpdateRelInfo();

	//计算运动数据
	UFUNCTION(BlueprintCallable, Category = "SpiralEffect")
	void Calculation();

	//计算位置相关
	void CalculationAngle();

	//计算半径相关
	void CalculationRadius();

	//计算位置相关
	FVector CalculationPosition();

	//计算旋转相关
	FRotator CalculationRotation();
};
