// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtShowTopCountDownInterface.generated.h"

/*
* 文件名称：MonsterExtShowTopCountDownInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-04-23
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtShowTopCountDownInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	UMonsterExtShowTopCountDownInterface();
	~UMonsterExtShowTopCountDownInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtShowTopCountDownInterface'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;

	/**
	*显示头顶倒计时
	*
	*param remainTime 剩余时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtShowTopCountDownInterface")
		void CLIENT_ShowRemainLifeTime(const float& remainTime);
};
