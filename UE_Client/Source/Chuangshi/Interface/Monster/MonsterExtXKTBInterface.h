// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterExtMachineInterface.h"
#include "MonsterExtXKTBInterface.generated.h"

/*
* 文件名称：MonsterExtXKTBInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-23
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtXKTBInterface : public UMonsterExtMachineInterface
{
	GENERATED_BODY()
		typedef UMonsterExtMachineInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtXKTBInterface();
	~UMonsterExtXKTBInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtXKTBInterface'"); } //获取蓝图对象路径

	///显示怪物血量下的描述
	void DisplyCurrentText(const FString& currentText, const int32& state);

	///清除怪物头上的动态图标及配置文字显示
	void CancelDisplyCurrentText();

};
