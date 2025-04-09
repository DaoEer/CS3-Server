// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimNotifies/AnimNotifyState.h"
#include "CatchTarget.generated.h"

/*
* 文件名称：CatchTarget.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：zhangfudong
* 创建时间：2018-02-27
*/

UCLASS(Abstract)
class CHUANGSHI_API UCatchTarget : public UAnimNotifyState
{
	GENERATED_BODY()
	
protected:
	/**
	*Define method
	*BlueprintCallable，抓住目标（链刃技能）
	*
	*@param TargetID 目标ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CatchTarget")
		void CatchTarget(const int32 TargetID, AActor* CurActor, const FName AnimID);
	
	/**
	*Define method
	*BlueprintCallable，释放目标（链刃技能）
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CatchTarget")
		void ReleaseTarget(AActor* CurActor);
};
