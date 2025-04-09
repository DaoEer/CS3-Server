// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/FlyEffectEmitter.h"
#include "SpecialEffectEmitter.generated.h"

/*
* 文件名称：SpecialEffectEmitter.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-03-09
*/

UCLASS(abstract)
class CHUANGSHI_API ASpecialEffectEmitter : public AFlyEffectEmitter
{
	GENERATED_BODY()

public:
	ASpecialEffectEmitter();

public:
	///第一阶段路径
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		class USplineComponent *FirstStageSpline;

	///第三阶段路径1
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		class USplineComponent *ThirdStageSplineOne;

	///第三阶段路径2
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		class USplineComponent *ThirdStageSplineTwo;

protected:
	///目标头顶飞起的高度
	UPROPERTY(BlueprintReadOnly)
		float SourceHeight = 0.f;

	///开始降落离头顶的距离
	UPROPERTY(BlueprintReadOnly)
		float TargetHeight = 0.f;

	///飞到最高的高度所走的距离占比
	UPROPERTY(BlueprintReadOnly)
		float PercentOfRisingDistance = 0.35f;

	///运动距离
	UPROPERTY(BlueprintReadOnly)
		float Distance = 1;

	///第一阶段上升曲线向前的距离的百分比
	UPROPERTY(BlueprintReadOnly)
		float ForwardDistance;

	///当前第三阶段曲线
	UPROPERTY(BlueprintReadOnly)
		USplineComponent* CurrentThirdStageSpline = nullptr;

	///第一个目标的最后更新位置
	UPROPERTY(BlueprintReadOnly)
		FTransform FirstTargetTransform;

	///第二个目标的最后更新位置
	UPROPERTY(BlueprintReadOnly)
		FTransform SecondTargetTransform;
public:
	virtual void Tick(float DeltaTime) override;

protected:
	///初始化位置
	virtual void InitEmitterTransform() override;

	///进入下一阶段
	virtual void EnterNextMove() override;

private:
	/*内部调用函数*/
	
	//设置第一阶段曲线
	void SetFirstStageSpline();

	//设置第三阶段曲线
	void SetThirdStageSpline();

	//返回第三阶曲线的位置
	const FVector GetThirdStageSplineLocation();

	//设置第三阶曲线的方向
	void SetThirdStageSplineRotation();

	//第一阶段移动
	void FirstStageMove(float DeltaTime);

	//第二阶段移动
	void SecondStageMove(float DeltaTime);

	//第三阶段移动
	void ThirdStageMove(float DeltaTime);
};
