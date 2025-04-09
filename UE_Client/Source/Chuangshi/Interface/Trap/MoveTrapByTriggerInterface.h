// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "TrapInterface.h"
#include "MoveTrapByTriggerInterface.generated.h"

/*
* 文件名称：MoveTrapByTriggerInterface.h
* 功能说明：
* 文件作者：zhutianyang
* 目前维护：chendongyong
* 创建时间：2017-10-17
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMoveTrapByTriggerInterface : public UTrapInterface
{
	GENERATED_BODY()
	typedef UTrapInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMoveTrapByTriggerInterface();
	~UMoveTrapByTriggerInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MoveTrapByTriggerInterface'"); } //获取蓝图对象路径

	
};
