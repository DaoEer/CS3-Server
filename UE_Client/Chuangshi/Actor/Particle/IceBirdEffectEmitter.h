// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/FlyEffectEmitter.h"
#include "IceBirdEffectEmitter.generated.h"

/*
* 文件名称：IceBirdEffectEmitter.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-10-27
*/

UCLASS(abstract)
class CHUANGSHI_API AIceBirdEffectEmitter : public AFlyEffectEmitter
{
	GENERATED_BODY()

protected:

	/*Begin AEffectEmitter Interface*/

	///初始化配置
	virtual void InitFromConfig();

	/*End AEffectEmitter Interface*/

	/*Begin AFlyEffectEmitter Interface*/

	///重写第二阶段移动
	virtual void SecondMove(float DeltaTime) override;

	///获得第二阶段运动的角度
	virtual void GetSecondMoveRotation(FRotator& OutRotation) override;

	///准备进入下一阶段阶段
	virtual void EnterNextMove() override;

	/*End AFlyEffectEmitter Interface*/
};
