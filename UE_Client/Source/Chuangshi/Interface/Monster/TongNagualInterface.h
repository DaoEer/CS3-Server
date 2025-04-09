// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "TongNagualInterface.generated.h"

/*
* 文件名称：TongNagualInterface.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-03-16
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTongNagualInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UTongNagualInterface();
	~UTongNagualInterface();
	static FString GetName() { return TEXT("TongNagualInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TongNagualInterface'"); } //获取蓝图对象路径

};
