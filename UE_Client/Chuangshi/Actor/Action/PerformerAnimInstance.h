// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "BaseAnimInstance.h"
#include "PerformerAnimInstance.generated.h"

/*
* 文件名称：PerformerAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-06-21
*/
UCLASS(Blueprintable, hideCategories = PerformerAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API UPerformerAnimInstance : public UBaseAnimInstance
{
	GENERATED_BODY()
public:
	UPerformerAnimInstance();
	~UPerformerAnimInstance();
protected:
private:
	
	
	
};
