// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/SpellBox/SpellBoxInterface.h"
#include "SpellBoxAdvancedInterface.generated.h"

/*
* 文件名称：SpellBoxAdvancedInterface.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2018-05-17
*/
UCLASS()
class CHUANGSHI_API USpellBoxAdvancedInterface : public USpellBoxInterface
{
	GENERATED_BODY()
	typedef USpellBoxInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	USpellBoxAdvancedInterface();
	~USpellBoxAdvancedInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.SpellBoxAdvancedInterface'"); } //获取蓝图对象路径

	void CELL_reqInterruptInteractive();
	
	void CELL_reqStartInteractive();
};
