// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtDemonGuardInterface.generated.h"

/*
* 文件名称：MonsterExtChartletInterface.h
* 功能说明：程序需求【30级】—环任务潜入妖境程序需求 妖卫
* 文件作者: liaojing
* 目前维护：liaojing
* 创建时间：2019-4-12
*/
UCLASS()
class CHUANGSHI_API UMonsterExtDemonGuardInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtDemonGuardInterface'"); } //获取蓝图对象路径

	//检测玩家是否在视野范围内
	void CheckIsInView(int32 targetID);

	//获取客户端导航点
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|UMonsterExtDemonGuardInterface")
		void CLIENT_GetClientNavPoint(FVector targetPos);
	
	//添加视野检测陷阱
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|UMonsterExtDemonGuardInterface")
		void CLIENT_CreateViewShapeTrap(float Range, float Angle, float Height);


	virtual void InitBlueCB() override;
public:
	UBaseShape* CreateViewShape(float Range, float Angle, float Height);
	void OnPlayerEnterViewRange(); ///玩家进入视野陷阱
	void OnPlayerLeaveViewRange(); ///玩家离开视野陷阱
private:
	FTimerHandle checkViewTimerHandle; //视野检测TimerHandle
	FTimerHandle delaySetViewTimerHandle; //延时移除checkViewTimerHandle
	FTimerHandle getNavPoint; //获取导航点 需要实时检测是否有动态障碍物（光墙）

	UBaseShape* pViewShape; //视野陷阱
};
