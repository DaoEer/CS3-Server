// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/Actor.h"
#include "Manager/Delegate/TongDelegateObject.h"

#include "Delegate.h"
#include "EventManager.generated.h"

/*
* 文件名称：EventManager.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-03-15
*/

DECLARE_MULTICAST_DELEGATE(FOnCancelMouseEvent);
DECLARE_DELEGATE(FOnCloseAutoShoot);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnTriggerDynamicEnvironmentEvent, FString, BoxEnvironmentName, float, EffectStartTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnTriggerSkyMaterialEvent, FString, MaterialName, float, EffectStartTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnBackDynamicEnvironmentEvent);


UCLASS(Blueprintable)
class CHUANGSHI_API UGEventManager : public UTongDelegateObject
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	UGEventManager();
	~UGEventManager();

	static UGEventManager* GetInstance();
	
	//取消鼠标操作事件
	FOnCancelMouseEvent OnCancelMouseEvent;
	
	//关闭自动射击事件（灵域狩魂）
	FOnCloseAutoShoot OnCloseAutoShoot;
	
	UPROPERTY(BlueprintAssignable, Category = "Level|Environment")
		FOnTriggerDynamicEnvironmentEvent OnTriggerDynamicEnvironmentEvent;///<触发动态环境效果事件
	UPROPERTY(BlueprintAssignable, Category = "Level|Environment")
		FOnTriggerSkyMaterialEvent OnTriggerSkyMaterialvent;///<触发动态环境效果事件
	UPROPERTY(BlueprintAssignable, Category = "Level|Environment")
		FOnBackDynamicEnvironmentEvent OnBackDynamicEnvironmentEvent;///<还原之前的环境效果事件

/*

private:
	static UGEventManager* Instance;*/
};
