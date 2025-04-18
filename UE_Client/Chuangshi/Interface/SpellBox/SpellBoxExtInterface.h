// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/SpellBox/SpellBoxInterface.h"
#include "SpellBoxExtInterface.generated.h"

/*
* 文件名称：SpellBoxExtInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USpellBoxExtInterface : public USpellBoxInterface
{
	GENERATED_BODY()
	typedef USpellBoxInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	USpellBoxExtInterface();
	~USpellBoxExtInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.SpellBoxExtInterface'"); } //获取蓝图对象路径


};