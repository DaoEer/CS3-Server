// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterCopyRoleModelInterface.h"
#include "MonsterExtTiShenInterface.generated.h"

/*
* 文件名称：MonsterExtTiShenInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-04-23
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtTiShenInterface : public UMonsterCopyRoleModelInterface
{
	GENERATED_BODY()
	typedef UMonsterCopyRoleModelInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtTiShenInterface();
	~UMonsterExtTiShenInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtTiShenInterface'"); } //获取蓝图对象路径

};
