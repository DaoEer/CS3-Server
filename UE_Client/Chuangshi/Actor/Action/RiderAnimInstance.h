// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include "BaseAnimInstance.h"
#include "RiderAnimInstance.generated.h"

/*
* 文件名称：RiderAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-08-18
*/
UCLASS(Blueprintable, hideCategories = RiderAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API URiderAnimInstance : public UBaseAnimInstance
{
	GENERATED_BODY()
public:
	URiderAnimInstance();
	~URiderAnimInstance();
	void PlayAction(FName InActionId, 
		float InStartPostion = 0.0f,
		const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate(), 
		int32 InContinuousId = 0,
		const FActionBlendOutDelegate& InActionBlendOutDelegate = FActionBlendOutDelegate())override;

	//设置移动时的速度与方向
	void SetMoveSpeedAndMoveDirection(float InMoveSpeed, float InMoveDirection);

protected:
	
private:
};
