// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtDisposableInterface.generated.h"

/*
* 文件名称：MonsterExtDisposableInterface.h
* 功能说明：一次性的随从怪物
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-11-10
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtDisposableInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtDisposableInterface();
	~UMonsterExtDisposableInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtDisposableInterface'"); } //获取蓝图对象路径

	//获取控制自身的玩家的ID
	int32 GetOwnerID();

};
