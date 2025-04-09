// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "AccountInterface.generated.h"

/*
* 文件名称：AccountInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：qiurunan
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UAccountInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	CS3_DECLARE_INTERFACE_MAP()
	typedef UCS3EntityInterface Supper;

public:
	UAccountInterface();
	~UAccountInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.AccountInterface'"); } //获取蓝图对象路径


public:
	/**
	*账号最近一次登录的角色DBID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Acount")
		void OnRep_lastLogonDBID();
};
