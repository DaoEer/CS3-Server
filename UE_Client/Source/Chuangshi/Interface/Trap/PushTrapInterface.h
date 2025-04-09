// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "TrapInterface.h"
#include "PushTrapInterface.generated.h"

/*
* 文件名称：PushTrapInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-25
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UPushTrapInterface : public UTrapInterface
{
	GENERATED_BODY()
	typedef UTrapInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UPushTrapInterface();
	~UPushTrapInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TrapInterface'"); } //获取蓝图对象路径
};
