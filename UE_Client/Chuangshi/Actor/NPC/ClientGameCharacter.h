// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "ClientGameCharacter.generated.h"

/*
* 文件名称：ClientGameCharacter.h
* 功能说明：客户端对象基类
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-06-29
*/

/*
* 客户端对象基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API AClientGameCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	AClientGameCharacter();
	virtual void BeginPlay()override;

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	
	UFUNCTION(BlueprintCallable, Category = "ClientCharacter")
		void PlayClientAction(FName InActionId);

	UFUNCTION(BlueprintImplementableEvent, Category = "ClientCharacter")
		void OnPlayClientActionFinished(ACharacter* Character, FACTION_DATA ActionData);

public:
	virtual void OnCreateApperanceOver() override;

	// 创建外观完毕的蓝图通知，很多工作只有创建完毕模型才开始运作
	UFUNCTION(BlueprintImplementableEvent, Category = "ClientCharacter")
		void OnCreateApperanceOverBP();
	// 执行自定义事件
	UFUNCTION(BlueprintImplementableEvent, Category = "ClientCharacter")
		void OnDoingCustomEvent(const int32& EventType);

public:

	// 配置表的行，读数据用的，客户端本地对象一般情况下是读取配置
	UPROPERTY(BlueprintReadWrite)
	FString DataTableRow;
};
