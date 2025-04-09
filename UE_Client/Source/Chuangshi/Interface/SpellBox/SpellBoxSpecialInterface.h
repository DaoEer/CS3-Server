// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/SpellBox/SpellBoxInterface.h"
#include "SpellBoxSpecialInterface.generated.h"

/*
* 文件名称：SpellBoxSpecialInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-04-02
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USpellBoxSpecialInterface : public USpellBoxInterface
{
	GENERATED_BODY()
	typedef USpellBoxInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	USpellBoxSpecialInterface();
	~USpellBoxSpecialInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.SpellBoxSpecialInterface'"); } //获取蓝图对象路径
		
	virtual void InitBlueCB() override;

};
