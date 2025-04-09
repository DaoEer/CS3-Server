// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtMachineInterface.generated.h"

/*
* 文件名称：MonsterExtMachineInterface.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2017-08-09
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtMachineInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtMachineInterface();
	~UMonsterExtMachineInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtMachineInterface'"); } //获取蓝图对象路径
	
	
};
